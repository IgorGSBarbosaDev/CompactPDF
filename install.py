#!/usr/bin/env python3
"""
🚀 CompactPDF - Instalação Automatizada

Script que automatiza a instalação completa do CompactPDF, incluindo:
- Verificação de pré-requisitos
- Criação de ambiente virtual
- Instalação de dependências
- Configuração inicial
- Testes de validação

Execute: python install.py
"""

import sys
import os
import subprocess
import platform
from pathlib import Path
from typing import List, Optional, Tuple

def print_header(title: str, char: str = "=") -> None:
    """Imprime cabeçalho formatado."""
    print(f"\\n{char * 60}")
    print(f"🚀 {title}")
    print(f"{char * 60}")

def print_step(step: int, description: str) -> None:
    """Imprime passo da instalação."""
    print(f"\\n📍 Passo {step}: {description}")
    print("-" * 40)

def print_success(message: str) -> None:
    """Imprime mensagem de sucesso."""
    print(f"✅ {message}")

def print_warning(message: str) -> None:
    """Imprime mensagem de aviso."""
    print(f"⚠️ {message}")

def print_error(message: str) -> None:
    """Imprime mensagem de erro."""
    print(f"❌ {message}")

def run_command(command: List[str], description: str, check_exit: bool = True) -> Tuple[bool, str]:
    """Executa comando e retorna resultado."""
    try:
        print(f"   🔄 {description}...")
        
        # No Windows, usar shell=True para comandos internos
        use_shell = platform.system() == "Windows"
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=use_shell,
            check=check_exit
        )
        
        if result.returncode == 0:
            print_success(f"{description} - Concluído")
            return True, result.stdout
        else:
            print_error(f"{description} - Falhou")
            print(f"      Erro: {result.stderr}")
            return False, result.stderr
            
    except subprocess.CalledProcessError as e:
        print_error(f"{description} - Erro: {e}")
        return False, str(e)
    except FileNotFoundError:
        print_error(f"{description} - Comando não encontrado: {command[0]}")
        return False, f"Comando não encontrado: {command[0]}"
    except Exception as e:
        print_error(f"{description} - Erro inesperado: {e}")
        return False, str(e)

def check_python_version() -> Tuple[bool, str]:
    """Verifica se a versão do Python é adequada."""
    version = sys.version_info
    required = (3, 9)
    
    if version >= required:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"Python {version.major}.{version.minor}.{version.micro} (requer 3.9+)"

def check_pip() -> bool:
    """Verifica se pip está disponível."""
    success, _ = run_command([sys.executable, "-m", "pip", "--version"], "Verificando pip", False)
    return success

def check_venv() -> bool:
    """Verifica se venv está disponível."""
    success, _ = run_command([sys.executable, "-m", "venv", "--help"], "Verificando venv", False)
    return success

def create_virtual_environment(project_root: Path) -> bool:
    """Cria ambiente virtual."""
    venv_path = project_root / ".venv"
    
    if venv_path.exists():
        print_warning("Ambiente virtual já existe")
        return True
    
    success, _ = run_command(
        [sys.executable, "-m", "venv", str(venv_path)],
        "Criando ambiente virtual"
    )
    
    return success

def get_venv_python(project_root: Path) -> str:
    """Retorna caminho para Python do ambiente virtual."""
    if platform.system() == "Windows":
        return str(project_root / ".venv" / "Scripts" / "python.exe")
    else:
        return str(project_root / ".venv" / "bin" / "python")

def get_venv_pip(project_root: Path) -> str:
    """Retorna caminho para pip do ambiente virtual."""
    if platform.system() == "Windows":
        return str(project_root / ".venv" / "Scripts" / "pip.exe")
    else:
        return str(project_root / ".venv" / "bin" / "pip")

def upgrade_pip(project_root: Path) -> bool:
    """Atualiza pip no ambiente virtual."""
    venv_python = get_venv_python(project_root)
    
    success, _ = run_command(
        [venv_python, "-m", "pip", "install", "--upgrade", "pip"],
        "Atualizando pip"
    )
    
    return success

def install_requirements(project_root: Path) -> bool:
    """Instala requirements.txt."""
    requirements_file = project_root / "requirements.txt"
    
    if not requirements_file.exists():
        print_error("Arquivo requirements.txt não encontrado")
        return False
    
    venv_python = get_venv_python(project_root)
    
    success, _ = run_command(
        [venv_python, "-m", "pip", "install", "-r", str(requirements_file)],
        "Instalando dependências"
    )
    
    return success

