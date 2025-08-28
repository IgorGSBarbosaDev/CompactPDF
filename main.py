"""
Command Line Interface for PDF Compression Tool.
Provides easy-to-use CLI for PDF compression operations.
"""

import argparse
import os
import sys
from typing import List

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src import PDFCompressorFacade, CompressionConfig, PresetConfig, CompressionLevel


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="CompactPDF - High-performance PDF compression tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf                          # Basic compression
  %(prog)s input.pdf -o output.pdf           # Specify output file
  %(prog)s input.pdf --preset web            # Use web optimization preset
  %(prog)s input.pdf --quality 70            # Custom image quality
  %(prog)s *.pdf --batch --output-dir compressed/  # Batch compression
  %(prog)s input.pdf --target-ratio 0.3      # Target 30%% of original size

Presets:
  web      - Optimized for web display (small size, good quality)
  print    - Optimized for printing (larger size, high quality)
  maximum  - Maximum compression (smallest size, lower quality)
  balanced - Balanced compression (default settings)
        """
    )
    
    # Input/Output options
    parser.add_argument(
        'input',
        nargs='+',
        help='Input PDF file(s) to compress'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path (for single file) or filename pattern'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory for compressed files'
    )
    
    # Compression options
    parser.add_argument(
        '--preset',
        choices=['web', 'print', 'maximum', 'balanced'],
        help='Use predefined compression preset'
    )
    
    parser.add_argument(
        '--quality',
        type=int,
        metavar='1-100',
        help='Image quality (1-100, lower = more compression)'
    )
    
    parser.add_argument(
        '--target-ratio',
        type=float,
        metavar='0.1-0.9',
        help='Target compression ratio (0.1 = 10%% of original size)'
    )
    
    parser.add_argument(
        '--max-image-size',
        type=int,
        metavar='PIXELS',
        help='Maximum image dimension in pixels'
    )
    
    # Feature toggles
    parser.add_argument(
        '--no-image-resize',
        action='store_true',
        help='Disable image resizing'
    )
    
    parser.add_argument(
        '--no-font-optimization',
        action='store_true',
        help='Disable font optimization'
    )
    
    parser.add_argument(
        '--keep-metadata',
        action='store_true',
        help='Preserve PDF metadata'
    )
    
    parser.add_argument(
        '--keep-annotations',
        action='store_true',
        help='Preserve PDF annotations'
    )
    
    # Batch options
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Enable batch processing mode'
    )
    
    # Output options
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress output'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--log-file',
        help='Write logs to file'
    )
    
    return parser


def validate_args(args) -> bool:
    """Validate command line arguments."""
    # Check input files exist
    for input_file in args.input:
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
            return False
        
        if not input_file.lower().endswith('.pdf'):
            print(f"Error: '{input_file}' is not a PDF file.", file=sys.stderr)
            return False
    
    # Validate quality range
    if args.quality is not None and not (1 <= args.quality <= 100):
        print("Error: Quality must be between 1 and 100.", file=sys.stderr)
        return False
    
    # Validate target ratio
    if args.target_ratio is not None and not (0.1 <= args.target_ratio <= 0.9):
        print("Error: Target ratio must be between 0.1 and 0.9.", file=sys.stderr)
        return False
    
    # Validate batch mode
    if args.batch and len(args.input) == 1:
        print("Warning: Batch mode specified but only one input file provided.")
    
    if not args.batch and len(args.input) > 1 and not args.output_dir:
        print("Error: Multiple input files require --batch mode or --output-dir.", file=sys.stderr)
        return False
    
    return True


def create_config_from_args(args) -> CompressionConfig:
    """Create compression configuration from command line arguments."""
    if args.preset:
        # Use preset configuration
        preset_configs = {
            'web': PresetConfig.web_optimized(),
            'print': PresetConfig.print_quality(),
            'maximum': PresetConfig.maximum_compression(),
            'balanced': PresetConfig.balanced()
        }
        config = preset_configs[args.preset]
    else:
        # Use default configuration
        config = CompressionConfig()
    
    # Override with command line arguments
    if args.quality is not None:
        config.image_quality = args.quality
    
    if args.target_ratio is not None:
        config.target_compression_ratio = args.target_ratio
    
    if args.max_image_size is not None:
        config.max_image_width = args.max_image_size
        config.max_image_height = args.max_image_size
    
    # Feature toggles
    if args.no_image_resize:
        config.resize_images = False
    
    if args.no_font_optimization:
        config.optimize_fonts = False
        config.subset_fonts = False
    
    if args.keep_metadata:
        config.remove_metadata = False
    
    if args.keep_annotations:
        config.preserve_annotations = True
    
    return config


def setup_compressor(args) -> PDFCompressorFacade:
    """Setup PDF compressor with appropriate services."""
    from src.utils import SimpleLogger, NullLogger
    from src.services import ConsoleProgressTracker, SilentProgressTracker
    
    # Setup logger
    if args.quiet:
        logger = NullLogger()
    else:
        logger = SimpleLogger(log_file=args.log_file)
    
    # Setup progress tracker
    if args.quiet:
        progress_tracker = SilentProgressTracker(logger)
    else:
        progress_tracker = ConsoleProgressTracker(logger)
    
    return PDFCompressorFacade(
        logger=logger,
        progress_tracker=progress_tracker
    )


def compress_single_file(compressor: PDFCompressorFacade, input_file: str, output_file: str, config: CompressionConfig):
    """Compress a single PDF file."""
    try:
        result = compressor.compress_pdf(input_file, output_file, config)
        
        if result.success:
            print(f"✓ Compressed: {input_file}")
            print(f"  Size: {result.original_size:,} → {result.compressed_size:,} bytes")
            print(f"  Ratio: {result.compression_ratio:.1%}")
            print(f"  Time: {result.time_taken:.2f}s")
            return True
        else:
            print(f"✗ Failed: {input_file}")
            print(f"  Error: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"✗ Error compressing {input_file}: {str(e)}")
        return False


def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate arguments
    if not validate_args(args):
        sys.exit(1)
    
    try:
        # Create configuration
        config = create_config_from_args(args)
        
        # Setup compressor
        compressor = setup_compressor(args)
        
        if args.batch or len(args.input) > 1:
            # Batch compression
            print(f"Starting batch compression of {len(args.input)} files...")
            
            results = compressor.batch_compress(
                args.input,
                args.output_dir,
                config
            )
            
            # Summary
            successful = sum(1 for r in results if r.success)
            print(f"\nBatch compression completed:")
            print(f"  Successful: {successful}/{len(results)}")
            
            if successful > 0:
                total_original = sum(r.original_size for r in results if r.success)
                total_compressed = sum(r.compressed_size for r in results if r.success)
                overall_ratio = 1 - (total_compressed / total_original) if total_original > 0 else 0
                print(f"  Overall compression: {overall_ratio:.1%}")
            
            sys.exit(0 if successful == len(results) else 1)
        
        else:
            # Single file compression
            input_file = args.input[0]
            
            if args.output:
                output_file = args.output
            else:
                from src.utils import generate_output_filename, get_unique_filename
                output_file = generate_output_filename(input_file)
                output_file = get_unique_filename(output_file)
            
            success = compress_single_file(compressor, input_file, output_file, config)
            sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(130)
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
