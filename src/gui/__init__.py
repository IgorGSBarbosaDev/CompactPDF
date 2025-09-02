#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo GUI do CompactPDF
========================

Sistema modular de interface gráfica dividido em componentes especializados.
"""

from .main_window import CompactPDFGUI
from .file_manager import FileManager
from .config_panel import ConfigurationPanel
from .processing_panel import ProcessingPanel
from .results_panel import ResultsPanel
from .styles import StyleManager

__all__ = [
    'CompactPDFGUI',
    'FileManager', 
    'ConfigurationPanel',
    'ProcessingPanel',
    'ResultsPanel',
    'StyleManager'
]
