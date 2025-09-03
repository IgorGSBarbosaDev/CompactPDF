#!/usr/bin/env python3
"""
CompactPDF - Lançador da Interface Gráfica
==========================================

Executar com: python launch_gui.py
"""

import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from compactpdf.gui import main as gui_main
except ImportError as e:
    print(f"Erro ao importar GUI: {e}")
    print("Verifique se o pacote compactpdf está configurado corretamente")
    sys.exit(1)


if __name__ == "__main__":
    gui_main()

