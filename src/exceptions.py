#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exceções customizadas - CompactPDF
==================================

Define todas as exceções específicas do sistema de compressão de PDFs.
"""

from typing import Optional


class CompressionError(Exception):
    """Exceção base para erros de compressão."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, original_error: Optional[Exception] = None):
        self.message = message
        self.error_code = error_code
        self.original_error = original_error
        super().__init__(self.message)


class InvalidPDFError(CompressionError):
    """Exceção lançada quando o arquivo PDF é inválido ou corrompido."""
    
    def __init__(self, message: str = "Arquivo PDF inválido ou corrompido"):
        super().__init__(message, error_code="INVALID_PDF")


class CompressionFailedError(CompressionError):
    """Exceção lançada quando a compressão falha por motivos técnicos."""
    
    def __init__(self, message: str = "Falha na compressão do PDF", strategy: Optional[str] = None):
        self.strategy = strategy
        if strategy:
            message = f"{message} (estratégia: {strategy})"
        super().__init__(message, error_code="COMPRESSION_FAILED")


class QualityThresholdError(CompressionError):
    """Exceção lançada quando a qualidade resultante está abaixo do threshold."""
    
    def __init__(self, message: str = "Qualidade resultante abaixo do threshold", 
                 quality_score: Optional[float] = None, threshold: Optional[float] = None):
        self.quality_score = quality_score
        self.threshold = threshold
        if quality_score is not None and threshold is not None:
            message = f"{message} (qualidade: {quality_score:.2f}, threshold: {threshold:.2f})"
        super().__init__(message, error_code="QUALITY_THRESHOLD")


class PluginLoadError(CompressionError):
    """Exceção lançada quando há erro ao carregar um plugin."""
    
    def __init__(self, message: str = "Erro ao carregar plugin", plugin_name: Optional[str] = None):
        self.plugin_name = plugin_name
        if plugin_name:
            message = f"{message}: {plugin_name}"
        super().__init__(message, error_code="PLUGIN_LOAD_ERROR")


class CacheError(CompressionError):
    """Exceção lançada quando há erro relacionado ao cache."""
    
    def __init__(self, message: str = "Erro no sistema de cache"):
        super().__init__(message, error_code="CACHE_ERROR")


class ConfigurationError(CompressionError):
    """Exceção lançada quando há erro na configuração."""
    
    def __init__(self, message: str = "Erro de configuração", parameter: Optional[str] = None):
        self.parameter = parameter
        if parameter:
            message = f"{message} (parâmetro: {parameter})"
        super().__init__(message, error_code="CONFIGURATION_ERROR")


class FileAccessError(CompressionError):
    """Exceção lançada quando há erro de acesso a arquivos."""
    
    def __init__(self, message: str = "Erro de acesso ao arquivo", file_path: Optional[str] = None):
        self.file_path = file_path
        if file_path:
            message = f"{message}: {file_path}"
        super().__init__(message, error_code="FILE_ACCESS_ERROR")


class MemoryError(CompressionError):
    """Exceção lançada quando há falta de memória durante a compressão."""
    
    def __init__(self, message: str = "Memória insuficiente para compressão"):
        super().__init__(message, error_code="MEMORY_ERROR")


class StrategyNotFoundError(CompressionError):
    """Exceção lançada quando uma estratégia de compressão não é encontrada."""
    
    def __init__(self, message: str = "Estratégia de compressão não encontrada", strategy_name: Optional[str] = None):
        self.strategy_name = strategy_name
        if strategy_name:
            message = f"{message}: {strategy_name}"
        super().__init__(message, error_code="STRATEGY_NOT_FOUND")


# Lista de todas as exceções para facilitar imports
__all__ = [
    'CompressionError',
    'InvalidPDFError', 
    'CompressionFailedError',
    'QualityThresholdError',
    'PluginLoadError',
    'CacheError',
    'ConfigurationError',
    'FileAccessError',
    'MemoryError',
    'StrategyNotFoundError'
]
