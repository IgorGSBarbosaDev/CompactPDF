#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher para CompactPDF GUI
============================

Script de inicialização que configura o ambiente e inicia a interface gráfica.
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
    """Verifica se a estrutura do projeto está correta."""
    arquivos_necessarios = [
        'src/__init__.py',
        'src/pdf_compressor_facade.py',
        'src/config/compression_config.py',
        'src/models/compression_result.py'
    ]
    
    arquivos_faltando = []
    
    for arquivo in arquivos_necessarios:
        if not (project_root / arquivo).exists():
            arquivos_faltando.append(arquivo)
    
    if arquivos_faltando:
        print("❌ Arquivos do projeto faltando:")
        for arquivo in arquivos_faltando:
            print(f"  - {arquivo}")
        print("\nCertifique-se de que o projeto está completo.")
        return False
    
    return True

def iniciar_gui():
    """Inicia a interface gráfica."""
    try:
        # Importar GUI
        from gui import CompactPDFGUI
        import tkinter as tk
        
        print("🚀 Iniciando CompactPDF GUI...")
        
        # Criar janela principal
        root = tk.Tk()
        
        # Criar aplicação
        app = CompactPDFGUI(root)
        
        print("✅ Interface gráfica iniciada com sucesso!")
        
        # Executar loop principal
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Certifique-se de que todos os módulos estão disponíveis.")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
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
