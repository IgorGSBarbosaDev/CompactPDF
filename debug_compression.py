#!/usr/bin/env python3
"""
Teste de debug da compactação PDF
================================

Verifica se a compactação está funcionando e onde está o problema.
"""

import sys
import os
from pathlib import Path
import tempfile

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def create_test_pdf():
    """Cria um PDF de teste com conteúdo para comprimir."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        
        # Criar arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()
        
        # Criar PDF com conteúdo
        c = canvas.Canvas(temp_path, pagesize=A4)
        
        # Adicionar múltiplas páginas com texto
        for page in range(5):
            c.showPage()
            c.setFont("Helvetica", 12)
            
            # Adicionar muito texto para ter algo para comprimir
            for line in range(50):
                y_pos = 800 - (line * 15)
                if y_pos > 50:
                    c.drawString(50, y_pos, f"Página {page+1} - Linha {line+1} - Este é um texto longo para testar compressão " * 3)
        
        c.save()
        
        return temp_path
        
    except ImportError:
        print("❌ reportlab não está instalado. Usando arquivo existente se disponível.")
        return None

def test_compression_debug():
    """Testa a compactação e mostra informações detalhadas."""
    
    print("🔍 TESTE DE DEBUG DA COMPACTAÇÃO")
    print("="*50)
    
    try:
        # Importar façade
        from pdf_compressor_facade import PDFCompressorFacade
        from config.compression_config import CompressionLevel
        
        print("✅ Módulos importados com sucesso")
        
        # Criar compressor
        compressor = PDFCompressorFacade()
        print("✅ PDFCompressorFacade criado")
        
        # Configurar para compressão agressiva
        compressor.set_compression_level(CompressionLevel.AGGRESSIVE)
        print(f"✅ Nível de compressão: {compressor.config.compression_level.value}")
        
        # Usar PDF da pasta pdfArchiveTest
        test_pdf_path = Path("pdfArchiveTest") / "Certificado FGV - Formação em Gestão de emissões e precificação de carbono - Bernardo José Antunes (1).pdf"
        
        if not test_pdf_path.exists():
            print(f"❌ PDF de teste não encontrado: {test_pdf_path}")
            print("💡 Verifique se o arquivo está na pasta pdfArchiveTest/")
            return
        
        test_pdf = str(test_pdf_path)
        print(f"📄 Usando PDF de teste: {test_pdf}")
        
        # Verificar tamanho original
        original_size = Path(test_pdf).stat().st_size
        print(f"📊 Tamanho original: {original_size:,} bytes ({original_size/1024:.1f} KB)")
        
        # Criar arquivo de saída
        output_pdf = test_pdf.replace('.pdf', '_compressed_debug.pdf')
        
        print("\n🗜️ Iniciando compressão...")
        
        # Executar compressão
        result = compressor.compress_file(test_pdf, output_pdf)
        
        print(f"\n📋 RESULTADO DA COMPRESSÃO:")
        print(f"   Sucesso: {result.success}")
        print(f"   Tamanho original: {result.original_size:,} bytes")
        print(f"   Tamanho comprimido: {result.compressed_size:,} bytes")
        print(f"   Espaço economizado: {result.space_saved:,} bytes")
        print(f"   Porcentagem de compressão: {result.compression_percentage:.2f}%")
        print(f"   Tempo de processamento: {result.processing_time:.2f}s")
        
        if result.success:
            # Verificar arquivo real
            if Path(output_pdf).exists():
                real_size = Path(output_pdf).stat().st_size
                real_reduction = ((original_size - real_size) / original_size) * 100
                space_saved_mb = (original_size - real_size) / 1024 / 1024
                
                print(f"\n🔍 VERIFICAÇÃO REAL:")
                print(f"   Tamanho do arquivo de saída: {real_size:,} bytes")
                print(f"   Redução real: {real_reduction:.2f}%")
                print(f"   Espaço economizado: {space_saved_mb:.2f} MB")
                
                if real_reduction < 5:
                    print("⚠️  PROBLEMA: Compressão muito baixa!")
                    print("🔧 Investigando métodos de compressão...")
                    
                    # Testar métodos individuais
                    test_compression_methods(compressor, test_pdf)
                elif real_reduction < 15:
                    print("📈 PROGRESSO: Compressão moderada, pode melhorar")
                else:
                    print("✅ Compressão funcionando adequadamente!")
            else:
                print("❌ Arquivo de saída não foi criado!")
        else:
            print(f"❌ Compressão falhou: {result.error_message}")
        
        # Manter arquivo de saída para análise
        if Path(output_pdf).exists():
            print(f"\n📁 Arquivo comprimido salvo em: {output_pdf}")
            print("💡 O arquivo foi mantido para análise")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()

def test_compression_methods(compressor, test_pdf):
    """Testa métodos individuais de compressão."""
    
    print("\n🔧 TESTANDO MÉTODOS INDIVIDUAIS:")
    
    try:
        import PyPDF2
        
        # Abrir PDF
        with open(test_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            
            print(f"📖 PDF carregado: {len(reader.pages)} páginas")
            
            # Testar compressão básica
            for i, page in enumerate(reader.pages):
                print(f"📄 Processando página {i+1}...")
                
                # Método 1: compress_content_streams
                if hasattr(page, 'compress_content_streams'):
                    try:
                        page.compress_content_streams()
                        print(f"   ✅ compress_content_streams aplicado")
                    except Exception as e:
                        print(f"   ❌ compress_content_streams falhou: {e}")
                
                writer.add_page(page)
            
            # Salvar resultado de teste
            test_output = test_pdf.replace('.pdf', '_basic_test.pdf')
            with open(test_output, 'wb') as output_file:
                writer.write(output_file)
            
            # Verificar resultado
            if Path(test_output).exists():
                original_size = Path(test_pdf).stat().st_size
                compressed_size = Path(test_output).stat().st_size
                reduction = ((original_size - compressed_size) / original_size) * 100
                
                print(f"📊 Teste básico:")
                print(f"   Original: {original_size:,} bytes")
                print(f"   Comprimido: {compressed_size:,} bytes") 
                print(f"   Redução: {reduction:.2f}%")
                
                if reduction < 5:
                    print("⚠️  Problema confirmado: PyPDF2 não está comprimindo efetivamente")
                    print("💡 Possíveis causas:")
                    print("   - PDF já está otimizado")
                    print("   - Conteúdo principalmente de imagens")
                    print("   - Algoritmo PyPDF2 limitado para este tipo de PDF")
                
                # Limpeza
                try:
                    os.unlink(test_output)
                except:
                    pass
            
    except Exception as e:
        print(f"❌ Erro no teste de métodos: {e}")

if __name__ == "__main__":
    test_compression_debug()
