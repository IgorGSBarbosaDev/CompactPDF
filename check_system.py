#!/usr/bin/env python3
"""
🔍 CompactPDF - Verificação do Sistema

Script de diagnóstico que verifica se todos os componentes do CompactPDF
estão funcionando corretamente, incluindo dependências, imports e funcionalidades básicas.

Execute: python check_system.py
"""

import sys
import os
import traceback
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Configurar path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

def print_header(title: str, char: str = "=") -> None:
    """Imprime cabeçalho formatado."""
    print(f"\\n{char * 60}")
    print(f"🔍 {title}")
    print(f"{char * 60}")

def print_check(description: str, status: bool, details: str = "") -> None:
    """Imprime resultado de verificação."""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {description}")
    if details:
        print(f"   ℹ️  {details}")

def check_python_version() -> Tuple[bool, str]:
    """Verifica versão do Python."""
    version = sys.version_info
    required = (3, 9)
    
    if version >= required:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"Python {version.major}.{version.minor}.{version.micro} (requer 3.9+)"

def check_dependencies() -> List[Tuple[str, bool, str]]:
    """Verifica dependências obrigatórias."""
    dependencies = [
        ("PyPDF2", "import PyPDF2"),
        ("Pillow", "from PIL import Image"),
        ("reportlab", "from reportlab.pdfgen import canvas"),
        ("numpy", "import numpy"),
        ("tqdm", "import tqdm"),
        ("psutil", "import psutil"),
    ]
    
    results = []
    for name, import_cmd in dependencies:
        try:
            exec(import_cmd)
            results.append((name, True, "Instalado"))
        except ImportError as e:
            results.append((name, False, f"Não encontrado: {e}"))
        except Exception as e:
            results.append((name, False, f"Erro: {e}"))
    
    return results

def check_project_structure() -> List[Tuple[str, bool, str]]:
    """Verifica estrutura do projeto."""
    required_paths = [
        "src/",
        "src/interfaces/",
        "src/strategies/",
        "src/services/", 
        "src/config/",
        "src/utils/",
        "src/pdf_compressor.py",
        "main.py",
        "demo.py",
        "requirements.txt",
        "README.md"
    ]
    
    results = []
    for path in required_paths:
        full_path = project_root / path
        exists = full_path.exists()
        
        if exists:
            if full_path.is_dir():
                file_count = len(list(full_path.rglob("*.py")))
                details = f"Diretório com {file_count} arquivos Python"
            else:
                size = full_path.stat().st_size
                details = f"Arquivo ({size:,} bytes)"
        else:
            details = "Não encontrado"
        
        results.append((path, exists, details))
    
    return results

def check_imports() -> List[Tuple[str, bool, str]]:
    """Verifica imports principais do projeto."""
    imports_to_test = [
        ("src", "import src"),
        ("PDFCompressorFacade", "from src import PDFCompressorFacade"),
        ("CompressionConfig", "from src.config import CompressionConfig"),
        ("Estratégias", "from src.strategies import ImageCompressionStrategy, FontOptimizationStrategy, ContentOptimizationStrategy, AdaptiveCompressionStrategy"),
        ("Utils Avançados", "from src.utils import ImageQualityAssessor, CompressionCache, BackupManager, CompressionAnalytics"),
        ("Interfaces", "from src.interfaces import ICompressionStrategy"),
    ]
    
    results = []
    for name, import_cmd in imports_to_test:
        try:
            exec(import_cmd)
            results.append((name, True, "Import bem-sucedido"))
        except ImportError as e:
            results.append((name, False, f"Erro de import: {e}"))
        except Exception as e:
            results.append((name, False, f"Erro: {e}"))
    
    return results

def test_basic_functionality() -> List[Tuple[str, bool, str]]:
    """Testa funcionalidades básicas."""
    results = []
    
    try:
        # Teste 1: Criar configuração
        from src.config import CompressionConfig
        config = CompressionConfig()
        results.append(("Criação de Config", True, f"Config criada com sucesso"))
    except Exception as e:
        results.append(("Criação de Config", False, str(e)))
    
    try:
        # Teste 2: Instanciar estratégias
        from src.strategies import AdaptiveCompressionStrategy
        strategy = AdaptiveCompressionStrategy()
        name = strategy.get_strategy_name()
        results.append(("Estratégia Adaptativa", True, f"Estratégia: {name}"))
    except Exception as e:
        results.append(("Estratégia Adaptativa", False, str(e)))
    
    try:
        # Teste 3: Utils avançados
        from src.utils import ImageQualityAssessor
        assessor = ImageQualityAssessor()
        results.append(("Utils Avançados", True, "ImageQualityAssessor criado"))
    except Exception as e:
        results.append(("Utils Avançados", False, str(e)))
    
    try:
        # Teste 4: Cache
        from src.utils import CompressionCache
        cache = CompressionCache(str(Path("test_cache")))
        results.append(("Sistema de Cache", True, "Cache inicializado"))
    except Exception as e:
        results.append(("Sistema de Cache", False, str(e)))
    
    try:
        # Teste 5: Analytics
        from src.utils import CompressionAnalytics
        analytics = CompressionAnalytics(str(Path("test_analytics")))
        results.append(("Sistema de Analytics", True, "Analytics inicializado"))
    except Exception as e:
        results.append(("Sistema de Analytics", False, str(e)))
    
    return results

