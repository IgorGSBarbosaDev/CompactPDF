"""
PDF Compressor Facade - Main entry point for PDF compression.
Implements Facade Pattern and follows SOLID principles.
"""

from typing import List, Optional, Dict, Any
from io import BytesIO

from .interfaces import (
    ICompressionStrategy, 
    IPDFReader, 
    IPDFWriter, 
    IProgressTracker, 
    ICompressionMetrics,
    ILogger
)
from .strategies import (
    ImageCompressionStrategy,
    FontOptimizationStrategy,
    ContentOptimizationStrategy
)
from .services import (
    PDFFileService,
    CompressionMetricsService,
    CompressionResult,
    ConsoleProgressTracker
)
from .config import CompressionConfig, PresetConfig
from .utils import SimpleLogger, generate_output_filename, get_unique_filename


class PDFCompressorFacade:
    """
    Facade for PDF compression operations.
    
    Provides a simplified interface to the complex compression subsystem.
    Follows Facade Pattern and Dependency Inversion Principle.
    """
    
    def __init__(
        self,
        pdf_service: Optional[PDFFileService] = None,
        progress_tracker: Optional[IProgressTracker] = None,
        metrics_service: Optional[CompressionMetricsService] = None,
        logger: Optional[ILogger] = None
    ):
        """
        Initialize PDF compressor facade.
        
        Args:
            pdf_service: PDF file operations service
            progress_tracker: Progress tracking service
            metrics_service: Compression metrics service
            logger: Logging service
        """
        # Dependency injection following DIP
        self._logger = logger or SimpleLogger()
        self._pdf_service = pdf_service or PDFFileService(self._logger)
        self._progress_tracker = progress_tracker or ConsoleProgressTracker(self._logger)
        self._metrics_service = metrics_service or CompressionMetricsService(self._logger)
        
        # Initialize compression strategies
        self._strategies: List[ICompressionStrategy] = [
            ImageCompressionStrategy(),
            FontOptimizationStrategy(),
            ContentOptimizationStrategy()
        ]
    
    def compress_pdf(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        config: Optional[CompressionConfig] = None
    ) -> CompressionResult:
        """
        Compress a PDF file using configured strategies.
        
        Args:
            input_path: Path to input PDF file
            output_path: Path for output file (auto-generated if None)
            config: Compression configuration (default if None)
            
        Returns:
            CompressionResult with detailed metrics
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            RuntimeError: If compression fails
        """
        try:
            # Use default configuration if none provided
            if config is None:
                config = CompressionConfig()
            
            # Validate configuration
            if not config.validate():
                raise ValueError("Invalid compression configuration")
            
            # Generate output path if not provided
            if output_path is None:
                output_path = generate_output_filename(input_path)
                output_path = get_unique_filename(output_path)
            
            self._logger.log_info(f"Starting compression: {input_path} -> {output_path}")
            
            # Start metrics tracking
            self._metrics_service.start_timer()
            
            # Start progress tracking
            total_steps = len(self._strategies) + 2  # strategies + read + write
            self._progress_tracker.start_progress(total_steps)
            
            # Step 1: Read PDF
            self._progress_tracker.update_progress(1, "Reading PDF file")
            pdf_data = self._pdf_service.read_pdf(input_path)
            
            # Step 2-N: Apply compression strategies
            current_step = 2
            config_dict = config.to_dict()
            
            for strategy in self._strategies:
                strategy_name = strategy.get_strategy_name()
                self._progress_tracker.update_progress(
                    current_step, 
                    f"Applying {strategy_name}"
                )
                
                try:
                    pdf_data = strategy.compress(pdf_data, config_dict)
                    self._logger.log_info(f"Applied strategy: {strategy_name}")
                except Exception as e:
                    self._logger.log_warning(f"Strategy {strategy_name} failed: {str(e)}")
                    # Continue with next strategy
                
                current_step += 1
            
            # Final step: Write compressed PDF
            self._progress_tracker.update_progress(current_step, "Writing compressed PDF")
            
            if not self._pdf_service.write_pdf(pdf_data, output_path):
                raise RuntimeError("Failed to write compressed PDF")
            
            # Finish progress tracking
            self._progress_tracker.finish_progress()
            
            # Calculate metrics
            time_taken = self._metrics_service.stop_timer()
            result = self._metrics_service.create_compression_result(
                input_path,
                output_path,
                "Multi-Strategy",
                time_taken,
                success=True
            )
            
            self._logger.log_info(f"Compression completed successfully")
            return result
            
        except Exception as e:
            # Handle errors
            time_taken = self._metrics_service.stop_timer()
            error_message = str(e)
            
            self._progress_tracker.finish_progress()
            self._logger.log_error(f"Compression failed: {error_message}")
            
            return CompressionResult(
                original_size=self._metrics_service.get_file_size(input_path),
                compressed_size=0,
                compression_ratio=0.0,
                time_taken=time_taken,
                strategy_used="Multi-Strategy",
                success=False,
                error_message=error_message
            )
    
    def compress_with_preset(
        self,
        input_path: str,
        preset_name: str,
        output_path: Optional[str] = None
    ) -> CompressionResult:
        """
        Compress PDF using a predefined preset configuration.
        
        Args:
            input_path: Path to input PDF file
            preset_name: Name of preset configuration
            output_path: Path for output file (auto-generated if None)
            
        Returns:
            CompressionResult with detailed metrics
        """
        preset_configs = {
            'web': PresetConfig.web_optimized(),
            'print': PresetConfig.print_quality(),
            'maximum': PresetConfig.maximum_compression(),
            'balanced': PresetConfig.balanced()
        }
        
        if preset_name not in preset_configs:
            raise ValueError(f"Unknown preset: {preset_name}. Available: {list(preset_configs.keys())}")
        
        config = preset_configs[preset_name]
        return self.compress_pdf(input_path, output_path, config)
    
    def batch_compress(
        self,
        input_paths: List[str],
        output_directory: Optional[str] = None,
        config: Optional[CompressionConfig] = None
    ) -> List[CompressionResult]:
        """
        Compress multiple PDF files in batch.
        
        Args:
            input_paths: List of input PDF file paths
            output_directory: Directory for output files (same as input if None)
            config: Compression configuration (default if None)
            
        Returns:
            List of CompressionResult objects
        """
        results = []
        
        self._logger.log_info(f"Starting batch compression of {len(input_paths)} files")
        
        for i, input_path in enumerate(input_paths, 1):
            try:
                self._logger.log_info(f"Processing file {i}/{len(input_paths)}: {input_path}")
                
                # Generate output path
                if output_directory:
                    import os
                    filename = generate_output_filename(input_path)
                    output_path = os.path.join(output_directory, filename)
                    output_path = get_unique_filename(output_path)
                else:
                    output_path = None
                
                # Compress file
                result = self.compress_pdf(input_path, output_path, config)
                results.append(result)
                
            except Exception as e:
                self._logger.log_error(f"Failed to process {input_path}: {str(e)}")
                # Create failed result
                results.append(CompressionResult(
                    original_size=self._metrics_service.get_file_size(input_path),
                    compressed_size=0,
                    compression_ratio=0.0,
                    time_taken=0.0,
                    strategy_used="Multi-Strategy",
                    success=False,
                    error_message=str(e)
                ))
        
        self._logger.log_info(f"Batch compression completed")
        return results
    
    def get_compression_strategies(self) -> List[str]:
        """
        Get list of available compression strategies.
        
        Returns:
            List of strategy names
        """
        return [strategy.get_strategy_name() for strategy in self._strategies]
    
    def add_strategy(self, strategy: ICompressionStrategy) -> None:
        """
        Add a custom compression strategy.
        
        Args:
            strategy: Compression strategy to add
        """
        if strategy not in self._strategies:
            self._strategies.append(strategy)
            self._logger.log_info(f"Added compression strategy: {strategy.get_strategy_name()}")
    
    def remove_strategy(self, strategy_name: str) -> bool:
        """
        Remove a compression strategy by name.
        
        Args:
            strategy_name: Name of strategy to remove
            
        Returns:
            True if strategy was removed, False if not found
        """
        for strategy in self._strategies:
            if strategy.get_strategy_name() == strategy_name:
                self._strategies.remove(strategy)
                self._logger.log_info(f"Removed compression strategy: {strategy_name}")
                return True
        return False
