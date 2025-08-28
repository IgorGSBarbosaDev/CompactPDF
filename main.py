#!/usr/bin/env python3
"""
🗜️ CompactPDF - Interface de Linha de Comando

Sistema inteligente de compressão de PDF com múltiplas estratégias
e funcionalidades avançadas de cache, backup e analytics.

Exemplos de Uso:
    python main.py documento.pdf                    # Compressão automática
    python main.py doc.pdf --profile web           # Perfil web otimizado
    python main.py doc.pdf --quality 70            # Qualidade personalizada
    python main.py *.pdf --batch                   # Processamento em lote
    python main.py doc.pdf --analytics --cache     # Com funcionalidades avançadas
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any

# Configurar o path para imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

try:
    from pdf_compressor import PDFCompressor
    from config import CompressionConfig
    from strategies import (
        ImageCompressionStrategy,
        FontOptimizationStrategy, 
        ContentOptimizationStrategy,
        AdaptiveCompressionStrategy
    )
    from utils import (
        CompressionCache,
        BackupManager,
        CompressionAnalytics,
        AdaptiveCompressionOptimizer,
        SimpleLogger
    )
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("💡 Certifique-se de que está no diretório correto do projeto")
    sys.exit(1)


class CompactPDFCLI:
    """
    Interface de linha de comando para o CompactPDF.
    
    Gerencia argumentos, configura componentes e executa operações de compressão
    com suporte a funcionalidades avançadas como cache, backup e analytics.
    """
    
    def __init__(self):
        """Inicializa a interface CLI."""
        self.logger = SimpleLogger()
        self.cache = None
        self.backup_manager = None
        self.analytics = None
        self.optimizer = None
        
    def create_parser(self) -> argparse.ArgumentParser:
        """
        Cria o parser de argumentos da linha de comando.
        
        Returns:
            Parser configurado com todos os argumentos suportados
        """
        parser = argparse.ArgumentParser(
            prog='CompactPDF',
            description='🗜️ Sistema Inteligente de Compressão de PDF',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
📚 EXEMPLOS DE USO:

  Básico:
    %(prog)s documento.pdf                          # Compressão automática inteligente
    %(prog)s documento.pdf -o comprimido.pdf       # Especificar arquivo de saída
    
  Perfis Predefinidos:
    %(prog)s documento.pdf --profile web            # Otimizado para web
    %(prog)s documento.pdf --profile print          # Otimizado para impressão
    %(prog)s documento.pdf --profile maximum        # Máxima compressão
    %(prog)s documento.pdf --profile balanced       # Balanceado (padrão)
    
  Configuração Personalizada:
    %(prog)s documento.pdf --quality 70             # Qualidade de imagem personalizada
    %(prog)s documento.pdf --max-width 1200         # Largura máxima de imagens
    %(prog)s documento.pdf --target-ratio 0.4       # Meta de compressão (40%)
    
  Estratégias Específicas:
    %(prog)s documento.pdf --strategy adaptive      # Estratégia adaptativa (padrão)
    %(prog)s documento.pdf --strategy image         # Foco em imagens
    %(prog)s documento.pdf --strategy font          # Foco em fontes
    %(prog)s documento.pdf --strategy content       # Foco em conteúdo
    
  Processamento em Lote:
    %(prog)s *.pdf --batch                          # Múltiplos arquivos
    %(prog)s pasta/*.pdf --batch --output-dir saída/ # Com diretório de saída
    
  Funcionalidades Avançadas:
    %(prog)s documento.pdf --cache                  # Usar cache para performance
    %(prog)s documento.pdf --backup                 # Criar backup antes de comprimir
    %(prog)s documento.pdf --analytics              # Gerar relatórios detalhados
    %(prog)s documento.pdf --verbose                # Modo verboso com progresso
    
  Combinado (Recomendado):
    %(prog)s documento.pdf --cache --backup --analytics --verbose

🎯 PERFIS DISPONÍVEIS:
    web       - Otimizado para web (pequeno, boa qualidade)
    print     - Otimizado para impressão (maior, alta qualidade)  
    maximum   - Máxima compressão (menor tamanho, qualidade reduzida)
    balanced  - Balanceado entre tamanho e qualidade (padrão)
    quality   - Prioriza qualidade sobre compressão

⚡ ESTRATÉGIAS DISPONÍVEIS:
    adaptive  - Análise automática e seleção inteligente (padrão)
    image     - Foco na otimização de imagens
    font      - Foco na otimização de fontes
    content   - Foco na otimização de conteúdo
            """
        )
        
        # 📁 ARGUMENTOS DE ENTRADA E SAÍDA
        input_group = parser.add_argument_group('📁 Entrada e Saída')
        input_group.add_argument(
            'input',
            nargs='+',
            help='Arquivo(s) PDF para comprimir (suporta wildcards como *.pdf)'
        )
        
        input_group.add_argument(
            '-o', '--output',
            help='Arquivo de saída (para arquivo único) ou padrão de nome'
        )
        
        input_group.add_argument(
            '--output-dir',
            type=Path,
            help='Diretório de saída para processamento em lote'
        )
        
        input_group.add_argument(
            '--batch',
            action='store_true',
            help='Modo de processamento em lote para múltiplos arquivos'
        )
        
        # 🎯 CONFIGURAÇÃO DE COMPRESSÃO
        compression_group = parser.add_argument_group('🎯 Configuração de Compressão')
        compression_group.add_argument(
            '--profile',
            choices=['web', 'print', 'maximum', 'balanced', 'quality'],
            default='balanced',
            help='Perfil de compressão predefinido (padrão: balanced)'
        )
        
        compression_group.add_argument(
            '--strategy',
            choices=['adaptive', 'image', 'font', 'content'],
            default='adaptive',
            help='Estratégia de compressão (padrão: adaptive)'
        )
        
        compression_group.add_argument(
            '--quality',
            type=int,
            metavar='0-100',
            help='Qualidade de imagem (0-100, menor = mais compressão)'
        )
        
        compression_group.add_argument(
            '--max-width',
            type=int,
            metavar='PIXELS',
            help='Largura máxima de imagens em pixels'
        )
        
        compression_group.add_argument(
            '--max-height', 
            type=int,
            metavar='PIXELS',
            help='Altura máxima de imagens em pixels'
        )
        
        compression_group.add_argument(
            '--target-ratio',
            type=float,
            metavar='0.0-1.0',
            help='Meta de compressão como fração do tamanho original (ex: 0.5 = 50%%)'
        )
        
        # 🚀 FUNCIONALIDADES AVANÇADAS
        advanced_group = parser.add_argument_group('🚀 Funcionalidades Avançadas')
        advanced_group.add_argument(
            '--cache',
            action='store_true',
            help='Usar cache para evitar recompressão de arquivos similares'
        )
        
        advanced_group.add_argument(
            '--cache-dir',
            type=Path,
            default=Path.home() / '.compactpdf_cache',
            help='Diretório do cache (padrão: ~/.compactpdf_cache)'
        )
        
        advanced_group.add_argument(
            '--backup',
            action='store_true',
            help='Criar backup dos arquivos originais antes da compressão'
        )
        
        advanced_group.add_argument(
            '--backup-dir',
            type=Path, 
            default=Path.home() / '.compactpdf_backups',
            help='Diretório de backups (padrão: ~/.compactpdf_backups)'
        )
        
        advanced_group.add_argument(
            '--analytics',
            action='store_true',
            help='Gerar relatórios detalhados de analytics'
        )
        
        advanced_group.add_argument(
            '--analytics-dir',
            type=Path,
            default=Path.home() / '.compactpdf_analytics',
            help='Diretório de analytics (padrão: ~/.compactpdf_analytics)'
        )
        
        # 🔧 OPÇÕES DE EXECUÇÃO
        execution_group = parser.add_argument_group('🔧 Opções de Execução')
        execution_group.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Modo verboso com informações detalhadas'
        )
        
        execution_group.add_argument(
            '--quiet',
            action='store_true', 
            help='Modo silencioso (apenas erros)'
        )
        
        execution_group.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular operação sem executar compressão'
        )
        
        execution_group.add_argument(
            '--force',
            action='store_true',
            help='Sobrescrever arquivos de saída existentes'
        )
        
        # ℹ️ INFORMAÇÕES
        info_group = parser.add_argument_group('ℹ️ Informações')
        info_group.add_argument(
            '--version',
            action='version',
            version='CompactPDF v2.0.0'
        )
        
        info_group.add_argument(
            '--list-profiles',
            action='store_true',
            help='Listar todos os perfis disponíveis'
        )
        
        info_group.add_argument(
            '--list-strategies',
            action='store_true',
            help='Listar todas as estratégias disponíveis'
        )
        
        return parser
    
    def setup_components(self, args: argparse.Namespace) -> None:
        """
        Configura componentes avançados baseados nos argumentos.
        
        Args:
            args: Argumentos da linha de comando
        """
        # Cache
        if args.cache:
            args.cache_dir.mkdir(parents=True, exist_ok=True)
            self.cache = CompressionCache(
                cache_dir=args.cache_dir,
                max_cache_size_mb=500,  # 500MB de cache
                cleanup_interval_hours=24
            )
            if args.verbose:
                print(f"📁 Cache configurado: {args.cache_dir}")
        
        # Backup
        if args.backup:
            args.backup_dir.mkdir(parents=True, exist_ok=True)
            self.backup_manager = BackupManager(
                backup_dir=args.backup_dir,
                max_backups=50,
                auto_cleanup=True
            )
            if args.verbose:
                print(f"🛡️ Backup configurado: {args.backup_dir}")
        
        # Analytics
        if args.analytics:
            args.analytics_dir.mkdir(parents=True, exist_ok=True)
            self.analytics = CompressionAnalytics(
                data_dir=args.analytics_dir,
                enable_detailed_tracking=True
            )
            if args.verbose:
                print(f"📊 Analytics configurado: {args.analytics_dir}")
        
        # Otimizador adaptativo
        self.optimizer = AdaptiveCompressionOptimizer()
        
        # Logger
        if args.quiet:
            self.logger = SimpleLogger(level='ERROR')
        elif args.verbose:
            self.logger = SimpleLogger(level='DEBUG')
        else:
            self.logger = SimpleLogger(level='INFO')
    
    def get_config(self, args: argparse.Namespace) -> CompressionConfig:
        """
        Cria configuração baseada nos argumentos.
        
        Args:
            args: Argumentos da linha de comando
            
        Returns:
            Configuração de compressão
        """
        # Começar com perfil selecionado
        if args.profile == 'web':
            config = CompressionConfig.get_web_optimized_config()
        elif args.profile == 'print':
            config = CompressionConfig.get_print_ready_config()
        elif args.profile == 'maximum':
            config = CompressionConfig.get_maximum_compression_config()
        elif args.profile == 'quality':
            config = CompressionConfig.get_quality_preserving_config()
        else:  # balanced
            config = CompressionConfig.get_balanced_config()
        
        # Aplicar personalizações
        if args.quality is not None:
            config['image_quality'] = max(0, min(100, args.quality))
        
        if args.max_width is not None:
            config['max_image_width'] = max(100, args.max_width)
            
        if args.max_height is not None:
            config['max_image_height'] = max(100, args.max_height)
            
        if args.target_ratio is not None:
            config['target_compression_ratio'] = max(0.1, min(1.0, args.target_ratio))
        
        return config
    
    def get_strategy(self, args: argparse.Namespace):
        """
        Cria estratégia baseada nos argumentos.
        
        Args:
            args: Argumentos da linha de comando
            
        Returns:
            Instância da estratégia selecionada
        """
        if args.strategy == 'image':
            return ImageCompressionStrategy()
        elif args.strategy == 'font':
            return FontOptimizationStrategy()
        elif args.strategy == 'content':
            return ContentOptimizationStrategy()
        else:  # adaptive (padrão)
            return AdaptiveCompressionStrategy()
    
    def process_single_file(
        self,
        input_path: Path,
        output_path: Path,
        config: CompressionConfig,
        strategy,
        args: argparse.Namespace
    ) -> Dict[str, Any]:
        """
        Processa um único arquivo PDF.
        
        Args:
            input_path: Caminho do arquivo de entrada
            output_path: Caminho do arquivo de saída
            config: Configuração de compressão
            strategy: Estratégia de compressão
            args: Argumentos da linha de comando
            
        Returns:
            Resultado da compressão
        """
        if args.verbose:
            print(f"\\n🔄 Processando: {input_path.name}")
            print(f"📁 Saída: {output_path}")
            print(f"🎯 Perfil: {args.profile}")
            print(f"⚡ Estratégia: {args.strategy}")
        
        # Verificar se arquivo de saída já existe
        if output_path.exists() and not args.force:
            if not args.quiet:
                print(f"⚠️ Arquivo já existe: {output_path}")
                print(f"💡 Use --force para sobrescrever")
            return {'error': 'Arquivo já existe'}
        
        # Criar backup se solicitado
        backup_id = None
        if self.backup_manager:
            backup_id = self.backup_manager.create_backup(
                input_path,
                f"Backup antes da compressão - {input_path.name}"
            )
            if args.verbose:
                print(f"🛡️ Backup criado: {backup_id}")
        
        # Verificar cache
        if self.cache:
            cache_key = self.cache.generate_cache_key(input_path, config)
            cached_result = self.cache.get_cached_result(cache_key)
            
            if cached_result:
                if args.verbose:
                    print(f"⚡ Cache hit! Usando resultado em cache")
                # Copiar resultado do cache para saída
                try:
                    cached_path = self.cache._get_cached_file_path(cache_key)
                    if cached_path.exists():
                        import shutil
                        shutil.copy2(cached_path, output_path)
                        return cached_result
                except Exception:
                    pass  # Continuar com compressão normal se cache falhar
        
        # Iniciar tracking de analytics
        operation_id = None
        if self.analytics:
            operation_id = self.analytics.start_operation(
                str(input_path),
                str(output_path),
                config,
                strategy.get_strategy_name()
            )
        
        try:
            # Executar compressão
            if args.dry_run:
                if args.verbose:
                    print(f"🚀 [DRY RUN] Simulando compressão...")
                # Simular resultado
                original_size = input_path.stat().st_size
                result = {
                    'original_size': original_size,
                    'compressed_size': int(original_size * 0.6),  # Simular 40% de compressão
                    'compression_ratio': 0.4,
                    'space_saved': int(original_size * 0.4),
                    'processing_time': 1.5,
                    'strategy': strategy.get_strategy_name(),
                    'dry_run': True
                }
            else:
                compressor = PDFCompressor()
                
                start_time = time.time()
                result = compressor.compress_file(
                    str(input_path),
                    str(output_path),
                    config,
                    strategy
                )
                result['processing_time'] = time.time() - start_time
                result['strategy'] = strategy.get_strategy_name()
            
            # Armazenar no cache
            if self.cache and not args.dry_run:
                self.cache.store_result(cache_key, input_path, output_path, result)
            
            # Registrar analytics
            if self.analytics:
                self.analytics.record_operation(operation_id, result, True)
            
            # Exibir resultados
            if not args.quiet:
                self._display_results(result, input_path, output_path, args.verbose)
            
            return result
            
        except Exception as e:
            # Registrar erro em analytics
            if self.analytics:
                self.analytics.record_operation(
                    operation_id,
                    {'error': str(e)},
                    False
                )
            
            # Tentar recuperar do backup
            if backup_id and self.backup_manager:
                if args.verbose:
                    print(f"🔄 Tentando recuperar do backup...")
                if self.backup_manager.restore_backup(backup_id, input_path):
                    if args.verbose:
                        print(f"✅ Arquivo restaurado do backup")
            
            raise e
    
    def _display_results(
        self,
        result: Dict[str, Any],
        input_path: Path,
        output_path: Path,
        verbose: bool = False
    ) -> None:
        """Exibe resultados da compressão."""
        if result.get('dry_run'):
            print(f"🚀 [DRY RUN] Simulação completa!")
        else:
            print(f"✅ Compressão concluída!")
        
        print(f"📊 Resultados:")
        print(f"   📁 Original: {result['original_size']:,} bytes")
        print(f"   🗜️ Comprimido: {result['compressed_size']:,} bytes")
        print(f"   📉 Redução: {result['compression_ratio']:.1%}")
        print(f"   💾 Economia: {result['space_saved']:,} bytes")
        
        if verbose:
            print(f"   ⚡ Estratégia: {result.get('strategy', 'N/A')}")
            print(f"   ⏱️ Tempo: {result.get('processing_time', 0):.2f}s")
            
            if not result.get('dry_run'):
                print(f"   📂 Saída: {output_path}")
    
    def list_profiles(self) -> None:
        """Lista todos os perfis disponíveis."""
        print("\\n📋 PERFIS DE COMPRESSÃO DISPONÍVEIS:")
        print("=" * 50)
        
        profiles = {
            'web': {
                'desc': 'Otimizado para web e compartilhamento online',
                'compression': 'Alta (60-75%)',
                'quality': 'Boa',
                'use_case': 'Sites, email, redes sociais'
            },
            'print': {
                'desc': 'Otimizado para impressão e arquivamento',
                'compression': 'Moderada (35-50%)',
                'quality': 'Muito Alta',
                'use_case': 'Documentos oficiais, impressão'
            },
            'maximum': {
                'desc': 'Máxima compressão possível',
                'compression': 'Máxima (70-85%)',
                'quality': 'Básica',
                'use_case': 'Armazenamento, backup'
            },
            'balanced': {
                'desc': 'Equilíbrio entre tamanho e qualidade',
                'compression': 'Balanceada (45-60%)',
                'quality': 'Alta',
                'use_case': 'Uso geral (padrão)'
            },
            'quality': {
                'desc': 'Prioriza qualidade sobre compressão',
                'compression': 'Baixa (20-35%)',
                'quality': 'Máxima',
                'use_case': 'Documentos importantes'
            }
        }
        
        for name, info in profiles.items():
            print(f"\\n🎯 {name.upper()}")
            print(f"   📝 Descrição: {info['desc']}")
            print(f"   📊 Compressão: {info['compression']}")
            print(f"   🎨 Qualidade: {info['quality']}")
            print(f"   💼 Uso ideal: {info['use_case']}")
    
    def list_strategies(self) -> None:
        """Lista todas as estratégias disponíveis."""
        print("\\n⚡ ESTRATÉGIAS DE COMPRESSÃO DISPONÍVEIS:")
        print("=" * 50)
        
        strategies = {
            'adaptive': {
                'desc': 'Análise automática e seleção inteligente de técnicas',
                'focus': 'Otimização automática baseada no conteúdo',
                'best_for': 'Todos os tipos de documento (padrão)'
            },
            'image': {
                'desc': 'Foco na otimização de imagens',
                'focus': 'Compressão JPEG, redimensionamento, qualidade',
                'best_for': 'Documentos ricos em imagens'
            },
            'font': {
                'desc': 'Foco na otimização de fontes',
                'focus': 'Subsetting, remoção de fontes não usadas',
                'best_for': 'Documentos com muitas fontes'
            },
            'content': {
                'desc': 'Foco na otimização de conteúdo e estrutura',
                'focus': 'Streams, objetos não usados, metadados',
                'best_for': 'Documentos grandes e complexos'
            }
        }
        
        for name, info in strategies.items():
            print(f"\\n⚡ {name.upper()}")
            print(f"   📝 Descrição: {info['desc']}")
            print(f"   🎯 Foco: {info['focus']}")
            print(f"   📄 Ideal para: {info['best_for']}")
    
    def run(self) -> int:
        """
        Executa a interface de linha de comando.
        
        Returns:
            Código de saída (0 = sucesso, 1 = erro)
        """
        try:
            parser = self.create_parser()
            args = parser.parse_args()
            
            # Comandos de informação
            if args.list_profiles:
                self.list_profiles()
                return 0
                
            if args.list_strategies:
                self.list_strategies()
                return 0
            
            # Validar argumentos
            if not args.input:
                parser.error("Arquivo(s) de entrada são obrigatórios")
            
            # Configurar componentes
            self.setup_components(args)
            
            # Obter configuração e estratégia
            config = self.get_config(args)
            strategy = self.get_strategy(args)
            
            # Processar arquivos
            input_files = []
            for pattern in args.input:
                path = Path(pattern)
                if path.is_file():
                    input_files.append(path)
                else:
                    # Expandir wildcards
                    parent = path.parent
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
                
                result = self.process_single_file(input_file, output_file, config, strategy, args)
                
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
                        result = self.process_single_file(input_file, output_file, config, strategy, args)
                        
                        if 'error' not in result:
                            success_count += 1
                            total_original_size += result['original_size']
                            total_compressed_size += result['compressed_size']
                        
                    except Exception as e:
                        if not args.quiet:
                            print(f"❌ Erro: {e}")
                
                # Resumo do lote
                if not args.quiet:
                    print(f"\\n📊 RESUMO DO LOTE:")
                    print(f"   ✅ Sucessos: {success_count}/{len(input_files)}")
                    if success_count > 0:
                        overall_ratio = (total_original_size - total_compressed_size) / total_original_size
                        print(f"   📉 Compressão média: {overall_ratio:.1%}")
                        print(f"   💾 Economia total: {total_original_size - total_compressed_size:,} bytes")
            
            # Relatório de analytics se solicitado
            if self.analytics and args.verbose:
                print(f"\\n📈 Gerando relatório de analytics...")
                report = self.analytics.generate_report()
                print(f"   📊 Total de operações: {report.total_operations}")
                print(f"   ✅ Taxa de sucesso: {report.success_rate:.1%}")
                print(f"   📉 Compressão média: {report.average_compression_ratio:.1%}")
            
            return 0
            
        except KeyboardInterrupt:
            print("\\n⏹️ Operação cancelada pelo usuário")
            return 1
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            if args.verbose if 'args' in locals() else False:
                import traceback
                traceback.print_exc()
            return 1


def main() -> int:
    """Função principal."""
    cli = CompactPDFCLI()
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
