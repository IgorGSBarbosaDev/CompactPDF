"""
Progress tracking service.
Implements IProgressTracker interface.
"""

import sys
from typing import Optional

from ..interfaces import IProgressTracker, ILogger


class ConsoleProgressTracker(IProgressTracker):
    """
    Console-based progress tracker.
    Displays progress in the terminal.
    """
    
    def __init__(self, logger: Optional[ILogger] = None):
        """
        Initialize console progress tracker.
        
        Args:
            logger: Optional logger for operations
        """
        self._logger = logger
        self._total_steps = 0
        self._current_step = 0
        self._started = False
    
    def start_progress(self, total_steps: int) -> None:
        """
        Start progress tracking.
        
        Args:
            total_steps: Total number of steps in the process
        """
        self._total_steps = total_steps
        self._current_step = 0
        self._started = True
        
        print("Starting PDF compression...")
        if self._logger:
            self._logger.log_info(f"Started progress tracking with {total_steps} steps")
    
    def update_progress(self, current_step: int, message: Optional[str] = None) -> None:
        """
        Update progress.
        
        Args:
            current_step: Current step number
            message: Optional progress message
        """
        if not self._started:
            return
        
        self._current_step = current_step
        percentage = (current_step / self._total_steps) * 100 if self._total_steps > 0 else 0
        
        # Create progress bar
        bar_length = 30
        filled_length = int(bar_length * current_step / self._total_steps) if self._total_steps > 0 else 0
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # Display progress
        progress_line = f"\rProgress: |{bar}| {percentage:.1f}% ({current_step}/{self._total_steps})"
        if message:
            progress_line += f" - {message}"
        
        print(progress_line, end='', flush=True)
        
        if self._logger and message:
            self._logger.log_info(f"Progress: {percentage:.1f}% - {message}")
    
    def finish_progress(self) -> None:
        """Finish progress tracking."""
        if self._started:
            print("\nCompression completed!")
            if self._logger:
                self._logger.log_info("Progress tracking finished")
        
        self._started = False
        self._current_step = 0
        self._total_steps = 0


class SilentProgressTracker(IProgressTracker):
    """
    Silent progress tracker that doesn't display anything.
    Useful for batch operations or when UI integration is not needed.
    """
    
    def __init__(self, logger: Optional[ILogger] = None):
        """
        Initialize silent progress tracker.
        
        Args:
            logger: Optional logger for operations
        """
        self._logger = logger
    
    def start_progress(self, total_steps: int) -> None:
        """
        Start progress tracking (silent).
        
        Args:
            total_steps: Total number of steps in the process
        """
        if self._logger:
            self._logger.log_info(f"Started progress tracking with {total_steps} steps")
    
    def update_progress(self, current_step: int, message: Optional[str] = None) -> None:
        """
        Update progress (silent).
        
        Args:
            current_step: Current step number
            message: Optional progress message
        """
        if self._logger and message:
            self._logger.log_info(f"Step {current_step}: {message}")
    
    def finish_progress(self) -> None:
        """Finish progress tracking (silent)."""
        if self._logger:
            self._logger.log_info("Progress tracking finished")
