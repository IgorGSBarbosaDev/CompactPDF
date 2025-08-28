"""
Advanced image quality assessment for PDF compression.
Provides quality metrics and validation for compressed images.
"""

import math
from typing import Tuple, Dict, Any, Optional
from PIL import Image
import numpy as np
from io import BytesIO


class ImageQualityAssessor:
    """
    Advanced image quality assessment for PDF compression.
    Provides multiple quality metrics to ensure compression meets standards.
    """
    
    def __init__(self, min_quality_threshold: float = 0.8):
        """
        Initialize quality assessor.
        
        Args:
            min_quality_threshold: Minimum acceptable quality score (0-1)
        """
        self.min_quality_threshold = min_quality_threshold
    
    def calculate_psnr(self, original: Image.Image, compressed: Image.Image) -> float:
        """
        Calculate Peak Signal-to-Noise Ratio (PSNR) between images.
        
        Args:
            original: Original image
            compressed: Compressed image
            
        Returns:
            PSNR value in dB (higher is better)
        """
        try:
            # Ensure images are same size
            if original.size != compressed.size:
                compressed = compressed.resize(original.size, Image.Resampling.LANCZOS)
            
            # Convert to numpy arrays
            orig_array = np.array(original.convert('RGB'))
            comp_array = np.array(compressed.convert('RGB'))
            
            # Calculate MSE
            mse = np.mean((orig_array - comp_array) ** 2)
            
            if mse == 0:
                return float('inf')  # Perfect match
            
            # Calculate PSNR
            max_pixel_value = 255.0
            psnr = 20 * math.log10(max_pixel_value / math.sqrt(mse))
            
            return psnr
            
        except Exception:
            return 0.0  # Return 0 if calculation fails
    
    def calculate_ssim(self, original: Image.Image, compressed: Image.Image) -> float:
        """
        Calculate Structural Similarity Index (SSIM) between images.
        Simplified version without requiring scikit-image.
        
        Args:
            original: Original image
            compressed: Compressed image
            
        Returns:
            SSIM value (0-1, higher is better)
        """
        try:
            # Ensure images are same size
            if original.size != compressed.size:
                compressed = compressed.resize(original.size, Image.Resampling.LANCZOS)
            
            # Convert to grayscale arrays
            orig_gray = np.array(original.convert('L'))
            comp_gray = np.array(compressed.convert('L'))
            
            # Calculate means
            mu1 = np.mean(orig_gray)
            mu2 = np.mean(comp_gray)
            
            # Calculate variances
            var1 = np.var(orig_gray)
            var2 = np.var(comp_gray)
            
            # Calculate covariance
            covar = np.mean((orig_gray - mu1) * (comp_gray - mu2))
            
            # SSIM constants
            c1 = (0.01 * 255) ** 2
            c2 = (0.03 * 255) ** 2
            
            # Calculate SSIM
            numerator = (2 * mu1 * mu2 + c1) * (2 * covar + c2)
            denominator = (mu1**2 + mu2**2 + c1) * (var1 + var2 + c2)
            
            ssim = numerator / denominator if denominator != 0 else 0
            
            return max(0, min(1, ssim))  # Clamp to [0, 1]
            
        except Exception:
            return 0.0
    
    def calculate_file_size_ratio(self, original_size: int, compressed_size: int) -> float:
        """
        Calculate file size reduction ratio.
        
        Args:
            original_size: Original file size in bytes
            compressed_size: Compressed file size in bytes
            
        Returns:
            Size reduction ratio (0-1, higher means more compression)
        """
        if original_size <= 0:
            return 0.0
        
        return max(0, min(1, 1 - (compressed_size / original_size)))
    
    def assess_compression_quality(
        self,
        original_image: Image.Image,
        compressed_image: Image.Image,
        original_size: int,
        compressed_size: int
    ) -> Dict[str, Any]:
        """
        Comprehensive quality assessment of image compression.
        
        Args:
            original_image: Original image
            compressed_image: Compressed image
            original_size: Original file size in bytes
            compressed_size: Compressed file size in bytes
            
        Returns:
            Dictionary with quality metrics and assessment
        """
        # Calculate quality metrics
        psnr = self.calculate_psnr(original_image, compressed_image)
        ssim = self.calculate_ssim(original_image, compressed_image)
        size_ratio = self.calculate_file_size_ratio(original_size, compressed_size)
        
        # Overall quality score (weighted average)
        quality_score = (
            0.4 * min(1.0, psnr / 30.0) +  # PSNR normalized (30dB = good quality)
            0.4 * ssim +                    # SSIM (0-1)
            0.2 * min(1.0, size_ratio * 2)  # Size reduction bonus
        )
        
        # Quality assessment
        if quality_score >= self.min_quality_threshold:
            quality_level = "Excellent" if quality_score >= 0.9 else "Good"
            meets_standard = True
        else:
            quality_level = "Poor" if quality_score < 0.5 else "Fair"
            meets_standard = False
        
        return {
            'psnr': psnr,
            'ssim': ssim,
            'size_reduction_ratio': size_ratio,
            'quality_score': quality_score,
            'quality_level': quality_level,
            'meets_standard': meets_standard,
            'recommendations': self._get_recommendations(psnr, ssim, size_ratio)
        }
    
    def _get_recommendations(self, psnr: float, ssim: float, size_ratio: float) -> list:
        """Get recommendations based on quality metrics."""
        recommendations = []
        
        if psnr < 25:
            recommendations.append("Consider increasing image quality setting")
        
        if ssim < 0.7:
            recommendations.append("Structural quality is low - reduce compression level")
        
        if size_ratio < 0.1:
            recommendations.append("Very low compression achieved - try more aggressive settings")
        elif size_ratio > 0.8:
            recommendations.append("Very high compression - check if quality is acceptable")
        
        if not recommendations:
            recommendations.append("Compression quality is optimal")
        
        return recommendations


