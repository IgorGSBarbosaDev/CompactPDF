#!/usr/bin/env python3
"""
🧪 Teste Rápido de Imports - CompactPDF

Testa os imports principais para verificar se a reorganização foi bem-sucedida.
"""

def test_imports():
    """Testa imports básicos."""
    print("🧪 Testando imports do CompactPDF...")
    
    try:
        # Test 1: Import básico do módulo src
        import src
        print("✅ src - Import básico OK")
        
        # Test 2: Import do facade principal
        from src import PDFCompressorFacade
        print("✅ PDFCompressorFacade - Import OK")
        
        # Test 3: Import da configuração
        from src.config import CompressionConfig
        print("✅ CompressionConfig - Import OK")
        
        # Test 4: Import de estratégias
        from src.strategies import AdaptiveCompressionStrategy
        print("✅ AdaptiveCompressionStrategy - Import OK")
        
        # Test 5: Import de utils
        from src.utils import SimpleLogger
        print("✅ SimpleLogger - Import OK")
        
        # Test 6: Import de interfaces
        from src.interfaces import ICompressionStrategy
        print("✅ ICompressionStrategy - Import OK")
        
        # Test 7: Criar uma instância básica
        config = CompressionConfig()
        print("✅ CompressionConfig - Instanciação OK")
        
        strategy = AdaptiveCompressionStrategy()
        print("✅ AdaptiveCompressionStrategy - Instanciação OK")
        
        logger = SimpleLogger()
        print("✅ SimpleLogger - Instanciação OK")
        
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O sistema está funcionando corretamente após a reorganização")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)
