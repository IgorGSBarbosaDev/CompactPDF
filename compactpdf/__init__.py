"""
CompactPDF - Core Package
========================

Sistema de compressão de PDF focado em PyMuPDF e Spire.PDF
para compressão de 40-60%.
"""

__version__ = "2.0.0"
__author__ = "CompactPDF Team"

from .core.facade import PDFCompressor
from .core.models import CompressionResult, CompressionConfig, CompressionLevel
from .strategies.pymupdf_strategy import PyMuPDFStrategy
from .strategies.spire_strategy import SpireStrategy

__all__ = [
    'PDFCompressor',
    'CompressionResult', 
    'CompressionConfig',
    'CompressionLevel',
    'PyMuPDFStrategy',
    'SpireStrategy'
]
