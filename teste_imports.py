#!/usr/bin/env python3

import os
import sys

def main():
    print("=== TESTE DE IMPORTS CORRIGIDOS ===")
    
    # Adicionar src ao path
    src_path = os.path.join(os.path.dirname(__file__), "src")
    sys.path.insert(0, src_path)
    print(f"Adicionado ao path: {src_path}")
    
    try:
        print("Testando import de CompressionConfig...")
        from config.compression_config import CompressionConfig, CompressionLevel
        print("✓ CompressionConfig importado com sucesso")
        
        print("Testando import de PDFCompressorFacade...")
        from pdf_compressor_facade import PDFCompressorFacade
        print("✓ PDFCompressorFacade importado com sucesso")
        
        print("\n✓ TODAS AS LINHAS 21 E 22 FORAM CORRIGIDAS!")
        print("✓ Os imports agora funcionam corretamente")
        
        return True
        
    except Exception as e:
        print(f"✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print(f"\nStatus: {'SUCESSO' if success else 'FALHA'}")
