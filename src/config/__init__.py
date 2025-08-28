"""
Configuration classes for PDF compression.
Follows Single Responsibility principle.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class CompressionLevel(Enum):
    """Enumeration for compression levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"


@dataclass
class CompressionConfig:
    """
    Configuration for PDF compression operations.
    Centralizes all compression settings in one place.
    """
    
    # Image compression settings
    image_quality: int = 80  # JPEG quality (1-100)
    resize_images: bool = True
    max_image_width: int = 1200
    max_image_height: int = 1200
    
    # Font optimization settings
    optimize_fonts: bool = True
    subset_fonts: bool = True
    
    # Content optimization settings
    remove_metadata: bool = True
    remove_duplicates: bool = True
    compress_streams: bool = True
    
    # General settings
    compression_level: CompressionLevel = CompressionLevel.MEDIUM
    preserve_bookmarks: bool = True
    preserve_annotations: bool = True
    
    # Quality control
    target_compression_ratio: float = 0.5  # Target 50% compression
    min_quality_threshold: float = 0.8  # Minimum quality threshold
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'image_quality': self.image_quality,
            'resize_images': self.resize_images,
            'max_image_width': self.max_image_width,
            'max_image_height': self.max_image_height,
            'optimize_fonts': self.optimize_fonts,
            'subset_fonts': self.subset_fonts,
            'remove_metadata': self.remove_metadata,
            'remove_duplicates': self.remove_duplicates,
            'compress_streams': self.compress_streams,
            'compression_level': self.compression_level.value,
            'preserve_bookmarks': self.preserve_bookmarks,
            'preserve_annotations': self.preserve_annotations,
            'target_compression_ratio': self.target_compression_ratio,
            'min_quality_threshold': self.min_quality_threshold
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'CompressionConfig':
        """Create configuration from dictionary."""
        # Handle enum conversion
        if 'compression_level' in config_dict:
            config_dict['compression_level'] = CompressionLevel(config_dict['compression_level'])
        
        return cls(**config_dict)
    
    def validate(self) -> bool:
        """
        Validate configuration parameters.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not (1 <= self.image_quality <= 100):
            return False
        
        if not (0.1 <= self.target_compression_ratio <= 0.9):
            return False
        
        if not (0.1 <= self.min_quality_threshold <= 1.0):
            return False
        
        if self.max_image_width <= 0 or self.max_image_height <= 0:
            return False
        
        return True


@dataclass
class PresetConfig:
    """Predefined configuration presets for different use cases."""
    
    @staticmethod
    def web_optimized() -> CompressionConfig:
        """Configuration optimized for web display."""
        return CompressionConfig(
            image_quality=75,
            resize_images=True,
            max_image_width=800,
            max_image_height=800,
            optimize_fonts=True,
            subset_fonts=True,
            remove_metadata=True,
            remove_duplicates=True,
            compress_streams=True,
            compression_level=CompressionLevel.HIGH,
            target_compression_ratio=0.4
        )
    
    @staticmethod
    def print_quality() -> CompressionConfig:
        """Configuration optimized for printing."""
        return CompressionConfig(
            image_quality=90,
            resize_images=False,
            optimize_fonts=True,
            subset_fonts=False,
            remove_metadata=False,
            remove_duplicates=True,
            compress_streams=True,
            compression_level=CompressionLevel.MEDIUM,
            target_compression_ratio=0.7,
            preserve_bookmarks=True,
            preserve_annotations=True
        )
    
    @staticmethod
    def maximum_compression() -> CompressionConfig:
        """Configuration for maximum compression."""
        return CompressionConfig(
            image_quality=60,
            resize_images=True,
            max_image_width=600,
            max_image_height=600,
            optimize_fonts=True,
            subset_fonts=True,
            remove_metadata=True,
            remove_duplicates=True,
            compress_streams=True,
            compression_level=CompressionLevel.MAXIMUM,
            target_compression_ratio=0.3,
            min_quality_threshold=0.6
        )
    
    @staticmethod
    def balanced() -> CompressionConfig:
        """Balanced configuration - default settings."""
        return CompressionConfig()  # Uses default values
