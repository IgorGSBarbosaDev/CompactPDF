"""
Simple test to verify the project structure and imports.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all main modules can be imported."""
    try:
        from src import PDFCompressorFacade, CompressionConfig, PresetConfig
        print("✓ Main imports successful")
        
        from src.strategies import ImageCompressionStrategy, FontOptimizationStrategy, ContentOptimizationStrategy
        print("✓ Strategy imports successful")
        
        from src.services import PDFFileService, CompressionMetricsService
        print("✓ Service imports successful")
        
        from src.utils import SimpleLogger, NullLogger
        print("✓ Utility imports successful")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality."""
    try:
        from src import PDFCompressorFacade, CompressionConfig
        
        # Create compressor instance
        compressor = PDFCompressorFacade()
        print("✓ PDFCompressorFacade creation successful")
        
        # Test strategy listing
        strategies = compressor.get_compression_strategies()
        print(f"✓ Available strategies: {', '.join(strategies)}")
        
        # Test configuration
        config = CompressionConfig()
        print(f"✓ Configuration created: target ratio = {config.target_compression_ratio}")
        
        # Test validation
        is_valid = config.validate()
        print(f"✓ Configuration validation: {is_valid}")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("PDF Compression Tool - Basic Tests")
    print("=" * 40)
    
    success = True
    
    print("\n1. Testing imports...")
    success &= test_imports()
    
    print("\n2. Testing basic functionality...")
    success &= test_basic_functionality()
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
