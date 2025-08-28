"""
Unit tests for PDF compression tool.
Tests the core functionality and SOLID principles implementation.
"""

import unittest
import os
import tempfile
from io import BytesIO
from unittest.mock import Mock, patch

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import CompressionConfig, PresetConfig, CompressionLevel
from src.interfaces import ICompressionStrategy, ILogger
from src.strategies import ImageCompressionStrategy, FontOptimizationStrategy, ContentOptimizationStrategy
from src.services import CompressionMetricsService, CompressionResult
from src.utils import SimpleLogger, NullLogger, is_pdf_file, generate_output_filename
from src.pdf_compressor import PDFCompressorFacade


class TestCompressionConfig(unittest.TestCase):
    """Test compression configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = CompressionConfig()
        
        self.assertEqual(config.image_quality, 80)
        self.assertTrue(config.resize_images)
        self.assertEqual(config.max_image_width, 1200)
        self.assertEqual(config.max_image_height, 1200)
        self.assertTrue(config.optimize_fonts)
        self.assertTrue(config.subset_fonts)
        self.assertTrue(config.remove_metadata)
        self.assertTrue(config.remove_duplicates)
        self.assertTrue(config.compress_streams)
        self.assertEqual(config.compression_level, CompressionLevel.MEDIUM)
        self.assertEqual(config.target_compression_ratio, 0.5)
        self.assertEqual(config.min_quality_threshold, 0.8)
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Valid config
        config = CompressionConfig()
        self.assertTrue(config.validate())
        
        # Invalid image quality
        config.image_quality = 150
        self.assertFalse(config.validate())
        
        # Invalid target ratio
        config.image_quality = 80
        config.target_compression_ratio = 1.5
        self.assertFalse(config.validate())
    
    def test_config_to_dict(self):
        """Test config to dictionary conversion."""
        config = CompressionConfig()
        config_dict = config.to_dict()
        
        self.assertIn('image_quality', config_dict)
        self.assertIn('compression_level', config_dict)
        self.assertEqual(config_dict['compression_level'], 'medium')
    
    def test_config_from_dict(self):
        """Test config from dictionary creation."""
        config_dict = {
            'image_quality': 70,
            'compression_level': 'high',
            'target_compression_ratio': 0.4
        }
        
        config = CompressionConfig.from_dict(config_dict)
        
        self.assertEqual(config.image_quality, 70)
        self.assertEqual(config.compression_level, CompressionLevel.HIGH)
        self.assertEqual(config.target_compression_ratio, 0.4)


class TestPresetConfig(unittest.TestCase):
    """Test preset configurations."""
    
    def test_web_optimized(self):
        """Test web optimized preset."""
        config = PresetConfig.web_optimized()
        
        self.assertEqual(config.image_quality, 75)
        self.assertEqual(config.max_image_width, 800)
        self.assertEqual(config.compression_level, CompressionLevel.HIGH)
        self.assertEqual(config.target_compression_ratio, 0.4)
    
    def test_print_quality(self):
        """Test print quality preset."""
        config = PresetConfig.print_quality()
        
        self.assertEqual(config.image_quality, 90)
        self.assertFalse(config.resize_images)
        self.assertEqual(config.compression_level, CompressionLevel.MEDIUM)
        self.assertEqual(config.target_compression_ratio, 0.7)
    
    def test_maximum_compression(self):
        """Test maximum compression preset."""
        config = PresetConfig.maximum_compression()
        
        self.assertEqual(config.image_quality, 60)
        self.assertEqual(config.max_image_width, 600)
        self.assertEqual(config.compression_level, CompressionLevel.MAXIMUM)
        self.assertEqual(config.target_compression_ratio, 0.3)
    
    def test_balanced(self):
        """Test balanced preset."""
        config = PresetConfig.balanced()
        
        # Should be same as default
        default_config = CompressionConfig()
        self.assertEqual(config.image_quality, default_config.image_quality)
        self.assertEqual(config.target_compression_ratio, default_config.target_compression_ratio)


class TestCompressionStrategies(unittest.TestCase):
    """Test compression strategies."""
    
    def test_strategy_interface(self):
        """Test that strategies implement the interface correctly."""
        strategies = [
            ImageCompressionStrategy(),
            FontOptimizationStrategy(),
            ContentOptimizationStrategy()
        ]
        
        for strategy in strategies:
            self.assertIsInstance(strategy, ICompressionStrategy)
            self.assertTrue(hasattr(strategy, 'compress'))
            self.assertTrue(hasattr(strategy, 'get_strategy_name'))
            
            # Test strategy name
            name = strategy.get_strategy_name()
            self.assertIsInstance(name, str)
            self.assertGreater(len(name), 0)
    
    def test_image_compression_strategy(self):
        """Test image compression strategy."""
        strategy = ImageCompressionStrategy()
        
        self.assertEqual(strategy.get_strategy_name(), "Image Compression")
        
        # Test with mock PDF data
        mock_pdf_data = BytesIO(b'%PDF-1.4 mock data')
        config = {'image_quality': 80, 'resize_images': True}
        
        # Should return BytesIO (even if processing fails)
        result = strategy.compress(mock_pdf_data, config)
        self.assertIsInstance(result, BytesIO)
    
    def test_font_optimization_strategy(self):
        """Test font optimization strategy."""
        strategy = FontOptimizationStrategy()
        
        self.assertEqual(strategy.get_strategy_name(), "Font Optimization")
        
        # Test with mock PDF data
        mock_pdf_data = BytesIO(b'%PDF-1.4 mock data')
        config = {'optimize_fonts': True, 'subset_fonts': True}
        
        # Should return BytesIO (even if processing fails)
        result = strategy.compress(mock_pdf_data, config)
        self.assertIsInstance(result, BytesIO)
    
    def test_content_optimization_strategy(self):
        """Test content optimization strategy."""
        strategy = ContentOptimizationStrategy()
        
        self.assertEqual(strategy.get_strategy_name(), "Content Optimization")
        
        # Test with mock PDF data
        mock_pdf_data = BytesIO(b'%PDF-1.4 mock data')
        config = {'remove_duplicates': True, 'compress_streams': True}
        
        # Should return BytesIO (even if processing fails)
        result = strategy.compress(mock_pdf_data, config)
        self.assertIsInstance(result, BytesIO)


class TestCompressionMetrics(unittest.TestCase):
    """Test compression metrics service."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.metrics = CompressionMetricsService()
    
    def test_compression_ratio_calculation(self):
        """Test compression ratio calculation."""
        # 50% compression
        ratio = self.metrics.calculate_compression_ratio(1000, 500)
        self.assertAlmostEqual(ratio, 0.5, places=2)
        
        # No compression
        ratio = self.metrics.calculate_compression_ratio(1000, 1000)
        self.assertAlmostEqual(ratio, 0.0, places=2)
        
        # Maximum compression
        ratio = self.metrics.calculate_compression_ratio(1000, 0)
        self.assertAlmostEqual(ratio, 1.0, places=2)
        
        # Invalid input
        ratio = self.metrics.calculate_compression_ratio(0, 500)
        self.assertEqual(ratio, 0.0)
    
    def test_timer_functionality(self):
        """Test timer functionality."""
        import time
        
        self.metrics.start_timer()
        time.sleep(0.1)  # Sleep for 100ms
        elapsed = self.metrics.stop_timer()
        
        self.assertGreaterEqual(elapsed, 0.09)  # Allow for timing precision
        self.assertLessEqual(elapsed, 0.2)
    
    def test_compression_result_creation(self):
        """Test compression result creation."""
        # Create temporary files for testing
        with tempfile.NamedTemporaryFile(delete=False) as original:
            original.write(b'original data')
            original_path = original.name
        
        with tempfile.NamedTemporaryFile(delete=False) as compressed:
            compressed.write(b'compressed')
            compressed_path = compressed.name
        
        try:
            result = self.metrics.create_compression_result(
                original_path,
                compressed_path,
                "Test Strategy",
                1.5,
                success=True
            )
            
            self.assertIsInstance(result, CompressionResult)
            self.assertTrue(result.success)
            self.assertEqual(result.strategy_used, "Test Strategy")
            self.assertEqual(result.time_taken, 1.5)
            self.assertGreater(result.original_size, 0)
            self.assertGreater(result.compressed_size, 0)
            
        finally:
            # Clean up
            os.unlink(original_path)
            os.unlink(compressed_path)


