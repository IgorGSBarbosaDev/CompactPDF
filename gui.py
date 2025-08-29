#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica para CompactPDF
=================================

Interface gráfica moderna e intuitiva para compressão de PDFs
usando a API do CompactPDF.

Funcionalidades:
- Seleção de arquivos PDF
- Configuração de presets
- Monitoramento de progresso
- Visualização de resultados
- Processamento em lote
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import time
from datetime import datetime
from pathlib import Path
import json

# Importações do CompactPDF
try:
    from src.pdf_compressor_facade import PDFCompressorFacade
    from src.config.compression_config import CompressionConfig, CompressionLevel
    from src.models.compression_result import CompressionResult
except ImportError as e:
    print(f"Erro ao importar módulos do CompactPDF: {e}")
    print("Certifique-se de que o projeto está configurado corretamente.")
    exit(1)


class CompactPDFGUI:
    """Interface gráfica principal do CompactPDF."""
    
    def __init__(self, root):
        """Inicializa a interface gráfica."""
        self.root = root
        self.compressor = PDFCompressorFacade()
        
        # Configurações da janela
        self.setup_window()
        
        # Variáveis de estado
        self.arquivos_selecionados = []
        self.processamento_ativo = False
        self.resultados_historico = []
        
        # Criar interface
        self.criar_interface()
        
        # Configurar estilos
        self.configurar_estilos()
    
    def setup_window(self):
        """Configura a janela principal."""
        self.root.title("CompactPDF - Compressor de PDFs")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Ícone da janela (se disponível)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Centralizar janela
        self.centralizar_janela()
    
    def centralizar_janela(self):
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def configurar_estilos(self):
        """Configura estilos personalizados."""
        self.style = ttk.Style()
        
        # Configurar tema
        try:
            self.style.theme_use('clam')
        except:
            pass
        
        # Estilos personalizados
        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 16, "bold"),
            foreground="#2c3e50"
        )
        
        self.style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10, "bold"),
            foreground="#34495e"
        )
        
        self.style.configure(
            "Success.TLabel",
            foreground="#27ae60",
            font=("Segoe UI", 9, "bold")
        )
        
        self.style.configure(
            "Error.TLabel",
            foreground="#e74c3c",
            font=("Segoe UI", 9, "bold")
        )
        
        self.style.configure(
            "Compress.TButton",
            font=("Segoe UI", 11, "bold")
        )
    
    def criar_interface(self):
        """Cria todos os elementos da interface."""
        # Frame principal com scroll
        self.criar_frame_principal()
        
        # Cabeçalho
        self.criar_cabecalho()
        
        # Seção de seleção de arquivos
        self.criar_secao_arquivos()
        
        # Seção de configurações
        self.criar_secao_configuracoes()
        
        # Seção de processamento
        self.criar_secao_processamento()
        
        # Seção de resultados
        self.criar_secao_resultados()
        
        # Rodapé com informações
        self.criar_rodape()
    
    def criar_frame_principal(self):
        """Cria o frame principal com scroll."""
        # Canvas e scrollbar para scroll vertical
        self.canvas = tk.Canvas(self.root, bg="#f8f9fa")
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame principal dentro do canvas
        self.main_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configurar grid
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Atualizar scroll quando o conteúdo muda
        self.main_frame.bind("<Configure>", self.atualizar_scroll)
        self.canvas.bind("<Configure>", self.redimensionar_canvas)
        
        # Scroll com mouse wheel
        self.canvas.bind("<MouseWheel>", self.scroll_mouse)
    
    def atualizar_scroll(self, event=None):
        """Atualiza a região de scroll."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def redimensionar_canvas(self, event):
        """Redimensiona o canvas quando a janela muda de tamanho."""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def scroll_mouse(self, event):
        """Permite scroll com mouse wheel."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def criar_cabecalho(self):
        """Cria o cabeçalho da aplicação."""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        # Título principal  
        titulo = ttk.Label(
            header_frame,
            text="� CompactPDF",
            style="Title.TLabel"
        )
        titulo.grid(row=0, column=0, sticky="w")
        
        # Descrição simples
        descricao = ttk.Label(
            header_frame,
            text="Comprima seus arquivos PDF rapidamente",
            style="Subtitle.TLabel"
        )
        descricao.grid(row=1, column=0, sticky="w", pady=(5, 15))
        
        # Separador
        separator = ttk.Separator(header_frame, orient="horizontal")
        separator.grid(row=2, column=0, sticky="ew", pady=10)
        
        header_frame.grid_columnconfigure(0, weight=1)
    
    def criar_secao_arquivos(self):
        """Cria a seção de seleção de arquivos."""
        # Frame da seção
        arquivos_frame = ttk.LabelFrame(
            self.main_frame,
            text=" Arquivos ",
            padding=15
        )
        arquivos_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Botões de seleção
        botoes_frame = ttk.Frame(arquivos_frame)
        botoes_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.btn_selecionar = ttk.Button(
            botoes_frame,
            text="Selecionar PDFs",
            command=self.selecionar_arquivos
        )
        self.btn_selecionar.grid(row=0, column=0, padx=(0, 10))
        
        self.btn_selecionar_pasta = ttk.Button(
            botoes_frame,
            text="Selecionar Pasta",
            command=self.selecionar_pasta
        )
        self.btn_selecionar_pasta.grid(row=0, column=1, padx=(0, 10))
        
        self.btn_limpar = ttk.Button(
            botoes_frame,
            text="Limpar",
            command=self.limpar_arquivos
        )
        self.btn_limpar.grid(row=0, column=2)
        
        # Lista de arquivos selecionados
        lista_frame = ttk.Frame(arquivos_frame)
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
        
        # Label de informações
        self.lbl_info_arquivos = ttk.Label(
            arquivos_frame,
            text="Nenhum arquivo selecionado",
            foreground="#7f8c8d"
        )
        self.lbl_info_arquivos.grid(row=2, column=0, sticky="w", pady=(10, 0))
        
        # Configurar expansão
        arquivos_frame.grid_columnconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def criar_secao_configuracoes(self):
        """Cria a seção de configurações."""
        config_frame = ttk.LabelFrame(
            self.main_frame,
            text=" Configurações ",
            padding=15
        )
        config_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        # Frame para presets
        preset_frame = ttk.Frame(config_frame)
        preset_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        ttk.Label(preset_frame, text="Nível de compressão:").grid(row=0, column=0, sticky="w")
        
        self.preset_var = tk.StringVar(value="balanced")
        preset_combo = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_var,
            values=["minimal", "balanced", "aggressive"],
            state="readonly",
            width=15
        )
        preset_combo.grid(row=0, column=1, padx=(10, 20), sticky="w")
        preset_combo.bind("<<ComboboxSelected>>", self.atualizar_descricao_preset)
        
        # Descrição do preset
        self.lbl_descricao_preset = ttk.Label(
            preset_frame,
            text=self.get_descricao_preset("balanced"),
            foreground="#7f8c8d",
            wraplength=400
        )
        self.lbl_descricao_preset.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))
        
        # Configurações avançadas (opcionais)
        self.mostrar_avancado = tk.BooleanVar()
        chk_avancado = ttk.Checkbutton(
            config_frame,
            text="Mostrar opções avançadas",
            variable=self.mostrar_avancado,
            command=self.toggle_configuracoes_avancadas
        )
        chk_avancado.grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        # Frame para configurações avançadas (inicialmente oculto)
        self.avancado_frame = ttk.Frame(config_frame)
        
        self.criar_configuracoes_avancadas()
        
        # Opções de saída
        saida_frame = ttk.LabelFrame(config_frame, text="Opções de Saída", padding=10)
        saida_frame.grid(row=3, column=0, sticky="ew", pady=10)
        
        # Pasta de destino
        ttk.Label(saida_frame, text="Pasta de Destino:").grid(row=0, column=0, sticky="w")
        
        destino_frame = ttk.Frame(saida_frame)
        destino_frame.grid(row=1, column=0, sticky="ew", pady=(5, 10))
        
        self.destino_var = tk.StringVar(value="./comprimidos")
        self.entry_destino = ttk.Entry(destino_frame, textvariable=self.destino_var, width=50)
        self.entry_destino.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        btn_procurar_destino = ttk.Button(
            destino_frame,
            text="Procurar",
            command=self.selecionar_pasta_destino
        )
        btn_procurar_destino.grid(row=0, column=1)
        
        # Opções adicionais
        self.criar_backup = tk.BooleanVar(value=True)
        chk_backup = ttk.Checkbutton(
            saida_frame,
            text="Criar backup dos arquivos originais",
            variable=self.criar_backup
        )
        chk_backup.grid(row=2, column=0, sticky="w")
        
        self.sobrescrever = tk.BooleanVar(value=False)
        chk_sobrescrever = ttk.Checkbutton(
            saida_frame,
            text="Sobrescrever arquivos existentes",
            variable=self.sobrescrever
        )
        chk_sobrescrever.grid(row=3, column=0, sticky="w")
        
        # Configurar expansão
        config_frame.grid_columnconfigure(0, weight=1)
        preset_frame.grid_columnconfigure(2, weight=1)
        destino_frame.grid_columnconfigure(0, weight=1)
        saida_frame.grid_columnconfigure(0, weight=1)
    
    def criar_configuracoes_avancadas(self):
        """Cria as configurações avançadas."""
        # Frame para qualidade
        qualidade_frame = ttk.LabelFrame(self.avancado_frame, text="Qualidade", padding=10)
        qualidade_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ttk.Label(qualidade_frame, text="Qualidade Geral:").grid(row=0, column=0, sticky="w")
        self.qualidade_var = tk.IntVar(value=80)
        scale_qualidade = ttk.Scale(
            qualidade_frame,
            from_=10,
            to=100,
            variable=self.qualidade_var,
            orient="horizontal"
        )
        scale_qualidade.grid(row=1, column=0, sticky="ew", pady=5)
        
        self.lbl_qualidade = ttk.Label(qualidade_frame, text="80%")
        self.lbl_qualidade.grid(row=1, column=1, padx=(10, 0))
        
        scale_qualidade.configure(command=self.atualizar_label_qualidade)
        
        # Frame para imagens
        imagem_frame = ttk.LabelFrame(self.avancado_frame, text="Imagens", padding=10)
        imagem_frame.grid(row=0, column=1, sticky="ew")
        
        ttk.Label(imagem_frame, text="Qualidade das Imagens:").grid(row=0, column=0, sticky="w")
        self.qualidade_imagem_var = tk.IntVar(value=75)
        scale_imagem = ttk.Scale(
            imagem_frame,
            from_=10,
            to=100,
            variable=self.qualidade_imagem_var,
            orient="horizontal"
        )
        scale_imagem.grid(row=1, column=0, sticky="ew", pady=5)
        
        self.lbl_qualidade_imagem = ttk.Label(imagem_frame, text="75%")
        self.lbl_qualidade_imagem.grid(row=1, column=1, padx=(10, 0))
        
        scale_imagem.configure(command=self.atualizar_label_qualidade_imagem)
        
        ttk.Label(imagem_frame, text="DPI Máximo:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.dpi_var = tk.IntVar(value=150)
        spin_dpi = ttk.Spinbox(
            imagem_frame,
            from_=72,
            to=300,
            textvariable=self.dpi_var,
            width=10
        )
        spin_dpi.grid(row=3, column=0, sticky="w", pady=5)
        
        # Opções de processamento
        processamento_frame = ttk.LabelFrame(self.avancado_frame, text="Processamento", padding=10)
        processamento_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        self.usar_cache = tk.BooleanVar(value=True)
        chk_cache = ttk.Checkbutton(
            processamento_frame,
            text="Usar cache para acelerar reprocessamento",
            variable=self.usar_cache
        )
        chk_cache.grid(row=0, column=0, sticky="w")
        
        self.processamento_paralelo = tk.BooleanVar(value=True)
        chk_paralelo = ttk.Checkbutton(
            processamento_frame,
            text="Processamento paralelo (mais rápido)",
            variable=self.processamento_paralelo
        )
        chk_paralelo.grid(row=1, column=0, sticky="w")
        
        # Configurar expansão
        qualidade_frame.grid_columnconfigure(0, weight=1)
        imagem_frame.grid_columnconfigure(0, weight=1)
        processamento_frame.grid_columnconfigure(0, weight=1)
        self.avancado_frame.grid_columnconfigure(0, weight=1)
        self.avancado_frame.grid_columnconfigure(1, weight=1)
    
    def criar_secao_processamento(self):
        """Cria a seção de processamento."""
        processo_frame = ttk.LabelFrame(
            self.main_frame,
            text=" Processamento ",
            padding=15
        )
        processo_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        
        # Botão principal de compressão
        self.btn_comprimir = ttk.Button(
            processo_frame,
            text="COMPRIMIR ARQUIVOS",
            command=self.iniciar_compressao,
            style="Compress.TButton"
        )
        self.btn_comprimir.grid(row=0, column=0, pady=(0, 15))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            processo_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Label de status
        self.lbl_status = ttk.Label(
            processo_frame,
            text="Pronto para processar",
            foreground="#7f8c8d"
        )
        self.lbl_status.grid(row=2, column=0, sticky="w")
        
        # Botão para cancelar (inicialmente oculto)
        self.btn_cancelar = ttk.Button(
            processo_frame,
            text="Cancelar",
            command=self.cancelar_processamento,
            state="disabled"
        )
        self.btn_cancelar.grid(row=3, column=0, pady=(10, 0))
        
        processo_frame.grid_columnconfigure(0, weight=1)
    
    def criar_secao_resultados(self):
        """Cria a seção de resultados."""
        resultados_frame = ttk.LabelFrame(
            self.main_frame,
            text=" Resultados ",
            padding=15
        )
        resultados_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=10)
        
        # Frame para estatísticas
        stats_frame = ttk.Frame(resultados_frame)
        stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Labels de estatísticas
        self.lbl_arquivos_processados = ttk.Label(
            stats_frame,
            text="Arquivos processados: 0",
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_arquivos_processados.grid(row=0, column=0, sticky="w")
        
        self.lbl_espaco_economizado = ttk.Label(
            stats_frame,
            text="Espaço economizado: 0 MB",
            font=("Segoe UI", 9, "bold"),
            foreground="#27ae60"
        )
        self.lbl_espaco_economizado.grid(row=1, column=0, sticky="w")
        
        self.lbl_compressao_media = ttk.Label(
            stats_frame,
            text="Compressão média: 0%",
            font=("Segoe UI", 9, "bold"),
            foreground="#3498db"
        )
        self.lbl_compressao_media.grid(row=2, column=0, sticky="w")
        
        # Lista de resultados detalhados
        resultados_lista_frame = ttk.Frame(resultados_frame)
        resultados_lista_frame.grid(row=1, column=0, sticky="ew")
        
        # Treeview para resultados
        colunas_result = ("Arquivo", "Original", "Final", "Compressão", "Status")
        self.tree_resultados = ttk.Treeview(
            resultados_lista_frame,
            columns=colunas_result,
            show="tree headings",
            height=6
        )
        
        # Configurar colunas dos resultados
        self.tree_resultados.heading("#0", text="")
        self.tree_resultados.column("#0", width=30, minwidth=30)
        
        larguras_col = [300, 100, 100, 80, 100]
        for i, col in enumerate(colunas_result):
            self.tree_resultados.heading(col, text=col)
            self.tree_resultados.column(col, width=larguras_col[i], minwidth=larguras_col[i] - 20)
        
        # Scrollbar para resultados
        scrollbar_resultados = ttk.Scrollbar(
            resultados_lista_frame,
            orient="vertical",
            command=self.tree_resultados.yview
        )
        self.tree_resultados.configure(yscrollcommand=scrollbar_resultados.set)
        
        # Grid dos resultados
        self.tree_resultados.grid(row=0, column=0, sticky="ew")
        scrollbar_resultados.grid(row=0, column=1, sticky="ns")
        
        # Botões de ação nos resultados
        acoes_frame = ttk.Frame(resultados_frame)
        acoes_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        self.btn_limpar_resultados = ttk.Button(
            acoes_frame,
            text="Limpar Resultados",
            command=self.limpar_resultados
        )
        self.btn_limpar_resultados.grid(row=0, column=0, padx=(0, 10))
        
        self.btn_exportar_relatorio = ttk.Button(
            acoes_frame,
            text="Exportar Relatório",
            command=self.exportar_relatorio
        )
        self.btn_exportar_relatorio.grid(row=0, column=1)
        
        # Configurar expansão
        resultados_frame.grid_columnconfigure(0, weight=1)
        resultados_lista_frame.grid_columnconfigure(0, weight=1)
    
    def criar_rodape(self):
        """Cria o rodapé com informações."""
        rodape_frame = ttk.Frame(self.main_frame)
        rodape_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=20)
        
        # Separador
        separator = ttk.Separator(rodape_frame, orient="horizontal")
        separator.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Informações
        info_text = "CompactPDF v1.0"
        lbl_info = ttk.Label(
            rodape_frame,
            text=info_text,
            foreground="#95a5a6",
            font=("Segoe UI", 8)
        )
        lbl_info.grid(row=1, column=0)
        
        rodape_frame.grid_columnconfigure(0, weight=1)
    
    # ==================== MÉTODOS DE INTERAÇÃO ====================
    
    def selecionar_arquivos(self):
        """Permite selecionar arquivos PDF."""
        arquivos = filedialog.askopenfilenames(
            title="Selecionar Arquivos PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivos:
            self.adicionar_arquivos(arquivos)
    
    def selecionar_pasta(self):
        """Permite selecionar uma pasta para processar todos os PDFs."""
        pasta = filedialog.askdirectory(title="Selecionar Pasta com PDFs")
        
        if pasta:
            # Encontrar todos os PDFs na pasta
            pdfs = []
            for root, dirs, files in os.walk(pasta):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdfs.append(os.path.join(root, file))
            
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
    
    def adicionar_arquivos(self, arquivos):
        """Adiciona arquivos à lista."""
        for arquivo in arquivos:
            if arquivo not in self.arquivos_selecionados:
                self.arquivos_selecionados.append(arquivo)
        
        self.atualizar_lista_arquivos()
        self.atualizar_info_arquivos()
    
    def limpar_arquivos(self):
        """Limpa a lista de arquivos selecionados."""
        self.arquivos_selecionados.clear()
        self.atualizar_lista_arquivos()
        self.atualizar_info_arquivos()
    
    def atualizar_lista_arquivos(self):
        """Atualiza a visualização da lista de arquivos."""
        # Limpar lista atual
        for item in self.tree_arquivos.get_children():
            self.tree_arquivos.delete(item)
        
        # Adicionar arquivos
        for i, arquivo in enumerate(self.arquivos_selecionados):
            nome = os.path.basename(arquivo)
            
            try:
                tamanho = os.path.getsize(arquivo)
                tamanho_str = self.formatar_tamanho(tamanho)
                status = "Pronto"
            except:
                tamanho_str = "Erro"
                status = "Arquivo não encontrado"
            
            self.tree_arquivos.insert(
                "",
                "end",
                values=(nome, tamanho_str, status)
            )
    
    def atualizar_info_arquivos(self):
        """Atualiza as informações sobre os arquivos selecionados."""
        total = len(self.arquivos_selecionados)
        
        if total == 0:
            self.lbl_info_arquivos.config(text="Nenhum arquivo selecionado")
        else:
            # Calcular tamanho total
            tamanho_total = 0
            for arquivo in self.arquivos_selecionados:
                try:
                    tamanho_total += os.path.getsize(arquivo)
                except:
                    pass
            
            tamanho_str = self.formatar_tamanho(tamanho_total)
            self.lbl_info_arquivos.config(
                text=f"{total} arquivo(s) selecionado(s) • Tamanho total: {tamanho_str}"
            )
    
    def selecionar_pasta_destino(self):
        """Permite selecionar pasta de destino."""
        pasta = filedialog.askdirectory(title="Selecionar Pasta de Destino")
        if pasta:
            self.destino_var.set(pasta)
    
    def atualizar_descricao_preset(self, event=None):
        """Atualiza a descrição do preset selecionado."""
        preset = self.preset_var.get()
        descricao = self.get_descricao_preset(preset)
        self.lbl_descricao_preset.config(text=descricao)
    
    def get_descricao_preset(self, preset):
        """Retorna a descrição do preset."""
        descricoes = {
            "minimal": "Compressão leve - Mantém alta qualidade",
            "balanced": "Compressão equilibrada - Boa relação tamanho/qualidade",
            "aggressive": "Compressão máxima - Reduz drasticamente o tamanho"
        }
        return descricoes.get(preset, "Preset personalizado")
    
    def toggle_configuracoes_avancadas(self):
        """Mostra/oculta configurações avançadas."""
        if self.mostrar_avancado.get():
            self.avancado_frame.grid(row=2, column=0, sticky="ew", pady=10)
        else:
            self.avancado_frame.grid_remove()
    
    def atualizar_label_qualidade(self, valor):
        """Atualiza o label da qualidade geral."""
        self.lbl_qualidade.config(text=f"{int(float(valor))}%")
    
    def atualizar_label_qualidade_imagem(self, valor):
        """Atualiza o label da qualidade das imagens."""
        self.lbl_qualidade_imagem.config(text=f"{int(float(valor))}%")
    
    def criar_configuracao(self):
        """Cria configuração baseada nas opções selecionadas."""
        if self.mostrar_avancado.get():
            # Configuração personalizada
            config = CompressionConfig()
            
            # Aplicar configurações da interface
            config.image_config.jpeg_quality = self.qualidade_imagem_var.get()
            config.image_config.max_dpi = self.dpi_var.get()
            config.performance_config.use_cache = self.usar_cache.get()
            config.backup_config.create_backup = self.criar_backup.get()
            config.performance_config.max_threads = 4 if self.processamento_paralelo.get() else 1
            
            # Definir nível baseado na qualidade
            qualidade = self.qualidade_var.get()
            if qualidade <= 3:
                config.apply_preset(CompressionLevel.AGGRESSIVE)
            elif qualidade <= 7:
                config.apply_preset(CompressionLevel.BALANCED)
            else:
                config.apply_preset(CompressionLevel.MINIMAL)
        else:
            # Usar preset
            config = CompressionConfig()
            preset_name = self.preset_var.get()
            
            if preset_name == "minimal":
                config.apply_preset(CompressionLevel.MINIMAL)
            elif preset_name == "balanced":
                config.apply_preset(CompressionLevel.BALANCED)
            elif preset_name == "aggressive":
                config.apply_preset(CompressionLevel.AGGRESSIVE)
            
            # Aplicar configurações gerais
            config.backup_config.create_backup = self.criar_backup.get()
        
        return config
    
    def iniciar_compressao(self):
        """Inicia o processo de compressão."""
        if not self.arquivos_selecionados:
            messagebox.showwarning(
                "Nenhum Arquivo",
                "Selecione pelo menos um arquivo PDF para comprimir."
            )
            return
        
        if self.processamento_ativo:
            messagebox.showwarning(
                "Processamento Ativo",
                "Já existe um processamento em andamento."
            )
            return
        
        # Verificar pasta de destino
        pasta_destino = self.destino_var.get()
        if not pasta_destino:
            messagebox.showerror(
                "Pasta de Destino",
                "Selecione uma pasta de destino."
            )
            return
        
        # Criar pasta se não existir
        try:
            os.makedirs(pasta_destino, exist_ok=True)
        except Exception as e:
            messagebox.showerror(
                "Erro na Pasta",
                f"Erro ao criar pasta de destino: {e}"
            )
            return
        
        # Configurar interface para processamento
        self.processar_iniciar_ui()
        
        # Iniciar processamento em thread separada
        config = self.criar_configuracao()
        
        self.thread_processamento = threading.Thread(
            target=self.processar_arquivos,
            args=(self.arquivos_selecionados.copy(), pasta_destino, config),
            daemon=True
        )
        self.thread_processamento.start()
    
    def processar_iniciar_ui(self):
        """Configura a UI para o início do processamento."""
        self.processamento_ativo = True
        self.btn_comprimir.config(state="disabled")
        self.btn_cancelar.config(state="normal")
        self.progress_var.set(0)
        self.lbl_status.config(text="Iniciando processamento...", foreground="#3498db")
    
    def processar_finalizar_ui(self):
        """Configura a UI para o fim do processamento."""
        self.processamento_ativo = False
        self.btn_comprimir.config(state="normal")
        self.btn_cancelar.config(state="disabled")
        self.progress_var.set(100)
        self.lbl_status.config(text="Processamento concluído!", foreground="#27ae60")
    
    def processar_arquivos(self, arquivos, pasta_destino, config):
        """Processa os arquivos em thread separada."""
        total_arquivos = len(arquivos)
        arquivos_processados = 0
        sucessos = 0
        falhas = 0
        
        resultados_sessao = []
        
        for i, arquivo in enumerate(arquivos):
            if not self.processamento_ativo:  # Verificar cancelamento
                break
            
            try:
                # Atualizar status
                nome_arquivo = os.path.basename(arquivo)
                self.root.after(
                    0,
                    lambda msg=f"Processando: {nome_arquivo}": 
                    self.lbl_status.config(text=msg, foreground="#3498db")
                )
                
                # Definir arquivo de saída
                output_path = os.path.join(pasta_destino, nome_arquivo)
                
                # Comprimir
                resultado = self.compressor.compress_file(arquivo, output_path, config_override=config)
                
                # Atualizar resultado na UI
                self.root.after(0, self.adicionar_resultado, arquivo, resultado, "Sucesso")
                
                resultados_sessao.append(resultado)
                sucessos += 1
                
            except Exception as e:
                # Erro no processamento
                self.root.after(0, self.adicionar_resultado, arquivo, None, f"Erro: {str(e)}")
                falhas += 1
            
            # Atualizar progresso
            arquivos_processados += 1
            progresso = (arquivos_processados / total_arquivos) * 100
            self.root.after(0, self.progress_var.set, progresso)
        
        # Finalizar processamento
        if self.processamento_ativo:
            self.root.after(0, self.processar_finalizar_ui)
            self.root.after(0, self.atualizar_estatisticas, resultados_sessao)
            
            # Mostrar resumo
            mensagem = f"Processamento concluído!\n\n"
            mensagem += f"Sucessos: {sucessos}\n"
            mensagem += f"Falhas: {falhas}\n"
            mensagem += f"Total: {total_arquivos}"
            
            self.root.after(
                0,
                messagebox.showinfo,
                "Processamento Concluído",
                mensagem
            )
    
    def cancelar_processamento(self):
        """Cancela o processamento em andamento."""
        if messagebox.askyesno(
            "Cancelar Processamento",
            "Deseja realmente cancelar o processamento em andamento?"
        ):
            self.processamento_ativo = False
            self.btn_comprimir.config(state="normal")
            self.btn_cancelar.config(state="disabled")
            self.lbl_status.config(text="Processamento cancelado", foreground="#e74c3c")
    
    def adicionar_resultado(self, arquivo, resultado, status):
        """Adiciona resultado à lista de resultados."""
        nome = os.path.basename(arquivo)
        
        if resultado and status == "Sucesso":
            tamanho_original = self.formatar_tamanho(resultado.original_size)
            tamanho_final = self.formatar_tamanho(resultado.compressed_size)
            compressao = f"{resultado.compression_percentage:.1f}%"
            
            # Adicionar ao histórico
            self.resultados_historico.append(resultado)
        else:
            tamanho_original = "N/A"
            tamanho_final = "N/A"
            compressao = "N/A"
        
        # Adicionar à árvore
        item = self.tree_resultados.insert(
            "",
            "end",
            values=(nome, tamanho_original, tamanho_final, compressao, status)
        )
        
        # Colorir baseado no status
        if "Erro" in status:
            self.tree_resultados.set(item, "Status", status)
        
        # Scroll para o item recém-adicionado
        self.tree_resultados.see(item)
    
    def atualizar_estatisticas(self, resultados_sessao):
        """Atualiza as estatísticas gerais."""
        if not self.resultados_historico:
            return
        
        total_arquivos = len(self.resultados_historico)
        
        # Calcular estatísticas
        espaco_economizado = sum(r.space_saved for r in self.resultados_historico)
        compressao_media = sum(r.compression_ratio for r in self.resultados_historico) / total_arquivos
        
        # Atualizar labels
        self.lbl_arquivos_processados.config(text=f"Arquivos processados: {total_arquivos}")
        self.lbl_espaco_economizado.config(
            text=f"Espaço economizado: {self.formatar_tamanho(espaco_economizado)}"
        )
        self.lbl_compressao_media.config(text=f"Compressão média: {compressao_media:.1f}%")
    
    def limpar_resultados(self):
        """Limpa a lista de resultados."""
        if messagebox.askyesno(
            "Limpar Resultados",
            "Deseja limpar todos os resultados da sessão atual?"
        ):
            # Limpar árvore
            for item in self.tree_resultados.get_children():
                self.tree_resultados.delete(item)
            
            # Limpar histórico
            self.resultados_historico.clear()
            
            # Resetar estatísticas
            self.lbl_arquivos_processados.config(text="Arquivos processados: 0")
            self.lbl_espaco_economizado.config(text="Espaço economizado: 0 MB")
            self.lbl_compressao_media.config(text="Compressão média: 0%")
    
    def exportar_relatorio(self):
        """Exporta relatório dos resultados."""
        if not self.resultados_historico:
            messagebox.showwarning(
                "Nenhum Resultado",
                "Não há resultados para exportar."
            )
            return
        
        arquivo_relatorio = filedialog.asksaveasfilename(
            title="Salvar Relatório",
            defaultextension=".txt",
            filetypes=[
                ("Arquivo de Texto", "*.txt"),
                ("Arquivo JSON", "*.json"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if not arquivo_relatorio:
            return
        
        try:
            if arquivo_relatorio.endswith('.json'):
                self.exportar_relatorio_json(arquivo_relatorio)
            else:
                self.exportar_relatorio_texto(arquivo_relatorio)
            
            messagebox.showinfo(
                "Relatório Exportado",
                f"Relatório salvo em:\n{arquivo_relatorio}"
            )
        except Exception as e:
            messagebox.showerror(
                "Erro na Exportação",
                f"Erro ao exportar relatório: {e}"
            )
    
    def exportar_relatorio_texto(self, arquivo):
        """Exporta relatório em formato texto."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE COMPRESSÃO - CompactPDF\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Arquivos processados: {len(self.resultados_historico)}\n\n")
            
            # Estatísticas gerais
            espaco_total = sum(r.space_saved for r in self.resultados_historico)
            compressao_media = sum(r.compression_ratio for r in self.resultados_historico) / len(self.resultados_historico)
            
            f.write("ESTATÍSTICAS GERAIS:\n")
            f.write(f"  Espaço economizado: {self.formatar_tamanho(espaco_total)}\n")
            f.write(f"  Compressão média: {compressao_media:.1f}%\n\n")
            
            # Detalhes por arquivo
            f.write("DETALHES POR ARQUIVO:\n")
            f.write("-" * 50 + "\n")
            
            for resultado in self.resultados_historico:
                nome = os.path.basename(resultado.input_path)
                f.write(f"Arquivo: {nome}\n")
                f.write(f"  Tamanho original: {self.formatar_tamanho(resultado.original_size)}\n")
                f.write(f"  Tamanho comprimido: {self.formatar_tamanho(resultado.compressed_size)}\n")
                f.write(f"  Compressão: {resultado.compression_percentage:.1f}%\n")
                f.write(f"  Espaço economizado: {self.formatar_tamanho(resultado.space_saved)}\n")
                f.write(f"  Tempo de processamento: {resultado.processing_time:.2f}s\n")
                f.write(f"  Estratégias usadas: {', '.join(resultado.strategies_used)}\n\n")
    
    def exportar_relatorio_json(self, arquivo):
        """Exporta relatório em formato JSON."""
        dados = {
            "relatorio": {
                "data": datetime.now().isoformat(),
                "total_arquivos": len(self.resultados_historico),
                "estatisticas": {
                    "espaco_economizado": sum(r.space_saved for r in self.resultados_historico),
                    "compressao_media": sum(r.compression_ratio for r in self.resultados_historico) / len(self.resultados_historico)
                },
                "resultados": []
            }
        }
        
        for resultado in self.resultados_historico:
            dados["relatorio"]["resultados"].append({
                "arquivo": os.path.basename(resultado.input_path),
                "tamanho_original": resultado.original_size,
                "tamanho_comprimido": resultado.compressed_size,
                "compressao_percentual": resultado.compression_percentage,
                "espaco_economizado": resultado.space_saved,
                "tempo_processamento": resultado.processing_time,
                "estrategias_usadas": resultado.strategies_used
            })
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    
    # ==================== MÉTODOS UTILITÁRIOS ====================
    
    def formatar_tamanho(self, tamanho_bytes):
        """Formata tamanho em bytes para formato legível."""
        if tamanho_bytes < 1024:
            return f"{tamanho_bytes} B"
        elif tamanho_bytes < 1024 * 1024:
            return f"{tamanho_bytes / 1024:.1f} KB"
        elif tamanho_bytes < 1024 * 1024 * 1024:
            return f"{tamanho_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{tamanho_bytes / (1024 * 1024 * 1024):.1f} GB"


def main():
    """Função principal para executar a GUI."""
    try:
        # Criar janela principal
        root = tk.Tk()
        
        # Configurar tema do Windows se disponível
        try:
            root.tk.call('source', 'azure.tcl')
            root.tk.call('set_theme', 'light')
        except:
            pass
        
        # Criar aplicação
        app = CompactPDFGUI(root)
        
        # Executar loop principal
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n🛑 Aplicação interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        messagebox.showerror("Erro Fatal", f"Erro inesperado na aplicação:\n{e}")


if __name__ == "__main__":
    main()