class AdaptiveCompressionOptimizer:
    """
    Automatically optimizes compression settings based on image characteristics.
    """
    
    def __init__(self, quality_assessor: Optional[ImageQualityAssessor] = None):
        """
        Initialize adaptive optimizer.
        
        Args:
            quality_assessor: Quality assessment tool
        """
        self.quality_assessor = quality_assessor or ImageQualityAssessor()
    
    def analyze_image_characteristics(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze image characteristics to determine optimal compression settings.
        
        Args:
            image: Image to analyze
            
        Returns:
            Dictionary with image characteristics
        """
        try:
            # Convert to arrays for analysis
            img_array = np.array(image.convert('RGB'))
            
            # Calculate characteristics
            characteristics = {
                'width': image.width,
                'height': image.height,
                'total_pixels': image.width * image.height,
                'aspect_ratio': image.width / image.height,
                'color_channels': len(img_array.shape),
                'has_transparency': image.mode in ('RGBA', 'LA', 'P'),
                'color_complexity': self._calculate_color_complexity(img_array),
                'edge_density': self._calculate_edge_density(img_array),
                'compression_difficulty': 'unknown'
            }
            
            # Determine compression difficulty
            if characteristics['color_complexity'] > 0.7 or characteristics['edge_density'] > 0.8:
                characteristics['compression_difficulty'] = 'high'
            elif characteristics['color_complexity'] < 0.3 and characteristics['edge_density'] < 0.4:
                characteristics['compression_difficulty'] = 'low'
            else:
                characteristics['compression_difficulty'] = 'medium'
            
            return characteristics
            
        except Exception:
            return {
                'width': image.width,
                'height': image.height,
                'compression_difficulty': 'unknown'
            }
    
    def _calculate_color_complexity(self, img_array: np.ndarray) -> float:
        """Calculate color complexity of image (0-1)."""
        try:
            # Calculate number of unique colors relative to total pixels
            reshaped = img_array.reshape(-1, img_array.shape[-1])
            unique_colors = len(np.unique(reshaped.view(np.void), axis=0))
            total_pixels = reshaped.shape[0]
            
            complexity = min(1.0, unique_colors / (total_pixels * 0.1))
            return complexity
        except Exception:
            return 0.5  # Default medium complexity
    
    def _calculate_edge_density(self, img_array: np.ndarray) -> float:
        """Calculate edge density of image (0-1)."""
        try:
            # Simple edge detection using gradient
            gray = np.mean(img_array, axis=2) if len(img_array.shape) == 3 else img_array
            
            # Calculate gradients
            grad_x = np.abs(np.diff(gray, axis=1))
            grad_y = np.abs(np.diff(gray, axis=0))
            
            # Edge strength
            edge_strength = np.mean(grad_x) + np.mean(grad_y)
            
            # Normalize to 0-1 range
            edge_density = min(1.0, edge_strength / 50.0)  # 50 is empirical threshold
            return edge_density
        except Exception:
            return 0.5  # Default medium edge density
    
    def optimize_compression_settings(
        self,
        image: Image.Image,
        target_compression: float = 0.5,
        quality_threshold: float = 0.8
    ) -> Dict[str, Any]:
        """
        Optimize compression settings based on image characteristics.
        
        Args:
            image: Image to optimize for
            target_compression: Target compression ratio (0-1)
            quality_threshold: Minimum quality threshold (0-1)
            
        Returns:
            Optimized compression settings
        """
        characteristics = self.analyze_image_characteristics(image)
        difficulty = characteristics.get('compression_difficulty', 'medium')
        
        # Base settings
        settings = {
            'image_quality': 80,
            'resize_images': True,
            'max_image_width': 1200,
            'max_image_height': 1200
        }
        
        # Adjust based on difficulty
        if difficulty == 'low':
            # Easy to compress - can be more aggressive
            settings['image_quality'] = max(60, int(80 - (target_compression * 30)))
            settings['max_image_width'] = int(1200 * (1 - target_compression * 0.3))
            settings['max_image_height'] = int(1200 * (1 - target_compression * 0.3))
        
        elif difficulty == 'high':
            # Hard to compress - be more conservative
            settings['image_quality'] = max(70, int(80 - (target_compression * 15)))
            settings['max_image_width'] = int(1200 * (1 - target_compression * 0.15))
            settings['max_image_height'] = int(1200 * (1 - target_compression * 0.15))
        
        else:  # medium
            # Standard settings with moderate adjustment
            settings['image_quality'] = max(65, int(80 - (target_compression * 20)))
            settings['max_image_width'] = int(1200 * (1 - target_compression * 0.2))
            settings['max_image_height'] = int(1200 * (1 - target_compression * 0.2))
        
        # Adjust for very large images
        total_pixels = characteristics.get('total_pixels', 0)
        if total_pixels > 2000000:  # > 2MP
            settings['max_image_width'] = min(settings['max_image_width'], 1000)
            settings['max_image_height'] = min(settings['max_image_height'], 1000)
        
        # Quality adjustments
        if quality_threshold > 0.9:
            settings['image_quality'] = min(95, settings['image_quality'] + 10)
        
        settings['optimization_info'] = {
            'difficulty': difficulty,
            'characteristics': characteristics,
            'reasoning': f"Optimized for {difficulty} compression difficulty with {target_compression:.0%} target"
        }
        
        return settings
