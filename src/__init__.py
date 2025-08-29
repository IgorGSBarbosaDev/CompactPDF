"""
🗜️ CompactPDF - Sistema Inteligente de Compressão de PDF

Um sistema avançado de compressão de PDF construído com princípios SOLID,
oferecendo até 60% de compressão mantendo qualidade visual superior.

Características:
    - 🧠 Compressão inteligente com análise automática de conteúdo
    - 📊 Múltiplos níveis de compressão (minimal, balanced, aggressive)
    - 🎯 Alta performance com processamento otimizado
    - 🛡️ Sistema de validação e verificação de integridade
    - 📈 Interface gráfica intuitiva e fácil de usar
    - 🏗️ Arquitetura limpa e mantível

Uso Básico:
    >>> from src import PDFCompressorFacade
    >>> compressor = PDFCompressorFacade()
    >>> result = compressor.compress_file("input.pdf", "output.pdf")
    >>> print(f"Compressão: {result.compression_ratio:.1%}")
"""

__version__ = "2.0.0"
__author__ = "CompactPDF Team"

# Importações principais
print("DEBUG: Iniciando imports...")

try:
    from .pdf_compressor_facade import PDFCompressorFacade, quick_compress
    print("DEBUG: PDFCompressorFacade importado")
except Exception as e:
    print(f"DEBUG: Erro PDFCompressorFacade: {e}")

try:
    from .models import (
        CompressionResult, 
        PDFAnalysis, 
        CompressionRecommendations,
        create_error_result,
        create_success_result
    )
    print("DEBUG: Models importados")
except Exception as e:
    print(f"DEBUG: Erro Models: {e}")

try:
    from .config.compression_config import (
        CompressionConfig,
        CompressionLevel,
        QualityProfile
    )
    print("DEBUG: Config importado")
except Exception as e:
    print(f"DEBUG: Erro Config: {e}")

# Lista de exportações
__all__ = [
    'PDFCompressorFacade',
    'quick_compress',
    'CompressionResult',
    'PDFAnalysis', 
    'CompressionRecommendations',
    'CompressionConfig',
    'CompressionLevel',
    'QualityProfile',
    'create_error_result',
    'create_success_result'
]

print(f"DEBUG: __all__ definido: {__all__}")
