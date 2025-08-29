#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de resultado de compressão - CompactPDF
==============================================

Define a estrutura de dados para resultados de compressão de PDFs.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
import json


@dataclass
class CompressionResult:
    """
    Resultado de uma operação de compressão de PDF.
    
    Contém todas as informações sobre o processo de compressão,
    incluindo métricas, tempo de execução e metadados.
    """
    
    # Informações básicas
    input_path: str
    output_path: str
    success: bool
    
    # Métricas de tamanho
    original_size: int
    compressed_size: int
    compression_ratio: float = 0.0
    space_saved: int = 0
    
    # Métricas de tempo
    processing_time: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Estratégias aplicadas
    strategies_used: Optional[List[str]] = None
    strategy_results: Optional[Dict[str, Any]] = None
    
    # Métricas de qualidade
    quality_score: Optional[float] = None
    quality_metrics: Optional[Dict[str, float]] = None
    
    # Informações do arquivo
    page_count: Optional[int] = None
    has_images: Optional[bool] = None
    has_fonts: Optional[bool] = None
    has_forms: Optional[bool] = None
    
    # Metadados
    backup_created: bool = False
    backup_path: Optional[str] = None
    cache_hit: bool = False
    error_message: Optional[str] = None
    
    def __post_init__(self):
        """Calcula campos derivados após inicialização."""
        if self.strategies_used is None:
            self.strategies_used = []
        if self.strategy_results is None:
            self.strategy_results = {}
        
        if self.original_size > 0 and self.compressed_size > 0:
            self.compression_ratio = 1 - (self.compressed_size / self.original_size)
            self.space_saved = self.original_size - self.compressed_size
        
        if self.start_time is None:
            self.start_time = datetime.now()
        if self.end_time is None:
            self.end_time = datetime.now()
    
    @property
    def compression_percentage(self) -> float:
        """Retorna porcentagem de compressão."""
        return self.compression_ratio * 100
    
    @property
    def size_reduction_mb(self) -> float:
        """Retorna redução de tamanho em MB."""
        return self.space_saved / (1024 * 1024)
    
    @property
    def original_size_mb(self) -> float:
        """Retorna tamanho original em MB."""
        return self.original_size / (1024 * 1024)
    
    @property
    def compressed_size_mb(self) -> float:
        """Retorna tamanho comprimido em MB."""
        return self.compressed_size / (1024 * 1024)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte resultado para dicionário."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
    
    def to_json(self) -> str:
        """Converte resultado para JSON."""
        return json.dumps(self.to_dict(), default=str, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompressionResult':
        """Cria instância a partir de dicionário."""
        # Converter strings de data de volta para datetime
        if 'start_time' in data and isinstance(data['start_time'], str):
            data['start_time'] = datetime.fromisoformat(data['start_time'])
        if 'end_time' in data and isinstance(data['end_time'], str):
            data['end_time'] = datetime.fromisoformat(data['end_time'])
        
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'CompressionResult':
        """Cria instância a partir de JSON."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def get_summary(self) -> str:
        """Retorna resumo legível do resultado."""
        if not self.success:
            return f"❌ Falha: {self.error_message or 'Erro desconhecido'}"
        
        return (
            f"✅ {self.compression_percentage:.1f}% redução • "
            f"{self.size_reduction_mb:.2f} MB economizado • "
            f"{self.processing_time:.2f}s"
        )
    
    def is_significant_compression(self, threshold: float = 10.0) -> bool:
        """Verifica se a compressão foi significativa."""
        return self.compression_percentage >= threshold
    
    def get_efficiency_score(self) -> float:
        """
        Calcula score de eficiência baseado em compressão vs tempo.
        
        Returns:
            float: Score de 0-100 (maior é melhor)
        """
        if not self.success or self.processing_time <= 0:
            return 0.0
        
        # Fórmula: (compressão% * tamanho_mb) / tempo
        efficiency = (self.compression_percentage * self.original_size_mb) / self.processing_time
        
        # Normalizar para 0-100 (valores típicos: 1-50)
        return min(100.0, efficiency * 2)


# Função de conveniência para criar resultado de erro
def create_error_result(
    input_path: str,
    output_path: str,
    error_message: str,
    processing_time: float = 0.0
) -> CompressionResult:
    """
    Cria um CompressionResult para casos de erro.
    
    Args:
        input_path: Caminho do arquivo de entrada
        output_path: Caminho do arquivo de saída
        error_message: Mensagem de erro
        processing_time: Tempo gasto antes do erro
    
    Returns:
        CompressionResult: Resultado marcado como falha
    """
    return CompressionResult(
        input_path=input_path,
        output_path=output_path,
        success=False,
        original_size=0,
        compressed_size=0,
        processing_time=processing_time,
        error_message=error_message,
        start_time=datetime.now(),
        end_time=datetime.now()
    )


# Função de conveniência para criar resultado de sucesso
def create_success_result(
    input_path: str,
    output_path: str,
    original_size: int,
    compressed_size: int,
    processing_time: float,
    strategies_used: Optional[List[str]] = None
) -> CompressionResult:
    """
    Cria um CompressionResult para casos de sucesso.
    
    Args:
        input_path: Caminho do arquivo de entrada
        output_path: Caminho do arquivo de saída
        original_size: Tamanho original em bytes
        compressed_size: Tamanho comprimido em bytes
        processing_time: Tempo de processamento
        strategies_used: Lista de estratégias aplicadas
    
    Returns:
        CompressionResult: Resultado marcado como sucesso
    """
    return CompressionResult(
        input_path=input_path,
        output_path=output_path,
        success=True,
        original_size=original_size,
        compressed_size=compressed_size,
        processing_time=processing_time,
        strategies_used=strategies_used or [],
        start_time=datetime.now(),
        end_time=datetime.now()
    )
