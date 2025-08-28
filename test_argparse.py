#!/usr/bin/env python3
"""
Teste simples do argparse para diagnosticar problemas
"""

import argparse
import sys

def test_simple_argparse():
    """Teste básico do argparse."""
    parser = argparse.ArgumentParser(
        prog='CompactPDF-Test',
        description='Teste simples'
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='Arquivos de entrada'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Arquivo de saida'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verboso'
    )
    
    try:
        args = parser.parse_args()
        print(f"✅ Args parsed: {args}")
    except SystemExit as e:
        print(f"SystemExit: {e}")
        return e.code
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    result = test_simple_argparse()
    print(f"Resultado: {result}")
    sys.exit(result)
