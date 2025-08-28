"""
Compression metrics service.
Implements ICompressionMetrics interface.
Follows Single Responsibility principle.
"""

import os
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass

from ..interfaces import ICompressionMetrics, ILogger


@dataclass
class CompressionResult:
    """Data class for compression results."""
    original_size: int
    compressed_size: int
    compression_ratio: float
    time_taken: float
    strategy_used: str
    success: bool
    error_message: Optional[str] = None


class CompressionMetricsService(ICompressionMetrics):
    """
    Service for calculating compression metrics.
    Provides detailed analysis of compression results.
    """
    
    def __init__(self, logger: Optional[ILogger] = None):
        """
        Initialize compression metrics service.
        
        Args:
            logger: Optional logger for operations
        """
        self._logger = logger
        self._start_time: Optional[float] = None
    
    def start_timer(self) -> None:
        """Start timing a compression operation."""
        self._start_time = time.time()
    
    def stop_timer(self) -> float:
        """
        Stop timing and return elapsed time.
        
        Returns:
            Elapsed time in seconds
        """
        if self._start_time is None:
            return 0.0
        
        elapsed = time.time() - self._start_time
        self._start_time = None
        return elapsed
    
    def calculate_compression_ratio(self, original_size: int, compressed_size: int) -> float:
        """
        Calculate compression ratio.
        
        Args:
            original_size: Original file size in bytes
            compressed_size: Compressed file size in bytes
            
        Returns:
            Compression ratio as percentage (0.0 to 1.0)
        """
        if original_size <= 0:
            return 0.0
        
        ratio = 1.0 - (compressed_size / original_size)
        return max(0.0, min(1.0, ratio))  # Clamp between 0 and 1
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes
        """
        try:
            if os.path.exists(file_path):
                return os.path.getsize(file_path)
            return 0
        except Exception:
            return 0
    
    def create_compression_result(
        self,
        original_path: str,
        compressed_path: str,
        strategy_name: str,
        time_taken: float,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> CompressionResult:
        """
        Create a comprehensive compression result.
        
        Args:
            original_path: Path to original file
            compressed_path: Path to compressed file
            strategy_name: Name of compression strategy used
            time_taken: Time taken for compression
            success: Whether compression was successful
            error_message: Error message if compression failed
            
        Returns:
            CompressionResult object
        """
        original_size = self.get_file_size(original_path)
        compressed_size = self.get_file_size(compressed_path) if success else 0
        compression_ratio = self.calculate_compression_ratio(original_size, compressed_size)
        
        result = CompressionResult(
            original_size=original_size,
            compressed_size=compressed_size,
            compression_ratio=compression_ratio,
            time_taken=time_taken,
            strategy_used=strategy_name,
            success=success,
            error_message=error_message
        )
        
        if self._logger:
            self._log_compression_result(result)
        
        return result
    
    def _log_compression_result(self, result: CompressionResult) -> None:
        """
        Log compression result.
        
        Args:
            result: Compression result to log
        """
        if result.success:
            size_reduction = self._format_file_size(result.original_size - result.compressed_size)
            percentage = result.compression_ratio * 100
            
            message = (
                f"Compression successful - "
                f"Original: {self._format_file_size(result.original_size)}, "
                f"Compressed: {self._format_file_size(result.compressed_size)}, "
                f"Saved: {size_reduction} ({percentage:.1f}%), "
                f"Time: {result.time_taken:.2f}s, "
                f"Strategy: {result.strategy_used}"
            )
            self._logger.log_info(message)
        else:
            message = (
                f"Compression failed - "
                f"Strategy: {result.strategy_used}, "
                f"Time: {result.time_taken:.2f}s, "
                f"Error: {result.error_message or 'Unknown error'}"
            )
            self._logger.log_error(message)
    
    def _format_file_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string
        """
        if size_bytes == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1
        
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.1f} {units[unit_index]}"
    
    def analyze_compression_effectiveness(
        self,
        result: CompressionResult,
        target_ratio: float = 0.5
    ) -> Dict[str, Any]:
        """
        Analyze the effectiveness of compression.
        
        Args:
            result: Compression result to analyze
            target_ratio: Target compression ratio
            
        Returns:
            Analysis dictionary
        """
        analysis = {
            'met_target': result.compression_ratio >= target_ratio,
            'ratio_difference': result.compression_ratio - target_ratio,
            'effectiveness_score': min(1.0, result.compression_ratio / target_ratio),
            'speed_category': self._categorize_speed(result.time_taken, result.original_size),
            'size_category': self._categorize_size(result.original_size),
            'recommendation': self._get_recommendation(result, target_ratio)
        }
        
        return analysis
    
    def _categorize_speed(self, time_taken: float, file_size: int) -> str:
        """Categorize compression speed."""
        if file_size == 0:
            return "unknown"
        
        # MB per second
        speed = (file_size / (1024 * 1024)) / max(time_taken, 0.001)
        
        if speed > 10:
            return "fast"
        elif speed > 2:
            return "moderate"
        else:
            return "slow"
    
    def _categorize_size(self, file_size: int) -> str:
        """Categorize file size."""
        mb_size = file_size / (1024 * 1024)
        
        if mb_size < 1:
            return "small"
        elif mb_size < 10:
            return "medium"
        elif mb_size < 100:
            return "large"
        else:
            return "very_large"
    
    def _get_recommendation(self, result: CompressionResult, target_ratio: float) -> str:
        """Get recommendation based on compression result."""
        if not result.success:
            return "Try a different compression strategy or check file integrity"
        
        if result.compression_ratio >= target_ratio:
            return "Compression target achieved successfully"
        elif result.compression_ratio >= target_ratio * 0.8:
            return "Close to target - consider adjusting compression settings"
        else:
            return "Poor compression - try maximum compression settings or different strategy"
