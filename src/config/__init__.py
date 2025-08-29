#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações - CompactPDF
==========================

Este módulo contém todas as configurações utilizadas pelo CompactPDF.
"""

# Importar classes principais
from .compression_config import (
    CompressionConfig,
    CompressionLevel,
    QualityProfile,
    ImageCompressionConfig,
    FontOptimizationConfig,
    StreamCompressionConfig,
    MetadataConfig,
    OptimizationConfig,
    BackupConfig,
    PerformanceConfig,
    create_minimal_config,
    create_balanced_config,
    create_aggressive_config,
    create_web_optimized_config,
    create_email_optimized_config
)

# Definir what will be available when importing from config
__all__ = [
    # Classes principais
    "CompressionConfig",
    
    # Enums
    "CompressionLevel",
    "QualityProfile",
    
    # Classes de configuração específicas
    "ImageCompressionConfig",
    "FontOptimizationConfig",
    "StreamCompressionConfig",
    "MetadataConfig",
    "OptimizationConfig",
    "BackupConfig",
    "PerformanceConfig",
    
    # Funções de conveniência
    "create_minimal_config",
    "create_balanced_config",
    "create_aggressive_config",
    "create_web_optimized_config",
    "create_email_optimized_config"
]
