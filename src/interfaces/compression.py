#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface de Compressão - CompactPDF
====================================

Define a interface abstrata para estratégias de compressão.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..models.compression_result import CompressionResult
from ..models.pdf_analysis import PDFAnalysis
from ..config.compression_config import CompressionConfig


class ICompressionStrategy(ABC):
    """
    Interface abstrata para estratégias de compressão de PDF.
    
    Todas as estratégias de compressão devem implementar esta interface
    para garantir compatibilidade com o sistema.
    """
    
    @abstractmethod
    def compress(self, 
                 input_path: str, 
                 output_path: str, 
                 config: CompressionConfig,
                 analysis: Optional[PDFAnalysis] = None) -> CompressionResult:
        """
        Executa a compressão do PDF.
        
        Args:
            input_path: Caminho do arquivo PDF de entrada
            output_path: Caminho do arquivo PDF de saída
            config: Configuração de compressão
            analysis: Análise prévia do PDF (opcional)
            
        Returns:
            CompressionResult: Resultado da compressão
            
        Raises:
            CompressionError: Se houver erro na compressão
        """
        pass
    
    @abstractmethod
    def can_handle(self, analysis: PDFAnalysis) -> bool:
        """
        Verifica se esta estratégia pode processar o PDF.
        
        Args:
            analysis: Análise do PDF
            
        Returns:
            bool: True se pode processar, False caso contrário
        """
        pass
    
    @abstractmethod
    def estimate_compression(self, analysis: PDFAnalysis, config: CompressionConfig) -> float:
        """
        Estima a taxa de compressão esperada.
        
        Args:
            analysis: Análise do PDF
            config: Configuração de compressão
            
        Returns:
            float: Taxa de compressão estimada (0.0 a 1.0)
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nome da estratégia."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Descrição da estratégia."""
        pass
    
    @property
    @abstractmethod
    def supported_features(self) -> Dict[str, bool]:
        """
        Features suportadas pela estratégia.
        
        Returns:
            Dict com features: images, fonts, metadata, content, etc.
        """
        pass


class IAnalysisStrategy(ABC):
    """Interface para estratégias de análise de PDF."""
    
    @abstractmethod
    def analyze(self, file_path: str) -> PDFAnalysis:
        """
        Analisa um arquivo PDF.
        
        Args:
            file_path: Caminho do arquivo PDF
            
        Returns:
            PDFAnalysis: Resultado da análise
        """
        pass


class IQualityValidator(ABC):
    """Interface para validadores de qualidade."""
    
    @abstractmethod
    def validate(self, 
                 original_path: str, 
                 compressed_path: str, 
                 config: CompressionConfig) -> Dict[str, Any]:
        """
        Valida a qualidade do PDF comprimido.
        
        Args:
            original_path: Caminho do PDF original
            compressed_path: Caminho do PDF comprimido
            config: Configuração usada
            
        Returns:
            Dict com métricas de qualidade
        """
        pass


class IProgressCallback(ABC):
    """Interface para callbacks de progresso."""
    
    @abstractmethod
    def on_progress(self, stage: str, progress: float, message: str = ""):
        """
        Chamado durante o progresso da compressão.
        
        Args:
            stage: Estágio atual (analyze, compress, validate, etc.)
            progress: Progresso de 0.0 a 1.0
            message: Mensagem opcional
        """
        pass
    
    @abstractmethod
    def on_error(self, error: Exception, stage: str = ""):
        """
        Chamado quando ocorre um erro.
        
        Args:
            error: Exceção que ocorreu
            stage: Estágio onde ocorreu o erro
        """
        pass
    
    @abstractmethod
    def on_complete(self, result: CompressionResult):
        """
        Chamado quando a compressão é completada.
        
        Args:
            result: Resultado da compressão
        """
        pass


# Aliases para backward compatibility
CompressionStrategyInterface = ICompressionStrategy
AnalysisStrategyInterface = IAnalysisStrategy
QualityValidatorInterface = IQualityValidator
ProgressCallbackInterface = IProgressCallback


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