class TestUtilities(unittest.TestCase):
    """Test utility functions."""
    
    def test_loggers(self):
        """Test logger implementations."""
        # Test SimpleLogger
        logger = SimpleLogger()
        self.assertIsInstance(logger, ILogger)
        
        # Should not raise exceptions
        logger.log_info("Test info")
        logger.log_warning("Test warning")
        logger.log_error("Test error")
        
        # Test NullLogger
        null_logger = NullLogger()
        self.assertIsInstance(null_logger, ILogger)
        
        # Should not raise exceptions and should do nothing
        null_logger.log_info("Test info")
        null_logger.log_warning("Test warning")
        null_logger.log_error("Test error")
    
    def test_file_utils(self):
        """Test file utility functions."""
        # Test PDF file detection
        self.assertFalse(is_pdf_file("nonexistent.pdf"))
        self.assertFalse(is_pdf_file("test.txt"))
        
        # Test output filename generation
        output_name = generate_output_filename("test.pdf")
        self.assertTrue(output_name.endswith("_compressed.pdf"))
        self.assertIn("test", output_name)
        
        output_name = generate_output_filename("/path/to/document.pdf", "_small")
        self.assertTrue(output_name.endswith("_small.pdf"))
        self.assertIn("document", output_name)


class TestPDFCompressorFacade(unittest.TestCase):
    """Test the main PDF compressor facade."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.compressor = PDFCompressorFacade()
    
    def test_facade_initialization(self):
        """Test facade initialization."""
        self.assertIsInstance(self.compressor, PDFCompressorFacade)
        
        # Test that strategies are loaded
        strategies = self.compressor.get_compression_strategies()
        self.assertGreater(len(strategies), 0)
        self.assertIn("Image Compression", strategies)
        self.assertIn("Font Optimization", strategies)
        self.assertIn("Content Optimization", strategies)
    
    def test_strategy_management(self):
        """Test strategy management functionality."""
        initial_strategies = self.compressor.get_compression_strategies()
        initial_count = len(initial_strategies)
        
        # Test removing a strategy
        removed = self.compressor.remove_strategy("Image Compression")
        self.assertTrue(removed)
        
        updated_strategies = self.compressor.get_compression_strategies()
        self.assertEqual(len(updated_strategies), initial_count - 1)
        self.assertNotIn("Image Compression", updated_strategies)
        
        # Test removing non-existent strategy
        removed = self.compressor.remove_strategy("Non-existent Strategy")
        self.assertFalse(removed)
        
        # Test adding a custom strategy
        class CustomStrategy(ICompressionStrategy):
            def compress(self, pdf_data: BytesIO, config: dict) -> BytesIO:
                return pdf_data
            
            def get_strategy_name(self) -> str:
                return "Custom Test Strategy"
        
        custom_strategy = CustomStrategy()
        self.compressor.add_strategy(custom_strategy)
        
        final_strategies = self.compressor.get_compression_strategies()
        self.assertIn("Custom Test Strategy", final_strategies)
    
    @patch('src.services.pdf_file_service.PDFFileService.read_pdf')
    @patch('src.services.pdf_file_service.PDFFileService.write_pdf')
    @patch('src.services.pdf_file_service.PDFFileService.validate_pdf')
    def test_compression_workflow(self, mock_validate, mock_write, mock_read):
        """Test the compression workflow with mocked dependencies."""
        # Setup mocks
        mock_validate.return_value = True
        mock_read.return_value = BytesIO(b'%PDF-1.4 mock pdf data')
        mock_write.return_value = True
        
        # Test compression
        config = CompressionConfig()
        result = self.compressor.compress_pdf("test.pdf", "output.pdf", config)
        
        # Verify calls were made
        mock_validate.assert_called_once_with("test.pdf")
        mock_read.assert_called_once_with("test.pdf")
        mock_write.assert_called_once()
        
        # Verify result
        self.assertIsInstance(result, CompressionResult)
        self.assertTrue(result.success)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
