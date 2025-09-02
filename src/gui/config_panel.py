#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Painel de Configurações - CompactPDF GUI
========================================

Responsável pela configuração de parâmetros de compressão.
Segue o princípio SRP (Single Responsibility Principle).
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Optional, Callable

# Importar configurações do CompactPDF
import sys
from pathlib import Path

# Configurar path para importar módulos do projeto
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
src_dir = project_root / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

try:
    # Importar módulos de configuração
    from config import compression_config  # type: ignore
    CompressionConfig = compression_config.CompressionConfig  # type: ignore
    CompressionLevel = compression_config.CompressionLevel  # type: ignore
    IMPORT_SUCCESS = True
except ImportError:
    try:
        import src.config.compression_config as compression_config  # type: ignore
        CompressionConfig = compression_config.CompressionConfig  # type: ignore
        CompressionLevel = compression_config.CompressionLevel  # type: ignore
        IMPORT_SUCCESS = True
    except ImportError as e:
        print(f"Erro ao importar configurações: {e}")
        IMPORT_SUCCESS = False
        
        # Criar classes placeholder para evitar erros
        class CompressionLevel:  # type: ignore
            MINIMAL = "minimal"
            BALANCED = "balanced"
            AGGRESSIVE = "aggressive"
        
        class CompressionConfig:  # type: ignore
            def __init__(self):
                # Simular estrutura de configuração
                self.image_config = type('ImageConfig', (), {
                    'jpeg_quality': 85,
                    'max_dpi': 300
                })()
            
            def apply_preset(self, level):
                # Método placeholder
                pass


