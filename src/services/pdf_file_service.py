"""
PDF file operations service.
Implements IPDFReader and IPDFWriter interfaces.
Follows Single Responsibility principle.
"""

import os
from typing import Optional
from io import BytesIO

from ..interfaces import IPDFReader, IPDFWriter, ILogger


class PDFFileService(IPDFReader, IPDFWriter):
    """
    Service for PDF file operations.
    Handles reading and writing PDF files.
    """
    
    def __init__(self, logger: Optional[ILogger] = None):
        """
        Initialize PDF file service.
        
        Args:
            logger: Optional logger for operations
        """
        self._logger = logger
    
    def read_pdf(self, file_path: str) -> BytesIO:
        """
        Read PDF file and return as BytesIO stream.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            PDF data as BytesIO stream
            
        Raises:
            FileNotFoundError: If file doesn't exist
            RuntimeError: If file cannot be read
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            if not self.validate_pdf(file_path):
                raise RuntimeError(f"Invalid PDF file: {file_path}")
            
            with open(file_path, 'rb') as file:
                pdf_data = BytesIO(file.read())
            
            if self._logger:
                self._logger.log_info(f"Successfully read PDF: {file_path}")
            
            return pdf_data
            
        except Exception as e:
            if self._logger:
                self._logger.log_error(f"Failed to read PDF {file_path}: {str(e)}")
            raise RuntimeError(f"Failed to read PDF file: {str(e)}")
    
    def validate_pdf(self, file_path: str) -> bool:
        """
        Validate if the file is a valid PDF.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False
            
            # Check file extension
            if not file_path.lower().endswith('.pdf'):
                return False
            
            # Check file size
            if os.path.getsize(file_path) == 0:
                return False
            
            # Check PDF magic number
            with open(file_path, 'rb') as file:
                header = file.read(4)
                if header != b'%PDF':
                    return False
            
            # Try to read with PyPDF2
            try:
                from PyPDF2 import PdfReader
                with open(file_path, 'rb') as file:
                    reader = PdfReader(file)
                    # Try to access pages to validate structure
                    len(reader.pages)
                return True
            except Exception:
                return False
                
        except Exception:
            return False
    
    def write_pdf(self, pdf_data: BytesIO, output_path: str) -> bool:
        """
        Write PDF data to file.
        
        Args:
            pdf_data: PDF data as BytesIO stream
            output_path: Path where to write the PDF
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Reset stream position
            pdf_data.seek(0)
            
            # Write to file
            with open(output_path, 'wb') as file:
                file.write(pdf_data.read())
            
            # Verify written file
            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                raise RuntimeError("Written file is empty or doesn't exist")
            
            if self._logger:
                self._logger.log_info(f"Successfully wrote PDF: {output_path}")
            
            return True
            
        except Exception as e:
            if self._logger:
                self._logger.log_error(f"Failed to write PDF {output_path}: {str(e)}")
            return False
    
    def get_file_info(self, file_path: str) -> dict:
        """
        Get information about a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary with file information
        """
        try:
            if not os.path.exists(file_path):
                return {}
            
            info = {
                'file_size': os.path.getsize(file_path),
                'file_path': os.path.abspath(file_path),
                'is_valid': self.validate_pdf(file_path)
            }
            
            if info['is_valid']:
                try:
                    from PyPDF2 import PdfReader
                    with open(file_path, 'rb') as file:
                        reader = PdfReader(file)
                        info['page_count'] = len(reader.pages)
                        info['has_metadata'] = reader.metadata is not None
                        info['is_encrypted'] = reader.is_encrypted
                except Exception:
                    pass
            
            return info
            
        except Exception:
            return {}
