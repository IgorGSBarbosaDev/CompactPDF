#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Janela Principal - CompactPDF GUI
================================

Janela principal que integra todos os componentes da interface.
Segue o princípio de Inversão de Dependência (DIP) e atua como Facade.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from typing import List, Optional

# Importar componentes da GUI
try:
    from .styles import StyleManager
    from .file_manager import FileManager
    from .config_panel import ConfigurationPanel
    from .processing_panel import ProcessingPanel
    from .results_panel import ResultsPanel
except ImportError:
    # Imports absolutos se relativos falharem
    from styles import StyleManager
    from file_manager import FileManager
    from config_panel import ConfigurationPanel
    from processing_panel import ProcessingPanel
    from results_panel import ResultsPanel

# Importar modelos
import sys
from pathlib import Path

current_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(current_dir))

try:
    from models.compression_result import CompressionResult
except ImportError:
    from src.models.compression_result import CompressionResult


class CompactPDFGUI:
    """
    Janela principal da aplicação CompactPDF.
    
    Esta classe atua como um Facade que coordena todos os componentes
    da interface gráfica, seguindo os princípios SOLID.
    """
    
    def __init__(self, root: tk.Tk):
        """Inicializa a interface gráfica principal."""
        self.root = root
        
        # Configurar janela principal
        self._setup_window()
        
        # Inicializar gerenciador de estilos
        self.style_manager = StyleManager(root)
        
        # Criar interface principal
        self._create_main_interface()
        
        # Inicializar componentes
        self._initialize_components()
        
        # Configurar callbacks
        self._setup_callbacks()
        
        print("🚀 Iniciando CompactPDF GUI...")
        print("✅ Interface gráfica iniciada com sucesso!")
    
    def _setup_window(self):
        """Configura a janela principal."""
        self.root.title("CompactPDF - Compressor de PDFs")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Ícone da janela (se disponível)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Centralizar janela
        self._center_window()
    
    def _center_window(self):
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_main_interface(self):
        """Cria a estrutura principal da interface."""
        # Canvas e scrollbar para scroll vertical
        self.canvas = tk.Canvas(self.root, bg="#f8f9fa")
        self.scrollbar = ttk.Scrollbar(
            self.root, 
            orient="vertical", 
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame principal dentro do canvas
        self.main_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window(
            (0, 0), 
            window=self.main_frame, 
            anchor="nw"
        )
        
        # Configurar grid principal
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Criar cabeçalho
        self._create_header()
        
        # Configurar eventos de scroll
        self._setup_scroll_events()
    
    def _create_header(self):
        """Cria o cabeçalho da aplicação."""
        header_frame = ttk.Frame(self.root)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        
        # Título principal
        title_label = ttk.Label(
            header_frame,
            text="📄 CompactPDF",
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Descrição
        desc_label = ttk.Label(
            header_frame,
            text="Comprima seus arquivos PDF rapidamente e com qualidade",
            style="Subtitle.TLabel"
        )
        desc_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Separador
        separator = ttk.Separator(header_frame, orient="horizontal")
        separator.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        
        header_frame.grid_columnconfigure(0, weight=1)
    
    def _setup_scroll_events(self):
        """Configura eventos de scroll."""
        # Atualizar scroll quando o conteúdo muda
        self.main_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Scroll com mouse wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Bind mouse wheel para toda a janela
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_frame_configure(self, event=None):
        """Callback para redimensionamento do frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Callback para redimensionamento do canvas."""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def _on_mousewheel(self, event):
        """Callback para scroll com mouse wheel."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _initialize_components(self):
        """Inicializa todos os componentes da interface."""
        # Container para componentes
        components_container = ttk.Frame(self.main_frame)
        components_container.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        components_container.grid_columnconfigure(0, weight=1)
        
        # Inicializar componentes em ordem
        self.file_manager = FileManager(components_container, self.style_manager)
        self.file_manager.main_frame.grid(row=0, column=0, sticky="ew")
        
        self.config_panel = ConfigurationPanel(components_container, self.style_manager)
        self.config_panel.main_frame.grid(row=1, column=0, sticky="ew")
        
        self.processing_panel = ProcessingPanel(components_container, self.style_manager)
        self.processing_panel.main_frame.grid(row=2, column=0, sticky="ew")
        
        self.results_panel = ResultsPanel(components_container, self.style_manager)
        self.results_panel.frame.grid(row=3, column=0, sticky="ew")
        
        # Criar rodapé
        self._create_footer(components_container)
        
        # Configurar expansão
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def _create_footer(self, parent):
        """Cria o rodapé da aplicação."""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=20)
        
        # Separador
        separator = ttk.Separator(footer_frame, orient="horizontal")
        separator.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Informações
        info_label = ttk.Label(
            footer_frame,
            text="CompactPDF v2.0 - Sistema Modular com Arquitetura SOLID",
            foreground=self.style_manager.get_color('muted'),
            font=self.style_manager.get_font('small')
        )
        info_label.grid(row=1, column=0)
        
        footer_frame.grid_columnconfigure(0, weight=1)
    
    def _setup_callbacks(self):
        """Configura os callbacks entre componentes."""
        # File Manager -> Processing Panel
        self.file_manager.on_files_changed = self._on_files_changed
        
        # Processing Panel callbacks
        self.processing_panel.on_processing_started = self._on_processing_started  # type: ignore
        self.processing_panel.on_processing_finished = self._on_processing_finished  # type: ignore
        self.processing_panel.on_file_processed = self._on_file_processed  # type: ignore
        self.processing_panel.on_progress_updated = self._on_progress_updated  # type: ignore
        
        # Configuration Panel callback
        self.config_panel.on_config_changed = self._on_config_changed
    
    def _on_files_changed(self, files: List[str]):
        """Callback para mudanças na lista de arquivos."""
        # Atualizar estado dos botões de processamento baseado na lista de arquivos
        has_files = len(files) > 0
        
        if hasattr(self.processing_panel, 'btn_comprimir'):
            if has_files and self.processing_panel.is_ready_to_process():
                self.processing_panel.btn_comprimir.config(state="normal")
            else:
                self.processing_panel.btn_comprimir.config(state="disabled")
    
    def _on_processing_started(self):
        """Callback para início do processamento."""
        # Validar configuração
        is_valid, message = self.config_panel.validate_configuration()
        if not is_valid:
            messagebox.showerror("Configuração Inválida", message)
            return
        
        # Obter arquivos e configurações
        files = self.file_manager.get_selected_files()
        if not files:
            messagebox.showwarning(
                "Nenhum Arquivo",
                "Selecione pelo menos um arquivo PDF para comprimir."
            )
            return
        
        # Obter configurações
        config = self.config_panel.create_compression_config()
        destination = self.config_panel.get_destination_folder()
        
        # Verificar pasta de destino
        try:
            os.makedirs(destination, exist_ok=True)
        except Exception as e:
            messagebox.showerror(
                "Erro na Pasta",
                f"Erro ao criar pasta de destino: {e}"
            )
            return
        
        # Iniciar processamento
        self.processing_panel.start_processing(files, destination, config)
    
    def _on_processing_finished(self, results: List[CompressionResult]):
        """Callback para término do processamento."""
        if results:
            # Mostrar resumo
            total_files = len(results)
            total_saved = sum(r.space_saved for r in results)
            avg_compression = sum(r.compression_ratio for r in results) / total_files
            
            message = f"""Processamento concluído com sucesso! 🎉

📊 Resumo:
• Arquivos processados: {total_files}
• Espaço economizado: {self._format_file_size(total_saved)}
• Compressão média: {avg_compression:.1f}%

Os arquivos comprimidos foram salvos em:
{self.config_panel.get_destination_folder()}"""
            
            messagebox.showinfo("Processamento Concluído", message)
    
    def _on_file_processed(self, file_path: str, result: Optional[CompressionResult], status: str):
        """Callback para arquivo processado."""
        # Atualizar status do arquivo no gerenciador
        self.file_manager.set_file_status(file_path, status)
        
        # Adicionar resultado ao painel de resultados
        if result and result.success:
            self.results_panel.update_result(result)  # type: ignore
    
    def _on_progress_updated(self, percentage: int, status_text: str):
        """Callback para atualização de progresso."""
        # Atualizar título da janela com progresso
        if percentage > 0 and percentage < 100:
            self.root.title(f"CompactPDF - Processando ({percentage}%)")
        else:
            self.root.title("CompactPDF - Compressor de PDFs")
    
    def _on_config_changed(self):
        """Callback para mudanças na configuração."""
        # Revalidar configuração se necessário
        pass
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Formata tamanho em bytes para formato legível."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def show_about(self):
        """Mostra diálogo sobre a aplicação."""
        about_text = """CompactPDF v2.0

Sistema modular de compressão de PDFs desenvolvido
seguindo os princípios SOLID:

• Single Responsibility Principle (SRP)
• Open/Closed Principle (OCP)  
• Liskov Substitution Principle (LSP)
• Interface Segregation Principle (ISP)
• Dependency Inversion Principle (DIP)

Componentes modulares:
- FileManager: Gerenciamento de arquivos
- ConfigurationPanel: Configurações de compressão
- ProcessingPanel: Controle de processamento
- ResultsPanel: Exibição de resultados
- StyleManager: Gerenciamento de estilos

Desenvolvido com Python e Tkinter."""
        
        messagebox.showinfo("Sobre o CompactPDF", about_text)
    
    def run(self):
        """Executa o loop principal da aplicação."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n🛑 Aplicação interrompida pelo usuário")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            messagebox.showerror("Erro Fatal", f"Erro inesperado na aplicação:\n{e}")


def main():
    """Função principal para executar a GUI."""
    try:
        # Criar janela principal
        root = tk.Tk()
        
        # Criar e executar aplicação
        app = CompactPDFGUI(root)
        app.run()
        
    except Exception as e:
        print(f"❌ Erro ao inicializar aplicação: {e}")
        messagebox.showerror("Erro de Inicialização", f"Erro ao inicializar a aplicação:\n{e}")


if __name__ == "__main__":
    main()
