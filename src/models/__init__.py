#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelos de dados - CompactPDF
=============================

Este módulo contém todos os modelos de dados utilizados pelo CompactPDF.
"""

# Importar classes principais
from .compression_result import CompressionResult, create_error_result, create_success_result
from .pdf_analysis import PDFAnalysis, ImageInfo, FontInfo, PageInfo, create_basic_analysis
from .compression_recommendations import (
    CompressionRecommendations, 
    StrategyRecommendation, 
    StrategyPriority, 
    CompressionImpact,
    RecommendationFactory,
    create_basic_recommendations
)

# Definir what will be available when importing from models
__all__ = [
    # Classes principais
    "CompressionResult",
    "PDFAnalysis", 
    "CompressionRecommendations",
    
    # Classes auxiliares
    "ImageInfo",
    "FontInfo", 
    "PageInfo",
    "StrategyRecommendation",
    
    # Enums
    "StrategyPriority",
    "CompressionImpact",
    
    # Factories e funções de conveniência
    "RecommendationFactory",
    "create_error_result",
    "create_success_result", 
    "create_basic_analysis",
    "create_basic_recommendations"
]
