#!/usr/bin/env python3
"""
Teste simples do CompactPDF CLI
"""

import subprocess
import sys
import os

def test_compactpdf():
    """Testa as funcionalidades básicas do CompactPDF."""
    print("🧪 Testando CompactPDF CLI...")
    
    # Teste 1: Help
    print("\n1️⃣ Testando --help:")
    try:
        result = subprocess.run([sys.executable, "main.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if "CompactPDF" in result.stdout:
            print("✅ Help funcionando")
        else:
            print("❌ Help não funcionou")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
    except Exception as e:
        print(f"❌ Erro no help: {e}")
    
    # Teste 2: Version
    print("\n2️⃣ Testando --version:")
    try:
        result = subprocess.run([sys.executable, "main.py", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Version funcionando")
        else:
            print("❌ Version não funcionou")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
    except Exception as e:
        print(f"❌ Erro no version: {e}")
    
    # Teste 3: List profiles
    print("\n3️⃣ Testando --list-profiles:")
    try:
        result = subprocess.run([sys.executable, "main.py", "--list-profiles"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ List profiles funcionando")
            print("Output:", result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
        else:
            print("❌ List profiles não funcionou")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
    except Exception as e:
        print(f"❌ Erro no list profiles: {e}")
    
    # Teste 4: Sem argumentos (deve mostrar erro)
    print("\n4️⃣ Testando sem argumentos:")
    try:
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=True, text=True, timeout=10)
        if "required: input" in result.stderr:
            print("✅ Erro esperado quando sem argumentos")
        else:
            print("❌ Comportamento inesperado sem argumentos")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
    except Exception as e:
        print(f"❌ Erro no teste sem argumentos: {e}")
    
    # Teste 5: Dry run com arquivo
    print("\n5️⃣ Testando dry-run:")
    if os.path.exists("test.pdf"):
        try:
            result = subprocess.run([sys.executable, "main.py", "--dry-run", "-v", "test.pdf"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Dry run funcionando")
                print("Output:", result.stdout[:300] + "..." if len(result.stdout) > 300 else result.stdout)
            else:
                print("❌ Dry run não funcionou")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
        except Exception as e:
            print(f"❌ Erro no dry run: {e}")
    else:
        print("⚠️ test.pdf não encontrado, pulando teste de dry-run")

if __name__ == "__main__":
    test_compactpdf()
