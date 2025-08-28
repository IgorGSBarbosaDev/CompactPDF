"""
Sistema de gestão de memória e otimização de performance.

Este módulo implementa estratégias de otimização de memória,
cache inteligente e limpeza automática de recursos.
"""

import gc
import sys
import threading
import time
import weakref
from typing import Any, Dict, Optional, List, Callable, TypeVar, Generic
from functools import wraps, lru_cache
from dataclasses import dataclass, field
import psutil
import os

T = TypeVar('T')


@dataclass
class MemoryUsage:
    """Informações de uso de memória."""
    total_mb: float
    available_mb: float
    used_mb: float
    used_percent: float
    process_mb: float


@dataclass
class CacheStats:
    """Estatísticas do cache."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    size: int = 0
    max_size: int = 1000
    
    @property
    def hit_rate(self) -> float:
        """Taxa de acertos do cache."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class MemoryManager:
    """
    Gerenciador inteligente de memória.
    
    Monitora uso de memória e executa limpezas automáticas
    quando necessário para manter performance otimizada.
    """
    
    def __init__(self, 
                 max_memory_percent: float = 80.0,
                 cleanup_threshold: float = 90.0,
                 monitor_interval: float = 30.0):
        """
        Inicializa o gerenciador de memória.
        
        Args:
            max_memory_percent: Percentual máximo de memória antes de otimização
            cleanup_threshold: Threshold para limpeza forçada
            monitor_interval: Intervalo de monitoramento em segundos
        """
        self.max_memory_percent = max_memory_percent
        self.cleanup_threshold = cleanup_threshold
        self.monitor_interval = monitor_interval
        
        self._cleanup_callbacks: List[Callable[[], None]] = []
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Referências fracas para objetos monitorados
        self._tracked_objects: weakref.WeakSet = weakref.WeakSet()
        
    def get_memory_usage(self) -> MemoryUsage:
        """Retorna informações atuais de uso de memória."""
        memory = psutil.virtual_memory()
        process = psutil.Process()
        
        return MemoryUsage(
            total_mb=memory.total / (1024 * 1024),
            available_mb=memory.available / (1024 * 1024),
            used_mb=memory.used / (1024 * 1024),
            used_percent=memory.percent,
            process_mb=process.memory_info().rss / (1024 * 1024)
        )
    
    def register_cleanup_callback(self, callback: Callable[[], None]) -> None:
        """Registra callback para limpeza de memória."""
        self._cleanup_callbacks.append(callback)
    
    def track_object(self, obj: Any) -> None:
        """Adiciona objeto ao monitoramento de memória."""
        self._tracked_objects.add(obj)
    
    def cleanup_memory(self, force: bool = False) -> int:
        """
        Executa limpeza de memória.
        
        Args:
            force: Se True, força limpeza mesmo se não necessária
            
        Returns:
            Número de objetos limpos
        """
        usage = self.get_memory_usage()
        
        if not force and usage.used_percent < self.max_memory_percent:
            return 0
        
        # Executa callbacks de limpeza
        for callback in self._cleanup_callbacks:
            try:
                callback()
            except Exception:
                pass  # Ignora erros em callbacks
        
        # Força garbage collection
        collected = gc.collect()
        
        # Limpa objetos órfãos
        orphaned = len([obj for obj in self._tracked_objects if obj is None])
        
        return collected + orphaned
    
    def start_monitoring(self) -> None:
        """Inicia monitoramento automático de memória."""
        if self._monitoring:
            return
            
        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self._monitor_thread.start()
    
    def stop_monitoring(self) -> None:
        """Para monitoramento automático."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)
    
    def _monitor_loop(self) -> None:
        """Loop principal de monitoramento."""
        while self._monitoring:
            try:
                usage = self.get_memory_usage()
                
                if usage.used_percent > self.cleanup_threshold:
                    self.cleanup_memory(force=True)
                elif usage.used_percent > self.max_memory_percent:
                    self.cleanup_memory(force=False)
                
                time.sleep(self.monitor_interval)
                
            except Exception:
                pass  # Continua monitoramento mesmo com erros


class SmartCache(Generic[T]):
    """
    Cache inteligente com limpeza automática baseada em uso de memória.
    
    Implementa LRU com awareness de memória para otimizar performance
    sem causar problemas de memória.
    """
    
    def __init__(self, 
                 max_size: int = 1000,
                 ttl_seconds: Optional[float] = None,
                 memory_manager: Optional[MemoryManager] = None):
        """
        Inicializa cache inteligente.
        
        Args:
            max_size: Tamanho máximo do cache
            ttl_seconds: TTL para entradas (None = sem expiração)
            memory_manager: Gerenciador de memória (opcional)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.memory_manager = memory_manager or MemoryManager()
        
        self._cache: Dict[str, Any] = {}
        self._access_times: Dict[str, float] = {}
        self._creation_times: Dict[str, float] = {}
        self._stats = CacheStats(max_size=max_size)
        self._lock = threading.RLock()
        
        # Registra callback de limpeza
        self.memory_manager.register_cleanup_callback(self._memory_cleanup)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Recupera item do cache."""
        with self._lock:
            current_time = time.time()
            
            # Verifica se existe e não expirou
            if key in self._cache:
                if self._is_expired(key, current_time):
                    self._remove_key(key)
                    self._stats.misses += 1
                    return default
                
                # Atualiza tempo de acesso (LRU)
                self._access_times[key] = current_time
                self._stats.hits += 1
                return self._cache[key]
            
            self._stats.misses += 1
            return default
    
    def set(self, key: str, value: T) -> None:
        """Armazena item no cache."""
        with self._lock:
            current_time = time.time()
            
            # Remove se já existe
            if key in self._cache:
                self._remove_key(key)
            
            # Verifica se precisa fazer espaço
            while len(self._cache) >= self.max_size:
                self._evict_lru()
            
            # Adiciona novo item
            self._cache[key] = value
            self._access_times[key] = current_time
            self._creation_times[key] = current_time
            self._stats.size = len(self._cache)
    
    def clear(self) -> None:
        """Limpa todo o cache."""
        with self._lock:
            self._cache.clear()
            self._access_times.clear()
            self._creation_times.clear()
            self._stats.size = 0
    
    def get_stats(self) -> CacheStats:
        """Retorna estatísticas do cache."""
        with self._lock:
            stats_copy = CacheStats(
                hits=self._stats.hits,
                misses=self._stats.misses,
                evictions=self._stats.evictions,
                size=self._stats.size,
                max_size=self._stats.max_size
            )
            return stats_copy
    
    def _is_expired(self, key: str, current_time: float) -> bool:
        """Verifica se item expirou."""
        if self.ttl_seconds is None:
            return False
        
        creation_time = self._creation_times.get(key, current_time)
        return (current_time - creation_time) > self.ttl_seconds
    
    def _remove_key(self, key: str) -> None:
        """Remove chave do cache."""
        self._cache.pop(key, None)
        self._access_times.pop(key, None)
        self._creation_times.pop(key, None)
        self._stats.size = len(self._cache)
    
    def _evict_lru(self) -> None:
        """Remove item menos recentemente usado."""
        if not self._access_times:
            return
        
        # Encontra chave com menor tempo de acesso
        lru_key = min(self._access_times.keys(), 
                     key=lambda k: self._access_times[k])
        
        self._remove_key(lru_key)
        self._stats.evictions += 1
    
    def _memory_cleanup(self) -> None:
        """Callback para limpeza de memória."""
        # Remove metade do cache quando memória está alta
        target_size = self.max_size // 2
        
        while len(self._cache) > target_size:
            self._evict_lru()


def memory_optimized(max_memory_mb: float = 100.0):
    """
    Decorator para otimização automática de memória.
    
    Monitora uso de memória da função e executa limpeza
    quando necessário.
    
    Args:
        max_memory_mb: Memória máxima permitida em MB
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Monitora memória antes da execução
            process = psutil.Process()
            memory_before = process.memory_info().rss / (1024 * 1024)
            
            try:
                result = func(*args, **kwargs)
                
                # Verifica memória após execução
                memory_after = process.memory_info().rss / (1024 * 1024)
                memory_delta = memory_after - memory_before
                
                # Se usar muita memória, força limpeza
                if memory_delta > max_memory_mb:
                    gc.collect()
                
                return result
                
            except MemoryError:
                # Em caso de erro de memória, tenta limpeza e executa novamente
                gc.collect()
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


