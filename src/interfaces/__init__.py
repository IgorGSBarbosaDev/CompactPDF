"""
Interface definitions following SOLID principles.
These interfaces define contracts for PDF compression components.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from io import BytesIO


class ICompressionStrategy(ABC):
    """
    Interface for compression strategies (Strategy Pattern).
    Follows Single Responsibility and Open/Closed principles.
    """
    
    @abstractmethod
    def compress(self, pdf_data: BytesIO, config: Dict[str, Any]) -> BytesIO:
        """
        Compress PDF data according to specific strategy.
        
        Args:
            pdf_data: PDF data as BytesIO stream
            config: Configuration dictionary for compression
            
        Returns:
            Compressed PDF data as BytesIO stream
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of this compression strategy."""
        pass


class IPDFReader(ABC):
    """
    Interface for PDF reading operations.
    Separates reading concerns from compression logic.
    """
    
    @abstractmethod
    def read_pdf(self, file_path: str) -> BytesIO:
        """
        Read PDF file and return as BytesIO stream.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            PDF data as BytesIO stream
        """
        pass
    
    @abstractmethod
    def validate_pdf(self, file_path: str) -> bool:
        """
        Validate if the file is a valid PDF.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            True if valid PDF, False otherwise
        """
        pass


class IPDFWriter(ABC):
    """
    Interface for PDF writing operations.
    Separates writing concerns from compression logic.
    """
    
    @abstractmethod
    def write_pdf(self, pdf_data: BytesIO, output_path: str) -> bool:
        """
        Write PDF data to file.
        
        Args:
            pdf_data: PDF data as BytesIO stream
            output_path: Path where to write the PDF
            
        Returns:
            True if successful, False otherwise
        """
        pass


class IProgressTracker(ABC):
    """
    Interface for tracking compression progress.
    Allows different progress tracking implementations.
    """
    
    @abstractmethod
    def start_progress(self, total_steps: int) -> None:
        """
        Start progress tracking.
        
        Args:
            total_steps: Total number of steps in the process
        """
        pass
    
    @abstractmethod
    def update_progress(self, current_step: int, message: Optional[str] = None) -> None:
        """
        Update progress.
        
        Args:
            current_step: Current step number
            message: Optional progress message
        """
        pass
    
    @abstractmethod
    def finish_progress(self) -> None:
        """Finish progress tracking."""
        pass


class ICompressionMetrics(ABC):
    """
    Interface for compression metrics calculation.
    Follows Single Responsibility principle.
    """
    
    @abstractmethod
    def calculate_compression_ratio(self, original_size: int, compressed_size: int) -> float:
        """
        Calculate compression ratio.
        
        Args:
            original_size: Original file size in bytes
            compressed_size: Compressed file size in bytes
            
        Returns:
            Compression ratio as percentage
        """
        pass
    
    @abstractmethod
    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes
        """
        pass


class ILogger(ABC):
    """
    Interface for logging operations.
    Allows different logging implementations.
    """
    
    @abstractmethod
    def log_info(self, message: str) -> None:
        """Log info message."""
        pass
    
    @abstractmethod
    def log_warning(self, message: str) -> None:
        """Log warning message."""
        pass
    
    @abstractmethod
    def log_error(self, message: str) -> None:
        """Log error message."""
        pass
