"""
🗜️ CompactPDF - Sistema Inteligente de Compressão de PDF

Um sistema avançado de compressão de PDF construído com princípios SOLID,
oferecendo até 60% de compressão mantendo qualidade visual superior.

Características:
    - 🧠 Compressão inteligente com análise automática de conteúdo
    - 📊 4 estratégias de compressão especializadas  
    - 🎯 Alta performance com cache e otimizações
    - 🛡️ Sistema completo de backup e recuperação
    - 📈 Analytics avançado com relatórios detalhados
    - 🏗️ Arquitetura SOLID extensível e mantível

Uso Básico:
    >>> from src import PDFCompressorFacade, CompressionConfig
    >>> compressor = PDFCompressorFacade()
    >>> result = compressor.compress_pdf("input.pdf", "output.pdf")
    >>> print(f"Compressão: {result.compression_ratio:.1%}")

Exemplo Avançado:
    >>> from src.strategies import AdaptiveCompressionStrategy
    >>> from src.utils import CompressionCache, BackupManager
    >>> 
    >>> strategy = AdaptiveCompressionStrategy()
    >>> config = CompressionConfig.get_web_optimized_config()
    >>> result = compressor.compress_pdf("input.pdf", "output.pdf", config, strategy)
"""

import sys
import os
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

# Lazy imports para melhor performance inicial
if TYPE_CHECKING:
    # Import apenas para type checking, não runtime
    from .pdf_compressor import PDFCompressorFacade
    from .config import CompressionConfig, PresetConfig, CompressionLevel
    from .services import PDFFileService, CompressionMetricsService, CompressionResult
    from .strategies import (
        ImageCompressionStrategy, FontOptimizationStrategy,
        ContentOptimizationStrategy, AdaptiveCompressionStrategy
    )
    from .utils import (
        SimpleLogger, NullLogger, ImageQualityAssessor,
        CompressionCache, BackupManager, CompressionAnalytics,
        AdaptiveCompressionOptimizer, is_pdf_file, validate_output_path,
        get_safe_filename, generate_output_filename
    )
    from .interfaces import ICompressionStrategy, ILogger

# Metadata
__version__ = "2.1.0"  # Atualizada para refletir melhorias
__author__ = "CompactPDF Team"
__description__ = "Sistema Inteligente de Compressão de PDF com Arquitetura SOLID"
__license__ = "MIT"
__url__ = "https://github.com/IgorGSBarbosaDev/CompactPDF"

# Cache para módulos carregados lazy
_loaded_modules: Dict[str, Any] = {}

# Core exports - carregamento lazy
__all__ = [
    # 🎯 COMPONENTES PRINCIPAIS
    'PDFCompressorFacade',
    'CompressionConfig', 
    'PresetConfig',
    'CompressionLevel',
    
    # 🛠️ SERVIÇOS
    'PDFFileService',
    'CompressionMetricsService', 
    'CompressionResult',
    
    # ⚡ ESTRATÉGIAS
    'ImageCompressionStrategy',
    'FontOptimizationStrategy',
    'ContentOptimizationStrategy',
    'AdaptiveCompressionStrategy',
    
    # 🔧 UTILITÁRIOS BÁSICOS
    'SimpleLogger',
    'NullLogger',
    'is_pdf_file',
    'validate_output_path',
    'get_safe_filename',
    'generate_output_filename',
    
    # 🚀 FUNCIONALIDADES AVANÇADAS
    'ImageQualityAssessor',
    'CompressionCache',
    'BackupManager',
    'CompressionAnalytics',
    'AdaptiveCompressionOptimizer',
    
    # 🔌 INTERFACES
    'ICompressionStrategy',
    'ILogger',
    
    # 🛠️ UTILITÁRIOS DO MÓDULO
    'get_version_info',
    'print_welcome',
    'quick_compress',
    'is_available'
]


