#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serviço de Arquivos PDF
=======================

Gerencia operações de arquivo PDF.
"""

import os
import shutil
from typing import Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PDFFileService:
    """Serviço para operações com arquivos PDF."""
    
    def __init__(self):
        self.temp_dir = None
    
    def validate_pdf_file(self, file_path: str) -> bool:
        """Valida se o arquivo é um PDF válido."""
        try:
            if not os.path.exists(file_path):
                return False
            
            if not file_path.lower().endswith('.pdf'):
                return False
            
            # Verificação básica do cabeçalho PDF
            with open(file_path, 'rb') as f:
                header = f.read(8)
                return header.startswith(b'%PDF-')
                
        except Exception as e:
            logger.error(f"Erro ao validar PDF {file_path}: {e}")
            return False
    
    def get_file_size(self, file_path: str) -> int:
        """Retorna o tamanho do arquivo em bytes."""
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"Erro ao obter tamanho do arquivo {file_path}: {e}")
            return 0
    
    def create_backup(self, file_path: str, backup_suffix: str = ".backup") -> Optional[str]:
        """Cria backup do arquivo."""
        try:
            backup_path = f"{file_path}{backup_suffix}"
            shutil.copy2(file_path, backup_path)
            logger.info(f"Backup criado: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Erro ao criar backup de {file_path}: {e}")
            return None
    
    def ensure_output_directory(self, output_path: str) -> bool:
        """Garante que o diretório de saída existe."""
        try:
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Erro ao criar diretório de saída {output_path}: {e}")
            return False
    
    def cleanup_temp_files(self):
        """Remove arquivos temporários."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info("Arquivos temporários removidos")
            except Exception as e:
                logger.error(f"Erro ao remover arquivos temporários: {e}")
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Retorna informações básicas do arquivo."""
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'created': stat.st_ctime,
                'extension': Path(file_path).suffix.lower(),
                'name': Path(file_path).name
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações do arquivo {file_path}: {e}")
            return {}
