#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher para Interface Modular - CompactPDF
============================================

Launcher específico para a nova interface modular que configura
corretamente os paths e imports.
"""

import sys
import os
from pathlib import Path

def configurar_paths():
    """Configura os paths necessários para os imports."""
    # Diretório do projeto
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    gui_dir = src_dir / "gui"
    
    # Adicionar paths
    paths_to_add = [
        str(project_root),
        str(src_dir),
        str(gui_dir)
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"📁 Projeto: {project_root}")
    print(f"📁 Src: {src_dir}")
    print(f"📁 GUI: {gui_dir}")

def main():
    """Função principal."""
    print("🚀 Iniciando CompactPDF - Interface Modular")
    print("=" * 50)
    
    # Configurar paths
    configurar_paths()
    
    try:
        # Importar e executar GUI modular
        import tkinter as tk
        from main_window import CompactPDFGUI
        
        print("✅ Módulos importados com sucesso!")
        print("🎨 Iniciando interface gráfica...")
        
        # Criar aplicação
        root = tk.Tk()
        app = CompactPDFGUI(root)
        
        print("✅ Interface iniciada!")
        
        # Executar
        app.run()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("\n🔧 Verifique se todos os módulos estão corretos:")
        print("  - main_window.py")
        print("  - styles.py")
        print("  - file_manager.py")
        print("  - config_panel.py")
        print("  - processing_panel.py")
        print("  - results_panel.py")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
