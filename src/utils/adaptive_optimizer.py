"""
Adaptive compression optimizer for intelligent PDF compression.
"""

from typing import Any, Dict, List, Tuple, Optional
import math
from dataclasses import dataclass


@dataclass
class CompressionProfile:
    """Profile defining compression characteristics for different use cases."""
    
    name: str
    description: str
    target_ratio: float
    quality_threshold: float
    aggressiveness: float
    preserve_metadata: bool
    settings: Dict[str, Any]


class AdaptiveCompressionOptimizer:
    """
    Intelligent optimizer that adapts compression parameters based on
    PDF characteristics and user requirements.
    """
    
    def __init__(self):
        """Initialize the adaptive compression optimizer."""
        self.profiles = self._create_compression_profiles()
        self.performance_history = []
    
    def _create_compression_profiles(self) -> Dict[str, CompressionProfile]:
        """Create predefined compression profiles."""
        return {
            'maximum_compression': CompressionProfile(
                name='Maximum Compression',
                description='Achieve maximum compression ratio, accept quality loss',
                target_ratio=0.3,
                quality_threshold=0.6,
                aggressiveness=1.0,
                preserve_metadata=False,
                settings={
                    'image_quality': 50,
                    'max_image_width': 600,
                    'max_image_height': 600,
                    'aggressive_font_subset': True,
                    'remove_unused_objects': True,
                    'compress_streams': True,
                    'remove_metadata': True
                }
            ),
            'balanced': CompressionProfile(
                name='Balanced',
                description='Balance between compression and quality',
                target_ratio=0.5,
                quality_threshold=0.75,
                aggressiveness=0.7,
                preserve_metadata=True,
                settings={
                    'image_quality': 70,
                    'max_image_width': 1000,
                    'max_image_height': 1000,
                    'aggressive_font_subset': False,
                    'remove_unused_objects': True,
                    'compress_streams': True,
                    'remove_metadata': False
                }
            ),
            'quality_preserving': CompressionProfile(
                name='Quality Preserving',
                description='Minimal quality loss, moderate compression',
                target_ratio=0.7,
                quality_threshold=0.9,
                aggressiveness=0.4,
                preserve_metadata=True,
                settings={
                    'image_quality': 85,
                    'max_image_width': 1500,
                    'max_image_height': 1500,
                    'aggressive_font_subset': False,
                    'remove_unused_objects': False,
                    'compress_streams': True,
                    'remove_metadata': False
                }
            ),
            'web_optimized': CompressionProfile(
                name='Web Optimized',
                description='Optimized for web viewing and downloading',
                target_ratio=0.4,
                quality_threshold=0.8,
                aggressiveness=0.8,
                preserve_metadata=False,
                settings={
                    'image_quality': 65,
                    'max_image_width': 800,
                    'max_image_height': 800,
                    'aggressive_font_subset': True,
                    'remove_unused_objects': True,
                    'compress_streams': True,
                    'remove_metadata': True,
                    'optimize_for_web': True
                }
            ),
            'print_ready': CompressionProfile(
                name='Print Ready',
                description='Optimized for printing while reducing file size',
                target_ratio=0.6,
                quality_threshold=0.85,
                aggressiveness=0.5,
                preserve_metadata=True,
                settings={
                    'image_quality': 80,
                    'max_image_width': 2000,
                    'max_image_height': 2000,
                    'aggressive_font_subset': False,
                    'remove_unused_objects': True,
                    'compress_streams': True,
                    'remove_metadata': False,
                    'preserve_print_quality': True
                }
            )
        }
    
    def select_optimal_profile(
        self,
        analysis: Dict[str, Any],
        user_requirements: Optional[Dict[str, Any]] = None
    ) -> CompressionProfile:
        """
        Select the most appropriate compression profile based on analysis and requirements.
        
        Args:
            analysis: PDF content analysis results
            user_requirements: User-specified requirements
            
        Returns:
            Optimal compression profile
        """
        if user_requirements is None:
            user_requirements = {}
        
        # Start with balanced profile as default
        profile_scores = {}
        
        for name, profile in self.profiles.items():
            score = self._calculate_profile_score(profile, analysis, user_requirements)
            profile_scores[name] = score
        
        # Select profile with highest score
        if profile_scores:
            best_profile_name = max(profile_scores.keys(), key=lambda k: profile_scores[k])
            return self.profiles[best_profile_name]
        else:
            return self.profiles['balanced']
    
    def _calculate_profile_score(
        self,
        profile: CompressionProfile,
        analysis: Dict[str, Any],
        user_requirements: Dict[str, Any]
    ) -> float:
        """Calculate how well a profile matches the requirements."""
        score = 0.0
        
        # Content type matching
        if analysis.get('content_types', {}).get('image_heavy') and 'web' in profile.name.lower():
            score += 2.0
        elif analysis.get('content_types', {}).get('text_heavy') and 'print' in profile.name.lower():
            score += 2.0
        
        # Size requirements
        if user_requirements.get('target_compression_ratio'):
            target = user_requirements['target_compression_ratio']
            ratio_diff = abs(profile.target_ratio - target)
            score += max(0, 2.0 - ratio_diff * 4)
        
        # Quality requirements
        if user_requirements.get('minimum_quality'):
            min_quality = user_requirements['minimum_quality']
            if profile.quality_threshold >= min_quality:
                score += 1.5
            else:
                score -= 2.0  # Penalty for not meeting quality requirements
        
        # Use case specific scoring
        use_case = user_requirements.get('use_case', '').lower()
        if use_case:
            if 'web' in use_case and 'web' in profile.name.lower():
                score += 3.0
            elif 'print' in use_case and 'print' in profile.name.lower():
                score += 3.0
            elif 'archive' in use_case and 'quality' in profile.name.lower():
                score += 3.0
            elif 'email' in use_case and 'maximum' in profile.name.lower():
                score += 3.0
        
        # Document complexity adjustment
        complexity = analysis.get('estimated_complexity', 'medium')
        if complexity == 'high' and profile.aggressiveness > 0.7:
            score += 1.0
        elif complexity == 'low' and profile.aggressiveness < 0.5:
            score += 1.0
        
        return score
    
    def optimize_configuration(
        self,
        base_config: Dict[str, Any],
        analysis: Dict[str, Any],
        profile: CompressionProfile
    ) -> Dict[str, Any]:
        """
        Optimize configuration based on profile and analysis.
        
        Args:
            base_config: Base configuration
            analysis: PDF content analysis
            profile: Selected compression profile
            
        Returns:
            Optimized configuration
        """
        optimized = base_config.copy()
        
        # Apply profile settings
        optimized.update(profile.settings)
        
        # Fine-tune based on specific analysis
        optimized = self._apply_content_specific_optimizations(
            optimized, analysis, profile
        )
        
        # Apply learned optimizations from history
        optimized = self._apply_historical_optimizations(
            optimized, analysis, profile
        )
        
        return optimized
    
    def _apply_content_specific_optimizations(
        self,
        config: Dict[str, Any],
        analysis: Dict[str, Any],
        profile: CompressionProfile
    ) -> Dict[str, Any]:
        """Apply optimizations based on specific content characteristics."""
        
        # Image-heavy documents
        if analysis.get('content_types', {}).get('image_heavy'):
            if analysis.get('image_count', 0) > 50:
                # Many images: be more aggressive with image compression
                config['image_quality'] = max(30, config.get('image_quality', 70) - 15)
                config['max_image_width'] = min(600, config.get('max_image_width', 1000))
                config['max_image_height'] = min(600, config.get('max_image_height', 1000))
        
        # Text-heavy documents
        elif analysis.get('content_types', {}).get('text_heavy'):
            if analysis.get('font_count', 0) > 20:
                # Many fonts: aggressive font optimization
                config['aggressive_font_subset'] = True
                config['merge_similar_fonts'] = True
        
        # Large documents
        if analysis.get('page_count', 0) > 100:
            config['remove_unused_objects'] = True
            config['compress_streams'] = True
            if not profile.preserve_metadata:
                config['remove_metadata'] = True
        
        # Complex documents
        if analysis.get('estimated_complexity') == 'high':
            # Increase aggressiveness for complex documents
            aggressiveness_boost = 0.1
            
            if 'image_quality' in config:
                config['image_quality'] = max(30, int(config['image_quality'] * (1 - aggressiveness_boost)))
            
            config['remove_unused_objects'] = True
            config['compress_streams'] = True
        
        return config
    
    def _apply_historical_optimizations(
        self,
        config: Dict[str, Any],
        analysis: Dict[str, Any],
        profile: CompressionProfile
    ) -> Dict[str, Any]:
        """Apply optimizations learned from historical performance."""
        
        if not self.performance_history:
            return config
        
        # Find similar documents in history
        similar_docs = self._find_similar_documents(analysis)
        
        if similar_docs:
            # Learn from successful optimizations
            successful_configs = [
                entry['config'] for entry in similar_docs
                if entry['success_ratio'] > 0.8
            ]
            
            if successful_configs:
                # Apply most successful settings
                config = self._merge_successful_settings(config, successful_configs)
        
        return config
    
    def _find_similar_documents(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find similar documents in performance history."""
        similar = []
        
        for entry in self.performance_history:
            similarity = self._calculate_document_similarity(
                analysis, entry['analysis']
            )
            
            if similarity > 0.7:  # 70% similarity threshold
                entry['similarity'] = similarity
                similar.append(entry)
        
        return sorted(similar, key=lambda x: x['similarity'], reverse=True)[:5]
    
    def _calculate_document_similarity(
        self,
        analysis1: Dict[str, Any],
        analysis2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between two document analyses."""
        
        similarity = 0.0
        factors = 0
        
        # Page count similarity
        pages1 = analysis1.get('page_count', 0)
        pages2 = analysis2.get('page_count', 0)
        if pages1 > 0 and pages2 > 0:
            page_sim = 1 - abs(pages1 - pages2) / max(pages1, pages2)
            similarity += page_sim * 0.2
            factors += 0.2
        
        # Image count similarity
        images1 = analysis1.get('image_count', 0)
        images2 = analysis2.get('image_count', 0)
        if images1 > 0 or images2 > 0:
            max_images = max(images1, images2, 1)
            image_sim = 1 - abs(images1 - images2) / max_images
            similarity += image_sim * 0.3
            factors += 0.3
        
        # Font count similarity
        fonts1 = analysis1.get('font_count', 0)
        fonts2 = analysis2.get('font_count', 0)
        if fonts1 > 0 or fonts2 > 0:
            max_fonts = max(fonts1, fonts2, 1)
            font_sim = 1 - abs(fonts1 - fonts2) / max_fonts
            similarity += font_sim * 0.2
            factors += 0.2
        
        # Content type similarity
        content1 = analysis1.get('content_types', {})
        content2 = analysis2.get('content_types', {})
        
        content_match = 0
        for key in ['text_heavy', 'image_heavy', 'mixed_content']:
            if content1.get(key) == content2.get(key):
                content_match += 1
        
        content_sim = content_match / 3
        similarity += content_sim * 0.3
        factors += 0.3
        
        return similarity / max(factors, 1) if factors > 0 else 0
    
    def _merge_successful_settings(
        self,
        base_config: Dict[str, Any],
        successful_configs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Merge settings from successful configurations."""
        
        if not successful_configs:
            return base_config
        
        merged = base_config.copy()
        
        # For numeric settings, use weighted average
        numeric_settings = ['image_quality', 'max_image_width', 'max_image_height']
        
        for setting in numeric_settings:
            values = [config.get(setting) for config in successful_configs if setting in config and config.get(setting) is not None]
            if values:
                numeric_values = [v for v in values if isinstance(v, (int, float))]
                if numeric_values:
                    merged[setting] = int(sum(numeric_values) / len(numeric_values))
        
        # For boolean settings, use majority vote
        boolean_settings = [
            'aggressive_font_subset', 'remove_unused_objects',
            'compress_streams', 'remove_metadata'
        ]
        
        for setting in boolean_settings:
            votes = [config.get(setting, False) for config in successful_configs if setting in config]
            if votes:
                merged[setting] = sum(votes) > len(votes) / 2
        
        return merged
    
    def record_performance(
        self,
        analysis: Dict[str, Any],
        config: Dict[str, Any],
        result: Dict[str, Any]
    ) -> None:
        """
        Record compression performance for future optimization.
        
        Args:
            analysis: Document analysis used
            config: Configuration used
            result: Compression results
        """
        
        # Calculate success ratio
        target_ratio = config.get('target_compression_ratio', 0.5)
        actual_ratio = result.get('compression_ratio', 1.0)
        quality_score = result.get('quality_score', 0.5)
        
        success_ratio = self._calculate_success_ratio(
            target_ratio, actual_ratio, quality_score
        )
        
        entry = {
            'analysis': analysis,
            'config': config,
            'result': result,
            'success_ratio': success_ratio,
            'timestamp': result.get('timestamp', 0)
        }
        
        self.performance_history.append(entry)
        
        # Keep only recent entries (limit memory usage)
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-500:]
    
    def _calculate_success_ratio(
        self,
        target_ratio: float,
        actual_ratio: float,
        quality_score: float
    ) -> float:
        """Calculate success ratio for a compression operation."""
        
        # Compression effectiveness (how close to target)
        ratio_effectiveness = 1 - abs(target_ratio - actual_ratio) / target_ratio
        ratio_effectiveness = max(0, ratio_effectiveness)
        
        # Quality preservation
        quality_preservation = quality_score
        
        # Combined score (weighted)
        success_ratio = 0.6 * ratio_effectiveness + 0.4 * quality_preservation
        
        return min(1.0, max(0.0, success_ratio))
    
    def get_optimization_recommendations(
        self,
        analysis: Dict[str, Any],
        current_config: Dict[str, Any]
    ) -> List[str]:
        """
        Get specific optimization recommendations.
        
        Args:
            analysis: Document analysis
            current_config: Current configuration
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        # Content-based recommendations
        if analysis.get('content_types', {}).get('image_heavy'):
            if current_config.get('image_quality', 100) > 70:
                recommendations.append(
                    "Consider reducing image quality to 60-70 for better compression on image-heavy documents"
                )
        
        if analysis.get('font_count', 0) > 15:
            if not current_config.get('aggressive_font_subset'):
                recommendations.append(
                    "Enable aggressive font subsetting for documents with many fonts"
                )
        
        if analysis.get('page_count', 0) > 50:
            if not current_config.get('remove_unused_objects'):
                recommendations.append(
                    "Enable removal of unused objects for large documents"
                )
        
        # Historical recommendations
        similar_docs = self._find_similar_documents(analysis)
        if similar_docs:
            best_performing = max(similar_docs, key=lambda x: x['success_ratio'])
            if best_performing['success_ratio'] > 0.9:
                recommendations.append(
                    f"Similar documents achieved {best_performing['success_ratio']:.1%} success with optimized settings"
                )
        
        return recommendations
    
    def estimate_compression_outcome(
        self,
        analysis: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Estimate compression outcome based on analysis and configuration.
        
        Args:
            analysis: Document analysis
            config: Configuration to use
            
        Returns:
            Estimated compression outcome
        """
        
        # Base compression estimates
        image_compression = self._estimate_image_compression(analysis, config)
        font_compression = self._estimate_font_compression(analysis, config)
        content_compression = self._estimate_content_compression(analysis, config)
        
        # Combined estimate
        total_compression = (
            image_compression * 0.5 +
            font_compression * 0.2 +
            content_compression * 0.3
        )
        
        # Quality estimate
        quality_estimate = self._estimate_quality_impact(analysis, config)
        
        # Confidence based on historical data
        confidence = self._calculate_confidence(analysis)
        
        return {
            'estimated_compression_ratio': total_compression,
            'estimated_quality_score': quality_estimate,
            'confidence_level': confidence,
            'component_estimates': {
                'image_compression': image_compression,
                'font_compression': font_compression,
                'content_compression': content_compression
            }
        }
    
    def _estimate_image_compression(self, analysis: Dict[str, Any], config: Dict[str, Any]) -> float:
        """Estimate image compression ratio."""
        if not analysis.get('has_images'):
            return 1.0
        
        image_quality = config.get('image_quality', 80)
        image_count = analysis.get('image_count', 0)
        
        # Base compression based on quality setting
        base_compression = 0.3 + (image_quality / 100) * 0.5
        
        # Adjust for image count
        if image_count > 20:
            base_compression *= 0.8  # More aggressive for many images
        
        return base_compression
    
    def _estimate_font_compression(self, analysis: Dict[str, Any], config: Dict[str, Any]) -> float:
        """Estimate font compression ratio."""
        if not analysis.get('has_fonts'):
            return 1.0
        
        font_count = analysis.get('font_count', 0)
        aggressive_subset = config.get('aggressive_font_subset', False)
        
        base_compression = 0.7
        
        if aggressive_subset and font_count > 10:
            base_compression = 0.5
        elif font_count > 5:
            base_compression = 0.6
        
        return base_compression
    
    def _estimate_content_compression(self, analysis: Dict[str, Any], config: Dict[str, Any]) -> float:
        """Estimate content compression ratio."""
        page_count = analysis.get('page_count', 1)
        remove_unused = config.get('remove_unused_objects', False)
        compress_streams = config.get('compress_streams', False)
        
        base_compression = 0.8
        
        if remove_unused:
            base_compression *= 0.9
        
        if compress_streams:
            base_compression *= 0.85
        
        # Larger documents often compress better
        if page_count > 50:
            base_compression *= 0.9
        
        return base_compression
    
    def _estimate_quality_impact(self, analysis: Dict[str, Any], config: Dict[str, Any]) -> float:
        """Estimate quality impact of compression."""
        quality_score = 1.0
        
        # Image quality impact
        if analysis.get('has_images'):
            image_quality = config.get('image_quality', 80)
            image_quality_factor = image_quality / 100
            quality_score *= 0.3 + image_quality_factor * 0.7
        
        # Font optimization impact
        if analysis.get('has_fonts') and config.get('aggressive_font_subset'):
            quality_score *= 0.95  # Minimal impact
        
        # Content optimization impact
        if config.get('remove_metadata'):
            quality_score *= 0.98  # Very minimal impact
        
        return min(1.0, quality_score)
    
    def _calculate_confidence(self, analysis: Dict[str, Any]) -> str:
        """Calculate confidence level based on historical data."""
        similar_count = len(self._find_similar_documents(analysis))
        
        if similar_count >= 10:
            return 'high'
        elif similar_count >= 5:
            return 'medium'
        else:
            return 'low'