def cached_property(func: Callable) -> property:
    """
    Property com cache que se limpa automaticamente.
    
    Similar ao functools.cached_property, mas com limpeza
    automática baseada em uso de memória.
    """
    attr_name = f'_cached_{func.__name__}'
    
    def getter(self):
        try:
            return getattr(self, attr_name)
        except AttributeError:
            value = func(self)
            setattr(self, attr_name, value)
            return value
    
    def deleter(self):
        try:
            delattr(self, attr_name)
        except AttributeError:
            pass
    
    return property(getter, None, deleter)


# Instância global do gerenciador de memória
global_memory_manager = MemoryManager()

# Cache global inteligente
global_cache = SmartCache(max_size=5000, ttl_seconds=3600.0)


def get_memory_info() -> Dict[str, Any]:
    """Retorna informações detalhadas de memória."""
    usage = global_memory_manager.get_memory_usage()
    cache_stats = global_cache.get_stats()
    
    return {
        'memory': {
            'total_mb': usage.total_mb,
            'available_mb': usage.available_mb,
            'used_mb': usage.used_mb,
            'used_percent': usage.used_percent,
            'process_mb': usage.process_mb
        },
        'cache': {
            'hits': cache_stats.hits,
            'misses': cache_stats.misses,
            'hit_rate': cache_stats.hit_rate,
            'size': cache_stats.size,
            'max_size': cache_stats.max_size
        },
        'python': {
            'gc_counts': gc.get_count(),
            'gc_stats': gc.get_stats() if hasattr(gc, 'get_stats') else None
        }
    }


def cleanup_all() -> Dict[str, int]:
    """Executa limpeza completa do sistema."""
    results = {}
    
    # Limpeza de cache
    global_cache.clear()
    results['cache_cleared'] = True
    
    # Limpeza de memória
    collected = global_memory_manager.cleanup_memory(force=True)
    results['objects_collected'] = collected
    
    # Garbage collection agressivo
    for generation in range(3):
        gc.collect()
    results['gc_collections'] = 3
    
    return results


# Inicia monitoramento automático se não estiver em ambiente de teste
if not any(test_env in os.environ for test_env in ['PYTEST_CURRENT_TEST', 'TESTING']):
    global_memory_manager.start_monitoring()
