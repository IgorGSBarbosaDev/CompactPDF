"""
CompactPDF - CLI Otimizada com Performance Melhorada

Interface de linha de comando otimizada para o sistema CompactPDF
com melhorias de performance, cache inteligente e monitoramento de recursos.
"""

import argparse
import sys
import time
import signal
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Imports otimizados com lazy loading
try:
    from src import (
        PDFCompressorFacade, CompressionConfig, 
        get_memory_info, cleanup_all, global_memory_manager
    )
    from src.config.optimized_config import auto_select_config, get_web_config
    from src.utils import get_logger, memory_optimized
    from src.utils.memory_optimizer import MemoryManager
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("💡 Execute: python install.py")
    sys.exit(1)


class OptimizedCLI:
    """
    CLI otimizada com gestão de recursos e performance melhorada.
    
    Implementa processamento em batch, cache inteligente e
    monitoramento de recursos para máxima eficiência.
    """
    
    def __init__(self):
        """Inicializa CLI com otimizações."""
        self.logger = get_logger("CompactPDF-CLI", use_buffer=True)
        self.memory_manager = MemoryManager(
            max_memory_percent=85.0,
            cleanup_threshold=95.0,
            monitor_interval=15.0
        )
        self.compressor = None  # Lazy loading
        self.stats = {
            'files_processed': 0,
            'total_input_size': 0,
            'total_output_size': 0,
            'total_time': 0.0,
            'errors': 0
        }
        
        # Configuração de sinais para limpeza
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Inicia monitoramento de memória
        self.memory_manager.start_monitoring()
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de sistema."""
        self.logger.log_info("🛑 Interrupção detectada, finalizando...")
        self._cleanup()
        sys.exit(0)
    
    def _cleanup(self):
        """Limpeza de recursos."""
        self.memory_manager.stop_monitoring()
        cleanup_all()
        if hasattr(self.logger, 'shutdown'):
            self.logger.shutdown()
    
    def _get_compressor(self) -> PDFCompressorFacade:
        """Lazy loading do compressor."""
        if self.compressor is None:
            self.compressor = PDFCompressorFacade(logger=self.logger)
        return self.compressor
    
    @memory_optimized(max_memory_mb=200.0)
    def compress_single_file(self, input_file: str, output_file: str, 
                           config: CompressionConfig) -> Dict[str, Any]:
        """
        Comprime um único arquivo com otimizações de memória.
        
        Args:
            input_file: Arquivo de entrada
            output_file: Arquivo de saída
            config: Configuração de compressão
            
        Returns:
            Resultado da compressão com métricas
        """
        start_time = time.time()
        input_path = Path(input_file)
        
        try:
            # Verifica arquivo de entrada
            if not input_path.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")
            
            if not input_path.suffix.lower() == '.pdf':
                raise ValueError(f"Arquivo deve ser PDF: {input_file}")
            
            input_size = input_path.stat().st_size
            
            # Executa compressão
            compressor = self._get_compressor()
            result = compressor.compress_pdf(input_file, output_file, config)
            
            # Calcula métricas
            output_path = Path(output_file)
            output_size = output_path.stat().st_size if output_path.exists() else 0
            compression_time = time.time() - start_time
            
            # Atualiza estatísticas
            self.stats['files_processed'] += 1
            self.stats['total_input_size'] += input_size
            self.stats['total_output_size'] += output_size
            self.stats['total_time'] += compression_time
            
            return {
                'success': True,
                'input_file': input_file,
                'output_file': output_file,
                'input_size': input_size,
                'output_size': output_size,
                'compression_ratio': result.compression_ratio,
                'time_taken': compression_time,
                'savings_mb': (input_size - output_size) / (1024 * 1024)
            }
            
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.log_error(f"Erro ao comprimir {input_file}: {e}")
            return {
                'success': False,
                'input_file': input_file,
                'error': str(e),
                'time_taken': time.time() - start_time
            }
    
    def compress_batch(self, input_files: List[str], output_dir: str,
                      config: CompressionConfig, max_workers: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Comprime múltiplos arquivos em paralelo.
        
        Args:
            input_files: Lista de arquivos de entrada
            output_dir: Diretório de saída
            config: Configuração de compressão
            max_workers: Número máximo de workers (None = auto)
            
        Returns:
            Lista de resultados
        """
        if not input_files:
            return []
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Calcula workers baseado na configuração e recursos
        if max_workers is None:
            max_workers = min(len(input_files), config.max_workers or 4)
            # Ajusta baseado na memória disponível
            memory_info = get_memory_info()
            if memory_info['memory']['available_mb'] < 1000:
                max_workers = min(max_workers, 2)
        
        self.logger.log_info(f"🚀 Processando {len(input_files)} arquivos com {max_workers} workers")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submete tarefas
            future_to_file = {}
            
            for input_file in input_files:
                input_path = Path(input_file)
                output_file = output_path / f"compressed_{input_path.name}"
                
                future = executor.submit(
                    self.compress_single_file,
                    input_file,
                    str(output_file),
                    config
                )
                future_to_file[future] = input_file
            
            # Coleta resultados conforme completam
            for future in as_completed(future_to_file):
                result = future.result()
                results.append(result)
                
                if result['success']:
                    self.logger.log_info(
                        f"✅ {Path(result['input_file']).name}: "
                        f"{result['compression_ratio']:.1%} compressão, "
                        f"{result['savings_mb']:.1f}MB economizados"
                    )
                else:
                    self.logger.log_error(f"❌ {Path(result['input_file']).name}: {result['error']}")
        
        return results
    
    def print_performance_summary(self, results: List[Dict[str, Any]]) -> None:
        """Imprime resumo de performance detalhado."""
        if not results:
            return
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        if successful:
            total_input = sum(r['input_size'] for r in successful)
            total_output = sum(r['output_size'] for r in successful)
            total_time = sum(r['time_taken'] for r in successful)
            avg_compression = sum(r['compression_ratio'] for r in successful) / len(successful)
            total_savings = (total_input - total_output) / (1024 * 1024)
            
            print("\n" + "=" * 60)
            print("📊 RESUMO DE PERFORMANCE")
            print("=" * 60)
            print(f"✅ Arquivos processados: {len(successful)}")
            print(f"❌ Arquivos com erro: {len(failed)}")
            print(f"📁 Tamanho original: {total_input / (1024*1024):.1f} MB")
            print(f"📁 Tamanho comprimido: {total_output / (1024*1024):.1f} MB")
            print(f"💾 Espaço economizado: {total_savings:.1f} MB ({avg_compression:.1%})")
            print(f"⏱️  Tempo total: {total_time:.1f}s")
            print(f"🚀 Velocidade média: {total_input / (1024*1024) / total_time:.1f} MB/s")
            
            # Informações de memória
            memory_info = get_memory_info()
            print(f"🧠 Uso de memória: {memory_info['memory']['process_mb']:.1f} MB")
            print(f"📊 Cache hit rate: {memory_info['cache']['hit_rate']:.1%}")
        
        if failed:
            print(f"\n❌ Arquivos com erro:")
            for result in failed:
                print(f"   • {Path(result['input_file']).name}: {result['error']}")
    
    def run(self):
        """Executa CLI principal."""
        parser = self._create_parser()
        args = parser.parse_args()
        
        try:
            if args.command == 'compress':
                self._handle_compress(args)
            elif args.command == 'batch':
                self._handle_batch(args)
            elif args.command == 'info':
                self._handle_info(args)
            elif args.command == 'presets':
                self._handle_presets()
            else:
                parser.print_help()
                
        except KeyboardInterrupt:
            self.logger.log_info("🛑 Operação cancelada pelo usuário")
        except Exception as e:
            self.logger.log_error(f"❌ Erro inesperado: {e}")
            return 1
        finally:
            self._cleanup()
        
        return 0
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Cria parser de argumentos otimizado."""
        parser = argparse.ArgumentParser(
            description='🗜️ CompactPDF - Compressão inteligente de PDF com performance otimizada',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemplos de uso:
  %(prog)s compress input.pdf output.pdf --preset web
  %(prog)s batch *.pdf --output-dir compressed/ --preset archive
  %(prog)s info document.pdf
  %(prog)s presets
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
        
        # Comando compress
        compress_parser = subparsers.add_parser('compress', help='Comprime um arquivo PDF')
        compress_parser.add_argument('input', help='Arquivo PDF de entrada')
        compress_parser.add_argument('output', help='Arquivo PDF de saída')
        compress_parser.add_argument('--preset', choices=['web', 'print', 'archive', 'mobile', 'email', 'ultra_fast', 'quality'],
                                   default='web', help='Preset de compressão (padrão: web)')
        compress_parser.add_argument('--quality', type=int, metavar='1-100',
                                   help='Qualidade de imagem (sobrescreve preset)')
        compress_parser.add_argument('--no-multithreading', action='store_true',
                                   help='Desabilita processamento paralelo')
        
        # Comando batch
        batch_parser = subparsers.add_parser('batch', help='Comprime múltiplos arquivos')
        batch_parser.add_argument('inputs', nargs='+', help='Arquivos PDF de entrada (suporta wildcards)')
        batch_parser.add_argument('--output-dir', required=True, help='Diretório de saída')
        batch_parser.add_argument('--preset', choices=['web', 'print', 'archive', 'mobile', 'email', 'ultra_fast', 'quality'],
                                default='web', help='Preset de compressão (padrão: web)')
        batch_parser.add_argument('--workers', type=int, metavar='N',
                                help='Número de workers paralelos (padrão: auto)')
        batch_parser.add_argument('--quality', type=int, metavar='1-100',
                                help='Qualidade de imagem (sobrescreve preset)')
        
        # Comando info
        info_parser = subparsers.add_parser('info', help='Mostra informações de um arquivo PDF')
        info_parser.add_argument('file', help='Arquivo PDF para analisar')
        
        # Comando presets
        subparsers.add_parser('presets', help='Lista presets disponíveis')
        
        return parser
    
    def _handle_compress(self, args):
        """Lida com comando de compressão única."""
        # Cria configuração
        config = CompressionConfig.get_preset(args.preset)
        
        if args.quality:
            config = config.clone(image_quality=args.quality)
        
        if args.no_multithreading:
            config = config.clone(use_multithreading=False)
        
        self.logger.log_info(f"🗜️  Comprimindo: {args.input} → {args.output}")
        self.logger.log_info(f"⚙️  Configuração: {config}")
        
        # Executa compressão
        result = self.compress_single_file(args.input, args.output, config)
        
        if result['success']:
            print(f"\n✅ Compressão concluída!")
            print(f"📊 Taxa de compressão: {result['compression_ratio']:.1%}")
            print(f"💾 Espaço economizado: {result['savings_mb']:.1f} MB")
            print(f"⏱️  Tempo: {result['time_taken']:.1f}s")
        else:
            print(f"\n❌ Falha na compressão: {result['error']}")
            return 1
    
    def _handle_batch(self, args):
        """Lida com comando de processamento em lote."""
        # Expande wildcards
        import glob
        all_files = []
        for pattern in args.inputs:
            files = glob.glob(pattern)
            if files:
                all_files.extend(files)
            else:
                all_files.append(pattern)  # Pode ser um arquivo específico
        
        # Filtra apenas PDFs existentes
        pdf_files = [f for f in all_files 
                    if Path(f).exists() and Path(f).suffix.lower() == '.pdf']
        
        if not pdf_files:
            print("❌ Nenhum arquivo PDF encontrado")
            return 1
        
        # Cria configuração
        config = CompressionConfig.get_preset(args.preset)
        
        if args.quality:
            config = config.clone(image_quality=args.quality)
        
        if args.workers:
            config = config.clone(max_workers=args.workers)
        
        self.logger.log_info(f"🗜️  Processando {len(pdf_files)} arquivos em lote")
        self.logger.log_info(f"📁 Diretório de saída: {args.output_dir}")
        self.logger.log_info(f"⚙️  Configuração: {config}")
        
        # Executa processamento em lote
        results = self.compress_batch(pdf_files, args.output_dir, config, args.workers)
        
        # Mostra resumo
        self.print_performance_summary(results)
    
    def _handle_info(self, args):
        """Lida com comando de informações."""
        file_path = Path(args.file)
        
        if not file_path.exists():
            print(f"❌ Arquivo não encontrado: {args.file}")
            return 1
        
        if not file_path.suffix.lower() == '.pdf':
            print(f"❌ Arquivo deve ser PDF: {args.file}")
            return 1
        
        # Informações básicas
        file_size = file_path.stat().st_size
        print(f"\n📄 Informações do arquivo: {file_path.name}")
        print(f"📊 Tamanho: {file_size / (1024*1024):.2f} MB")
        
        # Sugestão de configuração
        auto_config = auto_select_config(file_size / (1024*1024))
        print(f"💡 Configuração sugerida: {auto_config}")
        
        # Estimativa de compressão
        estimated_size = file_size * (1 - auto_config.target_compression_ratio)
        estimated_savings = (file_size - estimated_size) / (1024*1024)
        
        print(f"📈 Compressão estimada: {auto_config.target_compression_ratio:.1%}")
        print(f"💾 Economia estimada: {estimated_savings:.1f} MB")
    
    def _handle_presets(self):
        """Lida com comando de listagem de presets."""
        presets = {
            'web': 'Otimizado para web (rápido carregamento)',
            'print': 'Pronto para impressão (alta qualidade)',
            'archive': 'Arquivo de longo prazo (máxima compressão)',
            'mobile': 'Amigável para dispositivos móveis',
            'email': 'Anexo de email (tamanho reduzido)',
            'ultra_fast': 'Velocidade máxima (compressão mínima)',
            'quality': 'Máxima qualidade (compressão moderada)'
        }
        
        print("\n🎯 Presets disponíveis:")
        print("=" * 50)
        
        for preset, description in presets.items():
            config = CompressionConfig.get_preset(preset)
            performance_score = config.get_performance_score()
            compression_score = config.get_compression_score()
            
            print(f"\n📋 {preset.upper()}")
            print(f"   {description}")
            print(f"   🚀 Performance: {performance_score:.1%}")
            print(f"   🗜️  Compressão: {compression_score:.1%}")
            print(f"   ⚙️  Qualidade: {config.image_quality}")


def main():
    """Ponto de entrada principal otimizado."""
    try:
        cli = OptimizedCLI()
        return cli.run()
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
