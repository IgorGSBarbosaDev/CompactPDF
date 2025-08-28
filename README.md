# CompactPDF - PDF Compression Tool

A high-performance PDF compression tool built with Python following SOLID principles.

## Features

- **Smart Compression**: Compresses PDF files up to 50% while maintaining quality
- **Multiple Strategies**: Image compression, font optimization, and metadata cleanup
- **Extensible Architecture**: Built with SOLID principles for easy extension
- **Progress Tracking**: Real-time compression progress monitoring
- **Quality Control**: Configurable compression levels

## Architecture

The project follows SOLID principles:

- **Single Responsibility**: Each class has one specific purpose
- **Open/Closed**: Easy to extend with new compression strategies
- **Liskov Substitution**: Strategies are interchangeable
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depends on abstractions, not concretions

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.pdf_compressor import PDFCompressorFacade
from src.config import CompressionConfig

config = CompressionConfig(
    image_quality=80,
    remove_duplicates=True,
    optimize_fonts=True
)

compressor = PDFCompressorFacade()
compressor.compress_pdf("input.pdf", "output.pdf", config)
```

## Project Structure

```
src/
├── interfaces/           # Abstract interfaces
├── strategies/          # Compression strategies
├── services/           # Core services
├── config/            # Configuration classes
├── utils/             # Utility functions
└── pdf_compressor.py  # Main facade
```

## Requirements

- Python 3.8+
- PyPDF2
- Pillow
- reportlab
