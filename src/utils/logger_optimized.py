"""
Sistema de logging otimizado e eficiente.

Implementa logging com buffer, rotação automática e
otimizações de performance para minimizar impacto.
"""

import logging
import sys
import threading
import time
import queue
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import atexit
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from ..interfaces import ILogger


@dataclass
class LogEntry:
    """Entrada de log estruturada."""
    timestamp: float
    level: str
    message: str
    context: Optional[Dict[str, Any]] = None
    thread_id: Optional[int] = None


class BufferedLogger(ILogger):
    """
    Logger com buffer para performance otimizada.
    
    Agrupa mensagens de log em batch para reduzir I/O
    e melhorar performance em operações intensivas.
    """
    
    def __init__(self, 
                 name: str = "PDFCompressor",
                 log_file: Optional[str] = None,
                 buffer_size: int = 100,
                 flush_interval: float = 5.0,
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5):
        """
        Inicializa logger com buffer.
        
        Args:
            name: Nome do logger
            log_file: Arquivo de log (opcional)
            buffer_size: Tamanho do buffer
            flush_interval: Intervalo de flush em segundos
            max_file_size: Tamanho máximo do arquivo de log
            backup_count: Número de backups a manter
        """
        self.name = name
        self.log_file = log_file
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        
        # Buffer thread-safe
        self._buffer: queue.Queue = queue.Queue()
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="LogWriter")
        self._should_stop = threading.Event()
        self._last_flush = time.time()
        
        # Configuração do logger interno
        self._setup_logger()
        
        # Thread para flush automático
        self._flush_thread = threading.Thread(
            target=self._flush_loop,
            daemon=True,
            name="LogFlusher"
        )
        self._flush_thread.start()
        
        # Registra cleanup no exit
        atexit.register(self.shutdown)
    
    def _setup_logger(self) -> None:
        """Configura logger interno com otimizações."""
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        
        # Remove handlers existentes
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Formatter otimizado
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Handler para arquivo se especificado
        if self.log_file:
            from logging.handlers import RotatingFileHandler
            
            file_handler = RotatingFileHandler(
                self.log_file,
                maxBytes=self.max_file_size,
                backupCount=self.backup_count
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def _add_to_buffer(self, level: str, message: str, 
                      context: Optional[Dict[str, Any]] = None) -> None:
        """Adiciona entrada ao buffer."""
        entry = LogEntry(
            timestamp=time.time(),
            level=level,
            message=message,
            context=context,
            thread_id=threading.get_ident()
        )
        
        try:
            self._buffer.put_nowait(entry)
        except queue.Full:
            # Se buffer está cheio, força flush
            self._flush_buffer()
            self._buffer.put_nowait(entry)
        
        # Flush se buffer atingiu limite
        if self._buffer.qsize() >= self.buffer_size:
            self._flush_buffer()
    
    def _flush_buffer(self) -> None:
        """Força flush do buffer."""
        if self._buffer.empty():
            return
        
        # Coleta todas as entradas do buffer
        entries = []
        while not self._buffer.empty():
            try:
                entries.append(self._buffer.get_nowait())
            except queue.Empty:
                break
        
        if entries:
            # Envia para thread de escrita
            self._executor.submit(self._write_entries, entries)
            self._last_flush = time.time()
    
    def _write_entries(self, entries: List[LogEntry]) -> None:
        """Escreve entradas no log (executa em thread separada)."""
        for entry in entries:
            timestamp_str = datetime.fromtimestamp(entry.timestamp).strftime('%H:%M:%S')
            
            # Monta mensagem completa
            full_message = entry.message
            if entry.context:
                context_str = " | ".join(f"{k}={v}" for k, v in entry.context.items())
                full_message = f"{entry.message} | {context_str}"
            
            # Log via logger interno
            level_map = {
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'DEBUG': logging.DEBUG
            }
            
            self.logger.log(
                level_map.get(entry.level, logging.INFO),
                full_message
            )
    
    def _flush_loop(self) -> None:
        """Loop de flush automático."""
        while not self._should_stop.is_set():
            try:
                # Flush se passou do intervalo
                if time.time() - self._last_flush >= self.flush_interval:
                    self._flush_buffer()
                
                # Sleep curto para não consumir CPU
                time.sleep(0.1)
                
            except Exception:
                pass  # Continua loop mesmo com erros
    
    def log_info(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log de informação."""
        self._add_to_buffer('INFO', message, context)
    
    def log_warning(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log de aviso."""
        self._add_to_buffer('WARNING', message, context)
    
    def log_error(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log de erro."""
        self._add_to_buffer('ERROR', message, context)
    
    def log_debug(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log de debug."""
        self._add_to_buffer('DEBUG', message, context)
    
    def flush(self) -> None:
        """Força flush imediato do buffer."""
        self._flush_buffer()
        
        # Aguarda conclusão das escritas pendentes
        self._executor.shutdown(wait=True)
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="LogWriter")
    
    def shutdown(self) -> None:
        """Finaliza logger e limpa recursos."""
        self._should_stop.set()
        
        # Flush final
        self._flush_buffer()
        
        # Aguarda threads finalizarem
        if self._flush_thread.is_alive():
            self._flush_thread.join(timeout=1.0)
        
        self._executor.shutdown(wait=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do logger."""
        return {
            'buffer_size': self._buffer.qsize(),
            'max_buffer_size': self.buffer_size,
            'last_flush': self._last_flush,
            'flush_interval': self.flush_interval,
            'log_file': self.log_file
        }


class OptimizedSimpleLogger(ILogger):
    """
    Logger simples e eficiente para uso geral.
    
    Versão otimizada mantendo compatibilidade com SimpleLogger original.
    """
    
    def __init__(self, name: str = "PDFCompressor", log_file: Optional[str] = None):
        """
        Inicializa logger simples.
        
        Args:
            name: Nome do logger
            log_file: Arquivo de log (opcional)
        """
        self.name = name
        self.log_file = log_file
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        
        # Remove handlers existentes
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)
        
        # Formatter otimizado
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Console handler com buffer
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(self._rate_limit_filter)
        self._logger.addHandler(console_handler)
        
        # File handler se especificado
        if log_file:
            from logging.handlers import RotatingFileHandler
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,  # 5MB
                backupCount=3
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
        
        # Rate limiting para evitar spam
        self._last_messages = {}
        self._message_counts = {}
    
    def _rate_limit_filter(self, record):
        """Filtro para rate limiting de mensagens duplicadas."""
        message = record.getMessage()
        current_time = time.time()
        
        # Se já vimos esta mensagem recentemente
        if message in self._last_messages:
            last_time = self._last_messages[message]
            if current_time - last_time < 1.0:  # 1 segundo
                self._message_counts[message] = self._message_counts.get(message, 0) + 1
                return False  # Suprime mensagem
        
        # Atualiza tracking
        self._last_messages[message] = current_time
        
        # Se temos mensagens suprimidas, adiciona contador
        if message in self._message_counts and self._message_counts[message] > 0:
            count = self._message_counts[message]
            record.msg = f"{record.msg} (+ {count} similares suprimidas)"
            self._message_counts[message] = 0
        
        return True
    
    def log_info(self, message: str) -> None:
        """Log de informação."""
        self._logger.info(message)
    
    def log_warning(self, message: str) -> None:
        """Log de aviso."""
        self._logger.warning(message)
    
    def log_error(self, message: str) -> None:
        """Log de erro."""
        self._logger.error(message)


# Manter compatibilidade com código existente
SimpleLogger = OptimizedSimpleLogger


class NullLogger(ILogger):
    """
    Null logger que não produz saída.
    
    Útil para testes ou quando logging não é desejado.
    """
    
    def log_info(self, message: str) -> None:
        """No-op log info."""
        pass
    
    def log_warning(self, message: str) -> None:
        """No-op log warning."""
        pass
    
    def log_error(self, message: str) -> None:
        """No-op log error."""
        pass


# Logger global para conveniência
_global_logger: Optional[ILogger] = None


def get_logger(name: str = "PDFCompressor", 
               log_file: Optional[str] = None,
               use_buffer: bool = False) -> ILogger:
    """
    Factory function para obter logger otimizado.
    
    Args:
        name: Nome do logger
        log_file: Arquivo de log (opcional)
        use_buffer: Se True, usa BufferedLogger para alta performance
        
    Returns:
        Instância de logger otimizada
    """
    if use_buffer:
        return BufferedLogger(name=name, log_file=log_file)
    else:
        return OptimizedSimpleLogger(name=name, log_file=log_file)


def set_global_logger(logger: ILogger) -> None:
    """Define logger global."""
    global _global_logger
    _global_logger = logger


def get_global_logger() -> ILogger:
    """Retorna logger global ou cria um novo."""
    global _global_logger
    if _global_logger is None:
        _global_logger = OptimizedSimpleLogger()
    return _global_logger
