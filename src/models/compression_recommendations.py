#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de recomendações de compressão - CompactPDF
==================================================

Define a estrutura de dados para recomendações de estratégias de compressão.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import json


class StrategyPriority(Enum):
    """Prioridade das estratégias de compressão."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CompressionImpact(Enum):
    """Impacto esperado da compressão."""
    MINIMAL = "minimal"     # < 5%
    LOW = "low"            # 5-15%
    MODERATE = "moderate"  # 15-30%
    HIGH = "high"          # 30-50%
    EXTREME = "extreme"    # > 50%


@dataclass
class StrategyRecommendation:
    """Recomendação individual de estratégia."""
    
    name: str
    description: str
    priority: StrategyPriority
    expected_reduction: float  # Porcentagem
    expected_impact: CompressionImpact
    processing_time_estimate: float  # Segundos
    quality_impact: str  # "none", "minimal", "moderate", "high"
    
    # Condições para aplicação
    requires_images: bool = False
    requires_fonts: bool = False
    requires_metadata: bool = False
    min_file_size_mb: float = 0.0
    
    # Parâmetros específicos
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Conflitos e dependências
    conflicts_with: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    
    @property
    def risk_level(self) -> str:
        """Calcula nível de risco baseado no impacto na qualidade."""
        if self.quality_impact == "none":
            return "safe"
        elif self.quality_impact == "minimal":
            return "low"
        elif self.quality_impact == "moderate":
            return "medium"
        else:
            return "high"
    
    def is_applicable_to_file(self, file_size_mb: float, has_images: bool, 
                             has_fonts: bool, has_metadata: bool) -> bool:
        """Verifica se a estratégia é aplicável ao arquivo."""
        if file_size_mb < self.min_file_size_mb:
            return False
        
        if self.requires_images and not has_images:
            return False
        
        if self.requires_fonts and not has_fonts:
            return False
        
        if self.requires_metadata and not has_metadata:
            return False
        
        return True


@dataclass
class CompressionRecommendations:
    """
    Conjunto completo de recomendações de compressão para um PDF.
    
    Analisa o arquivo e sugere estratégias otimizadas baseadas
    no conteúdo e características específicas.
    """
    
    # Informações do arquivo analisado
    file_path: str
    file_size_mb: float
    analysis_date: datetime = field(default_factory=datetime.now)
    
    # Características do arquivo
    has_images: bool = False
    has_fonts: bool = False
    has_metadata: bool = False
    has_forms: bool = False
    page_count: int = 0
    
    # Análise de potencial
    estimated_total_reduction: float = 0.0
    confidence_score: float = 0.0
    risk_assessment: str = "low"
    
    # Recomendações organizadas por prioridade
    high_priority: List[StrategyRecommendation] = field(default_factory=list)
    medium_priority: List[StrategyRecommendation] = field(default_factory=list)
    low_priority: List[StrategyRecommendation] = field(default_factory=list)
    
    # Estratégias ordenadas
    recommended_order: List[str] = field(default_factory=list)
    
    # Análise de cenários
    conservative_plan: List[str] = field(default_factory=list)  # Menor risco
    balanced_plan: List[str] = field(default_factory=list)      # Meio termo
    aggressive_plan: List[str] = field(default_factory=list)    # Máxima compressão
    
    # Avisos e limitações
    warnings: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    
    @property
    def all_recommendations(self) -> List[StrategyRecommendation]:
        """Retorna todas as recomendações em uma lista."""
        return self.high_priority + self.medium_priority + self.low_priority
    
    @property
    def total_strategies(self) -> int:
        """Retorna número total de estratégias recomendadas."""
        return len(self.all_recommendations)
    
    def get_recommendations_by_priority(self, priority: StrategyPriority) -> List[StrategyRecommendation]:
        """Retorna recomendações de uma prioridade específica."""
        if priority == StrategyPriority.HIGH:
            return self.high_priority
        elif priority == StrategyPriority.MEDIUM:
            return self.medium_priority
        elif priority == StrategyPriority.LOW:
            return self.low_priority
        else:
            return []
    
    def get_strategies_by_impact(self, min_impact: CompressionImpact) -> List[StrategyRecommendation]:
        """Retorna estratégias com impacto mínimo especificado."""
        impact_order = [CompressionImpact.MINIMAL, CompressionImpact.LOW, 
                       CompressionImpact.MODERATE, CompressionImpact.HIGH, 
                       CompressionImpact.EXTREME]
        
        min_index = impact_order.index(min_impact)
        target_impacts = impact_order[min_index:]
        
        return [rec for rec in self.all_recommendations 
                if rec.expected_impact in target_impacts]
    
    def get_safe_strategies(self) -> List[StrategyRecommendation]:
        """Retorna apenas estratégias seguras (sem impacto na qualidade)."""
        return [rec for rec in self.all_recommendations 
                if rec.quality_impact in ["none", "minimal"]]
    
    def calculate_plan_metrics(self, strategy_names: List[str]) -> Dict[str, float]:
        """Calcula métricas para um plano específico."""
        strategies = [rec for rec in self.all_recommendations 
                     if rec.name in strategy_names]
        
        if not strategies:
            return {"reduction": 0, "time": 0, "risk": 0}
        
        # Redução total (não é simplesmente soma devido a sobreposições)
        total_reduction = sum(rec.expected_reduction for rec in strategies)
        # Aplicar fator de diminuição para múltiplas estratégias
        if len(strategies) > 1:
            total_reduction *= 0.8  # 80% da soma devido a sobreposições
        
        total_time = sum(rec.processing_time_estimate for rec in strategies)
        
        # Calcular risco médio
        risk_values = {"none": 0, "minimal": 1, "moderate": 2, "high": 3}
        avg_risk = sum(risk_values.get(rec.quality_impact, 0) for rec in strategies) / len(strategies)
        
        return {
            "reduction": min(total_reduction, 80.0),  # Máximo 80%
            "time": total_time,
            "risk": avg_risk
        }
    
    def generate_execution_order(self, strategy_names: List[str]) -> List[str]:
        """Gera ordem otimizada de execução das estratégias."""
        strategies = {rec.name: rec for rec in self.all_recommendations 
                     if rec.name in strategy_names}
        
        ordered = []
        remaining = strategy_names.copy()
        
        # Primeiro: estratégias sem dependências
        for name in remaining[:]:
            strategy = strategies[name]
            if not strategy.depends_on or not any(dep in remaining for dep in strategy.depends_on):
                ordered.append(name)
                remaining.remove(name)
        
        # Segundo: por prioridade e impacto
        remaining.sort(key=lambda name: (
            strategies[name].priority.value,
            -strategies[name].expected_reduction
        ))
        
        ordered.extend(remaining)
        return ordered
    
    def validate_plan(self, strategy_names: List[str]) -> Tuple[bool, List[str]]:
        """Valida um plano de compressão e retorna conflitos."""
        strategies = {rec.name: rec for rec in self.all_recommendations 
                     if rec.name in strategy_names}
        
        conflicts = []
        
        for name in strategy_names:
            strategy = strategies[name]
            
            # Verificar conflitos
            for conflict in strategy.conflicts_with:
                if conflict in strategy_names:
                    conflicts.append(f"{name} conflita com {conflict}")
            
            # Verificar dependências
            for dependency in strategy.depends_on:
                if dependency not in strategy_names:
                    conflicts.append(f"{name} requer {dependency}")
        
        return len(conflicts) == 0, conflicts
    
    def get_summary_report(self) -> str:
        """Gera relatório resumido das recomendações."""
        lines = []
        lines.append(f"📋 Recomendações para: {self.file_path}")
        lines.append(f"📊 Arquivo: {self.file_size_mb:.2f} MB • {self.page_count} páginas")
        lines.append(f"🎯 Redução estimada: {self.estimated_total_reduction:.1f}%")
        lines.append(f"🔒 Avaliação de risco: {self.risk_assessment}")
        lines.append(f"⭐ Confiança: {self.confidence_score:.0f}%")
        lines.append("")
        
        lines.append(f"🔥 Alta prioridade: {len(self.high_priority)} estratégias")
        lines.append(f"🟡 Média prioridade: {len(self.medium_priority)} estratégias")
        lines.append(f"🟢 Baixa prioridade: {len(self.low_priority)} estratégias")
        lines.append("")
        
        # Planos recomendados
        if self.conservative_plan:
            cons_metrics = self.calculate_plan_metrics(self.conservative_plan)
            lines.append(f"🛡️ Plano conservador: {cons_metrics['reduction']:.1f}% redução")
        
        if self.balanced_plan:
            bal_metrics = self.calculate_plan_metrics(self.balanced_plan)
            lines.append(f"⚖️ Plano balanceado: {bal_metrics['reduction']:.1f}% redução")
        
        if self.aggressive_plan:
            agg_metrics = self.calculate_plan_metrics(self.aggressive_plan)
            lines.append(f"🚀 Plano agressivo: {agg_metrics['reduction']:.1f}% redução")
        
        if self.warnings:
            lines.append("")
            lines.append("⚠️ Avisos:")
            for warning in self.warnings:
                lines.append(f"  • {warning}")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte recomendações para dicionário."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, list) and value and hasattr(value[0], '__dict__'):
                result[key] = [item.__dict__ for item in value]
            elif isinstance(value, Enum):
                result[key] = value.value
            else:
                result[key] = value
        return result
    
    def to_json(self) -> str:
        """Converte recomendações para JSON."""
        return json.dumps(self.to_dict(), default=str, indent=2)


# Fábrica de recomendações pré-definidas
class RecommendationFactory:
    """Fábrica para criar recomendações padronizadas."""
    
    @staticmethod
    def create_image_compression() -> StrategyRecommendation:
        """Cria recomendação de compressão de imagens."""
        return StrategyRecommendation(
            name="image_compression",
            description="Comprime imagens usando algoritmos eficientes",
            priority=StrategyPriority.HIGH,
            expected_reduction=25.0,
            expected_impact=CompressionImpact.HIGH,
            processing_time_estimate=10.0,
            quality_impact="minimal",
            requires_images=True,
            parameters={
                "quality": 85,
                "method": "JPEG",
                "progressive": True
            }
        )
    
    @staticmethod
    def create_image_downsampling() -> StrategyRecommendation:
        """Cria recomendação de redução de resolução."""
        return StrategyRecommendation(
            name="image_downsampling",
            description="Reduz resolução de imagens mantendo qualidade visual",
            priority=StrategyPriority.MEDIUM,
            expected_reduction=15.0,
            expected_impact=CompressionImpact.MODERATE,
            processing_time_estimate=8.0,
            quality_impact="moderate",
            requires_images=True,
            parameters={
                "max_width": 1200,
                "max_height": 1200,
                "dpi": 150
            }
        )
    
    @staticmethod
    def create_stream_compression() -> StrategyRecommendation:
        """Cria recomendação de compressão de streams."""
        return StrategyRecommendation(
            name="stream_compression",
            description="Comprime streams não comprimidos do PDF",
            priority=StrategyPriority.HIGH,
            expected_reduction=20.0,
            expected_impact=CompressionImpact.MODERATE,
            processing_time_estimate=5.0,
            quality_impact="none",
            parameters={
                "compression_level": 9,
                "method": "flate"
            }
        )
    
    @staticmethod
    def create_font_optimization() -> StrategyRecommendation:
        """Cria recomendação de otimização de fontes."""
        return StrategyRecommendation(
            name="font_optimization",
            description="Remove fontes desnecessárias e otimiza subsets",
            priority=StrategyPriority.MEDIUM,
            expected_reduction=10.0,
            expected_impact=CompressionImpact.LOW,
            processing_time_estimate=3.0,
            quality_impact="none",
            requires_fonts=True,
            parameters={
                "remove_unused": True,
                "optimize_subsets": True
            }
        )
    
    @staticmethod
    def create_metadata_removal() -> StrategyRecommendation:
        """Cria recomendação de remoção de metadados."""
        return StrategyRecommendation(
            name="metadata_removal",
            description="Remove metadados desnecessários do PDF",
            priority=StrategyPriority.LOW,
            expected_reduction=2.0,
            expected_impact=CompressionImpact.MINIMAL,
            processing_time_estimate=1.0,
            quality_impact="none",
            requires_metadata=True,
            parameters={
                "keep_essential": True,
                "remove_comments": True
            }
        )
    
    @staticmethod
    def get_all_standard_recommendations() -> List[StrategyRecommendation]:
        """Retorna todas as recomendações padrão."""
        return [
            RecommendationFactory.create_image_compression(),
            RecommendationFactory.create_image_downsampling(),
            RecommendationFactory.create_stream_compression(),
            RecommendationFactory.create_font_optimization(),
            RecommendationFactory.create_metadata_removal()
        ]


# Função de conveniência para criar recomendações básicas
def create_basic_recommendations(
    file_path: str,
    file_size_mb: float,
    has_images: bool = False,
    has_fonts: bool = False,
    has_metadata: bool = False,
    page_count: int = 0
) -> CompressionRecommendations:
    """
    Cria recomendações básicas baseadas nas características do arquivo.
    
    Args:
        file_path: Caminho do arquivo
        file_size_mb: Tamanho em MB
        has_images: Se tem imagens
        has_fonts: Se tem fontes
        has_metadata: Se tem metadados
        page_count: Número de páginas
    
    Returns:
        CompressionRecommendations: Recomendações geradas
    """
    recommendations = CompressionRecommendations(
        file_path=file_path,
        file_size_mb=file_size_mb,
        has_images=has_images,
        has_fonts=has_fonts,
        has_metadata=has_metadata,
        page_count=page_count
    )
    
    # Adicionar recomendações aplicáveis
    all_strategies = RecommendationFactory.get_all_standard_recommendations()
    
    for strategy in all_strategies:
        if strategy.is_applicable_to_file(file_size_mb, has_images, has_fonts, has_metadata):
            if strategy.priority == StrategyPriority.HIGH:
                recommendations.high_priority.append(strategy)
            elif strategy.priority == StrategyPriority.MEDIUM:
                recommendations.medium_priority.append(strategy)
            else:
                recommendations.low_priority.append(strategy)
    
    # Calcular estimativas
    total_reduction = sum(rec.expected_reduction for rec in recommendations.all_recommendations)
    recommendations.estimated_total_reduction = min(total_reduction * 0.7, 70.0)  # 70% da soma, máx 70%
    
    # Gerar planos
    safe_strategies = [rec.name for rec in recommendations.get_safe_strategies()]
    all_strategy_names = [rec.name for rec in recommendations.all_recommendations]
    
    recommendations.conservative_plan = safe_strategies[:2]  # Apenas 2 mais seguras
    recommendations.balanced_plan = safe_strategies + [rec.name for rec in recommendations.medium_priority][:1]
    recommendations.aggressive_plan = all_strategy_names
    
    # Definir ordem recomendada
    recommendations.recommended_order = recommendations.generate_execution_order(all_strategy_names)
    
    # Avaliar risco e confiança
    avg_quality_impact = sum(1 for rec in recommendations.all_recommendations 
                           if rec.quality_impact in ["moderate", "high"]) / max(1, len(recommendations.all_recommendations))
    
    if avg_quality_impact < 0.3:
        recommendations.risk_assessment = "low"
        recommendations.confidence_score = 85.0
    elif avg_quality_impact < 0.6:
        recommendations.risk_assessment = "medium"
        recommendations.confidence_score = 70.0
    else:
        recommendations.risk_assessment = "high"
        recommendations.confidence_score = 55.0
    
    return recommendations
