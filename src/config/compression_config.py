#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuração de compressão - CompactPDF
=======================================

Define configurações e parâmetros para compressão de PDFs.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
import json


class CompressionLevel(Enum):
    """Níveis de compressão predefinidos."""
    MINIMAL = "minimal"        # Compressão mínima, máxima qualidade
    BALANCED = "balanced"      # Equilíbrio entre tamanho e qualidade
    AGGRESSIVE = "aggressive"  # Máxima compressão, qualidade reduzida
    CUSTOM = "custom"         # Configuração personalizada


class QualityProfile(Enum):
    """Perfis de qualidade."""
    ARCHIVE = "archive"       # Qualidade de arquivo (máxima)
    PRINT = "print"          # Qualidade para impressão
    WEB = "web"              # Qualidade para web
    EMAIL = "email"          # Qualidade para email (compacto)


@dataclass
class ImageCompressionConfig:
    """Configuração para compressão de imagens."""
    
    # Qualidade JPEG (0-100)
    jpeg_quality: int = 85
    
    # Resolução máxima
    max_width: int = 1200
    max_height: int = 1200
    max_dpi: int = 150
    
    # Formato preferido para conversão
    preferred_format: str = "JPEG"  # JPEG, PNG, WEBP
    
    # Compressão progressiva
    progressive_jpeg: bool = True
    
    # Otimizar paleta de cores
    optimize_palette: bool = True
    
    # Conversão para escala de cinza quando apropriado
    auto_grayscale: bool = False
    
    # Limiar para conversão monocromática (0-1)
    monochrome_threshold: float = 0.95


@dataclass
class FontOptimizationConfig:
    """Configuração para otimização de fontes."""
    
    # Remover fontes não utilizadas
    remove_unused_fonts: bool = True
    
    # Otimizar subsets de fontes
    optimize_font_subsets: bool = True
    
    # Converter para fontes do sistema quando possível
    use_system_fonts: bool = False
    
    # Fontes essenciais que não devem ser removidas
    essential_fonts: List[str] = field(default_factory=lambda: [
        "Arial", "Times", "Helvetica", "Courier"
    ])


@dataclass
class StreamCompressionConfig:
    """Configuração para compressão de streams."""
    
    # Nível de compressão (1-9)
    compression_level: int = 6
    
    # Método de compressão
    compression_method: str = "flate"  # flate, lzw, runlength
    
    # Comprimir streams já comprimidos
    recompress_streams: bool = False
    
    # Predictor para melhor compressão
    use_predictor: bool = True


@dataclass
class MetadataConfig:
    """Configuração para processamento de metadados."""
    
    # Remover metadados desnecessários
    remove_unused_metadata: bool = True
    
    # Remover comentários
    remove_comments: bool = True
    
    # Remover informações de criação
    remove_creation_info: bool = False
    
    # Manter metadados essenciais
    keep_essential_metadata: bool = True
    
    # Metadados essenciais para manter
    essential_fields: List[str] = field(default_factory=lambda: [
        "Title", "Author", "Subject"
    ])


@dataclass
class OptimizationConfig:
    """Configuração para otimizações gerais."""
    
    # Linearizar PDF para web
    linearize_for_web: bool = False
    
    # Remover objetos não utilizados
    remove_unused_objects: bool = True
    
    # Deduplicar objetos idênticos
    deduplicate_objects: bool = True
    
    # Otimizar estrutura do PDF
    optimize_structure: bool = True
    
    # Remover elementos invisíveis
    remove_invisible_elements: bool = True


@dataclass
class BackupConfig:
    """Configuração para backup."""
    
    # Criar backup antes da compressão
    create_backup: bool = True
    
    # Diretório para backups
    backup_directory: Optional[str] = None
    
    # Sufixo para arquivos de backup
    backup_suffix: str = ".backup"
    
    # Manter backups por quantos dias
    backup_retention_days: int = 30


@dataclass
class PerformanceConfig:
    """Configuração de performance."""
    
    # Número máximo de threads
    max_threads: int = 4
    
    # Tamanho do buffer de processamento (MB)
    buffer_size_mb: int = 64
    
    # Timeout para operações (segundos)
    operation_timeout: int = 300
    
    # Usar cache para resultados
    use_cache: bool = True
    
    # Tamanho máximo do cache (MB)
    cache_size_mb: int = 256


