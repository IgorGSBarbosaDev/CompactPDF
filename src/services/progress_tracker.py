#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rastreador de Progresso
=======================

Gerencia o progresso de operações de compressão.
"""

from typing import Callable, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProgressTracker:
    """Rastreador de progresso para operações de compressão."""
    
    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback
        self.current_stage = ""
        self.current_progress = 0.0
        self.start_time = None
        self.stages_completed = 0
        self.total_stages = 0
        self.is_cancelled = False
    
    def start(self, total_stages: int = 5):
        """Inicia o rastreamento de progresso."""
        self.start_time = datetime.now()
        self.total_stages = total_stages
        self.stages_completed = 0
        self.current_progress = 0.0
        self.is_cancelled = False
        logger.info(f"Iniciando progresso com {total_stages} estágios")
    
    def update_stage(self, stage_name: str, progress: float = 0.0):
        """Atualiza o estágio atual."""
        self.current_stage = stage_name
        self.current_progress = progress
        
        # Calcula progresso geral
        overall_progress = (self.stages_completed + progress) / self.total_stages
        
        if self.callback:
            self.callback(stage_name, overall_progress, "")
        
        logger.debug(f"Estágio: {stage_name}, Progresso: {progress:.1%}")
    
    def complete_stage(self, stage_name: str):
        """Marca um estágio como completo."""
        self.stages_completed += 1
        self.current_stage = stage_name
        self.current_progress = 1.0
        
        overall_progress = self.stages_completed / self.total_stages
        
        if self.callback:
            self.callback(stage_name, overall_progress, f"Estágio {stage_name} completo")
        
        logger.info(f"Estágio completo: {stage_name} ({self.stages_completed}/{self.total_stages})")
    
    def report_error(self, error: Exception, stage: str = ""):
        """Reporta um erro."""
        error_stage = stage or self.current_stage
        logger.error(f"Erro no estágio {error_stage}: {error}")
        
        # Chama callback simples se disponível
        if self.callback:
            try:
                self.callback(error_stage, self.current_progress, f"Erro: {error}")
            except Exception as cb_error:
                logger.error(f"Erro no callback: {cb_error}")
    
    def cancel(self):
        """Cancela a operação."""
        self.is_cancelled = True
        logger.info("Operação cancelada pelo usuário")
    
    def is_complete(self) -> bool:
        """Verifica se o progresso está completo."""
        return self.stages_completed >= self.total_stages
    
    def get_elapsed_time(self) -> float:
        """Retorna o tempo decorrido em segundos."""
        if not self.start_time:
            return 0.0
        return (datetime.now() - self.start_time).total_seconds()
    
    def get_estimated_remaining_time(self) -> float:
        """Estima o tempo restante."""
        if not self.start_time or self.stages_completed == 0:
            return 0.0
        
        elapsed = self.get_elapsed_time()
        rate = elapsed / self.stages_completed
        remaining_stages = self.total_stages - self.stages_completed
        
        return rate * remaining_stages
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna o status atual do progresso."""
        overall_progress = self.stages_completed / self.total_stages if self.total_stages > 0 else 0
        
        return {
            'current_stage': self.current_stage,
            'stage_progress': self.current_progress,
            'overall_progress': overall_progress,
            'stages_completed': self.stages_completed,
            'total_stages': self.total_stages,
            'elapsed_time': self.get_elapsed_time(),
            'estimated_remaining': self.get_estimated_remaining_time(),
            'is_cancelled': self.is_cancelled,
            'is_complete': self.is_complete()
        }