class ConfigurationPanel:
    """Painel de configuração de compressão."""
    
    def __init__(self, parent_frame: ttk.Frame, style_manager):
        """Inicializa o painel de configurações."""
        self.parent_frame = parent_frame
        self.style_manager = style_manager
        
        # Variáveis de configuração
        self.preset_var = tk.StringVar(value="balanced")
        self.destino_var = tk.StringVar(value="./comprimidos")
        self.mostrar_avancado = tk.BooleanVar()
        self.criar_backup = tk.BooleanVar(value=True)
        self.sobrescrever = tk.BooleanVar(value=False)
        
        # Variáveis avançadas
        self.qualidade_var = tk.IntVar(value=80)
        self.qualidade_imagem_var = tk.IntVar(value=75)
        self.dpi_var = tk.IntVar(value=150)
        self.usar_cache = tk.BooleanVar(value=True)
        self.processamento_paralelo = tk.BooleanVar(value=True)
        
        # Callback para mudanças de configuração
        self.on_config_changed: Optional[Callable] = None
        
        # Criar interface
        self._create_interface()
    
    def _create_interface(self):
        """Cria a interface de configurações."""
        self.main_frame = ttk.LabelFrame(
            self.parent_frame,
            text=" ⚙️ Configurações ",
            padding=15
        )
        self.main_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        # Criar seções
        self._create_preset_section()
        self._create_advanced_toggle()
        self._create_advanced_section()
        self._create_output_section()
        
        # Configurar expansão
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def _create_preset_section(self):
        """Cria a seção de presets."""
        preset_frame = ttk.Frame(self.main_frame)
        preset_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        ttk.Label(preset_frame, text="Nível de compressão:").grid(row=0, column=0, sticky="w")
        
        preset_combo = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_var,
            values=["minimal", "balanced", "aggressive"],
            state="readonly",
            width=15
        )
        preset_combo.grid(row=0, column=1, padx=(10, 20), sticky="w")
        preset_combo.bind("<<ComboboxSelected>>", self._on_preset_changed)
        
        # Descrição do preset
        self.lbl_descricao_preset = ttk.Label(
            preset_frame,
            text=self._get_preset_description("balanced"),
            foreground=self.style_manager.get_color('muted'),
            wraplength=400
        )
        self.lbl_descricao_preset.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))
        
        preset_frame.grid_columnconfigure(2, weight=1)
    
    def _create_advanced_toggle(self):
        """Cria o toggle para configurações avançadas."""
        chk_avancado = ttk.Checkbutton(
            self.main_frame,
            text="🔧 Mostrar opções avançadas",
            variable=self.mostrar_avancado,
            command=self._toggle_advanced_options
        )
        chk_avancado.grid(row=1, column=0, sticky="w", pady=(0, 10))
    
    def _create_advanced_section(self):
        """Cria a seção de configurações avançadas."""
        # Frame principal (inicialmente oculto)
        self.avancado_frame = ttk.LabelFrame(
            self.main_frame,
            text="Configurações Avançadas",
            padding=10
        )
        
        # Seção de qualidade
        self._create_quality_section()
        
        # Seção de imagens
        self._create_image_section()
        
        # Seção de processamento
        self._create_processing_section()
    
    def _create_quality_section(self):
        """Cria a seção de configuração de qualidade."""
        qualidade_frame = ttk.LabelFrame(self.avancado_frame, text="Qualidade", padding=10)
        qualidade_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ttk.Label(qualidade_frame, text="Qualidade Geral:").grid(row=0, column=0, sticky="w")
        
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
        
        scale_qualidade.configure(command=self._update_quality_label)
        
        qualidade_frame.grid_columnconfigure(0, weight=1)
    
    def _create_image_section(self):
        """Cria a seção de configuração de imagens."""
        imagem_frame = ttk.LabelFrame(self.avancado_frame, text="Imagens", padding=10)
        imagem_frame.grid(row=0, column=1, sticky="ew")
        
        ttk.Label(imagem_frame, text="Qualidade das Imagens:").grid(row=0, column=0, sticky="w")
        
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
        
        scale_imagem.configure(command=self._update_image_quality_label)
        
        ttk.Label(imagem_frame, text="DPI Máximo:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        
        spin_dpi = ttk.Spinbox(
            imagem_frame,
            from_=72,
            to=300,
            textvariable=self.dpi_var,
            width=10
        )
        spin_dpi.grid(row=3, column=0, sticky="w", pady=5)
        
        imagem_frame.grid_columnconfigure(0, weight=1)
    
    def _create_processing_section(self):
        """Cria a seção de opções de processamento."""
        processamento_frame = ttk.LabelFrame(
            self.avancado_frame,
            text="Processamento",
            padding=10
        )
        processamento_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        chk_cache = ttk.Checkbutton(
            processamento_frame,
            text="💾 Usar cache para acelerar reprocessamento",
            variable=self.usar_cache
        )
        chk_cache.grid(row=0, column=0, sticky="w")
        
        chk_paralelo = ttk.Checkbutton(
            processamento_frame,
            text="⚡ Processamento paralelo (mais rápido)",
            variable=self.processamento_paralelo
        )
        chk_paralelo.grid(row=1, column=0, sticky="w")
        
        processamento_frame.grid_columnconfigure(0, weight=1)
        
        # Configurar expansão do frame avançado
        self.avancado_frame.grid_columnconfigure(0, weight=1)
        self.avancado_frame.grid_columnconfigure(1, weight=1)
    
    def _create_output_section(self):
        """Cria a seção de opções de saída."""
        saida_frame = ttk.LabelFrame(self.main_frame, text="📁 Opções de Saída", padding=10)
        saida_frame.grid(row=3, column=0, sticky="ew", pady=10)
        
        # Pasta de destino
        ttk.Label(saida_frame, text="Pasta de Destino:").grid(row=0, column=0, sticky="w")
        
        destino_frame = ttk.Frame(saida_frame)
        destino_frame.grid(row=1, column=0, sticky="ew", pady=(5, 10))
        
        self.entry_destino = ttk.Entry(destino_frame, textvariable=self.destino_var, width=50)
        self.entry_destino.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        btn_procurar_destino = ttk.Button(
            destino_frame,
            text="📂 Procurar",
            command=self._select_destination_folder,
            style="Action.TButton"
        )
        btn_procurar_destino.grid(row=0, column=1)
        
        # Opções adicionais
        chk_backup = ttk.Checkbutton(
            saida_frame,
            text="💾 Criar backup dos arquivos originais",
            variable=self.criar_backup
        )
        chk_backup.grid(row=2, column=0, sticky="w")
        
        chk_sobrescrever = ttk.Checkbutton(
            saida_frame,
            text="⚠️ Sobrescrever arquivos existentes",
            variable=self.sobrescrever
        )
        chk_sobrescrever.grid(row=3, column=0, sticky="w")
        
        # Configurar expansão
        destino_frame.grid_columnconfigure(0, weight=1)
        saida_frame.grid_columnconfigure(0, weight=1)
    
    def _on_preset_changed(self, event=None):
        """Callback para mudança de preset."""
        preset = self.preset_var.get()
        description = self._get_preset_description(preset)
        self.lbl_descricao_preset.config(text=description)
        
        if self.on_config_changed:
            self.on_config_changed()
    
    def _get_preset_description(self, preset: str) -> str:
        """Retorna a descrição do preset."""
        descriptions = {
            "minimal": "🟢 Compressão leve - Mantém alta qualidade visual com redução moderada de tamanho",
            "balanced": "🟡 Compressão equilibrada - Boa relação entre tamanho e qualidade",
            "aggressive": "🔴 Compressão máxima - Reduz drasticamente o tamanho, pode afetar a qualidade"
        }
        return descriptions.get(preset, "Preset personalizado")
    
    def _toggle_advanced_options(self):
        """Mostra/oculta configurações avançadas."""
        if self.mostrar_avancado.get():
            self.avancado_frame.grid(row=2, column=0, sticky="ew", pady=10)
        else:
            self.avancado_frame.grid_remove()
    
    def _update_quality_label(self, value):
        """Atualiza o label da qualidade geral."""
        self.lbl_qualidade.config(text=f"{int(float(value))}%")
        
        if self.on_config_changed:
            self.on_config_changed()
    
    def _update_image_quality_label(self, value):
        """Atualiza o label da qualidade das imagens."""
        self.lbl_qualidade_imagem.config(text=f"{int(float(value))}%")
        
        if self.on_config_changed:
            self.on_config_changed()
    
    def _select_destination_folder(self):
        """Permite selecionar pasta de destino."""
        pasta = filedialog.askdirectory(title="Selecionar Pasta de Destino")
        if pasta:
            self.destino_var.set(pasta)
            
            if self.on_config_changed:
                self.on_config_changed()
    
    def create_compression_config(self) -> CompressionConfig:
        """Cria configuração de compressão baseada nas opções selecionadas."""
        config = CompressionConfig()
        
        if self.mostrar_avancado.get():
            # Configuração personalizada
            if hasattr(config, 'image_config') and hasattr(config.image_config, 'jpeg_quality'):
                config.image_config.jpeg_quality = self.qualidade_imagem_var.get()  # type: ignore
                config.image_config.max_dpi = self.dpi_var.get()  # type: ignore
            
            # Definir nível baseado na qualidade
            qualidade = self.qualidade_var.get()
            if qualidade <= 30:
                if hasattr(config, 'apply_preset'):
                    config.apply_preset(CompressionLevel.AGGRESSIVE)
            elif qualidade <= 70:
                if hasattr(config, 'apply_preset'):
                    config.apply_preset(CompressionLevel.BALANCED)
            else:
                if hasattr(config, 'apply_preset'):
                    config.apply_preset(CompressionLevel.MINIMAL)
        else:
            # Usar preset selecionado
            preset_map = {
                "minimal": CompressionLevel.MINIMAL,
                "balanced": CompressionLevel.BALANCED,
                "aggressive": CompressionLevel.AGGRESSIVE
            }
            preset = preset_map.get(self.preset_var.get(), CompressionLevel.BALANCED)
            config.apply_preset(preset)
        
        return config
    
    def get_destination_folder(self) -> str:
        """Retorna a pasta de destino selecionada."""
        return self.destino_var.get()
    
    def should_create_backup(self) -> bool:
        """Retorna se deve criar backup."""
        return self.criar_backup.get()
    
    def should_overwrite(self) -> bool:
        """Retorna se deve sobrescrever arquivos."""
        return self.sobrescrever.get()
    
    def validate_configuration(self) -> tuple[bool, str]:
        """Valida a configuração atual."""
        # Verificar pasta de destino
        destination = self.get_destination_folder()
        if not destination:
            return False, "Selecione uma pasta de destino."
        
        # Verificar se é possível criar a pasta
        try:
            os.makedirs(destination, exist_ok=True)
        except Exception as e:
            return False, f"Erro ao criar pasta de destino: {e}"
        
        return True, "Configuração válida"