def __getattr__(name: str) -> Any:
    """
    Lazy loading implementation para melhor performance.
    
    Carrega módulos apenas quando necessário, reduzindo tempo de import inicial.
    """
    if name in _loaded_modules:
        return _loaded_modules[name]
    
    try:
        # Core Components
        if name == 'PDFCompressorFacade':
            from .pdf_compressor import PDFCompressorFacade
            _loaded_modules[name] = PDFCompressorFacade
            return PDFCompressorFacade
            
        elif name in ['CompressionConfig', 'PresetConfig', 'CompressionLevel']:
            from .config import CompressionConfig, PresetConfig, CompressionLevel
            if name == 'CompressionConfig':
                _loaded_modules[name] = CompressionConfig
                return CompressionConfig
            elif name == 'PresetConfig':
                _loaded_modules[name] = PresetConfig
                return PresetConfig
            elif name == 'CompressionLevel':
                _loaded_modules[name] = CompressionLevel
                return CompressionLevel
                
        # Services
        elif name in ['PDFFileService', 'CompressionMetricsService', 'CompressionResult']:
            from .services import PDFFileService, CompressionMetricsService, CompressionResult
            if name == 'PDFFileService':
                _loaded_modules[name] = PDFFileService
                return PDFFileService
            elif name == 'CompressionMetricsService':
                _loaded_modules[name] = CompressionMetricsService
                return CompressionMetricsService
            elif name == 'CompressionResult':
                _loaded_modules[name] = CompressionResult
                return CompressionResult
                
        # Strategies - lazy loading para evitar imports pesados
        elif name in ['ImageCompressionStrategy', 'FontOptimizationStrategy', 
                     'ContentOptimizationStrategy', 'AdaptiveCompressionStrategy']:
            from .strategies import (
                ImageCompressionStrategy, FontOptimizationStrategy,
                ContentOptimizationStrategy, AdaptiveCompressionStrategy
            )
            strategy_map = {
                'ImageCompressionStrategy': ImageCompressionStrategy,
                'FontOptimizationStrategy': FontOptimizationStrategy,
                'ContentOptimizationStrategy': ContentOptimizationStrategy,
                'AdaptiveCompressionStrategy': AdaptiveCompressionStrategy
            }
            _loaded_modules[name] = strategy_map[name]
            return strategy_map[name]
            
        # Basic Utils
        elif name in ['SimpleLogger', 'NullLogger']:
            from .utils.logger import SimpleLogger, NullLogger
            if name == 'SimpleLogger':
                _loaded_modules[name] = SimpleLogger
                return SimpleLogger
            else:
                _loaded_modules[name] = NullLogger
                return NullLogger
                
        # File Utils
        elif name in ['is_pdf_file', 'validate_output_path', 'get_safe_filename', 'generate_output_filename']:
            from .utils.file_utils import (
                is_pdf_file, validate_output_path, get_safe_filename, generate_output_filename
            )
            file_utils_map = {
                'is_pdf_file': is_pdf_file,
                'validate_output_path': validate_output_path,
                'get_safe_filename': get_safe_filename,
                'generate_output_filename': generate_output_filename
            }
            _loaded_modules[name] = file_utils_map[name]
            return file_utils_map[name]
            
        # Advanced Utils - carregamento sob demanda
        elif name in ['ImageQualityAssessor', 'CompressionCache', 'BackupManager', 
                     'CompressionAnalytics', 'AdaptiveCompressionOptimizer']:
            if name == 'ImageQualityAssessor':
                from .utils.image_quality import ImageQualityAssessor
                _loaded_modules[name] = ImageQualityAssessor
                return ImageQualityAssessor
            elif name == 'CompressionCache':
                from .utils.cache import CompressionCache
                _loaded_modules[name] = CompressionCache
                return CompressionCache
            elif name == 'BackupManager':
                from .utils.backup import BackupManager
                _loaded_modules[name] = BackupManager
                return BackupManager
            elif name == 'CompressionAnalytics':
                from .utils.analytics import CompressionAnalytics
                _loaded_modules[name] = CompressionAnalytics
                return CompressionAnalytics
            elif name == 'AdaptiveCompressionOptimizer':
                from .utils.adaptive_optimizer import AdaptiveCompressionOptimizer
                _loaded_modules[name] = AdaptiveCompressionOptimizer
                return AdaptiveCompressionOptimizer
                
        # Interfaces
        elif name in ['ICompressionStrategy', 'ILogger']:
            from .interfaces import ICompressionStrategy, ILogger
            if name == 'ICompressionStrategy':
                _loaded_modules[name] = ICompressionStrategy
                return ICompressionStrategy
            else:
                _loaded_modules[name] = ILogger
                return ILogger
                
    except ImportError as e:
        # Em caso de erro de import, forneça mensagem útil
        raise ImportError(f"Cannot import {name}: {e}. Verifique se todas as dependências estão instaladas.")
    
    # Se chegou aqui, o atributo não existe
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Informações de debug para desenvolvimento
def get_version_info() -> Dict[str, Any]:
    """
    Retorna informações detalhadas da versão.
    
    Returns:
        Dict com informações de versão, componentes e dependências
    """
    return {
        'version': __version__,
        'description': __description__,
        'author': __author__,
        'license': __license__,
        'url': __url__,
        'components': {
            'strategies': 4,
            'services': 3,
            'utils': 9,
            'interfaces': 2
        },
        'loaded_modules': list(_loaded_modules.keys()),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }


