#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serviço de Métricas de Compressão
=================================

Calcula e gerencia métricas de compressão.
"""

from typing import Dict, List, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CompressionMetricsService:
    """Serviço para cálculo de métricas de compressão."""
    
    def __init__(self):
        self.metrics_history: List[Dict[str, Any]] = []
    
    def calculate_compression_ratio(self, original_size: int, compressed_size: int) -> float:
        """Calcula a taxa de compressão."""
        if original_size <= 0:
            return 0.0
        return 1.0 - (compressed_size / original_size)
    
    def calculate_compression_percentage(self, original_size: int, compressed_size: int) -> float:
        """Calcula a porcentagem de compressão."""
        return self.calculate_compression_ratio(original_size, compressed_size) * 100
    
    def calculate_space_saved(self, original_size: int, compressed_size: int) -> int:
        """Calcula o espaço economizado em bytes."""
        return max(0, original_size - compressed_size)
    
    def calculate_space_saved_mb(self, original_size: int, compressed_size: int) -> float:
        """Calcula o espaço economizado em MB."""
        return self.calculate_space_saved(original_size, compressed_size) / (1024 * 1024)
    
    def add_metrics(self, metrics: Dict[str, Any]):
        """Adiciona métricas ao histórico."""
        metrics['timestamp'] = datetime.now()
        self.metrics_history.append(metrics)
    
    def get_average_compression_ratio(self) -> float:
        """Calcula a taxa média de compressão."""
        if not self.metrics_history:
            return 0.0
        
        ratios = [m.get('compression_ratio', 0) for m in self.metrics_history]
        return sum(ratios) / len(ratios)
    
    def get_total_space_saved(self) -> int:
        """Calcula o total de espaço economizado."""
        return sum(m.get('space_saved', 0) for m in self.metrics_history)
    
    def get_success_rate(self) -> float:
        """Calcula a taxa de sucesso das compressões."""
        if not self.metrics_history:
            return 0.0
        
        successful = sum(1 for m in self.metrics_history if m.get('success', False))
        return (successful / len(self.metrics_history)) * 100
    
    def generate_report(self) -> Dict[str, Any]:
        """Gera relatório das métricas."""
        return {
            'total_compressions': len(self.metrics_history),
            'average_compression_ratio': self.get_average_compression_ratio(),
            'total_space_saved_mb': self.get_total_space_saved() / (1024 * 1024),
            'success_rate': self.get_success_rate(),
            'last_compression': self.metrics_history[-1] if self.metrics_history else None
        }
