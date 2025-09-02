#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Estilos - CompactPDF GUI
=======================================

Responsável por configurar e gerenciar todos os estilos visuais da interface.
Segue o princípio SRP (Single Responsibility Principle).
"""

import tkinter as tk
from tkinter import ttk


class StyleManager:
    """Gerenciador de estilos e temas da interface."""
    
    def __init__(self, root):
        """Inicializa o gerenciador de estilos."""
        self.root = root
        self.style = ttk.Style()
        
        # Configurar tema base
        self._configure_theme()
        
        # Definir estilos personalizados
        self._define_custom_styles()
    
    def _configure_theme(self):
        """Configura o tema base da aplicação."""
        try:
            # Tentar usar tema clam para melhor aparência
            self.style.theme_use('clam')
        except tk.TclError:
            # Fallback para tema padrão
            pass
        
        # Tentar carregar tema do Windows se disponível
        try:
            self.root.tk.call('source', 'azure.tcl')
            self.root.tk.call('set_theme', 'light')
        except tk.TclError:
            pass
    
    def _define_custom_styles(self):
        """Define todos os estilos personalizados."""
        # Estilos para títulos
        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 16, "bold"),
            foreground="#2c3e50",
            background="#f8f9fa"
        )
        
        self.style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10, "bold"),
            foreground="#34495e"
        )
        
        # Estilos para status
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
            "Warning.TLabel",
            foreground="#f39c12",
            font=("Segoe UI", 9, "bold")
        )
        
        self.style.configure(
            "Info.TLabel",
            foreground="#3498db",
            font=("Segoe UI", 9, "bold")
        )
        
        # Estilos para botões
        self.style.configure(
            "Compress.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(20, 10)
        )
        
        self.style.configure(
            "Action.TButton",
            font=("Segoe UI", 9),
            padding=(10, 5)
        )
        
        # Estilos para frames
        self.style.configure(
            "Card.TLabelFrame",
            relief="solid",
            borderwidth=1,
            background="#ffffff"
        )
        
        # Estilos para progress bar
        self.style.configure(
            "Success.Horizontal.TProgressbar",
            background="#27ae60"
        )
        
        self.style.configure(
            "Processing.Horizontal.TProgressbar",
            background="#3498db"
        )
    
    def apply_status_style(self, widget, status_type):
        """Aplica estilo de status a um widget."""
        style_map = {
            'success': 'Success.TLabel',
            'error': 'Error.TLabel',
            'warning': 'Warning.TLabel',
            'info': 'Info.TLabel'
        }
        
        style = style_map.get(status_type, 'TLabel')
        widget.configure(style=style)
    
    def get_color(self, color_name):
        """Retorna cores predefinidas do tema."""
        colors = {
            'primary': '#3498db',
            'success': '#27ae60',
            'error': '#e74c3c',
            'warning': '#f39c12',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#2c3e50',
            'muted': '#7f8c8d'
        }
        return colors.get(color_name, '#000000')
    
    def get_font(self, font_type):
        """Retorna fontes predefinidas."""
        fonts = {
            'title': ("Segoe UI", 16, "bold"),
            'subtitle': ("Segoe UI", 12, "bold"),
            'heading': ("Segoe UI", 11, "bold"),
            'body': ("Segoe UI", 9),
            'small': ("Segoe UI", 8),
            'button': ("Segoe UI", 10)
        }
        return fonts.get(font_type, ("Segoe UI", 9))
