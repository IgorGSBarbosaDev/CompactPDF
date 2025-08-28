"""
Compression strategies module.
Contains all compression strategy implementations.
"""

from .image_compression import ImageCompressionStrategy
from .font_optimization import FontOptimizationStrategy
from .content_optimization import ContentOptimizationStrategy
from .adaptive_compression import AdaptiveCompressionStrategy

__all__ = [
    'ImageCompressionStrategy',
    'FontOptimizationStrategy', 
    'ContentOptimizationStrategy',
    'AdaptiveCompressionStrategy'
]