def print_welcome() -> None:
    """Exibe mensagem de boas-vindas com informações do sistema."""
    print(f"🗜️ CompactPDF v{__version__} - Sistema Inteligente de Compressão de PDF")
    print("🏗️ Arquitetura SOLID | 🧠 IA Integrada | 📊 Analytics Avançado")
    print("=" * 60)


def quick_compress(input_file: str, output_file: Optional[str] = None, 
                  preset: str = 'balanced') -> 'CompressionResult':
    """
    Função de conveniência para compressão rápida.
    
    Args:
        input_file: Caminho do arquivo PDF de entrada
        output_file: Caminho do arquivo de saída (opcional)
        preset: Preset de compressão ('web', 'print', 'balanced', 'quality')
        
    Returns:
        CompressionResult com informações da compressão
    """
    compressor = PDFCompressorFacade()
    
    # Configurações por preset
    preset_configs = {
        'web': CompressionConfig(image_quality=60, compress_streams=True, remove_duplicates=True),
        'print': CompressionConfig(image_quality=85, compress_streams=True, remove_duplicates=False),
        'balanced': CompressionConfig(image_quality=75, compress_streams=True, remove_duplicates=True),
        'quality': CompressionConfig(image_quality=95, compress_streams=False, remove_duplicates=True)
    }
    
    config = preset_configs.get(preset, preset_configs['balanced'])
    
    if not output_file:
        output_file = generate_output_filename(input_file)
    
    return compressor.compress_pdf(input_file, output_file, config)


def is_available() -> bool:
    """
    Verifica se o CompactPDF está corretamente instalado.
    
    Returns:
        True se todas as dependências estão disponíveis
    """
    try:
        import PyPDF2
        from PIL import Image
        from reportlab.pdfgen import canvas
        return True
    except ImportError:
        return False


# Auto-configuração para ambiente de desenvolvimento
if os.getenv('COMPACTPDF_DEBUG'):
    print_welcome()
    print(f"🔍 Modo Debug Ativo")
    print(f"📦 {len(__all__)} componentes disponíveis")
    print(f"� Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Pré-carrega componentes em modo debug
    if os.getenv('COMPACTPDF_PRELOAD'):
        print("⚡ Pré-carregando componentes...")
        _ = PDFCompressorFacade, CompressionConfig
        print(f"✅ {len(_loaded_modules)} componentes carregados")
