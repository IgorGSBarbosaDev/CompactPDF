#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interfaces - CompactPDF
=======================

Define todas as interfaces abstratas do sistema.
"""

from .compression import (
    ICompressionStrategy,
    IAnalysisStrategy,
    IQualityValidator,
    IProgressCallback,
    # Aliases
    CompressionStrategyInterface,
    AnalysisStrategyInterface,
    QualityValidatorInterface,
    ProgressCallbackInterface
)

__all__ = [
    'ICompressionStrategy',
    'IAnalysisStrategy', 
    'IQualityValidator',
    'IProgressCallback',
    # Aliases
    'CompressionStrategyInterface',
    'AnalysisStrategyInterface',
    'QualityValidatorInterface', 
    'ProgressCallbackInterface'
]
