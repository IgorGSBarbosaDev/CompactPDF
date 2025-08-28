"""
Sistema de configuração otimizado com cache e validação.

Implementa configurações inteligentes com cache, validação
automática e presets otimizados para diferentes casos de uso.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union, Callable
from enum import Enum, auto
import json
import threading
from pathlib import Path
from functools import lru_cache
import hashlib

# Cache thread-safe para configurações
_config_cache: Dict[str, 'CompressionConfig'] = {}
_cache_lock = threading.RLock()


class CompressionLevel(Enum):
    """Níveis de compressão otimizados."""
    ULTRA_FAST = ("ultra_fast", 1)      # Mínima compressão, máxima velocidade
    FAST = ("fast", 2)                  # Compressão rápida
    BALANCED = ("balanced", 3)          # Equilibrio entre qualidade e velocidade  
    QUALITY = ("quality", 4)            # Foco na qualidade
    MAXIMUM = ("maximum", 5)            # Máxima compressão
    
    def __init__(self, name: str, priority: int):
        self.preset_name = name
        self.priority = priority
    
    @property
    def is_fast(self) -> bool:
        """Retorna True se é um preset de velocidade."""
        return self.priority <= 2
    
    @property
    def is_quality_focused(self) -> bool:
        """Retorna True se é um preset focado em qualidade."""
        return self.priority >= 4


class CompressionStrategy(Enum):
    """Estratégias de compressão especializadas."""
    WEB_OPTIMIZED = auto()      # Otimizado para web (pequeno, loading rápido)
    PRINT_READY = auto()        # Pronto para impressão (qualidade alta)
    ARCHIVE = auto()            # Arquivo de longo prazo (compressão máxima)
    MOBILE_FRIENDLY = auto()    # Amigável para dispositivos móveis
    EMAIL_ATTACHMENT = auto()   # Anexo de email (pequeno, compatível)


@dataclass
class ValidationRule:
    """Regra de validação para configurações."""
    field_name: str
    validator: Callable[[Any], bool]
    error_message: str
    fix_function: Optional[Callable[[Any], Any]] = None


@dataclass
class CompressionConfig:
    """
    Configuração otimizada para compressão de PDF.
    
    Implementa cache, validação automática e otimizações
    de performance para diferentes cenários de uso.
    """
    
    # Image compression settings - otimizados
    image_quality: int = field(default=75, metadata={'min': 1, 'max': 100})
    resize_images: bool = True
    max_image_width: int = field(default=1920, metadata={'min': 100, 'max': 4096})
    max_image_height: int = field(default=1920, metadata={'min': 100, 'max': 4096})
    convert_to_jpeg: bool = True
    progressive_jpeg: bool = True
    
    # Font optimization settings
    optimize_fonts: bool = True
    subset_fonts: bool = True
    remove_unused_fonts: bool = True
    merge_duplicate_fonts: bool = True
    
    # Content optimization settings  
    remove_metadata: bool = True
    remove_duplicates: bool = True
    compress_streams: bool = True
    optimize_structure: bool = True
    remove_unused_objects: bool = True
    
    # Advanced settings
    compression_level: CompressionLevel = CompressionLevel.BALANCED
    strategy: CompressionStrategy = CompressionStrategy.WEB_OPTIMIZED
    preserve_bookmarks: bool = True
    preserve_annotations: bool = True
    preserve_forms: bool = True
    
    # Performance settings
    use_multithreading: bool = True
    max_workers: Optional[int] = None
    chunk_size: int = field(default=1024 * 1024, metadata={'min': 1024})  # 1MB chunks
    memory_limit_mb: int = field(default=512, metadata={'min': 64, 'max': 4096})
    
    # Quality control
    target_compression_ratio: float = field(default=0.6, metadata={'min': 0.1, 'max': 0.95})
    min_quality_threshold: float = field(default=0.75, metadata={'min': 0.1, 'max': 1.0})
    enable_quality_check: bool = True
    
    # Experimental features
    enable_ai_optimization: bool = False
    adaptive_quality: bool = True
    smart_image_detection: bool = True
    
    def __post_init__(self):
        """Validação e otimização automática após inicialização."""
        self._validate_and_fix()
        self._apply_strategy_optimizations()
        self._cache_hash = self._calculate_hash()
    
    def _validate_and_fix(self) -> None:
        """Valida e corrige automaticamente configurações inválidas."""
        rules = [
            ValidationRule(
                'image_quality',
                lambda x: 1 <= x <= 100,
                'image_quality deve estar entre 1 e 100',
                lambda x: max(1, min(100, x))
            ),
            ValidationRule(
                'target_compression_ratio',
                lambda x: 0.1 <= x <= 0.95,
                'target_compression_ratio deve estar entre 0.1 e 0.95',
                lambda x: max(0.1, min(0.95, x))
            ),
            ValidationRule(
                'min_quality_threshold',
                lambda x: 0.1 <= x <= 1.0,
                'min_quality_threshold deve estar entre 0.1 e 1.0',
                lambda x: max(0.1, min(1.0, x))
            ),
            ValidationRule(
                'max_image_width',
                lambda x: 100 <= x <= 4096,
                'max_image_width deve estar entre 100 e 4096',
                lambda x: max(100, min(4096, x))
            ),
            ValidationRule(
                'max_image_height', 
                lambda x: 100 <= x <= 4096,
                'max_image_height deve estar entre 100 e 4096',
                lambda x: max(100, min(4096, x))
            ),
            ValidationRule(
                'memory_limit_mb',
                lambda x: 64 <= x <= 4096,
                'memory_limit_mb deve estar entre 64 e 4096',
                lambda x: max(64, min(4096, x))
            )
        ]
        
        for rule in rules:
            value = getattr(self, rule.field_name)
            if not rule.validator(value):
                if rule.fix_function:
                    fixed_value = rule.fix_function(value)
                    setattr(self, rule.field_name, fixed_value)
                else:
                    raise ValueError(f"{rule.field_name}: {rule.error_message}")
    
    def _apply_strategy_optimizations(self) -> None:
        """Aplica otimizações baseadas na estratégia escolhida."""
        if self.strategy == CompressionStrategy.WEB_OPTIMIZED:
            self.image_quality = min(self.image_quality, 80)
            self.progressive_jpeg = True
            self.target_compression_ratio = 0.7
            
        elif self.strategy == CompressionStrategy.PRINT_READY:
            self.image_quality = max(self.image_quality, 85)
            self.resize_images = False
            self.target_compression_ratio = 0.4
            
        elif self.strategy == CompressionStrategy.ARCHIVE:
            self.compression_level = CompressionLevel.MAXIMUM
            self.remove_metadata = True
            self.target_compression_ratio = 0.8
            
        elif self.strategy == CompressionStrategy.MOBILE_FRIENDLY:
            self.max_image_width = min(self.max_image_width, 1024)
            self.max_image_height = min(self.max_image_height, 1024)
            self.image_quality = min(self.image_quality, 70)
            self.target_compression_ratio = 0.8
            
        elif self.strategy == CompressionStrategy.EMAIL_ATTACHMENT:
            self.max_image_width = min(self.max_image_width, 800)
            self.max_image_height = min(self.max_image_height, 800)
            self.image_quality = min(self.image_quality, 65)
            self.target_compression_ratio = 0.85
    
    def _calculate_hash(self) -> str:
        """Calcula hash da configuração para cache."""
        config_str = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()
    
    @lru_cache(maxsize=128)
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte configuração para dicionário.
        
        Cached para melhor performance em conversões repetidas.
        """
        return {
            # Image settings
            'image_quality': self.image_quality,
            'resize_images': self.resize_images,
            'max_image_width': self.max_image_width,
            'max_image_height': self.max_image_height,
            'convert_to_jpeg': self.convert_to_jpeg,
            'progressive_jpeg': self.progressive_jpeg,
            
            # Font settings
            'optimize_fonts': self.optimize_fonts,
            'subset_fonts': self.subset_fonts,
            'remove_unused_fonts': self.remove_unused_fonts,
            'merge_duplicate_fonts': self.merge_duplicate_fonts,
            
            # Content settings
            'remove_metadata': self.remove_metadata,
            'remove_duplicates': self.remove_duplicates,
            'compress_streams': self.compress_streams,
            'optimize_structure': self.optimize_structure,
            'remove_unused_objects': self.remove_unused_objects,
            
            # Advanced settings
            'compression_level': self.compression_level.preset_name,
            'strategy': self.strategy.name,
            'preserve_bookmarks': self.preserve_bookmarks,
            'preserve_annotations': self.preserve_annotations,
            'preserve_forms': self.preserve_forms,
            
            # Performance settings
            'use_multithreading': self.use_multithreading,
            'max_workers': self.max_workers,
            'chunk_size': self.chunk_size,
            'memory_limit_mb': self.memory_limit_mb,
            
            # Quality control
            'target_compression_ratio': self.target_compression_ratio,
            'min_quality_threshold': self.min_quality_threshold,
            'enable_quality_check': self.enable_quality_check,
            
            # Experimental
            'enable_ai_optimization': self.enable_ai_optimization,
            'adaptive_quality': self.adaptive_quality,
            'smart_image_detection': self.smart_image_detection
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompressionConfig':
        """Cria configuração a partir de dicionário."""
        # Converte enums
        if 'compression_level' in data and isinstance(data['compression_level'], str):
            for level in CompressionLevel:
                if level.preset_name == data['compression_level']:
                    data['compression_level'] = level
                    break
        
        if 'strategy' in data and isinstance(data['strategy'], str):
            for strategy in CompressionStrategy:
                if strategy.name == data['strategy']:
                    data['strategy'] = strategy
                    break
        
        return cls(**data)
    
    @classmethod
    def get_preset(cls, preset_name: str) -> 'CompressionConfig':
        """
        Retorna configuração pré-definida otimizada.
        
        Args:
            preset_name: Nome do preset ('web', 'print', 'archive', 'mobile', 'email')
        """
        with _cache_lock:
            if preset_name in _config_cache:
                return _config_cache[preset_name]
        
        preset_configs = {
            'web': cls(
                strategy=CompressionStrategy.WEB_OPTIMIZED,
                compression_level=CompressionLevel.BALANCED,
                image_quality=75,
                target_compression_ratio=0.7
            ),
            'print': cls(
                strategy=CompressionStrategy.PRINT_READY,
                compression_level=CompressionLevel.QUALITY,
                image_quality=90,
                resize_images=False,
                target_compression_ratio=0.4
            ),
            'archive': cls(
                strategy=CompressionStrategy.ARCHIVE,
                compression_level=CompressionLevel.MAXIMUM,
                image_quality=60,
                target_compression_ratio=0.8
            ),
            'mobile': cls(
                strategy=CompressionStrategy.MOBILE_FRIENDLY,
                compression_level=CompressionLevel.BALANCED,
                image_quality=65,
                max_image_width=1024,
                max_image_height=1024,
                target_compression_ratio=0.8
            ),
            'email': cls(
                strategy=CompressionStrategy.EMAIL_ATTACHMENT,
                compression_level=CompressionLevel.FAST,
                image_quality=60,
                max_image_width=800,
                max_image_height=800,
                target_compression_ratio=0.85
            ),
            'ultra_fast': cls(
                compression_level=CompressionLevel.ULTRA_FAST,
                image_quality=50,
                optimize_fonts=False,
                remove_duplicates=False,
                target_compression_ratio=0.5
            ),
            'quality': cls(
                compression_level=CompressionLevel.QUALITY,
                image_quality=95,
                resize_images=False,
                target_compression_ratio=0.3
            )
        }
        
        if preset_name not in preset_configs:
            raise ValueError(f"Preset desconhecido: {preset_name}")
        
        config = preset_configs[preset_name]
        
        # Cache o preset para uso futuro
        with _cache_lock:
            _config_cache[preset_name] = config
        
        return config
    
    def clone(self, **overrides) -> 'CompressionConfig':
        """
        Cria uma cópia da configuração com modificações opcionais.
        
        Args:
            **overrides: Parâmetros a serem sobrescritos
        """
        config_dict = self.to_dict()
        config_dict.update(overrides)
        return self.__class__.from_dict(config_dict)
    
    def is_compatible_with(self, other: 'CompressionConfig') -> bool:
        """Verifica se duas configurações são compatíveis."""
        # Configurações são compatíveis se têm a mesma estratégia e nível similar
        return (self.strategy == other.strategy and 
                abs(self.compression_level.priority - other.compression_level.priority) <= 1)
    
    def get_performance_score(self) -> float:
        """
        Calcula score de performance baseado nas configurações.
        
        Returns:
            Score de 0.0 (lento) a 1.0 (rápido)
        """
        score = 1.0
        
        # Penaliza configurações que reduzem performance
        if self.compression_level.priority > 3:
            score -= 0.2
        if self.image_quality > 85:
            score -= 0.1
        if not self.use_multithreading:
            score -= 0.3
        if self.enable_ai_optimization:
            score -= 0.2
        if self.resize_images and (self.max_image_width > 1920 or self.max_image_height > 1920):
            score -= 0.1
        
        return max(0.0, score)
    
    def get_compression_score(self) -> float:
        """
        Calcula score de compressão baseado nas configurações.
        
        Returns:
            Score de 0.0 (pouca compressão) a 1.0 (máxima compressão)
        """
        score = 0.0
        
        # Aumenta score baseado em configurações que melhoram compressão
        score += self.compression_level.priority * 0.2
        score += (100 - self.image_quality) * 0.005
        score += self.target_compression_ratio * 0.3
        
        if self.remove_duplicates:
            score += 0.1
        if self.compress_streams:
            score += 0.1
        if self.optimize_fonts:
            score += 0.05
        if self.remove_metadata:
            score += 0.05
        
        return min(1.0, score)
    
    def optimize_for_file_size(self, target_size_mb: float) -> 'CompressionConfig':
        """
        Otimiza configuração para atingir tamanho de arquivo específico.
        
        Args:
            target_size_mb: Tamanho alvo em MB
            
        Returns:
            Nova configuração otimizada
        """
        # Configuração base para arquivos pequenos
        if target_size_mb < 1.0:  # < 1MB
            return self.clone(
                strategy=CompressionStrategy.EMAIL_ATTACHMENT,
                image_quality=50,
                max_image_width=600,
                max_image_height=600,
                target_compression_ratio=0.9
            )
        elif target_size_mb < 5.0:  # < 5MB
            return self.clone(
                strategy=CompressionStrategy.WEB_OPTIMIZED,
                image_quality=65,
                target_compression_ratio=0.8
            )
        else:  # >= 5MB
            return self.clone(
                strategy=CompressionStrategy.QUALITY,
                target_compression_ratio=0.6
            )
    
    def __str__(self) -> str:
        """Representação string da configuração."""
        return (f"CompressionConfig("
                f"strategy={self.strategy.name}, "
                f"level={self.compression_level.preset_name}, "
                f"quality={self.image_quality}, "
                f"target_ratio={self.target_compression_ratio:.1%})")
    
    def __hash__(self) -> int:
        """Hash baseado no conteúdo da configuração."""
        return hash(self._cache_hash)


@dataclass 
class PresetConfig:
    """
    Configuração de preset com metadados otimizados.
    
    Armazena informações sobre presets incluindo métricas
    de performance e casos de uso recomendados.
    """
    name: str
    config: CompressionConfig
    description: str
    use_cases: List[str] = field(default_factory=list)
    expected_compression: float = 0.6
    expected_speed: float = 1.0  # Relativo ao baseline
    min_file_size_mb: float = 0.0
    max_file_size_mb: float = 100.0
    
    @property
    def performance_score(self) -> float:
        """Score de performance do preset."""
        return self.config.get_performance_score()
    
    @property
    def compression_score(self) -> float:
        """Score de compressão do preset."""
        return self.config.get_compression_score()
    
    def is_suitable_for_file_size(self, file_size_mb: float) -> bool:
        """Verifica se preset é adequado para tamanho de arquivo."""
        return self.min_file_size_mb <= file_size_mb <= self.max_file_size_mb


# Factory functions otimizadas
def get_web_config() -> CompressionConfig:
    """Configuração otimizada para web."""
    return CompressionConfig.get_preset('web')


def get_print_config() -> CompressionConfig:
    """Configuração otimizada para impressão."""
    return CompressionConfig.get_preset('print')


def get_archive_config() -> CompressionConfig:
    """Configuração otimizada para arquivo."""
    return CompressionConfig.get_preset('archive')


def get_mobile_config() -> CompressionConfig:
    """Configuração otimizada para mobile."""
    return CompressionConfig.get_preset('mobile')


def get_email_config() -> CompressionConfig:
    """Configuração otimizada para email."""
    return CompressionConfig.get_preset('email')


def auto_select_config(file_size_mb: float, 
                      target_use: str = 'general') -> CompressionConfig:
    """
    Seleciona automaticamente a melhor configuração.
    
    Args:
        file_size_mb: Tamanho do arquivo em MB
        target_use: Uso pretendido ('web', 'print', 'archive', 'mobile', 'email', 'general')
        
    Returns:
        Configuração otimizada para o cenário
    """
    if target_use != 'general':
        return CompressionConfig.get_preset(target_use)
    
    # Seleção automática baseada no tamanho
    if file_size_mb < 1.0:
        return get_email_config()
    elif file_size_mb < 10.0:
        return get_web_config()
    elif file_size_mb < 50.0:
        return get_print_config()
    else:
        return get_archive_config()


def clear_config_cache() -> None:
    """Limpa cache de configurações."""
    with _cache_lock:
        _config_cache.clear()
        CompressionConfig.to_dict.cache_clear()
