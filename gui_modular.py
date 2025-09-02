#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica para CompactPDF - REFATORADA
==============================================

Interface gráfica moderna e modular para compressão de PDFs.
Agora seguindo os princípios SOLID com arquitetura modular.

NOVA ARQUITETURA:
================

A interface foi completamente refatorada e dividida em componentes especializados:

🏗️ COMPONENTES PRINCIPAIS:
- StyleManager: Gerenciamento de estilos e temas
- FileManager: Seleção e gerenciamento de arquivos
- ConfigurationPanel: Configurações de compressão
- ProcessingPanel: Controle e monitoramento do processamento
- ResultsPanel: Exibição e export de resultados
- CompactPDFGUI: Facade que coordena todos os componentes

📐 PRINCÍPIOS SOLID APLICADOS:
- SRP: Cada classe tem uma única responsabilidade
- OCP: Aberto para extensão, fechado para modificação
- LSP: Componentes são substituíveis
- ISP: Interfaces específicas para cada necessidade
- DIP: Dependências invertidas via callbacks

🎯 BENEFÍCIOS DA REFATORAÇÃO:
- Código mais limpo e organizado
- Fácil manutenção e extensão
- Melhor testabilidade
- Reutilização de componentes
- Separação clara de responsabilidades

Para usar a nova interface modular, importe:
from src.gui import CompactPDFGUI
"""

import sys
from pathlib import Path

# Configurar paths
current_dir = Path(__file__).parent
src_dir = current_dir / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Importar nova interface modular
try:
    from gui.main_window import CompactPDFGUI, main
    
    # Manter compatibilidade com código existente
    def create_gui():
        """Cria e retorna a nova GUI modular."""
        import tkinter as tk
        root = tk.Tk()
        return CompactPDFGUI(root)
    
    # Executar se chamado diretamente
    if __name__ == "__main__":
        print("🔄 Carregando nova interface modular...")
        print("✨ Sistema refatorado seguindo princípios SOLID")
        main()
        
except ImportError as e:
    print(f"❌ Erro ao importar nova interface modular: {e}")
    print("📦 Verifique se todos os módulos estão no local correto")
    print("📁 Estrutura esperada:")
    print("   src/gui/")
    print("   ├── __init__.py")
    print("   ├── main_window.py")
    print("   ├── file_manager.py") 
    print("   ├── config_panel.py")
    print("   ├── processing_panel.py")
    print("   ├── results_panel.py")
    print("   └── styles.py")
    
    # Fallback para versão antiga se necessário
    print("\n⚠️  Usando versão de compatibilidade...")
    
    import tkinter as tk
    from tkinter import messagebox
    
    class LegacyGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("CompactPDF - Modo de Compatibilidade")
            self.root.geometry("600x400")
            
            frame = tk.Frame(root, padx=50, pady=50)
            frame.pack(expand=True, fill="both")
            
            title = tk.Label(
                frame, 
                text="🔧 Interface em Modo de Compatibilidade",
                font=("Arial", 16, "bold")
            )
            title.pack(pady=20)
            
            message = tk.Label(
                frame,
                text="A nova interface modular não pode ser carregada.\n\n"
                     "Para usar a versão completa, execute:\n"
                     "python launch_gui.py\n\n"
                     "Ou verifique se todos os módulos estão instalados corretamente.",
                justify="center",
                wraplength=400
            )
            message.pack(pady=20)
            
            btn_close = tk.Button(
                frame,
                text="Fechar",
                command=root.quit,
                font=("Arial", 12)
            )
            btn_close.pack(pady=20)
    
    def main():
        root = tk.Tk()
        app = LegacyGUI(root)
        root.mainloop()
    
    if __name__ == "__main__":
        main()
