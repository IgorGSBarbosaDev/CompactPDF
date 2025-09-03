"""
CompactPDF - Interface Gráfica Simplificada
===========================================

Interface moderna focada apenas em PyMuPDF e Spire.PDF.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
from typing import Optional

from ..core.facade import PDFCompressor
from ..core.models import CompressionConfig, CompressionLevel


class CompactPDFGUI:
    """Interface gráfica simplificada para CompactPDF."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.compressor = PDFCompressor()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface."""
        self.root.title("CompactPDF - Compressor Simplificado")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="ew")
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="🗜️ CompactPDF", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status das bibliotecas
        self.create_status_section(main_frame)
        
        # Seleção de arquivo
        self.create_file_section(main_frame)
        
        # Configurações
        self.create_config_section(main_frame)
        
        # Botões de ação
        self.create_action_section(main_frame)
        
        # Progresso
        self.create_progress_section(main_frame)
        
        # Configurar expansão
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
    def create_status_section(self, parent):
        """Cria seção de status das bibliotecas."""
        status_frame = ttk.LabelFrame(parent, text="📦 Status das Bibliotecas", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        methods = self.compressor.get_available_methods()
        
        if "pymupdf" in methods:
            ttk.Label(status_frame, text="✅ PyMuPDF disponível", foreground="green").pack(anchor="w")
        else:
            ttk.Label(status_frame, text="❌ PyMuPDF não encontrado", foreground="red").pack(anchor="w")
            
        if "spire" in methods:
            ttk.Label(status_frame, text="✅ Spire.PDF disponível", foreground="green").pack(anchor="w")
        else:
            ttk.Label(status_frame, text="❌ Spire.PDF não encontrado", foreground="red").pack(anchor="w")
            
        if not methods:
            ttk.Label(
                status_frame, 
                text="⚠️ Instale PyMuPDF ou Spire.PDF para usar o sistema", 
                foreground="orange"
            ).pack(anchor="w")
    
    def create_file_section(self, parent):
        """Cria seção de seleção de arquivo."""
        file_frame = ttk.LabelFrame(parent, text="📁 Arquivo PDF", padding="10")
        file_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Entrada de arquivo
        self.file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_var, width=50)
        file_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Botão procurar
        browse_btn = ttk.Button(
            file_frame, 
            text="📂 Procurar", 
            command=self.browse_file
        )
        browse_btn.grid(row=0, column=1)
        
        file_frame.grid_columnconfigure(0, weight=1)
    
    def create_config_section(self, parent):
        """Cria seção de configurações."""
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configurações", padding="10")
        config_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Método
        ttk.Label(config_frame, text="Método:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.method_var = tk.StringVar(value="auto")
        method_combo = ttk.Combobox(
            config_frame,
            textvariable=self.method_var,
            values=["auto", "pymupdf", "spire"],
            state="readonly",
            width=15
        )
        method_combo.grid(row=0, column=1, sticky="w")
        
        # Nível de compressão
        ttk.Label(config_frame, text="Nível:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.level_var = tk.StringVar(value="medium")
        level_combo = ttk.Combobox(
            config_frame,
            textvariable=self.level_var,
            values=["light", "medium", "aggressive"],
            state="readonly",
            width=15
        )
        level_combo.grid(row=1, column=1, sticky="w", pady=(10, 0))
        
        # Descrições
        desc_frame = ttk.Frame(config_frame)
        desc_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        ttk.Label(desc_frame, text="• Light: Preserva qualidade visual").pack(anchor="w")
        ttk.Label(desc_frame, text="• Medium: Balanceado (recomendado)").pack(anchor="w")
        ttk.Label(desc_frame, text="• Aggressive: Máxima compressão").pack(anchor="w")
    
    def create_action_section(self, parent):
        """Cria seção de botões de ação."""
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=4, column=0, columnspan=2, pady=(0, 15))
        
        # Botão comprimir
        self.compress_btn = ttk.Button(
            action_frame,
            text="🗜️ Comprimir PDF",
            command=self.compress_file,
            style="Accent.TButton"
        )
        self.compress_btn.pack(side="left", padx=(0, 10))
        
        # Botão limpar
        clear_btn = ttk.Button(
            action_frame,
            text="🗑️ Limpar",
            command=self.clear_fields
        )
        clear_btn.pack(side="left")
    
    def create_progress_section(self, parent):
        """Cria seção de progresso."""
        progress_frame = ttk.LabelFrame(parent, text="📊 Progresso", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=2, sticky="ew")
        
        # Barra de progresso
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para comprimir")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.grid(row=1, column=0, sticky="w")
        
        progress_frame.grid_columnconfigure(0, weight=1)
    
    def browse_file(self):
        """Abre diálogo para selecionar arquivo."""
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        if filename:
            self.file_var.set(filename)
    
    def clear_fields(self):
        """Limpa os campos."""
        self.file_var.set("")
        self.method_var.set("auto")
        self.level_var.set("medium")
        self.status_var.set("Pronto para comprimir")
    
    def compress_file(self):
        """Comprime o arquivo selecionado."""
        if not self.file_var.get():
            messagebox.showerror("Erro", "Selecione um arquivo PDF primeiro!")
            return
        
        if not self.compressor.is_ready():
            messagebox.showerror(
                "Erro", 
                "Nenhum método de compressão disponível.\\n"
                "Instale PyMuPDF ou Spire.PDF."
            )
            return
        
        # Executar compressão em thread separada
        thread = threading.Thread(target=self._compress_thread)
        thread.daemon = True
        thread.start()
    
    def _compress_thread(self):
        """Thread de compressão."""
        input_path = self.file_var.get()
        
        # Configurar saída
        input_file = Path(input_path)
        output_path = input_file.parent / f"{input_file.stem}_compressed.pdf"
        
        # Configurar compressão
        config = CompressionConfig()
        config.level = CompressionLevel(self.level_var.get())
        config.method = self.method_var.get() if self.method_var.get() != "auto" else None
        
        # Atualizar UI
        self.root.after(0, self._start_progress)
        
        try:
            # Comprimir
            result = self.compressor.compress(input_path, output_path, config)
            
            # Atualizar UI com resultado
            self.root.after(0, lambda: self._show_result(result))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_error(str(e)))
        
        finally:
            self.root.after(0, self._stop_progress)
    
    def _start_progress(self):
        """Inicia indicador de progresso."""
        self.progress.start()
        self.compress_btn.config(state="disabled")
        self.status_var.set("Comprimindo PDF...")
    
    def _stop_progress(self):
        """Para indicador de progresso."""
        self.progress.stop()
        self.compress_btn.config(state="normal")
    
    def _show_result(self, result):
        """Mostra resultado da compressão."""
        if result.success:
            reduction = result.reduction_percentage
            size_saved = result.size_saved / (1024 * 1024)  # MB
            
            message = (
                f"Compressão bem-sucedida!\\n\\n"
                f"Método: {result.method_used}\\n"
                f"Redução: {reduction:.1f}%\\n"
                f"Espaço economizado: {size_saved:.2f} MB\\n"
                f"Tempo: {result.processing_time:.2f}s\\n\\n"
                f"Arquivo salvo em:\\n{result.output_path}"
            )
            
            messagebox.showinfo("Sucesso", message)
            self.status_var.set(f"Concluído - {reduction:.1f}% de redução")
        else:
            self._show_error(result.error_message or "Erro desconhecido")
    
    def _show_error(self, error_message):
        """Mostra erro."""
        messagebox.showerror("Erro na Compressão", error_message)
        self.status_var.set("Erro na compressão")
    
    def run(self):
        """Executa a interface."""
        self.root.mainloop()


def main():
    """Função principal da GUI."""
    app = CompactPDFGUI()
    app.run()


if __name__ == "__main__":
    main()
