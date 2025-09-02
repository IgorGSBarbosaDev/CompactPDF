#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Painel de Resultados - CompactPDF GUI
====================================

Responsável pela exibição e gerenciamento dos resultados de compressão.
Segue o princípio SRP (Single Responsibility Principle).
"""

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from typing import List, Optional

# Importar modelos do CompactPDF
import sys
from pathlib import Path

# Configurar path para importar módulos do projeto
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
src_dir = project_root / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

try:
    from models.compression_result import CompressionResult # type: ignore
except ImportError:
    try:
        from src.models.compression_result import CompressionResult # type: ignore
    except ImportError as e:
        print(f"Erro ao importar CompressionResult: {e}")
        # Criar classe placeholder
        class CompressionResult:
            def __init__(self, *args, **kwargs):
                self.success = False
                self.original_size = 0
                self.compressed_size = 0
                self.compression_ratio = 0.0
                self.compression_percentage = 0.0
                self.space_saved = 0
                self.processing_time = 0.0
                self.input_path = ""
                self.output_path = ""
                self.strategies_used = []
                self.error_message = "Módulo não encontrado"


class ResultsPanel:
    """Painel responsável pela exibição e gerenciamento de resultados."""
    
    def __init__(self, parent, style_manager=None):
        """
        Inicializa o painel de resultados.
        
        Args:
            parent: Widget pai
            style_manager: Gerenciador de estilos (opcional)
        """
        self.parent = parent
        self.style_manager = style_manager
        self.results_history: List[CompressionResult] = []
        
        # Variáveis de controle
        self.current_result: Optional[CompressionResult] = None
        
        # Cache de histórico
        self.history_file = "compression_history.json"
        
        self._create_widgets()
        self._setup_layout()
        self._load_history()
    
    def _create_widgets(self):
        """Cria os widgets do painel."""
        # Frame principal
        self.frame = ttk.Frame(self.parent)
        
        # Notebook para organizar resultados
        self.notebook = ttk.Notebook(self.frame)
        
        # Aba: Resultado Atual
        self.current_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.current_frame, text="📊 Resultado Atual")
        
        # Aba: Histórico
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📚 Histórico")
        
        # Aba: Estatísticas
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="📈 Estatísticas")
        
        self._create_current_tab()
        self._create_history_tab()
        self._create_stats_tab()
    
    def _create_current_tab(self):
        """Cria a aba de resultado atual."""
        # Área de informações gerais
        info_frame = ttk.LabelFrame(self.current_frame, text="📋 Informações do Resultado")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        # Texto de informações
        self.info_text = tk.Text(
            info_frame,
            height=8,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        self.info_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar para o texto
        info_scroll = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scroll.set)
        
        # Área de métricas visuais
        metrics_frame = ttk.LabelFrame(self.current_frame, text="🎯 Métricas de Compressão")
        metrics_frame.pack(fill="x", padx=10, pady=5)
        
        # Frame para as barras de progresso
        progress_frame = ttk.Frame(metrics_frame)
        progress_frame.pack(fill="x", padx=5, pady=5)
        
        # Barra de compressão
        ttk.Label(progress_frame, text="Taxa de Compressão:").pack(anchor="w")
        self.compression_bar = ttk.Progressbar(
            progress_frame,
            length=300,
            mode='determinate'
        )
        self.compression_bar.pack(fill="x", pady=(0, 10))
        
        # Label da taxa
        self.compression_label = ttk.Label(progress_frame, text="0%")
        self.compression_label.pack(anchor="w")
        
        # Botões de ação
        actions_frame = ttk.Frame(self.current_frame)
        actions_frame.pack(fill="x", padx=10, pady=5)
        
        self.open_file_btn = ttk.Button(
            actions_frame,
            text="📂 Abrir Arquivo Comprimido",
            command=self._open_compressed_file
        )
        self.open_file_btn.pack(side="left", padx=(0, 5))
        
        self.open_folder_btn = ttk.Button(
            actions_frame,
            text="📁 Abrir Pasta",
            command=self._open_output_folder
        )
        self.open_folder_btn.pack(side="left", padx=5)
        
        self.export_report_btn = ttk.Button(
            actions_frame,
            text="📄 Exportar Relatório",
            command=self._export_report
        )
        self.export_report_btn.pack(side="right")
    
    def _create_history_tab(self):
        """Cria a aba de histórico."""
        # Barra de ferramentas
        toolbar_frame = ttk.Frame(self.history_frame)
        toolbar_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(
            toolbar_frame,
            text="🔄 Atualizar",
            command=self._refresh_history
        ).pack(side="left", padx=(0, 5))
        
        ttk.Button(
            toolbar_frame,
            text="🗑️ Limpar",
            command=self._clear_history
        ).pack(side="left", padx=5)
        
        ttk.Button(
            toolbar_frame,
            text="📤 Exportar",
            command=self._export_history
        ).pack(side="right")
        
        # Lista de histórico
        list_frame = ttk.Frame(self.history_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview para histórico
        columns = ("Data", "Arquivo", "Tamanho Original", "Tamanho Final", "Compressão")
        self.history_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # Configurar colunas
        self.history_tree.heading("Data", text="📅 Data")
        self.history_tree.heading("Arquivo", text="📄 Arquivo")
        self.history_tree.heading("Tamanho Original", text="📏 Original")
        self.history_tree.heading("Tamanho Final", text="📏 Final")
        self.history_tree.heading("Compressão", text="📉 Compressão")
        
        # Larguras das colunas
        self.history_tree.column("Data", width=120)
        self.history_tree.column("Arquivo", width=200)
        self.history_tree.column("Tamanho Original", width=100)
        self.history_tree.column("Tamanho Final", width=100)
        self.history_tree.column("Compressão", width=100)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.history_tree.yview)
        h_scroll = ttk.Scrollbar(list_frame, orient="horizontal", command=self.history_tree.xview)
        
        self.history_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Layout
        self.history_tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Bind para seleção
        self.history_tree.bind("<<TreeviewSelect>>", self._on_history_select)
    
    def _create_stats_tab(self):
        """Cria a aba de estatísticas."""
        # Frame de estatísticas gerais
        general_frame = ttk.LabelFrame(self.stats_frame, text="📊 Estatísticas Gerais")
        general_frame.pack(fill="x", padx=10, pady=5)
        
        # Grid para estatísticas
        stats_grid = ttk.Frame(general_frame)
        stats_grid.pack(fill="x", padx=10, pady=10)
        
        # Labels de estatísticas
        self.total_files_label = ttk.Label(stats_grid, text="Total de Arquivos: 0")
        self.total_files_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        self.total_space_label = ttk.Label(stats_grid, text="Espaço Total Economizado: 0 MB")
        self.total_space_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        self.avg_compression_label = ttk.Label(stats_grid, text="Compressão Média: 0%")
        self.avg_compression_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        self.total_time_label = ttk.Label(stats_grid, text="Tempo Total: 0 min")
        self.total_time_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Gráfico de compressão (simulado com progressbar)
        chart_frame = ttk.LabelFrame(self.stats_frame, text="📈 Distribuição de Compressão")
        chart_frame.pack(fill="x", padx=10, pady=5)
        
        # Barras para diferentes níveis de compressão
        self._create_compression_chart(chart_frame)
    
    def _create_compression_chart(self, parent):
        """Cria um gráfico simples de distribuição de compressão."""
        chart_content = ttk.Frame(parent)
        chart_content.pack(fill="x", padx=10, pady=10)
        
        # Categorias de compressão
        categories = [
            ("< 25%", "lightcoral"),
            ("25-50%", "gold"),
            ("> 50%", "lightgreen")
        ]
        
        self.compression_bars = {}
        
        for i, (category, color) in enumerate(categories):
            # Label da categoria
            ttk.Label(chart_content, text=f"{category}:").grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            # Barra de progresso
            bar = ttk.Progressbar(
                chart_content,
                length=200,
                mode='determinate'
            )
            bar.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            
            # Label de contagem
            count_label = ttk.Label(chart_content, text="0 arquivos")
            count_label.grid(row=i, column=2, sticky="w", padx=5, pady=2)
            
            self.compression_bars[category] = (bar, count_label)
        
        chart_content.grid_columnconfigure(1, weight=1)
    
    def _setup_layout(self):
        """Configura o layout do painel."""
        self.frame.pack(fill="both", expand=True)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
    
    def update_result(self, result: CompressionResult):
        """
        Atualiza o painel com um novo resultado.
        
        Args:
            result: Resultado da compressão
        """
        self.current_result = result
        self.results_history.append(result)
        
        self._update_current_display()
        self._update_history_display()
        self._update_stats_display()
        self._save_history()
    
    def _update_current_display(self):
        """Atualiza a exibição do resultado atual."""
        if not self.current_result:
            return
        
        result = self.current_result
        
        # Atualizar texto de informações
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        if result.success:
            # Calcular estatísticas
            original_size = self._format_file_size(result.original_size)
            compressed_size = self._format_file_size(result.compressed_size)
            compression = f"{getattr(result, 'compression_percentage', 0):.1f}%"
            savings = self._format_file_size(getattr(result, 'space_saved', 0))
            
            # Aplicar cor baseada na compressão
            compression_percent = getattr(result, 'compression_percentage', 0)
            if compression_percent >= 50:
                status_color = "🟢"
            elif compression_percent >= 25:
                status_color = "🟡"
            else:
                status_color = "🔴"
            
            info_text = f"""✅ Compressão Concluída com Sucesso! {status_color}