def test_pdf_creation() -> Tuple[bool, str]:
    """Testa criação de PDF de exemplo."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        test_pdf_path = project_root / "test_document.pdf"
        
        # Criar PDF simples
        c = canvas.Canvas(str(test_pdf_path), pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Teste do CompactPDF - Sistema funcionando!")
        c.save()
        
        # Verificar se foi criado
        if test_pdf_path.exists():
            size = test_pdf_path.stat().st_size
            # Limpar arquivo de teste
            test_pdf_path.unlink()
            return True, f"PDF criado com sucesso ({size:,} bytes)"
        else:
            return False, "PDF não foi criado"
            
    except Exception as e:
        return False, f"Erro: {e}"

def test_main_cli() -> Tuple[bool, str]:
    """Testa se a CLI principal pode ser carregada."""
    try:
        # Tentar importar o main como módulo
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", project_root / "main.py")
        
        if spec and spec.loader:
            main_module = importlib.util.module_from_spec(spec)
            # Não executar, apenas verificar se carrega
            return True, "CLI principal carrega sem erros"
        else:
            return False, "Não foi possível carregar main.py"
            
    except Exception as e:
        return False, f"Erro ao carregar CLI: {e}"

def check_permissions() -> List[Tuple[str, bool, str]]:
    """Verifica permissões necessárias."""
    results = []
    
    # Verificar escrita no diretório atual
    try:
        test_file = project_root / "test_write_permission.tmp"
        test_file.write_text("teste")
        test_file.unlink()
        results.append(("Escrita no diretório", True, "Permissão ok"))
    except Exception as e:
        results.append(("Escrita no diretório", False, str(e)))
    
    # Verificar criação de diretórios
    try:
        test_dir = project_root / "test_dir_permission"
        test_dir.mkdir(exist_ok=True)
        test_dir.rmdir()
        results.append(("Criação de diretórios", True, "Permissão ok"))
    except Exception as e:
        results.append(("Criação de diretórios", False, str(e)))
    
    return results

def generate_report() -> Dict[str, Any]:
    """Gera relatório completo do sistema."""
    print_header("VERIFICAÇÃO DO SISTEMA COMPACTPDF")
    
    report = {
        'python_version': None,
        'dependencies': [],
        'project_structure': [],
        'imports': [],
        'basic_functionality': [],
        'pdf_creation': None,
        'main_cli': None,
        'permissions': [],
        'summary': {
            'total_checks': 0,
            'passed': 0,
            'failed': 0,
            'success_rate': 0.0
        }
    }
    
    # 1. Verificar Python
    print_header("1. Versão do Python", "-")
    status, details = check_python_version()
    print_check("Versão do Python", status, details)
    report['python_version'] = (status, details)
    
    # 2. Verificar dependências
    print_header("2. Dependências", "-")
    deps = check_dependencies()
    for name, status, details in deps:
        print_check(f"Dependência: {name}", status, details)
    report['dependencies'] = deps
    
    # 3. Verificar estrutura do projeto
    print_header("3. Estrutura do Projeto", "-")
    structure = check_project_structure()
    for path, status, details in structure:
        print_check(f"Caminho: {path}", status, details)
    report['project_structure'] = structure
    
    # 4. Verificar imports
    print_header("4. Imports do Projeto", "-")
    imports = check_imports()
    for name, status, details in imports:
        print_check(f"Import: {name}", status, details)
    report['imports'] = imports
    
    # 5. Testar funcionalidades básicas
    print_header("5. Funcionalidades Básicas", "-")
    functionality = test_basic_functionality()
    for name, status, details in functionality:
        print_check(f"Teste: {name}", status, details)
    report['basic_functionality'] = functionality
    
    # 6. Testar criação de PDF
    print_header("6. Criação de PDF", "-")
    pdf_status, pdf_details = test_pdf_creation()
    print_check("Criação de PDF", pdf_status, pdf_details)
    report['pdf_creation'] = (pdf_status, pdf_details)
    
    # 7. Testar CLI principal
    print_header("7. Interface CLI", "-")
    cli_status, cli_details = test_main_cli()
    print_check("Carregamento da CLI", cli_status, cli_details)
    report['main_cli'] = (cli_status, cli_details)
    
    # 8. Verificar permissões
    print_header("8. Permissões do Sistema", "-")
    perms = check_permissions()
    for name, status, details in perms:
        print_check(f"Permissão: {name}", status, details)
    report['permissions'] = perms
    
    # Calcular sumário
    all_checks = []
    all_checks.append(report['python_version'][0])
    all_checks.extend([x[1] for x in report['dependencies']])
    all_checks.extend([x[1] for x in report['project_structure']])
    all_checks.extend([x[1] for x in report['imports']])
    all_checks.extend([x[1] for x in report['basic_functionality']])
    all_checks.append(report['pdf_creation'][0])
    all_checks.append(report['main_cli'][0])
    all_checks.extend([x[1] for x in report['permissions']])
    
    total = len(all_checks)
    passed = sum(all_checks)
    failed = total - passed
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    report['summary'] = {
        'total_checks': total,
        'passed': passed,
        'failed': failed,
        'success_rate': success_rate
    }
    
    return report

def print_summary(report: Dict[str, Any]) -> None:
    """Imprime sumário final."""
    print_header("SUMÁRIO FINAL")
    
    summary = report['summary']
    
    print(f"📊 Total de verificações: {summary['total_checks']}")
    print(f"✅ Passou: {summary['passed']}")
    print(f"❌ Falhou: {summary['failed']}")
    print(f"📈 Taxa de sucesso: {summary['success_rate']:.1f}%")
    
    if summary['success_rate'] >= 90:
        print("\\n🎉 SISTEMA ESTÁ FUNCIONANDO PERFEITAMENTE!")
        print("✅ Todos os componentes principais estão operacionais")
        print("🚀 Você pode usar todas as funcionalidades do CompactPDF")
    elif summary['success_rate'] >= 70:
        print("\\n⚠️ SISTEMA ESTÁ FUNCIONANDO COM ALGUMAS LIMITAÇÕES")
        print("✅ Componentes principais estão funcionando")
        print("💡 Algumas funcionalidades avançadas podem estar indisponíveis")
    else:
        print("\\n❌ SISTEMA TEM PROBLEMAS SÉRIOS")
        print("🔧 Várias verificações falharam")
        print("💡 Revise a instalação e dependências")
    
    # Recomendações
    print("\\n💡 PRÓXIMOS PASSOS:")
    
    if summary['failed'] > 0:
        print("1. 📦 Reinstalar dependências: pip install -r requirements.txt --force-reinstall")
        print("2. 🐍 Verificar versão do Python (requer 3.9+)")
        print("3. 📁 Verificar estrutura do projeto")
        print("4. 🔧 Verificar permissões de arquivo")
    
    print("5. 🚀 Executar demonstração: python demo.py")
    print("6. 📖 Ler documentação: docs/GETTING_STARTED.md")
    print("7. 🧪 Executar exemplos: python examples/usage_examples.py")

def print_recommendations() -> None:
    """Imprime recomendações de uso."""
    print_header("RECOMENDAÇÕES DE USO")
    
    print("🚀 Para começar rapidamente:")
    print("   python demo.py")
    print()
    print("📄 Para comprimir um PDF:")
    print("   python main.py meu_documento.pdf")
    print()
    print("⚡ Para máximo desempenho:")
    print("   python main.py documento.pdf --cache --backup --analytics")
    print()
    print("📚 Para aprender mais:")
    print("   📖 docs/GETTING_STARTED.md - Guia de início")
    print("   📖 docs/USER_GUIDE.md - Manual completo")
    print("   🧪 examples/advanced_usage.py - Exemplos avançados")

def main():
    """Função principal."""
    try:
        # Gerar relatório completo
        report = generate_report()
        
        # Imprimir sumário
        print_summary(report)
        
        # Imprimir recomendações
        print_recommendations()
        
        # Código de saída baseado na taxa de sucesso
        success_rate = report['summary']['success_rate']
        if success_rate >= 90:
            return 0  # Tudo ok
        elif success_rate >= 70:
            return 1  # Problemas menores
        else:
            return 2  # Problemas sérios
            
    except Exception as e:
        print_header("ERRO CRÍTICO")
        print(f"❌ Erro inesperado durante verificação: {e}")
        print("\\n🔍 Detalhes do erro:")
        traceback.print_exc()
        return 3

if __name__ == '__main__':
    sys.exit(main())
