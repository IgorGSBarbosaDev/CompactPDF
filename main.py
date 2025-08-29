#!/usr/bin/env python3
"""
🗜️ CompactPDF - Interface de Linha de Comando

Sistema inteligente de compressão de PDF.

Exemplos de Uso:
    python main.py documento.pdf                    # Compressão automática
    python main.py doc.pdf --profile web           # Perfil web otimizado
    python main.py doc.pdf --level balanced        # Nível de compressão
    python main.py *.pdf --batch                   # Processamento em lote
    python main.py doc.pdf --verbose               # Com informações detalhadas
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any

# Configurar o path para imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.pdf_compressor_facade import PDFCompressorFacade
    from src.config.compression_config import CompressionConfig, CompressionLevel, QualityProfile
    from src.models import CompressionResult
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("💡 Verifique se o projeto está configurado corretamente")
    sys.exit(1)


class CompactPDFCLI:
    """Interface de linha de comando para o CompactPDF."""
    
    def __init__(self):
        """Inicializa a interface CLI."""
        pass
        
    def create_parser(self) -> argparse.ArgumentParser:
        """Cria o parser de argumentos da linha de comando."""
        parser = argparse.ArgumentParser(
            prog='CompactPDF',
            description='Sistema Inteligente de Compressão de PDF',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Argumentos de entrada e saida
        parser.add_argument(
            'input',
            nargs='+',
            help='Arquivo(s) PDF para comprimir (suporta wildcards como *.pdf)'
        )
        
        parser.add_argument(
            '-o', '--output',
            help='Arquivo de saída (para arquivo único) ou padrão de nome'
        )
        
        parser.add_argument(
            '--output-dir',
            type=Path,
            help='Diretório de saída para processamento em lote'
        )
        
        parser.add_argument(
            '--batch',
            action='store_true',
            help='Modo de processamento em lote para múltiplos arquivos'
        )
        
        # Configuração de compressão
        parser.add_argument(
            '--level',
            choices=['minimal', 'balanced', 'aggressive'],
            default='balanced',
            help='Nível de compressão (padrão: balanced)'
        )
        
        parser.add_argument(
            '--profile',
            choices=['web', 'print', 'archive'],
            help='Perfil de compressão predefinido'
        )
        
        # Opções de execução
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Modo verboso com informações detalhadas'
        )
        
        parser.add_argument(
            '--quiet',
            action='store_true', 
            help='Modo silencioso (apenas erros)'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Sobrescrever arquivos de saída existentes'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version='CompactPDF v2.0.0'
        )
        
        return parser
    
    def get_config(self, args: argparse.Namespace) -> CompressionConfig:
        """Cria configuração baseada nos argumentos."""
        # Começar com nível selecionado
        if args.level == 'minimal':
            level = CompressionLevel.MINIMAL
        elif args.level == 'aggressive':
            level = CompressionLevel.AGGRESSIVE
        else:  # balanced
            level = CompressionLevel.BALANCED
        
        # Aplicar perfil se especificado
        if args.profile == 'web':
            profile = QualityProfile.WEB
        elif args.profile == 'print':
            profile = QualityProfile.PRINT
        elif args.profile == 'archive':
            profile = QualityProfile.ARCHIVE
        else:
            profile = QualityProfile.WEB  # Padrão web
        
        return CompressionConfig(
            compression_level=level,
            quality_profile=profile
        )
    
    def process_single_file(
        self,
        input_path: Path,
        output_path: Path,
        config: CompressionConfig,
        args: argparse.Namespace
    ) -> Dict[str, Any]:
        """Processa um único arquivo PDF."""
        if args.verbose:
            print(f"\\n🔄 Processando: {input_path.name}")
            print(f"📁 Saída: {output_path}")
            print(f"🎯 Nível: {args.level}")
            if args.profile:
                print(f"📋 Perfil: {args.profile}")
        
        # Verificar se arquivo de saída já existe
        if output_path.exists() and not args.force:
            if not args.quiet:
                print(f"⚠️ Arquivo já existe: {output_path}")
                print(f"💡 Use --force para sobrescrever")
            return {'error': 'Arquivo já existe'}
        
        try:
            # Executar compressão
            compressor = PDFCompressorFacade(config)
            
            start_time = time.time()
            result = compressor.compress_file(str(input_path), str(output_path))
            processing_time = time.time() - start_time
            
            # Converter resultado para dict se necessário
            if hasattr(result, '__dict__'):
                result_dict = result.__dict__.copy()
            else:
                result_dict = result if isinstance(result, dict) else {}
            
            result_dict['processing_time'] = processing_time
            
            # Exibir resultados
            if not args.quiet:
                self._display_results(result_dict, input_path, output_path, args.verbose)
            
            return result_dict
            
        except Exception as e:
            if not args.quiet:
                print(f"❌ Erro ao processar {input_path.name}: {e}")
            return {'error': str(e)}
    
    def _display_results(
        self,
        result: Dict[str, Any],
        input_path: Path,
        output_path: Path,
        verbose: bool = False
    ) -> None:
        """Exibe resultados da compressão."""
        print(f"✅ Compressão concluída!")
        
        if hasattr(result, 'get') or isinstance(result, dict):
            original_size = result.get('original_size', 0)
            compressed_size = result.get('compressed_size', 0)
            
            if original_size > 0:
                compression_ratio = (original_size - compressed_size) / original_size
                space_saved = original_size - compressed_size
                
                print(f"📊 Resultados:")
                print(f"   📁 Original: {original_size:,} bytes")
                print(f"   🗜️ Comprimido: {compressed_size:,} bytes")
                print(f"   📉 Redução: {compression_ratio:.1%}")
                print(f"   💾 Economia: {space_saved:,} bytes")
                
                if verbose:
                    processing_time = result.get('processing_time', 0)
                    print(f"   ⏱️ Tempo: {processing_time:.2f}s")
                    print(f"   📂 Saída: {output_path}")
        else:
            print(f"📂 Arquivo salvo em: {output_path}")
    
    def run(self) -> int:
        """Executa a interface de linha de comando."""
        try:
            parser = self.create_parser()
            args = parser.parse_args()
            
            # Validar argumentos
            if not args.input:
                parser.error("Arquivo(s) de entrada são obrigatórios")
            
            # Obter configuração
            config = self.get_config(args)
            
            # Processar arquivos
            input_files = []
            for pattern in args.input:
                path = Path(pattern)
                if path.is_file():
                    input_files.append(path)
                else:
                    # Expandir wildcards
                    parent = path.parent if path.parent.exists() else Path.cwd()
                    pattern_name = path.name
                    matches = list(parent.glob(pattern_name))
                    input_files.extend([p for p in matches if p.is_file() and p.suffix.lower() == '.pdf'])
            
            if not input_files:
                print("❌ Nenhum arquivo PDF encontrado")
                return 1
            
            # Determinar arquivos de saída
            if len(input_files) == 1 and not args.batch:
                # Arquivo único
                input_file = input_files[0]
                if args.output:
                    output_file = Path(args.output)
                else:
                    output_file = input_file.parent / f"{input_file.stem}_compressed{input_file.suffix}"
                
                result = self.process_single_file(input_file, output_file, config, args)
                
                if 'error' in result:
                    return 1
                    
            else:
                # Processamento em lote
                if not args.quiet:
                    print(f"\\n🚀 Processamento em lote: {len(input_files)} arquivo(s)")
                
                output_dir = args.output_dir or Path.cwd() / 'compressed'
                output_dir.mkdir(parents=True, exist_ok=True)
                
                success_count = 0
                total_original_size = 0
                total_compressed_size = 0
                
                for i, input_file in enumerate(input_files, 1):
                    if not args.quiet:
                        print(f"\\n📄 [{i}/{len(input_files)}] {input_file.name}")
                    
                    output_file = output_dir / f"{input_file.stem}_compressed{input_file.suffix}"
                    
                    try:
                        result = self.process_single_file(input_file, output_file, config, args)
                        
                        if 'error' not in result:
                            success_count += 1
                            total_original_size += result.get('original_size', 0)
                            total_compressed_size += result.get('compressed_size', 0)
                        
                    except Exception as e:
                        if not args.quiet:
                            print(f"❌ Erro: {e}")
                
                # Resumo do lote
                if not args.quiet:
                    print(f"\\n📊 RESUMO DO LOTE:")
                    print(f"   ✅ Sucessos: {success_count}/{len(input_files)}")
                    if success_count > 0 and total_original_size > 0:
                        overall_ratio = (total_original_size - total_compressed_size) / total_original_size
                        print(f"   📉 Compressão média: {overall_ratio:.1%}")
                        print(f"   💾 Economia total: {total_original_size - total_compressed_size:,} bytes")
            
            return 0
            
        except KeyboardInterrupt:
            print("\\n⏹️ Operação cancelada pelo usuário")
            return 1
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return 1


def main() -> int:
    """Função principal."""
    cli = CompactPDFCLI()
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
