#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de análise de PDF - CompactPDF
=====================================

Define a estrutura de dados para análise detalhada de arquivos PDF.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import json


@dataclass
class ImageInfo:
    """Informações sobre uma imagem no PDF."""
    page_number: int
    width: int
    height: int
    bits_per_component: int
    color_space: str
    filter_type: str
    estimated_size: int
    compression_potential: float = 0.0


@dataclass
class FontInfo:
    """Informações sobre uma fonte no PDF."""
    name: str
    type: str
    embedded: bool
    subset: bool
    estimated_size: int


@dataclass
class PageInfo:
    """Informações sobre uma página do PDF."""
    page_number: int
    width: float
    height: float
    rotation: int
    has_images: bool
    has_text: bool
    has_forms: bool
    image_count: int
    estimated_size: int


@dataclass
class PDFAnalysis:
    """
    Análise completa de um arquivo PDF.
    
    Contém informações detalhadas sobre estrutura, conteúdo
    e potencial de compressão do arquivo.
    """
    
    # Informações básicas do arquivo
    file_path: str
    file_size: int
    creation_date: Optional[datetime] = None
    modification_date: Optional[datetime] = None
    analysis_date: datetime = field(default_factory=datetime.now)
    
    # Informações do documento
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    pdf_version: Optional[str] = None
    
    # Estrutura do documento
    page_count: int = 0
    pages: List[PageInfo] = field(default_factory=list)
    
    # Análise de conteúdo
    total_images: int = 0
    total_fonts: int = 0
    images: List[ImageInfo] = field(default_factory=list)
    fonts: List[FontInfo] = field(default_factory=list)
    
    # Análise de compressão
    has_compression: bool = False
    compression_filters: List[str] = field(default_factory=list)
    uncompressed_streams: int = 0
    
    # Análise de segurança
    is_encrypted: bool = False
    has_digital_signatures: bool = False
    has_form_fields: bool = False
    
    # Métricas de otimização
    estimated_compression_potential: float = 0.0
    recommended_strategies: List[str] = field(default_factory=list)
    optimization_score: float = 0.0
    
    # Análise detalhada
    object_count: int = 0
    stream_count: int = 0
    font_size_total: int = 0
    image_size_total: int = 0
    metadata_size: int = 0
    
    # Erros e avisos
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    @property
    def file_size_mb(self) -> float:
        """Retorna tamanho do arquivo em MB."""
        return self.file_size / (1024 * 1024)
    
    @property
    def average_page_size(self) -> float:
        """Retorna tamanho médio por página em bytes."""
        return self.file_size / self.page_count if self.page_count > 0 else 0
    
    @property
    def images_per_page(self) -> float:
        """Retorna média de imagens por página."""
        return self.total_images / self.page_count if self.page_count > 0 else 0
    
    @property
    def has_optimization_potential(self) -> bool:
        """Verifica se há potencial significativo de otimização."""
        return self.estimated_compression_potential > 10.0
    
    def get_largest_images(self, limit: int = 5) -> List[ImageInfo]:
        """Retorna as maiores imagens do PDF."""
        return sorted(self.images, key=lambda img: img.estimated_size, reverse=True)[:limit]
    
    def get_embedded_fonts(self) -> List[FontInfo]:
        """Retorna apenas fontes incorporadas."""
        return [font for font in self.fonts if font.embedded]
    
    def get_compression_summary(self) -> Dict[str, Any]:
        """Retorna resumo do potencial de compressão."""
        return {
            "potential_percentage": self.estimated_compression_potential,
            "recommended_strategies": self.recommended_strategies,
            "optimization_score": self.optimization_score,
            "has_uncompressed_content": self.uncompressed_streams > 0,
            "image_optimization_potential": sum(img.compression_potential for img in self.images),
            "font_optimization_potential": len(self.get_embedded_fonts()) > 0
        }
    
    def get_content_breakdown(self) -> Dict[str, int]:
        """Retorna distribuição de tamanho por tipo de conteúdo."""
        other_size = self.file_size - self.image_size_total - self.font_size_total - self.metadata_size
        
        return {
            "images": self.image_size_total,
            "fonts": self.font_size_total,
            "metadata": self.metadata_size,
            "other": max(0, other_size)
        }
    
    def get_quality_issues(self) -> List[str]:
        """Retorna lista de problemas de qualidade encontrados."""
        issues = []
        
        if self.uncompressed_streams > 5:
            issues.append(f"Muitos streams não comprimidos ({self.uncompressed_streams})")
        
        if self.image_size_total > self.file_size * 0.7:
            issues.append("Imagens ocupam mais de 70% do arquivo")
        
        if len(self.get_embedded_fonts()) > 10:
            issues.append("Muitas fontes incorporadas")
        
        if self.optimization_score < 50:
            issues.append("Score de otimização baixo")
        
        return issues
    
    def calculate_optimization_score(self):
        """Calcula score de otimização (0-100)."""
        score = 100.0
        
        # Penalizar por streams não comprimidos
        if self.stream_count > 0:
            uncompressed_ratio = self.uncompressed_streams / self.stream_count
            score -= uncompressed_ratio * 30
        
        # Penalizar por imagens não otimizadas
        if self.total_images > 0:
            high_compression_potential = sum(1 for img in self.images if img.compression_potential > 30)
            if high_compression_potential > 0:
                score -= (high_compression_potential / self.total_images) * 25
        
        # Penalizar por muitas fontes incorporadas
        embedded_fonts = len(self.get_embedded_fonts())
        if embedded_fonts > 5:
            score -= min(20, embedded_fonts * 2)
        
        # Bonificar por já ter compressão
        if self.has_compression:
            score += 10
        
        self.optimization_score = max(0, min(100, score))
    
    def estimate_compression_potential(self):
        """Estima potencial de compressão baseado na análise."""
        potential = 0.0
        
        # Potencial das imagens
        if self.images:
            image_potential = sum(img.compression_potential for img in self.images) / len(self.images)
            image_weight = self.image_size_total / self.file_size if self.file_size > 0 else 0
            potential += image_potential * image_weight
        
        # Potencial dos streams não comprimidos
        if self.stream_count > 0:
            uncompressed_ratio = self.uncompressed_streams / self.stream_count
            potential += uncompressed_ratio * 20  # Até 20% de redução
        
        # Potencial das fontes
        embedded_fonts_size = sum(font.estimated_size for font in self.get_embedded_fonts())
        if self.file_size > 0:
            font_weight = embedded_fonts_size / self.file_size
            potential += font_weight * 15  # Até 15% de redução
        
        self.estimated_compression_potential = min(80.0, potential)  # Máximo 80%
    
    def generate_recommendations(self):
        """Gera recomendações de estratégias baseadas na análise."""
        recommendations = []
        
        # Recomendações baseadas em imagens
        if self.total_images > 0:
            large_images = sum(1 for img in self.images if img.estimated_size > 100000)  # > 100KB
            if large_images > 0:
                recommendations.append("image_compression")
            
            high_res_images = sum(1 for img in self.images if img.width > 1200 or img.height > 1200)
            if high_res_images > 0:
                recommendations.append("image_downsampling")
        
        # Recomendações baseadas em streams
        if self.uncompressed_streams > 0:
            recommendations.append("stream_compression")
        
        # Recomendações baseadas em fontes
        if len(self.get_embedded_fonts()) > 3:
            recommendations.append("font_optimization")
        
        # Recomendações baseadas em metadados
        if self.metadata_size > 50000:  # > 50KB
            recommendations.append("metadata_removal")
        
        # Recomendação geral se score baixo
        if self.optimization_score < 60:
            recommendations.append("general_optimization")
        
        self.recommended_strategies = recommendations
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte análise para dicionário."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, list) and value and hasattr(value[0], '__dict__'):
                # Converter objetos dataclass para dict
                result[key] = [item.__dict__ for item in value]
            else:
                result[key] = value
        return result
    
    def to_json(self) -> str:
        """Converte análise para JSON."""
        return json.dumps(self.to_dict(), default=str, indent=2)
    
    def get_summary_report(self) -> str:
        """Gera relatório resumido legível."""
        report = []
        report.append(f"📄 Análise PDF: {self.file_path}")
        report.append(f"📊 Tamanho: {self.file_size_mb:.2f} MB • Páginas: {self.page_count}")
        report.append(f"🖼️ Imagens: {self.total_images} • Fontes: {self.total_fonts}")
        report.append(f"📈 Potencial de compressão: {self.estimated_compression_potential:.1f}%")
        report.append(f"⭐ Score de otimização: {self.optimization_score:.0f}/100")
        
        if self.recommended_strategies:
            report.append(f"💡 Estratégias recomendadas: {', '.join(self.recommended_strategies)}")
        
        if self.warnings:
            report.append(f"⚠️ Avisos: {len(self.warnings)}")
        
        if self.errors:
            report.append(f"❌ Erros: {len(self.errors)}")
        
        return "\n".join(report)


# Função de conveniência para criar análise básica
def create_basic_analysis(
    file_path: str,
    file_size: int,
    page_count: int = 0
) -> PDFAnalysis:
    """
    Cria uma análise básica de PDF.
    
    Args:
        file_path: Caminho do arquivo
        file_size: Tamanho do arquivo em bytes
        page_count: Número de páginas
    
    Returns:
        PDFAnalysis: Análise básica preenchida
    """
    analysis = PDFAnalysis(
        file_path=file_path,
        file_size=file_size,
        page_count=page_count
    )
    
    # Executar cálculos básicos
    analysis.calculate_optimization_score()
    analysis.estimate_compression_potential()
    analysis.generate_recommendations()
    
    return analysis
