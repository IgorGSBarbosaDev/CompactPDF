"""
File validation utilities.
Helper functions for file operations.
"""

import os
import mimetypes
from typing import List, Optional


def is_pdf_file(file_path: str) -> bool:
    """
    Check if a file is a PDF based on extension and content.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if file is a PDF, False otherwise
    """
    if not os.path.exists(file_path):
        return False
    
    # Check extension
    if not file_path.lower().endswith('.pdf'):
        return False
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type != 'application/pdf':
        return False
    
    # Check magic number
    try:
        with open(file_path, 'rb') as file:
            header = file.read(4)
            return header == b'%PDF'
    except Exception:
        return False


def validate_output_path(output_path: str) -> bool:
    """
    Validate if output path is writable.
    
    Args:
        output_path: Path where file will be written
        
    Returns:
        True if path is valid and writable, False otherwise
    """
    try:
        # Check if directory exists or can be created
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception:
                return False
        
        # Check if we can write to the directory
        if output_dir:
            return os.access(output_dir, os.W_OK)
        else:
            return os.access('.', os.W_OK)
    
    except Exception:
        return False


def get_safe_filename(filename: str) -> str:
    """
    Generate a safe filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    # Characters not allowed in Windows filenames
    invalid_chars = '<>:"/\\|?*'
    
    safe_name = filename
    for char in invalid_chars:
        safe_name = safe_name.replace(char, '_')
    
    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(' .')
    
    # Ensure it's not empty
    if not safe_name:
        safe_name = "output"
    
    return safe_name


def generate_output_filename(input_path: str, suffix: str = "_compressed") -> str:
    """
    Generate output filename based on input filename.
    
    Args:
        input_path: Path to input file
        suffix: Suffix to add before extension
        
    Returns:
        Generated output filename
    """
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    safe_base = get_safe_filename(base_name)
    return f"{safe_base}{suffix}.pdf"


def get_unique_filename(file_path: str) -> str:
    """
    Generate a unique filename if the given path already exists.
    
    Args:
        file_path: Desired file path
        
    Returns:
        Unique file path
    """
    if not os.path.exists(file_path):
        return file_path
    
    base_name, extension = os.path.splitext(file_path)
    counter = 1
    
    while os.path.exists(f"{base_name}_{counter}{extension}"):
        counter += 1
    
    return f"{base_name}_{counter}{extension}"


def find_pdf_files(directory: str) -> List[str]:
    """
    Find all PDF files in a directory.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of PDF file paths
    """
    pdf_files = []
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if is_pdf_file(file_path):
                    pdf_files.append(file_path)
    except Exception:
        pass
    
    return pdf_files


def estimate_compression_time(file_size: int) -> float:
    """
    Estimate compression time based on file size.
    
    Args:
        file_size: File size in bytes
        
    Returns:
        Estimated time in seconds
    """
    # Rough estimation: 1MB per second for compression
    mb_size = file_size / (1024 * 1024)
    return max(1.0, mb_size)  # Minimum 1 second
