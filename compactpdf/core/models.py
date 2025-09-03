"""
CompactPDF - Modelos de Dados
=============================

Modelos essenciais para o sistema de compressão.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any
from pathlib import Path


class CompressionLevel(Enum):
    """Níveis de compressão disponíveis."""
    LIGHT = "light"
    MEDIUM = "medium" 
    AGGRESSIVE = "aggressive"


@dataclass
class CompressionResult:
    """Resultado de uma operação de compressão."""
    input_path: str
    output_path: str
    success: bool
    original_size: int
    compressed_size: int
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    method_used: Optional[str] = None
    
    @property
    def reduction_percentage(self) -> float:
        """Calcula a porcentagem de redução."""
        if self.original_size == 0:
            return 0.0
        return ((self.original_size - self.compressed_size) / self.original_size) * 100
    
    @property
    def size_saved(self) -> int:
        """Calcula o espaço economizado em bytes."""
        return max(0, self.original_size - self.compressed_size)


@dataclass
class CompressionConfig:
    """Configuração para compressão de PDF."""
    level: CompressionLevel = CompressionLevel.MEDIUM
    method: Optional[str] = None  # 'pymupdf', 'spire', ou None para auto
    create_backup: bool = True
    overwrite_existing: bool = False
    output_directory: Optional[str] = None
    
    def apply_preset(self, level: CompressionLevel):
        """Aplica um preset de compressão."""
        self.level = level


def create_success_result(
    input_path: str,
    output_path: str,
    original_size: int,
    compressed_size: int,
    processing_time: float = 0.0,
    method_used: str = "unknown"
) -> CompressionResult:
    """Cria um resultado de sucesso."""
    return CompressionResult(
        input_path=input_path,
        output_path=output_path,
        success=True,
        original_size=original_size,
        compressed_size=compressed_size,
        processing_time=processing_time,
        method_used=method_used
    )


def create_error_result(
    input_path: str,
    output_path: str,
    error_message: str,
    original_size: int = 0,
    method_used: str = "unknown"
) -> CompressionResult:
    """Cria um resultado de erro."""
    return CompressionResult(
        input_path=input_path,
        output_path=output_path,
        success=False,
        original_size=original_size,
        compressed_size=original_size,
        error_message=error_message,
        method_used=method_used
    )
