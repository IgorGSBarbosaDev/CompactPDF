#!/usr/bin/env python3
"""
Script para analisar PDFs de certificado e implementar compactação específica
"""

import os
import sys
import PyPDF2
from PIL import Image
import io
from pathlib import Path

def find_test_pdf():
    """Encontra o PDF de teste na pasta pdfArchiveTest"""
    test_folder = Path("pdfArchiveTest")
    if test_folder.exists():
        pdf_files = list(test_folder.glob("*.pdf"))
        if pdf_files:
            return pdf_files[0]
    return None

def analyze_pdf_basic(pdf_path):
    """Análise básica do PDF"""
    print(f"🔍 Analisando PDF: {pdf_path}")
    print("=" * 60)
    
    try:
        file_size = os.path.getsize(pdf_path)
        print(f"📊 Tamanho original: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            print(f"📄 Número de páginas: {len(reader.pages)}")
            
            # Verificar se tem metadados
            if reader.metadata:
                print(f"📋 Tem metadados: Sim ({len(reader.metadata)} itens)")
            else:
                print("📋 Tem metadados: Não")
            
            # Verificar conteúdo das páginas
            has_text = False
            has_images = False
            
            for page_num, page in enumerate(reader.pages):
                try:
                    # Tentar extrair texto
                    text = page.extract_text()
                    if text.strip():
                        has_text = True
                        print(f"📝 Página {page_num+1}: {len(text)} caracteres de texto")
                    
                    # Verificar se há recursos (possivelmente imagens)
                    try:
                        if hasattr(page, '_get_contents') or '/Contents' in page:
                            has_images = True  # Assumir que há imagens se há conteúdo complexo
                    except:
                        pass
                        
                except Exception as e:
                    print(f"⚠️  Erro ao analisar página {page_num+1}: {e}")
            
            print(f"\n📊 RESUMO:")
            print(f"  Contém texto: {'Sim' if has_text else 'Não'}")
            print(f"  Contém imagens/gráficos: {'Provável' if has_images else 'Improvável'}")
            
            # Diagnóstico
            if not has_text and has_images:
                print("  🎯 TIPO: PDF baseado em imagens (certificado escaneado)")
                return "image_based"
            elif has_text and has_images:
                print("  🎯 TIPO: PDF misto (texto + imagens)")
                return "mixed"
            elif has_text:
                print("  🎯 TIPO: PDF baseado em texto")
                return "text_based"
            else:
                print("  🎯 TIPO: PDF não identificado")
                return "unknown"
                
    except Exception as e:
        print(f"❌ Erro ao analisar PDF: {e}")
        return None

def test_compression_strategies(pdf_path, pdf_type):
    """Testa diferentes estratégias de compactação baseadas no tipo de PDF"""
    print(f"\n🔧 Testando estratégias de compactação para PDF tipo: {pdf_type}")
    print("=" * 60)
    
    from src.pdf_compressor_facade import PDFCompressorFacade
    
    # Configurações específicas para certificados
    configs = {
        "image_based": {
            "strategy": "aggressive",
            "image_quality": 70,
            "image_dpi": 150,
            "remove_duplicates": True,
            "compress_streams": True
        },
        "mixed": {
            "strategy": "balanced",
            "image_quality": 80,
            "image_dpi": 200,
            "remove_duplicates": True,
            "compress_streams": True
        },
        "text_based": {
            "strategy": "conservative",
            "image_quality": 90,
            "remove_duplicates": True,
            "compress_streams": True
        }
    }
    
    config = configs.get(pdf_type, configs["mixed"])
    
    try:
        compressor = PDFCompressorFacade()
        
        # Testar com configuração específica
        output_path = f"test_output_optimized_{pdf_type}.pdf"
        
        print(f"⚙️  Configuração para {pdf_type}:")
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        result = compressor.compress_file(
            input_path=str(pdf_path),
            output_path=output_path,
            **config
        )
        
        if result.success:
            original_size = os.path.getsize(pdf_path)
            compressed_size = os.path.getsize(output_path)
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            print(f"\n✅ Compactação bem-sucedida!")
            print(f"📊 Tamanho original: {original_size:,} bytes")
            print(f"📊 Tamanho compactado: {compressed_size:,} bytes")
            print(f"📊 Redução: {reduction:.2f}%")
            
            if reduction < 5:
                print("⚠️  PROBLEMA: Redução muito baixa!")
                return suggest_advanced_solutions(pdf_path, pdf_type)
            else:
                print("✅ Redução satisfatória!")
                return True
        else:
            print(f"❌ Falha na compactação: {result.error if hasattr(result, 'error') else 'Erro desconhecido'}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de compactação: {e}")
        return False

def suggest_advanced_solutions(pdf_path, pdf_type):
    """Sugere soluções avançadas para PDFs problemáticos"""
    print(f"\n💡 SOLUÇÕES AVANÇADAS PARA {pdf_type.upper()}:")
    print("=" * 60)
    
    if pdf_type == "image_based":
        print("🎯 Para PDFs baseados em imagens (certificados escaneados):")
        print("  1. Reduzir DPI para 72-150 (suficiente para visualização)")
        print("  2. Converter para escala de cinza se possível")
        print("  3. Usar compactação JPEG agressiva (qualidade 60-70)")
        print("  4. Remover metadados desnecessários")
        print("  5. Considerar OCR + reconstrução como texto")
        
        return implement_aggressive_image_compression(pdf_path)
        
    elif pdf_type == "mixed":
        print("🎯 Para PDFs mistos:")
        print("  1. Separar texto e imagens")
        print("  2. Otimizar imagens individualmente")
        print("  3. Recomprimir streams de conteúdo")
        print("  4. Remover objetos duplicados")
        
    else:
        print("🎯 Soluções gerais:")
        print("  1. Verificar se o PDF já está otimizado")
        print("  2. Tentar remover anotações e metadados")
        print("  3. Recomprimir com diferentes algoritmos")
    
    return False

def implement_aggressive_image_compression(pdf_path):
    """Implementa compactação agressiva específica para imagens"""
    print(f"\n🚀 Implementando compactação agressiva de imagens...")
    
    try:
        # Vou criar uma nova versão da função de compactação
        from src.pdf_compressor_facade import PDFCompressorFacade
        
        # Configuração super agressiva
        aggressive_config = {
            "strategy": "aggressive",
            "image_quality": 60,  # Muito baixo para máxima compactação
            "image_dpi": 100,     # DPI baixo
            "remove_duplicates": True,
            "compress_streams": True
        }
        
        compressor = PDFCompressorFacade()
        output_path = "test_output_super_aggressive.pdf"
        
        result = compressor.compress_file(
            input_path=str(pdf_path),
            output_path=output_path,
            **aggressive_config
        )
        
        if result.success:
            original_size = os.path.getsize(pdf_path)
            compressed_size = os.path.getsize(output_path)
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            print(f"✅ Compactação super agressiva:")
            print(f"📊 Redução: {reduction:.2f}%")
            
            if reduction > 10:
                print("🎉 Sucesso! Compactação efetiva alcançada!")
                return True
            else:
                print("⚠️  Ainda precisa de otimizações adicionais")
                return implement_custom_image_processor(pdf_path)
        
    except Exception as e:
        print(f"❌ Erro na compactação agressiva: {e}")
        
    return implement_custom_image_processor(pdf_path)

def implement_custom_image_processor(pdf_path):
    """Implementa processamento customizado de imagens para certificados"""
    print(f"\n🔧 Implementando processador customizado de imagens...")
    
    # Esta será nossa solução final para certificados problemáticos
    print("📝 Criando estratégia customizada para certificados...")
    
    # Código para implementar mais tarde se necessário
    print("💡 Próximos passos:")
    print("  1. Extrair imagens individualmente")
    print("  2. Recomprimir cada imagem com PIL")
    print("  3. Reconstruir PDF com imagens otimizadas")
    print("  4. Aplicar compactação adicional de streams")
    
    return False

def main():
    print("🎓 ANÁLISE DE PDF DE CERTIFICADO")
    print("=" * 60)
    
    # Encontrar o PDF
    pdf_path = find_test_pdf()
    if not pdf_path:
        print("❌ PDF não encontrado na pasta pdfArchiveTest")
        return
    
    # Analisar tipo do PDF
    pdf_type = analyze_pdf_basic(pdf_path)
    if not pdf_type:
        print("❌ Não foi possível analisar o PDF")
        return
    
    # Testar estratégias de compactação
    success = test_compression_strategies(pdf_path, pdf_type)
    
    if not success:
        print("\n🔧 Implementando soluções customizadas...")
        implement_custom_image_processor(pdf_path)
    
    print("\n✅ Análise concluída!")

if __name__ == "__main__":
    main()
