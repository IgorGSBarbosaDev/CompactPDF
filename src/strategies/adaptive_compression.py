"""
Adaptive compression strategy that intelligently selects and configures
compression techniques based on PDF content analysis.
"""

from typing import Any, Dict, List, Tuple
from io import BytesIO
import PyPDF2
from PyPDF2 import PdfReader

from ..interfaces import ICompressionStrategy
from ..utils import ImageQualityAssessor, AdaptiveCompressionOptimizer
from .image_compression import ImageCompressionStrategy
from .font_optimization import FontOptimizationStrategy
from .content_optimization import ContentOptimizationStrategy


class AdaptiveCompressionStrategy(ICompressionStrategy):
    """
    Intelligent compression strategy that adapts to PDF content.
    
    Analyzes PDF characteristics and applies optimal compression techniques
    in the most effective order for maximum compression with quality preservation.
    """
    
    def __init__(self):
        """Initialize adaptive compression strategy."""
        self.image_strategy = ImageCompressionStrategy()
        self.font_strategy = FontOptimizationStrategy()
        self.content_strategy = ContentOptimizationStrategy()
        
        self.quality_assessor = ImageQualityAssessor()
        self.optimizer = AdaptiveCompressionOptimizer()
    
    def compress(self, pdf_data: BytesIO, config: Dict[str, Any]) -> BytesIO:
        """
        Apply adaptive compression based on PDF analysis.
        
        Args:
            pdf_data: PDF data as BytesIO stream
            config: Configuration dictionary
            
        Returns:
            Optimally compressed PDF data
        """
        try:
            # Reset stream position
            pdf_data.seek(0)
            
            # Analyze PDF content
            analysis = self._analyze_pdf_content(pdf_data)
            
            # Determine optimal compression approach
            compression_plan = self._create_compression_plan(analysis, config)
            
            # Apply compression strategies in optimal order
            result_data = pdf_data
            for strategy_info in compression_plan:
                strategy = strategy_info['strategy']
                strategy_config = strategy_info['config']
                
                try:
                    result_data = strategy.compress(result_data, strategy_config)
                except Exception:
                    # Continue with next strategy if one fails
                    continue
            
            return result_data
            
        except Exception as e:
            raise RuntimeError(f"Adaptive compression failed: {str(e)}")
    
    def _analyze_pdf_content(self, pdf_data: BytesIO) -> Dict[str, Any]:
        """
        Analyze PDF content to determine optimal compression approach.
        
        Args:
            pdf_data: PDF data to analyze
            
        Returns:
            Analysis results
        """
        try:
            pdf_data.seek(0)
            reader = PdfReader(pdf_data)
            
            analysis = {
                'page_count': len(reader.pages),
                'has_images': False,
                'image_count': 0,
                'has_fonts': False,
                'font_count': 0,
                'has_metadata': reader.metadata is not None,
                'is_encrypted': reader.is_encrypted,
                'estimated_complexity': 'medium',
                'recommended_strategies': [],
                'content_types': {
                    'text_heavy': False,
                    'image_heavy': False,
                    'mixed_content': False
                }
            }
            
            total_images = 0
            total_fonts = 0
            text_content_pages = 0
            image_content_pages = 0
            
            # Analyze each page
            for page in reader.pages:
                page_has_images = False
                page_has_fonts = False
                
                try:
                    # Check for images
                    if hasattr(page, 'get'):
                        resources = page.get('/Resources')
                        if resources and hasattr(resources, 'get'):
                            xobjects = resources.get('/XObject')
                            if xobjects and hasattr(xobjects, 'keys'):
                                for obj_name in xobjects.keys():
                                    obj = xobjects[obj_name]
                                    if hasattr(obj, 'get') and obj.get('/Subtype') == '/Image':
                                        total_images += 1
                                        page_has_images = True
                    
                    # Check for fonts
                    if hasattr(page, 'get'):
                        resources = page.get('/Resources')
                        if resources and hasattr(resources, 'get'):
                            fonts = resources.get('/Font')
                            if fonts and hasattr(fonts, 'keys'):
                                total_fonts += len(fonts.keys())
                                page_has_fonts = True
                except Exception:
                    # Skip page if analysis fails
                    continue
                
                # Categorize page content
                if page_has_images and not page_has_fonts:
                    image_content_pages += 1
                elif page_has_fonts and not page_has_images:
                    text_content_pages += 1
                elif page_has_images and page_has_fonts:
                    # Mixed content
                    pass
            
            # Update analysis
            analysis['has_images'] = total_images > 0
            analysis['image_count'] = total_images
            analysis['has_fonts'] = total_fonts > 0
            analysis['font_count'] = total_fonts
            
            # Determine content type
            if image_content_pages > text_content_pages:
                analysis['content_types']['image_heavy'] = True
            elif text_content_pages > image_content_pages:
                analysis['content_types']['text_heavy'] = True
            else:
                analysis['content_types']['mixed_content'] = True
            
            # Estimate complexity
            complexity_score = 0
            complexity_score += min(10, analysis['page_count']) / 10 * 0.3  # Page count
            complexity_score += min(50, total_images) / 50 * 0.4  # Image count
            complexity_score += min(20, total_fonts) / 20 * 0.3  # Font count
            
            if complexity_score < 0.3:
                analysis['estimated_complexity'] = 'low'
            elif complexity_score > 0.7:
                analysis['estimated_complexity'] = 'high'
            
            return analysis
            
        except Exception:
            # Return basic analysis if detailed analysis fails
            return {
                'page_count': 1,
                'has_images': True,
                'image_count': 0,
                'has_fonts': True,
                'font_count': 0,
                'has_metadata': True,
                'is_encrypted': False,
                'estimated_complexity': 'medium',
                'recommended_strategies': ['content', 'font', 'image'],
                'content_types': {'mixed_content': True}
            }
    
    def _create_compression_plan(
        self,
        analysis: Dict[str, Any],
        config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Create optimal compression plan based on analysis.
        
        Args:
            analysis: PDF content analysis
            config: Base configuration
            
        Returns:
            List of compression steps with optimized configurations
        """
        plan = []
        
        # Determine strategy order based on content
        if analysis['content_types']['image_heavy']:
            # Image-heavy: prioritize image compression
            strategy_order = ['image', 'content', 'font']
        elif analysis['content_types']['text_heavy']:
            # Text-heavy: prioritize font optimization
            strategy_order = ['font', 'content', 'image']
        else:
            # Mixed content: balanced approach
            strategy_order = ['content', 'image', 'font']
        
        # Create configurations for each strategy
        for strategy_name in strategy_order:
            strategy_config = self._optimize_strategy_config(
                strategy_name, analysis, config
            )
            
            if strategy_name == 'image' and analysis['has_images']:
                plan.append({
                    'strategy': self.image_strategy,
                    'config': strategy_config,
                    'priority': self._calculate_strategy_priority('image', analysis)
                })
            elif strategy_name == 'font' and analysis['has_fonts']:
                plan.append({
                    'strategy': self.font_strategy,
                    'config': strategy_config,
                    'priority': self._calculate_strategy_priority('font', analysis)
                })
            elif strategy_name == 'content':
                plan.append({
                    'strategy': self.content_strategy,
                    'config': strategy_config,
                    'priority': self._calculate_strategy_priority('content', analysis)
                })
        
        # Sort by priority (higher priority first)
        plan.sort(key=lambda x: x['priority'], reverse=True)
        
        return plan
    
    def _optimize_strategy_config(
        self,
        strategy_name: str,
        analysis: Dict[str, Any],
        base_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimize configuration for specific strategy based on analysis.
        
        Args:
            strategy_name: Name of strategy to configure
            analysis: PDF content analysis
            base_config: Base configuration
            
        Returns:
            Optimized configuration for strategy
        """
        config = base_config.copy()
        
        complexity = analysis['estimated_complexity']
        
        if strategy_name == 'image':
            if complexity == 'high' or analysis['image_count'] > 20:
                # High complexity: be more aggressive
                config['image_quality'] = max(60, config.get('image_quality', 80) - 15)
                config['max_image_width'] = min(800, config.get('max_image_width', 1200))
                config['max_image_height'] = min(800, config.get('max_image_height', 1200))
            elif complexity == 'low':
                # Low complexity: maintain quality
                config['image_quality'] = min(90, config.get('image_quality', 80) + 10)
        
        elif strategy_name == 'font':
            if analysis['font_count'] > 10:
                # Many fonts: aggressive optimization
                config['subset_fonts'] = True
                config['optimize_fonts'] = True
            elif analysis['content_types']['text_heavy']:
                # Text-heavy: careful optimization
                config['subset_fonts'] = True
                config['optimize_fonts'] = True
        
        elif strategy_name == 'content':
            if analysis['page_count'] > 50:
                # Large document: aggressive cleanup
                config['remove_duplicates'] = True
                config['compress_streams'] = True
                config['remove_metadata'] = True
            
            if not analysis['has_metadata']:
                config['remove_metadata'] = False
        
        return config
    
    def _calculate_strategy_priority(self, strategy_name: str, analysis: Dict[str, Any]) -> float:
        """
        Calculate priority score for a strategy based on content analysis.
        
        Args:
            strategy_name: Name of strategy
            analysis: PDF content analysis
            
        Returns:
            Priority score (higher = more important)
        """
        base_priority = 5.0
        
        if strategy_name == 'image':
            if analysis['content_types']['image_heavy']:
                base_priority += 3.0
            elif analysis['has_images']:
                base_priority += 1.0
            
            # Bonus for many images
            base_priority += min(2.0, analysis['image_count'] / 10)
        
        elif strategy_name == 'font':
            if analysis['content_types']['text_heavy']:
                base_priority += 3.0
            elif analysis['has_fonts']:
                base_priority += 1.0
            
            # Bonus for many fonts
            base_priority += min(2.0, analysis['font_count'] / 5)
        
        elif strategy_name == 'content':
            # Content optimization is always beneficial
            base_priority += 2.0
            
            # Bonus for large documents
            base_priority += min(2.0, analysis['page_count'] / 25)
        
        return base_priority
    
    def get_strategy_name(self) -> str:
        """Get the name of this compression strategy."""
        return "Adaptive Compression"
    
    def get_analysis_report(self, pdf_data: BytesIO, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed analysis report for a PDF.
        
        Args:
            pdf_data: PDF data to analyze
            config: Configuration to use
            
        Returns:
            Detailed analysis and recommendations
        """
        try:
            analysis = self._analyze_pdf_content(pdf_data)
            plan = self._create_compression_plan(analysis, config)
            
            report = {
                'content_analysis': analysis,
                'compression_plan': [
                    {
                        'strategy': step['strategy'].get_strategy_name(),
                        'priority': step['priority'],
                        'config_adjustments': self._get_config_differences(config, step['config'])
                    }
                    for step in plan
                ],
                'recommendations': self._generate_strategy_recommendations(analysis),
                'expected_effectiveness': self._estimate_compression_effectiveness(analysis, config)
            }
            
            return report
            
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    def _get_config_differences(self, base_config: Dict[str, Any], optimized_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get differences between base and optimized configurations."""
        differences = {}
        
        for key, value in optimized_config.items():
            if key not in base_config or base_config[key] != value:
                differences[key] = {
                    'original': base_config.get(key, 'not_set'),
                    'optimized': value
                }
        
        return differences
    
    def _generate_strategy_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations based on analysis."""
        recommendations = []
        
        if analysis['content_types']['image_heavy']:
            recommendations.append("Document is image-heavy - focus on aggressive image compression")
        elif analysis['content_types']['text_heavy']:
            recommendations.append("Document is text-heavy - prioritize font optimization")
        
        if analysis['image_count'] > 30:
            recommendations.append("Many images detected - consider lower image quality settings")
        
        if analysis['font_count'] > 15:
            recommendations.append("Many fonts detected - font subsetting will be very effective")
        
        if analysis['page_count'] > 100:
            recommendations.append("Large document - content optimization will provide significant benefits")
        
        if analysis['estimated_complexity'] == 'high':
            recommendations.append("Complex document detected - use aggressive compression settings")
        
        return recommendations
    
    def _estimate_compression_effectiveness(self, analysis: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate compression effectiveness based on analysis."""
        
        # Base effectiveness scores
        image_effectiveness = 0.3 if analysis['has_images'] else 0.0
        font_effectiveness = 0.2 if analysis['has_fonts'] else 0.0
        content_effectiveness = 0.15  # Always some benefit
        
        # Adjust based on content characteristics
        if analysis['content_types']['image_heavy']:
            image_effectiveness += 0.2
        
        if analysis['content_types']['text_heavy']:
            font_effectiveness += 0.15
        
        if analysis['page_count'] > 50:
            content_effectiveness += 0.1
        
        # Adjust based on configuration aggressiveness
        target_ratio = config.get('target_compression_ratio', 0.5)
        aggressiveness_factor = target_ratio  # Higher target = more aggressive
        
        estimated_ratio = (
            image_effectiveness * aggressiveness_factor +
            font_effectiveness * aggressiveness_factor +
            content_effectiveness * aggressiveness_factor
        )
        
        return {
            'estimated_compression_ratio': min(0.8, estimated_ratio),  # Cap at 80%
            'image_contribution': image_effectiveness * aggressiveness_factor,
            'font_contribution': font_effectiveness * aggressiveness_factor,
            'content_contribution': content_effectiveness * aggressiveness_factor,
            'confidence_level': 'high' if analysis['estimated_complexity'] != 'high' else 'medium'
        }
