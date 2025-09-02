#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Arquivos - CompactPDF GUI
========================================

Responsável pela seleção, validação e gerenciamento de arquivos PDF.
Segue o princípio SRP (Single Responsibility Principle).
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Callable, Optional


class FileManager:
    """Gerenciador de arquivos PDF para a interface."""
    
    def __init__(self, parent_frame: ttk.Frame, style_manager):
        """Inicializa o gerenciador de arquivos."""
        self.parent_frame = parent_frame
        self.style_manager = style_manager
        self.arquivos_selecionados: List[str] = []
        
        # Callbacks para notificar mudanças
        self.on_files_changed: Optional[Callable[[List[str]], None]] = None
        
        # Criar interface
        self._create_interface()
    
    def _create_interface(self):
        """Cria a interface de gerenciamento de arquivos."""
        # Frame principal da seção
        self.main_frame = ttk.LabelFrame(
            self.parent_frame,
            text=" 📁 Arquivos ",
            padding=15
        )
        self.main_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        # Criar controles
        self._create_file_controls()
        self._create_file_list()
        self._create_info_label()
        
        # Configurar expansão
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_columnconfigure(0, weight=1)
    
    def _create_file_controls(self):
        """Cria os controles de seleção de arquivos."""
        botoes_frame = ttk.Frame(self.main_frame)
        botoes_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Botão para selecionar arquivos individuais
        self.btn_selecionar = ttk.Button(
            botoes_frame,
            text="📄 Selecionar PDFs",
            command=self.selecionar_arquivos,
            style="Action.TButton"
        )
        self.btn_selecionar.grid(row=0, column=0, padx=(0, 10))
        
        # Botão para selecionar pasta
        self.btn_selecionar_pasta = ttk.Button(
            botoes_frame,
            text="📂 Selecionar Pasta",
            command=self.selecionar_pasta,
            style="Action.TButton"
        )
        self.btn_selecionar_pasta.grid(row=0, column=1, padx=(0, 10))
        
        # Botão para limpar seleção
        self.btn_limpar = ttk.Button(
            botoes_frame,
            text="🗑️ Limpar",
            command=self.limpar_arquivos,
            style="Action.TButton"
        )
        self.btn_limpar.grid(row=0, column=2)
        
        # Botão para remover selecionado
        self.btn_remover = ttk.Button(
            botoes_frame,
            text="➖ Remover",
            command=self.remover_selecionado,
            style="Action.TButton",
            state="disabled"
        )
        self.btn_remover.grid(row=0, column=3, padx=(10, 0))
    
    def _create_file_list(self):
        """Cria a lista de arquivos selecionados."""
        lista_frame = ttk.Frame(self.main_frame)
        lista_frame.grid(row=1, column=0, sticky="ew", pady=10)
        
        # Treeview para mostrar arquivos
        colunas = ("Nome", "Tamanho", "Status")
        self.tree_arquivos = ttk.Treeview(
            lista_frame,
            columns=colunas,
            show="tree headings",
            height=6
        )
        
        # Configurar colunas
        self.tree_arquivos.heading("#0", text="")
        self.tree_arquivos.column("#0", width=30, minwidth=30)
        
        for col in colunas:
            self.tree_arquivos.heading(col, text=col)
            if col == "Nome":
                self.tree_arquivos.column(col, width=400, minwidth=200)
            elif col == "Tamanho":
                self.tree_arquivos.column(col, width=100, minwidth=80)
            else:
                self.tree_arquivos.column(col, width=120, minwidth=100)
        
        # Event binding para seleção
        self.tree_arquivos.bind('<<TreeviewSelect>>', self._on_tree_select)
        
        # Scrollbar para a lista
        scrollbar_arquivos = ttk.Scrollbar(
            lista_frame,
            orient="vertical",
            command=self.tree_arquivos.yview
        )
        self.tree_arquivos.configure(yscrollcommand=scrollbar_arquivos.set)
        
        # Grid da lista
        self.tree_arquivos.grid(row=0, column=0, sticky="ew")
        scrollbar_arquivos.grid(row=0, column=1, sticky="ns")
        
        lista_frame.grid_columnconfigure(0, weight=1)
    
    def _create_info_label(self):
        """Cria o label de informações."""
        self.lbl_info_arquivos = ttk.Label(
            self.main_frame,
            text="Nenhum arquivo selecionado",
            foreground=self.style_manager.get_color('muted')
        )
        self.lbl_info_arquivos.grid(row=2, column=0, sticky="w", pady=(10, 0))
    
    def _on_tree_select(self, event):
        """Callback para seleção na árvore."""
        selection = self.tree_arquivos.selection()
        self.btn_remover.config(state="normal" if selection else "disabled")
    
    def selecionar_arquivos(self):
        """Permite selecionar arquivos PDF individuais."""
        arquivos = filedialog.askopenfilenames(
            title="Selecionar Arquivos PDF",
            filetypes=[
                ("Arquivos PDF", "*.pdf"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if arquivos:
            self.adicionar_arquivos(list(arquivos))
    
    def selecionar_pasta(self):
        """Permite selecionar uma pasta para processar todos os PDFs."""
        pasta = filedialog.askdirectory(title="Selecionar Pasta com PDFs")
        
        if pasta:
            # Encontrar todos os PDFs na pasta
            pdfs = self._find_pdfs_in_directory(pasta)
            
            if pdfs:
                self.adicionar_arquivos(pdfs)
                messagebox.showinfo(
                    "Pasta Selecionada",
                    f"Encontrados {len(pdfs)} arquivos PDF na pasta selecionada."
                )
            else:
                messagebox.showwarning(
                    "Nenhum PDF Encontrado",
                    "Não foram encontrados arquivos PDF na pasta selecionada."
                )
    
    def _find_pdfs_in_directory(self, directory: str) -> List[str]:
        """Encontra todos os arquivos PDF em um diretório."""
        pdfs = []
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdfs.append(os.path.join(root, file))
        except Exception as e:
            messagebox.showerror(
                "Erro na Busca",
                f"Erro ao buscar PDFs na pasta: {e}"
            )
        return pdfs
    
    def adicionar_arquivos(self, arquivos: List[str]):
        """Adiciona arquivos à lista."""
        arquivos_adicionados = 0
        
        for arquivo in arquivos:
            if arquivo not in self.arquivos_selecionados:
                if self._validate_file(arquivo):
                    self.arquivos_selecionados.append(arquivo)
                    arquivos_adicionados += 1
        
        if arquivos_adicionados > 0:
            self._update_file_list()
            self._update_info()
            self._notify_files_changed()
        
        return arquivos_adicionados
    
    def _validate_file(self, arquivo: str) -> bool:
        """Valida se o arquivo é válido."""
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(arquivo):
                return False
            
            # Verificar se é um arquivo (não diretório)
            if not os.path.isfile(arquivo):
                return False
            
            # Verificar extensão PDF
            if not arquivo.lower().endswith('.pdf'):
                return False
            
            # Verificar se o arquivo não está vazio
            if os.path.getsize(arquivo) == 0:
                return False
            
            return True
            
        except Exception:
            return False
    
    def remover_selecionado(self):
        """Remove o arquivo selecionado da lista."""
        selection = self.tree_arquivos.selection()
        if not selection:
            return
        
        # Obter índice do item selecionado
        item = selection[0]
        index = self.tree_arquivos.index(item)
        
        # Remover da lista
        if 0 <= index < len(self.arquivos_selecionados):
            self.arquivos_selecionados.pop(index)
            self._update_file_list()
            self._update_info()
            self._notify_files_changed()
    
    def limpar_arquivos(self):
        """Limpa a lista de arquivos selecionados."""
        if self.arquivos_selecionados:
            if messagebox.askyesno(
                "Limpar Arquivos",
                f"Deseja remover todos os {len(self.arquivos_selecionados)} arquivos da lista?"
            ):
                self.arquivos_selecionados.clear()
                self._update_file_list()
                self._update_info()
                self._notify_files_changed()
    
    def _update_file_list(self):
        """Atualiza a visualização da lista de arquivos."""
        # Limpar lista atual
        for item in self.tree_arquivos.get_children():
            self.tree_arquivos.delete(item)
        
        # Adicionar arquivos
        for arquivo in self.arquivos_selecionados:
            nome = os.path.basename(arquivo)
            
            try:
                tamanho = os.path.getsize(arquivo)
                tamanho_str = self._format_file_size(tamanho)
                status = "✅ Pronto"
            except Exception:
                tamanho_str = "❌ Erro"
                status = "❌ Arquivo não encontrado"
            
            self.tree_arquivos.insert(
                "",
                "end",
                values=(nome, tamanho_str, status)
            )
    
    def _update_info(self):
        """Atualiza as informações sobre os arquivos selecionados."""
        total = len(self.arquivos_selecionados)
        
        if total == 0:
            self.lbl_info_arquivos.config(text="Nenhum arquivo selecionado")
        else:
            # Calcular tamanho total
            tamanho_total = 0
            arquivos_validos = 0
            
            for arquivo in self.arquivos_selecionados:
                try:
                    tamanho_total += os.path.getsize(arquivo)
                    arquivos_validos += 1
                except Exception:
                    pass
            
            tamanho_str = self._format_file_size(tamanho_total)
            
            if arquivos_validos == total:
                self.lbl_info_arquivos.config(
                    text=f"✅ {total} arquivo(s) selecionado(s) • Tamanho total: {tamanho_str}"
                )
            else:
                self.lbl_info_arquivos.config(
                    text=f"⚠️ {arquivos_validos}/{total} arquivos válidos • Tamanho: {tamanho_str}"
                )
    
    def _format_file_size(self, tamanho_bytes: int) -> str:
        """Formata tamanho em bytes para formato legível."""
        if tamanho_bytes < 1024:
            return f"{tamanho_bytes} B"
        elif tamanho_bytes < 1024 * 1024:
            return f"{tamanho_bytes / 1024:.1f} KB"
        elif tamanho_bytes < 1024 * 1024 * 1024:
            return f"{tamanho_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{tamanho_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def _notify_files_changed(self):
        """Notifica sobre mudanças na lista de arquivos."""
        if self.on_files_changed:
            self.on_files_changed(self.arquivos_selecionados.copy())
    
    def get_selected_files(self) -> List[str]:
        """Retorna lista de arquivos selecionados."""
        return self.arquivos_selecionados.copy()
    
    def has_files(self) -> bool:
        """Verifica se há arquivos selecionados."""
        return len(self.arquivos_selecionados) > 0
    
    def set_file_status(self, arquivo: str, status: str):
        """Define o status de um arquivo específico."""
        for item in self.tree_arquivos.get_children():
            values = self.tree_arquivos.item(item)['values']
            if values and os.path.basename(arquivo) == values[0]:
                # Atualizar apenas o status
                self.tree_arquivos.set(item, "Status", status)
                break
