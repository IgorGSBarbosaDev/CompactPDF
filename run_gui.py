#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher Principal - CompactPDF
===============================

Script principal para executar a interface gráfica modular do CompactPDF.
"""

import sys
import os
from pathlib import Path

def main():
    """Função principal para iniciar a aplicação."""
    print("🚀 Iniciando CompactPDF")
    print("="*50)
    
    # Configurar paths
    project_root = Path(__file__).parent
    src_dir = project_root / "src"
    gui_dir = src_dir / "gui"
    
    print(f"📁 Projeto: {project_root}")
    print(f"📁 Código-fonte: {src_dir}")
    print(f"📁 Interface: {gui_dir}")
    
    # Adicionar paths ao sys.path
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    if str(gui_dir) not in sys.path:
        sys.path.insert(0, str(gui_dir))
    
    # Tentar importar e executar
    try:
        print("\n🎨 Iniciando interface gráfica...")
        
        # Importar módulo launcher
        from gui.launcher import main as gui_main
        
        # Executar interface
        gui_main()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("\n💡 Verifique se todas as dependências estão instaladas:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
