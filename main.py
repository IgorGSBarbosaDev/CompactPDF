"""
CompactPDF - Sistema de Compressão de PDFs
==========================================

Sistema simplificado com suporte apenas a PyMuPDF e Spire.PDF.

Instalação:
    pip install pymupdf
    pip install Spire.PDF

Uso básico:
    from compactpdf import PDFCompressor
    
    compressor = PDFCompressor()
    result = compressor.compress("input.pdf", "output.pdf")
    print(f"Redução: {result.reduction_percentage:.1f}%")

Interface gráfica:
    python -m compactpdf.gui
"""

import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from compactpdf.core.facade import PDFCompressor
from compactpdf.core.models import CompressionConfig, CompressionLevel, CompressionResult

def main():
    """Interface de linha de comando simples."""
    import argparse
    
    parser = argparse.ArgumentParser(description='CompactPDF - Compressor de PDFs')
    parser.add_argument('input', help='Arquivo PDF de entrada')
    parser.add_argument('-o', '--output', help='Arquivo PDF de saída')
    parser.add_argument('-m', '--method', choices=['auto', 'pymupdf', 'spire'], 
                       default='auto', help='Método de compressão')
    parser.add_argument('-l', '--level', choices=['light', 'medium', 'aggressive'],
                       default='medium', help='Nível de compressão')
    parser.add_argument('--gui', action='store_true', help='Abrir interface gráfica')
    
    args = parser.parse_args()
    
    # Interface gráfica
    if args.gui:
        try:
            from compactpdf.gui import main as gui_main
            gui_main()
        except ImportError:
            print("Erro: tkinter não está disponível para interface gráfica")
            return 1
        return 0
    
    # Verificar entrada
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Erro: Arquivo '{input_path}' não encontrado")
        return 1
    
    if not input_path.suffix.lower() == '.pdf':
        print("Erro: Arquivo deve ser um PDF")
        return 1
    
    # Configurar saída
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_compressed.pdf"
    
    # Comprimir
    try:
        compressor = PDFCompressor()
        
        if not compressor.is_ready():
            print("Erro: Nenhum método de compressão disponível")
            print("Instale PyMuPDF: pip install pymupdf")
            print("Ou Spire.PDF: pip install Spire.PDF")
            return 1
        
        config = CompressionConfig()
        config.level = CompressionLevel(args.level)
        config.method = args.method if args.method != 'auto' else None
        
        print(f"Comprimindo '{input_path}'...")
        print(f"Método: {args.method}")
        print(f"Nível: {args.level}")
        
        result = compressor.compress(str(input_path), str(output_path), config)
        
        if result.success:
            print(f"✅ Compressão concluída!")
            print(f"Método usado: {result.method_used}")
            print(f"Redução: {result.reduction_percentage:.1f}%")
            print(f"Espaço economizado: {result.size_saved / (1024*1024):.2f} MB")
            print(f"Tempo: {result.processing_time:.2f}s")
            print(f"Arquivo salvo: {output_path}")
            return 0
        else:
            print(f"❌ Erro na compressão: {result.error_message}")
            return 1
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
