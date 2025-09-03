"""
CompactPDF - Facade Principal
============================

Interface principal simplificada para compressão de PDFs
usando apenas PyMuPDF e Spire.PDF.
"""

import time
import logging
from pathlib import Path
from typing import Optional, Union

from .models import CompressionResult, CompressionConfig, CompressionLevel, create_error_result


logger = logging.getLogger(__name__)


class PDFCompressor:
    """
    Facade principal para compressão de PDFs.
    
    Suporta apenas PyMuPDF e Spire.PDF para garantir
    compressão de 40-60%.
    """
    
    def __init__(self):
        """Inicializa o compressor."""
        # Lazy loading das estratégias
        self._pymupdf_strategy = None
        self._spire_strategy = None
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
    
    @property
    def pymupdf_strategy(self):
        """PyMuPDF strategy com lazy loading."""
        if self._pymupdf_strategy is None:
            try:
                from ..strategies.pymupdf_strategy import PyMuPDFStrategy
                self._pymupdf_strategy = PyMuPDFStrategy()
            except ImportError:
                self._pymupdf_strategy = None
        return self._pymupdf_strategy
    
    @property
    def spire_strategy(self):
        """Spire strategy com lazy loading."""
        if self._spire_strategy is None:
            try:
                from ..strategies.spire_strategy import SpireStrategy
                self._spire_strategy = SpireStrategy()
            except ImportError:
                self._spire_strategy = None
        return self._spire_strategy
    
    def compress(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        config: Optional[CompressionConfig] = None
    ) -> CompressionResult:
        """
        Comprime um arquivo PDF.
        
        Args:
            input_path: Caminho do arquivo de entrada
            output_path: Caminho do arquivo de saída (opcional)
            config: Configuração de compressão (opcional)
            
        Returns:
            CompressionResult: Resultado da compressão
        """
        # Converter para Path
        input_path = Path(input_path)
        
        # Validar entrada
        if not input_path.exists():
            return create_error_result(
                str(input_path), 
                str(output_path or ""), 
                f"Arquivo não encontrado: {input_path}"
            )
        
        if not input_path.suffix.lower() == '.pdf':
            return create_error_result(
                str(input_path),
                str(output_path or ""),
                "Arquivo deve ter extensão .pdf"
            )
        
        # Configurar saída
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_compressed.pdf"
        else:
            output_path = Path(output_path)
        
        # Usar configuração padrão se não fornecida
        if config is None:
            config = CompressionConfig()
        
        # Tentar compressão
        start_time = time.time()
        
        try:
            # Escolher estratégia
            if config.method == "spire":
                result = self._try_spire(input_path, output_path, config)
            elif config.method == "pymupdf":
                result = self._try_pymupdf(input_path, output_path, config)
            else:
                # Auto: PyMuPDF primeiro, depois Spire
                result = self._try_auto(input_path, output_path, config)
            
            # Adicionar tempo de processamento
            if result.success:
                result.processing_time = time.time() - start_time
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na compressão: {e}")
            return create_error_result(
                str(input_path),
                str(output_path),
                f"Erro na compressão: {str(e)}"
            )
    
    def _try_auto(self, input_path: Path, output_path: Path, config: CompressionConfig) -> CompressionResult:
        """Tenta compressão automática (PyMuPDF primeiro)."""
        # Tentar PyMuPDF primeiro
        strategy = self.pymupdf_strategy
        if strategy and strategy.is_available():
            logger.info("Tentando compressão com PyMuPDF...")
            result = strategy.compress(str(input_path), str(output_path), config)
            if result.success:
                result.method_used = "PyMuPDF"
                return result
        
        # Fallback para Spire.PDF
        strategy = self.spire_strategy
        if strategy and strategy.is_available():
            logger.info("Tentando compressão com Spire.PDF...")
            result = strategy.compress(str(input_path), str(output_path), config)
            if result.success:
                result.method_used = "Spire.PDF"
                return result
        
        # Nenhum método disponível
        return create_error_result(
            str(input_path),
            str(output_path),
            "Nenhum método de compressão disponível. Instale PyMuPDF ou Spire.PDF."
        )
    
    def _try_pymupdf(self, input_path: Path, output_path: Path, config: CompressionConfig) -> CompressionResult:
        """Tenta compressão apenas com PyMuPDF."""
        strategy = self.pymupdf_strategy
        if not strategy or not strategy.is_available():
            return create_error_result(
                str(input_path),
                str(output_path),
                "PyMuPDF não está disponível. Execute: pip install PyMuPDF"
            )
        
        result = strategy.compress(str(input_path), str(output_path), config)
        result.method_used = "PyMuPDF"
        return result
    
    def _try_spire(self, input_path: Path, output_path: Path, config: CompressionConfig) -> CompressionResult:
        """Tenta compressão apenas com Spire.PDF."""
        strategy = self.spire_strategy
        if not strategy or not strategy.is_available():
            return create_error_result(
                str(input_path),
                str(output_path),
                "Spire.PDF não está disponível. Execute: pip install spire.pdf"
            )
        
        result = strategy.compress(str(input_path), str(output_path), config)
        result.method_used = "Spire.PDF"
        return result
    
    def get_available_methods(self) -> list[str]:
        """Retorna lista de métodos disponíveis."""
        methods = []
        strategy = self.pymupdf_strategy
        if strategy and strategy.is_available():
            methods.append("pymupdf")
        strategy = self.spire_strategy
        if strategy and strategy.is_available():
            methods.append("spire")
        return methods
    
    def is_ready(self) -> bool:
        """Verifica se pelo menos um método está disponível."""
        return len(self.get_available_methods()) > 0
