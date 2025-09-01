#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estratégias de Compressão - CompactPDF
======================================

Implementações das estratégias de compressão de PDF.
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