@dataclass
class CompressionConfig:
    """
    Configuração principal para compressão de PDFs.
    
    Centraliza todas as configurações de compressão e otimização.
    """
    
    # Nível geral de compressão
    compression_level: CompressionLevel = CompressionLevel.BALANCED
    
    # Perfil de qualidade
    quality_profile: QualityProfile = QualityProfile.WEB
    
    # Configurações específicas
    image_config: ImageCompressionConfig = field(default_factory=ImageCompressionConfig)
    font_config: FontOptimizationConfig = field(default_factory=FontOptimizationConfig)
    stream_config: StreamCompressionConfig = field(default_factory=StreamCompressionConfig)
    metadata_config: MetadataConfig = field(default_factory=MetadataConfig)
    optimization_config: OptimizationConfig = field(default_factory=OptimizationConfig)
    backup_config: BackupConfig = field(default_factory=BackupConfig)
    performance_config: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    # Estratégias habilitadas
    enabled_strategies: List[str] = field(default_factory=lambda: [
        "image_compression",
        "stream_compression", 
        "font_optimization",
        "metadata_removal"
    ])
    
    # Estratégias desabilitadas
    disabled_strategies: List[str] = field(default_factory=list)
    
    # Parâmetros customizados por estratégia
    strategy_params: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Validação de qualidade
    validate_output: bool = True
    max_quality_loss: float = 10.0  # Máximo 10% de perda aceitável
    
    def apply_preset(self, preset: CompressionLevel):
        """Aplica um preset de configuração."""
        self.compression_level = preset
        
        if preset == CompressionLevel.MINIMAL:
            self._apply_minimal_preset()
        elif preset == CompressionLevel.BALANCED:
            self._apply_balanced_preset()
        elif preset == CompressionLevel.AGGRESSIVE:
            self._apply_aggressive_preset()
    
    def _apply_minimal_preset(self):
        """Aplica configurações para compressão mínima."""
        self.image_config.jpeg_quality = 95
        self.image_config.max_width = 2400
        self.image_config.max_height = 2400
        self.image_config.max_dpi = 300
        
        self.stream_config.compression_level = 3
        self.stream_config.recompress_streams = False
        
        self.font_config.remove_unused_fonts = False
        self.metadata_config.remove_unused_metadata = False
        
        self.max_quality_loss = 5.0
    
    def _apply_balanced_preset(self):
        """Aplica configurações balanceadas."""
        self.image_config.jpeg_quality = 85
        self.image_config.max_width = 1200
        self.image_config.max_height = 1200
        self.image_config.max_dpi = 150
        
        self.stream_config.compression_level = 6
        self.stream_config.recompress_streams = False
        
        self.font_config.remove_unused_fonts = True
        self.metadata_config.remove_unused_metadata = True
        
        self.max_quality_loss = 10.0
    
    def _apply_aggressive_preset(self):
        """Aplica configurações para máxima compressão."""
        self.image_config.jpeg_quality = 70
        self.image_config.max_width = 800
        self.image_config.max_height = 800
        self.image_config.max_dpi = 96
        self.image_config.auto_grayscale = True
        
        self.stream_config.compression_level = 9
        self.stream_config.recompress_streams = True
        
        self.font_config.remove_unused_fonts = True
        self.font_config.use_system_fonts = True
        self.metadata_config.remove_unused_metadata = True
        self.metadata_config.remove_comments = True
        
        self.optimization_config.remove_invisible_elements = True
        
        self.max_quality_loss = 20.0
    
    def apply_quality_profile(self, profile: QualityProfile):
        """Aplica um perfil de qualidade específico."""
        self.quality_profile = profile
        
        if profile == QualityProfile.ARCHIVE:
            self._apply_archive_profile()
        elif profile == QualityProfile.PRINT:
            self._apply_print_profile()
        elif profile == QualityProfile.WEB:
            self._apply_web_profile()
        elif profile == QualityProfile.EMAIL:
            self._apply_email_profile()
    
    def _apply_archive_profile(self):
        """Configurações para qualidade de arquivo."""
        self.image_config.jpeg_quality = 95
        self.image_config.max_dpi = 300
        self.image_config.auto_grayscale = False
    
    def _apply_print_profile(self):
        """Configurações para impressão."""
        self.image_config.jpeg_quality = 90
        self.image_config.max_dpi = 200
        self.image_config.auto_grayscale = False
    
    def _apply_web_profile(self):
        """Configurações para web."""
        self.image_config.jpeg_quality = 85
        self.image_config.max_dpi = 150
        self.image_config.progressive_jpeg = True
        self.optimization_config.linearize_for_web = True
    
    def _apply_email_profile(self):
        """Configurações para email (máxima compressão)."""
        self.image_config.jpeg_quality = 75
        self.image_config.max_width = 800
        self.image_config.max_height = 800
        self.image_config.max_dpi = 96
        self.image_config.auto_grayscale = True
    
    def is_strategy_enabled(self, strategy_name: str) -> bool:
        """Verifica se uma estratégia está habilitada."""
        if strategy_name in self.disabled_strategies:
            return False
        return strategy_name in self.enabled_strategies
    
    def enable_strategy(self, strategy_name: str):
        """Habilita uma estratégia."""
        if strategy_name not in self.enabled_strategies:
            self.enabled_strategies.append(strategy_name)
        if strategy_name in self.disabled_strategies:
            self.disabled_strategies.remove(strategy_name)
    
    def disable_strategy(self, strategy_name: str):
        """Desabilita uma estratégia."""
        if strategy_name in self.enabled_strategies:
            self.enabled_strategies.remove(strategy_name)
        if strategy_name not in self.disabled_strategies:
            self.disabled_strategies.append(strategy_name)
    
    def set_strategy_param(self, strategy_name: str, param_name: str, value: Any):
        """Define um parâmetro específico para uma estratégia."""
        if strategy_name not in self.strategy_params:
            self.strategy_params[strategy_name] = {}
        self.strategy_params[strategy_name][param_name] = value
    
    def get_strategy_param(self, strategy_name: str, param_name: str, default: Any = None) -> Any:
        """Obtém um parâmetro específico de uma estratégia."""
        return self.strategy_params.get(strategy_name, {}).get(param_name, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário."""
        result = {}
        for key, value in self.__dict__.items():
            if hasattr(value, '__dict__'):
                # Objeto complexo
                result[key] = value.__dict__ if hasattr(value, '__dict__') else str(value)
            elif isinstance(value, Enum):
                result[key] = value.value
            else:
                result[key] = value
        return result
    
    def to_json(self) -> str:
        """Converte configuração para JSON."""
        return json.dumps(self.to_dict(), default=str, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompressionConfig':
        """Cria configuração a partir de dicionário."""
        # Converter enums
        if 'compression_level' in data and isinstance(data['compression_level'], str):
            data['compression_level'] = CompressionLevel(data['compression_level'])
        if 'quality_profile' in data and isinstance(data['quality_profile'], str):
            data['quality_profile'] = QualityProfile(data['quality_profile'])
        
        # Criar instância
        config = cls()
        
        # Atualizar campos
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config
    
    @classmethod
    def from_json(cls, json_str: str) -> 'CompressionConfig':
        """Cria configuração a partir de JSON."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def validate(self) -> List[str]:
        """Valida a configuração e retorna lista de erros."""
        errors = []
        
        # Validar qualidade JPEG
        if not 1 <= self.image_config.jpeg_quality <= 100:
            errors.append("Qualidade JPEG deve estar entre 1 e 100")
        
        # Validar nível de compressão
        if not 1 <= self.stream_config.compression_level <= 9:
            errors.append("Nível de compressão deve estar entre 1 e 9")
        
        # Validar dimensões máximas
        if self.image_config.max_width < 100 or self.image_config.max_height < 100:
            errors.append("Dimensões mínimas devem ser pelo menos 100px")
        
        # Validar timeout
        if self.performance_config.operation_timeout < 10:
            errors.append("Timeout deve ser pelo menos 10 segundos")
        
        return errors


# Configurações predefinidas
def create_minimal_config() -> CompressionConfig:
    """Cria configuração para compressão mínima."""
    config = CompressionConfig()
    config.apply_preset(CompressionLevel.MINIMAL)
    return config


def create_balanced_config() -> CompressionConfig:
    """Cria configuração balanceada."""
    config = CompressionConfig()
    config.apply_preset(CompressionLevel.BALANCED)
    return config


def create_aggressive_config() -> CompressionConfig:
    """Cria configuração para máxima compressão."""
    config = CompressionConfig()
    config.apply_preset(CompressionLevel.AGGRESSIVE)
    return config


def create_web_optimized_config() -> CompressionConfig:
    """Cria configuração otimizada para web."""
    config = create_balanced_config()
    config.apply_quality_profile(QualityProfile.WEB)
    return config


def create_email_optimized_config() -> CompressionConfig:
    """Cria configuração otimizada para email."""
    config = create_aggressive_config()
    config.apply_quality_profile(QualityProfile.EMAIL)
    return config