📁 Arquivo Original: {getattr(result, 'input_path', 'N/A')}
📁 Arquivo Comprimido: {getattr(result, 'output_path', 'N/A')}

📏 Tamanho Original: {original_size}
📏 Tamanho Comprimido: {compressed_size}
• Espaço Economizado: {savings}
• Compressão: {compression}
• Tempo de Processamento: {getattr(result, 'processing_time', 0):.2f} segundos

🔧 Estratégias Utilizadas:
{chr(10).join('• ' + strategy for strategy in (getattr(result, 'strategies_used', []) or []))}
"""
        else:
            info_text = f"""❌ Erro na Compressão

🚫 Erro: {result.error_message}
📁 Arquivo: {getattr(result, 'input_path', 'N/A')}
"""
        
        self.info_text.insert(1.0, info_text)
        self.info_text.config(state=tk.DISABLED)
        
        # Atualizar barra de progresso
        compression_percent = getattr(result, 'compression_percentage', 0) if result.success else 0
        self.compression_bar['value'] = compression_percent
        self.compression_label.config(text=f"{compression_percent:.1f}%")
    
    def _update_history_display(self):
        """Atualiza a exibição do histórico."""
        # Limpar lista atual
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Adicionar resultados (mais recentes primeiro)
        for result in reversed(self.results_history[-50:]):  # Últimos 50 resultados
            if result.success:
                values = (
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    os.path.basename(getattr(result, 'input_path', 'N/A')),
                    self._format_file_size(result.original_size),
                    self._format_file_size(result.compressed_size),
                    f"{getattr(result, 'compression_percentage', 0):.1f}%"
                )
                self.history_tree.insert("", "end", values=values)
    
    def _update_stats_display(self):
        """Atualiza as estatísticas."""
        if not self.results_history:
            return
        
        successful_results = [r for r in self.results_history if r.success]
        
        if not successful_results:
            return
        
        # Estatísticas gerais
        total_files = len(successful_results)
        total_space_saved = sum(getattr(r, 'space_saved', 0) for r in self.results_history)
        avg_compression = sum(getattr(r, 'compression_percentage', 0) for r in successful_results) / len(successful_results)
        total_time = sum(getattr(r, 'processing_time', 0) for r in self.results_history)
        
        # Atualizar labels
        self.total_files_label.config(text=f"Total de Arquivos: {total_files}")
        self.total_space_label.config(text=f"Espaço Total Economizado: {self._format_file_size(total_space_saved)}")
        self.avg_compression_label.config(text=f"Compressão Média: {avg_compression:.1f}%")
        self.total_time_label.config(text=f"Tempo Total: {total_time/60:.1f} min")
        
        # Atualizar gráfico de distribuição
        self._update_compression_chart(successful_results)
    
    def _update_compression_chart(self, results):
        """Atualiza o gráfico de distribuição de compressão."""
        # Categorizar resultados
        categories = {"< 25%": 0, "25-50%": 0, "> 50%": 0}
        
        for result in results:
            compression = getattr(result, 'compression_percentage', 0)
            if compression < 25:
                categories["< 25%"] += 1
            elif compression < 50:
                categories["25-50%"] += 1
            else:
                categories["> 50%"] += 1
        
        total = len(results)
        
        # Atualizar barras
        for category, (bar, label) in self.compression_bars.items():
            count = categories[category]
            percentage = (count / total * 100) if total > 0 else 0
            
            bar['value'] = percentage
            label.config(text=f"{count} arquivos ({percentage:.1f}%)")
    
    def _open_compressed_file(self):
        """Abre o arquivo comprimido."""
        if self.current_result and self.current_result.success:
            output_path = getattr(self.current_result, 'output_path', '')
            if output_path and os.path.exists(output_path):
                try:
                    os.startfile(output_path)
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")
            else:
                messagebox.showwarning("Aviso", "Arquivo não encontrado.")
    
    def _open_output_folder(self):
        """Abre a pasta onde está o arquivo comprimido."""
        if self.current_result and self.current_result.success:
            output_path = getattr(self.current_result, 'output_path', '')
            if output_path and os.path.exists(output_path):
                try:
                    folder_path = os.path.dirname(output_path)
                    os.startfile(folder_path)
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível abrir a pasta:\n{e}")
            else:
                messagebox.showwarning("Aviso", "Arquivo não encontrado.")
    
    def _export_report(self):
        """Exporta um relatório do resultado atual."""
        if not self.current_result:
            messagebox.showwarning("Aviso", "Nenhum resultado para exportar.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Salvar Relatório",
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    content = self.info_text.get(1.0, tk.END)
                    f.write(content)
                
                messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar relatório:\n{e}")
    
    def _on_history_select(self, event):
        """Manipula seleção no histórico."""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            filename = item['values'][1]
            
            # Encontrar resultado correspondente
            for result in self.results_history:
                if os.path.basename(getattr(result, 'input_path', '')) == filename:
                    self.current_result = result
                    self._update_current_display()
                    break
    
    def _refresh_history(self):
        """Atualiza a exibição do histórico."""
        self._load_history()
        self._update_history_display()
        self._update_stats_display()
    
    def _clear_history(self):
        """Limpa o histórico."""
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todo o histórico?"):
            self.results_history.clear()
            self._update_history_display()
            self._update_stats_display()
            self._save_history()
    
    def _export_history(self):
        """Exporta o histórico para arquivo."""
        if not self.results_history:
            messagebox.showwarning("Aviso", "Histórico vazio.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Exportar Histórico",
            defaultextension=".json",
            filetypes=[("Arquivo JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if filename:
            try:
                history_data = []
                for result in self.results_history:
                    if result.success:
                        history_data.append({
                            'timestamp': datetime.now().isoformat(),
                            'input_path': getattr(result, 'input_path', ''),
                            'output_path': getattr(result, 'output_path', ''),
                            'original_size': result.original_size,
                            'compressed_size': result.compressed_size,
                            'compression_percentage': getattr(result, 'compression_percentage', 0),
                            'processing_time': getattr(result, 'processing_time', 0),
                            'strategies_used': getattr(result, 'strategies_used', [])
                        })
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(history_data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Sucesso", f"Histórico exportado para:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar histórico:\n{e}")
    
    def _load_history(self):
        """Carrega o histórico de um arquivo."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                
                # Converter dados para objetos CompressionResult
                loaded_results = []
                for data in history_data:
                    result = CompressionResult()
                    result.success = True
                    result.original_size = data.get('original_size', 0)
                    result.compressed_size = data.get('compressed_size', 0)
                    result.compression_percentage = data.get('compression_percentage', 0)
                    result.space_saved = data.get('space_saved', 0)
                    result.processing_time = data.get('processing_time', 0)
                    result.input_path = data.get('input_path', '')
                    result.output_path = data.get('output_path', '')
                    result.strategies_used = data.get('strategies_used', [])
                    loaded_results.append(result)
                
                # Mesclar com histórico atual (evitar duplicatas)
                existing_paths = {getattr(r, 'input_path', '') for r in self.results_history}
                for result in loaded_results:
                    if getattr(result, 'input_path', '') not in existing_paths:
                        self.results_history.append(result)
        
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
    
    def _save_history(self):
        """Salva o histórico em arquivo."""
        try:
            history_data = []
            for result in self.results_history[-100:]:  # Salvar apenas últimos 100
                if result.success:
                    history_data.append({
                        'timestamp': datetime.now().isoformat(),
                        'input_path': getattr(result, 'input_path', ''),
                        'output_path': getattr(result, 'output_path', ''),
                        'original_size': result.original_size,
                        'compressed_size': result.compressed_size,
                        'compression_percentage': getattr(result, 'compression_percentage', 0),
                        'space_saved': getattr(result, 'space_saved', 0),
                        'processing_time': getattr(result, 'processing_time', 0),
                        'strategies_used': getattr(result, 'strategies_used', [])
                    })
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    def _format_file_size(self, size_bytes: int) -> str:
        """
        Formata o tamanho do arquivo em uma representação legível.
        
        Args:
            size_bytes: Tamanho em bytes
            
        Returns:
            String formatada com o tamanho
        """
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    def get_frame(self) -> ttk.Frame:
        """
        Retorna o frame principal do painel.
        
        Returns:
            Frame principal do painel
        """
        return self.frame
    
    def clear_results(self):
        """Limpa os resultados atuais."""
        self.current_result = None
        
        # Limpar texto
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, "Nenhum resultado ainda. Execute uma compressão para ver os resultados aqui.")
        self.info_text.config(state=tk.DISABLED)
        
        # Resetar barra de progresso
        self.compression_bar['value'] = 0
        self.compression_label.config(text="0%")
    
    def show_error(self, error_message: str):
        """
        Mostra uma mensagem de erro no painel.
        
        Args:
            error_message: Mensagem de erro
        """
        error_result = CompressionResult()
        error_result.success = False
        error_result.error_message = error_message
        
        self.current_result = error_result
        self._update_current_display()
