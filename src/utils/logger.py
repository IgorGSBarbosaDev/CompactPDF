"""
Logging utility.
Implements ILogger interface.
"""

import logging
import sys
from typing import Optional
from datetime import datetime

from ..interfaces import ILogger


class SimpleLogger(ILogger):
    """
    Simple logger implementation.
    Provides basic logging functionality to console and file.
    """
    
    def __init__(self, name: str = "PDFCompressor", log_file: Optional[str] = None):
        """
        Initialize logger.
        
        Args:
            name: Logger name
            log_file: Optional log file path
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        self._logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            try:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                self._logger.addHandler(file_handler)
            except Exception:
                pass  # Fail silently if file logging can't be set up
    
    def log_info(self, message: str) -> None:
        """Log info message."""
        self._logger.info(message)
    
    def log_warning(self, message: str) -> None:
        """Log warning message."""
        self._logger.warning(message)
    
    def log_error(self, message: str) -> None:
        """Log error message."""
        self._logger.error(message)


class NullLogger(ILogger):
    """
    Null logger that doesn't log anything.
    Useful for silent operations.
    """
    
    def log_info(self, message: str) -> None:
        """Log info message (does nothing)."""
        pass
    
    def log_warning(self, message: str) -> None:
        """Log warning message (does nothing)."""
        pass
    
    def log_error(self, message: str) -> None:
        """Log error message (does nothing)."""
        pass