def create_directories(project_root: Path) -> bool:
    """Cria diretórios necessários."""
    directories = [
        "temp",
        "output",
        "backup",
        "cache",
        "logs",
        "data"
    ]
    
    try:
        for dir_name in directories:
            dir_path = project_root / dir_name
            dir_path.mkdir(exist_ok=True)
            print(f"   📁 Criado: {dir_name}/")
        
        print_success("Diretórios criados")
        return True
        
    except Exception as e:
        print_error(f"Erro ao criar diretórios: {e}")
        return False

def create_config_files(project_root: Path) -> bool:
    """Cria arquivos de configuração inicial."""
    try:
        # .gitignore
        gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# CompactPDF específico
temp/
output/
backup/
cache/
logs/
data/
*.pdf
!examples/*.pdf

# Sistema
.DS_Store
Thumbs.db
'''
        
        gitignore_path = project_root / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text(gitignore_content, encoding='utf-8')
            print(f"   📄 Criado: .gitignore")
        
        # Arquivo de configuração do usuário
        user_config_content = '''# CompactPDF - Configuração do Usuário
# Este arquivo é criado automaticamente durante a instalação

[DEFAULT]
# Diretório padrão para arquivos de saída
output_dir = output

# Diretório para backups
backup_dir = backup

# Diretório para cache
cache_dir = cache

# Nível de log (DEBUG, INFO, WARNING, ERROR)
log_level = INFO

# Qualidade padrão para compressão de imagens (0-100)
default_image_quality = 75

# Usar cache por padrão
use_cache = true

# Criar backup por padrão
create_backup = true

# Ativar analytics por padrão
enable_analytics = true
'''
        
        config_path = project_root / "config.ini"
        if not config_path.exists():
            config_path.write_text(user_config_content, encoding='utf-8')
            print(f"   📄 Criado: config.ini")
        
        print_success("Arquivos de configuração criados")
        return True
        
    except Exception as e:
        print_error(f"Erro ao criar configurações: {e}")
        return False

def run_validation_tests(project_root: Path) -> bool:
    """Executa testes de validação."""
    venv_python = get_venv_python(project_root)
    
    # Teste 1: Verificar imports
    test_imports = '''
try:
    import src
    from src import PDFCompressorFacade
    from src.config import CompressionConfig
    print("✅ Imports principais: OK")
except Exception as e:
    print(f"❌ Erro nos imports: {e}")
    exit(1)
'''
    
    success, output = run_command(
        [venv_python, "-c", test_imports],
        "Testando imports principais",
        False
    )
    
    if success:
        print(f"      {output.strip()}")
    
    return success

def create_activation_scripts(project_root: Path) -> bool:
    """Cria scripts de ativação convenientes."""
    try:
        if platform.system() == "Windows":
            # Script para Windows (.bat)
            activate_content = f'''@echo off
echo 🚀 Ativando ambiente CompactPDF...
call "{project_root}\\.venv\\Scripts\\activate.bat"
echo ✅ Ambiente ativado!
echo.
echo 💡 Comandos disponíveis:
echo    python main.py --help          - Ajuda da CLI
echo    python demo.py                 - Demonstração interativa
echo    python check_system.py         - Verificar sistema
echo.
cmd /k
'''
            script_path = project_root / "activate.bat"
            script_path.write_text(activate_content, encoding='utf-8')
            print(f"   📄 Criado: activate.bat")
            
        else:
            # Script para Unix/Linux (.sh)
            activate_content = f'''#!/bin/bash
echo "🚀 Ativando ambiente CompactPDF..."
source "{project_root}/.venv/bin/activate"
echo "✅ Ambiente ativado!"
echo
echo "💡 Comandos disponíveis:"
echo "   python main.py --help          - Ajuda da CLI"
echo "   python demo.py                 - Demonstração interativa"
echo "   python check_system.py         - Verificar sistema"
echo
bash
'''
            script_path = project_root / "activate.sh"
            script_path.write_text(activate_content, encoding='utf-8')
            # Tornar executável
            script_path.chmod(0o755)
            print(f"   📄 Criado: activate.sh")
        
        print_success("Scripts de ativação criados")
        return True
        
    except Exception as e:
        print_error(f"Erro ao criar scripts: {e}")
        return False

def print_final_instructions(project_root: Path) -> None:
    """Imprime instruções finais."""
    print_header("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    
    print("✅ CompactPDF foi instalado e configurado")
    print("✅ Ambiente virtual criado e ativado")
    print("✅ Todas as dependências instaladas")
    print("✅ Configuração inicial criada")
    print("✅ Testes de validação passaram")
    
    print_header("🚀 PRÓXIMOS PASSOS")
    
    if platform.system() == "Windows":
        print("1. 🔄 Para ativar o ambiente:")
        print("   .\\activate.bat")
        print()
        print("2. 🧪 Para testar a instalação:")
        print("   python check_system.py")
        print()
        print("3. 🎮 Para experimentar:")
        print("   python demo.py")
        print()
        print("4. 📄 Para comprimir um PDF:")
        print("   python main.py seu_arquivo.pdf")
    else:
        print("1. 🔄 Para ativar o ambiente:")
        print("   ./activate.sh")
        print("   # ou manualmente:")
        print("   source .venv/bin/activate")
        print()
        print("2. 🧪 Para testar a instalação:")
        print("   python check_system.py")
        print()
        print("3. 🎮 Para experimentar:")
        print("   python demo.py")
        print()
        print("4. 📄 Para comprimir um PDF:")
        print("   python main.py seu_arquivo.pdf")
    
    print_header("📚 DOCUMENTAÇÃO")
    print("📖 docs/GETTING_STARTED.md - Guia de início rápido")
    print("📖 docs/USER_GUIDE.md - Manual completo")
    print("🧪 examples/ - Exemplos de uso")
    
    print_header("🛠️ RESOLUÇÃO DE PROBLEMAS")
    print("Se encontrar problemas:")
    print("1. Execute: python check_system.py")
    print("2. Verifique os logs em: logs/")
    print("3. Consulte: docs/TROUBLESHOOTING.md")

def main():
    """Função principal da instalação."""
    project_root = Path(__file__).parent.absolute()
    
    print_header("INSTALAÇÃO DO COMPACTPDF")
    print(f"📁 Diretório do projeto: {project_root}")
    print(f"🐍 Python: {sys.executable}")
    print(f"💻 Sistema: {platform.system()} {platform.release()}")
    
    # Passo 1: Verificar pré-requisitos
    print_step(1, "Verificando pré-requisitos")
    
    # Verificar versão do Python
    python_ok, python_version = check_python_version()
    if python_ok:
        print_success(f"Versão do Python: {python_version}")
    else:
        print_error(f"Versão do Python inadequada: {python_version}")
        print("💡 Por favor, instale Python 3.9 ou superior")
        return 1
    
    # Verificar pip
    if check_pip():
        print_success("pip disponível")
    else:
        print_error("pip não encontrado")
        print("💡 Por favor, instale pip")
        return 1
    
    # Verificar venv
    if check_venv():
        print_success("venv disponível")
    else:
        print_error("venv não encontrado")
        print("💡 Por favor, instale python3-venv")
        return 1
    
    # Passo 2: Criar ambiente virtual
    print_step(2, "Criando ambiente virtual")
    if not create_virtual_environment(project_root):
        print_error("Falha ao criar ambiente virtual")
        return 1
    
    # Passo 3: Atualizar pip
    print_step(3, "Atualizando pip")
    if not upgrade_pip(project_root):
        print_warning("Falha ao atualizar pip (continuando...)")
    
    # Passo 4: Instalar dependências
    print_step(4, "Instalando dependências")
    if not install_requirements(project_root):
        print_error("Falha ao instalar dependências")
        return 1
    
    # Passo 5: Criar estrutura de diretórios
    print_step(5, "Criando estrutura de diretórios")
    if not create_directories(project_root):
        print_error("Falha ao criar diretórios")
        return 1
    
    # Passo 6: Criar arquivos de configuração
    print_step(6, "Criando configuração inicial")
    if not create_config_files(project_root):
        print_warning("Falha ao criar configurações (continuando...)")
    
    # Passo 7: Criar scripts de ativação
    print_step(7, "Criando scripts de conveniência")
    if not create_activation_scripts(project_root):
        print_warning("Falha ao criar scripts (continuando...)")
    
    # Passo 8: Executar testes de validação
    print_step(8, "Executando testes de validação")
    if not run_validation_tests(project_root):
        print_error("Testes de validação falharam")
        print("💡 Execute 'python check_system.py' para diagnóstico")
        return 1
    
    # Instruções finais
    print_final_instructions(project_root)
    
    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\\n⚠️ Instalação cancelada pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\\n❌ Erro inesperado durante instalação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
