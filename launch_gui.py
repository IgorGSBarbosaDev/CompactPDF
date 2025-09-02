#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher para CompactPDF GUI - REFATORADO
=========================================

Script de inicialização que configura o ambiente e inicia a nova interface 
gráfica modular seguindo os princípios SOLID.

NOVA INTERFACE MODULAR:
======================

A interface foi completamente refatorada em componentes especializados:

🏗️ ARQUITETURA:
- StyleManager: Gerenciamento de estilos
- FileManager: Gerenciamento de arquivos
- ConfigurationPanel: Painel de configurações
- ProcessingPanel: Controle de processamento
- ResultsPanel: Exibição de resultados
- CompactPDFGUI: Facade principal

📐 PRINCÍPIOS SOLID:
- SRP: Uma responsabilidade por classe
- OCP: Aberto para extensão
- LSP: Substituição de componentes
- ISP: Interfaces específicas
- DIP: Inversão de dependências
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas."""
    dependencias_necessarias = [
        'tkinter',
        'threading', 
        'json',
        'datetime',
        'pathlib'
    ]
    
    dependencias_faltando = []
    
    for dep in dependencias_necessarias:
        try:
            __import__(dep)
        except ImportError:
            dependencias_faltando.append(dep)
    
    if dependencias_faltando:
        print("❌ Dependências faltando:")
        for dep in dependencias_faltando:
            print(f"  - {dep}")
        print("\nInstale as dependências com:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def verificar_estrutura_projeto():
    """Verifica se a estrutura do projeto e os novos módulos estão corretos."""
    # Arquivos principais do projeto
    arquivos_necessarios = [
        'src/__init__.py',
        'src/pdf_compressor_facade.py',
        'src/config/compression_config.py',
        'src/models/compression_result.py',
    ]
    
    # Novos módulos da interface modular
    modulos_gui = [
        'src/gui/__init__.py',
        'src/gui/main_window.py',
        'src/gui/styles.py',
        'src/gui/file_manager.py',
        'src/gui/config_panel.py',
        'src/gui/processing_panel.py',
        'src/gui/results_panel.py'
    ]
    
    # Combinar listas
    todos_arquivos = arquivos_necessarios + modulos_gui
    
    arquivos_faltando = []
    
    for arquivo in todos_arquivos:
        if not (project_root / arquivo).exists():
            arquivos_faltando.append(arquivo)
    
    if arquivos_faltando:
        print("❌ Arquivos do projeto faltando:")
        for arquivo in arquivos_faltando:
            if 'gui/' in arquivo:
                print(f"  - {arquivo} (novo módulo da interface modular)")
            else:
                print(f"  - {arquivo}")
        
        print("\n📋 Status da refatoração:")
        print("  ✅ Interface antiga (gui.py) ainda disponível")
        print("  🔄 Interface modular em desenvolvimento")
        print("  📦 Execute 'python gui.py' para versão atual")
        return False
    
    return True

def iniciar_gui_modular():
    """Inicia a nova interface gráfica modular."""
    try:
        # Tentar importar nova GUI modular
        sys.path.insert(0, str(project_root / "src"))
        from gui.main_window import CompactPDFGUI
        import tkinter as tk
        
        print("🚀 Iniciando CompactPDF GUI Modular...")
        print("✨ Sistema refatorado seguindo princípios SOLID")
        
        # Criar janela principal
        root = tk.Tk()
        
        # Criar aplicação
        app = CompactPDFGUI(root)
        
        print("✅ Interface gráfica modular iniciada com sucesso!")
        
        # Executar loop principal
        app.run()
        
    except ImportError as e:
        print(f"❌ Erro ao carregar interface modular: {e}")
        print("\n🔄 Tentando carregar interface de compatibilidade...")
        iniciar_gui_compatibilidade()
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import tkinter.messagebox as msgbox
        msgbox.showerror("Erro Fatal", f"Erro inesperado na aplicação:\n{e}")

def iniciar_gui_compatibilidade():
    """Inicia a GUI usando a versão de compatibilidade."""
    try:
        # Importar GUI original
        from gui import main as gui_main
        
        print("🔧 Carregando interface de compatibilidade...")
        gui_main()
        
    except Exception as e:
        print(f"❌ Erro ao carregar interface de compatibilidade: {e}")
        print("\n💡 Execute diretamente: python gui.py")

def iniciar_gui():
    """Inicia a interface gráfica (método de compatibilidade)."""
    try:
        # Tentar nova interface modular primeiro
        if verificar_estrutura_projeto():
            iniciar_gui_modular()
        else:
            iniciar_gui_compatibilidade()
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        print("🔄 Tentando interface de compatibilidade...")
        iniciar_gui_compatibilidade()
    
    return True

def main():
    """Função principal do launcher."""
    print("🗜️ CompactPDF - Launcher da Interface Gráfica")
    print("=" * 50)
    
    # Verificar dependências
    print("🔍 Verificando dependências...")
    if not verificar_dependencias():
        sys.exit(1)
    
    # Verificar estrutura do projeto
    print("📁 Verificando estrutura do projeto...")
    if not verificar_estrutura_projeto():
        sys.exit(1)
    
    print("✅ Todas as verificações passaram!")
    print()
    
    # Iniciar GUI
    if not iniciar_gui():
        sys.exit(1)

if __name__ == "__main__":
    main()
