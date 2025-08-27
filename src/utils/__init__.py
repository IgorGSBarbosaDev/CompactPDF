"""
Utilities module.
Contains helper functions and utilities.
"""

from .logger import SimpleLogger, NullLogger
from .file_utils import (
    is_pdf_file,
    validate_output_path,
    get_safe_filename,
    generate_output_filename,
    get_unique_filename,
    find_pdf_files,
    estimate_compression_time
)

__all__ = [
    'SimpleLogger',
    'NullLogger',
    'is_pdf_file',
    'validate_output_path',
    'get_safe_filename',
    'generate_output_filename',
    'get_unique_filename',
    'find_pdf_files',
    'estimate_compression_time'
]
