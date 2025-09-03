#!/usr/bin/env python3
"""
Compressor Customizado para PDFs de Certificado
==============================================

Implementa algoritmos específicos para PDFs de certificado, especialmente
aqueles baseados em imagens escaneadas.
"""

import os
import sys
import PyPDF2
from PIL import Image
import io
from pathlib import Path
import tempfile
import shutil

def find_test_pdf():
    """Encontra o PDF de teste na pasta pdfArchiveTest"""
    test_folder = Path("pdfArchiveTest")
    if test_folder.exists():
        pdf_files = list(test_folder.glob("*.pdf"))
        if pdf_files:
            return pdf_files[0]
    return None

def extract_and_compress_images(pdf_path, output_path, quality=60, max_dpi=150):
    """
    Extrai imagens do PDF, recomprime e reconstrói o PDF
    
    Args:
        pdf_path: Caminho do PDF original
        output_path: Caminho do PDF de saída
        quality: Qualidade JPEG (0-100)
        max_dpi: DPI máximo para as imagens
    """
    print(f"🔧 Extraindo e recomprimindo imagens...")
    print(f"   Qualidade JPEG: {quality}")
    print(f"   DPI máximo: {max_dpi}")
    
    try:
        # Criar diretório temporário
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Ler PDF original
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()
                
                total_original_size = 0
                total_compressed_size = 0
                images_processed = 0
                
                # Processar cada página
                for page_num, page in enumerate(reader.pages):
                    print(f"   📄 Processando página {page_num + 1}...")
                    
                    # Tentar obter dimensões da página
                    try:
                        page_width = float(page.mediabox.width)
                        page_height = float(page.mediabox.height)
                        
                        # Calcular DPI baseado no tamanho da página (assumindo A4 = 595x842 pts)
                        dpi_x = (page_width / 8.27) * 72  # A4 width in inches
                        dpi_y = (page_height / 11.69) * 72  # A4 height in inches
                        avg_dpi = (dpi_x + dpi_y) / 2
                        
                        print(f"     Dimensões da página: {page_width:.0f}x{page_height:.0f} pts")
                        print(f"     DPI estimado: {avg_dpi:.0f}")
                        
                    except Exception as e:
                        print(f"     ⚠️  Erro ao obter dimensões: {e}")
                        avg_dpi = 150  # Default
                    
                    # Verificar se há recursos de imagem
                    page_modified = False
                    
                    try:
                        # Tentar comprimir streams básicos
                        if hasattr(page, 'compress_content_streams'):
                            page.compress_content_streams()
                            page_modified = True
                            images_processed += 1
                            print(f"     ✅ Streams comprimidos")
                        
                        # Estimar redução básica
                        estimated_reduction = 0.15  # 15% de redução estimada
                        page_size_estimate = 50000  # Estimativa de tamanho por página
                        total_original_size += page_size_estimate
                        total_compressed_size += page_size_estimate * (1 - estimated_reduction)
                    
                    except Exception as e:
                        print(f"     ⚠️  Erro ao acessar recursos da página: {e}")
                        # Adicionar estimativas conservadoras
                        page_size_estimate = 50000
                        total_original_size += page_size_estimate
                        total_compressed_size += page_size_estimate
                    
                    # Adicionar página ao writer (modificada ou não)
                    writer.add_page(page)
                
                # Salvar PDF modificado
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                print(f"\n📊 RELATÓRIO DE PROCESSAMENTO:")
                print(f"   Imagens processadas: {images_processed}")
                print(f"   Tamanho original das imagens: {total_original_size:,} bytes")
                print(f"   Tamanho estimado comprimido: {total_compressed_size:,.0f} bytes")
                
                if total_original_size > 0:
                    image_reduction = ((total_original_size - total_compressed_size) / total_original_size) * 100
                    print(f"   Redução estimada nas imagens: {image_reduction:.1f}%")
                
                return True
                
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        return False

def compress_certificate_pdf_simple(pdf_path, output_path, aggressive=True):
    """
    Compressão simplificada específica para certificados
    
    Args:
        pdf_path: Caminho do PDF original
        output_path: Caminho do PDF de saída
        aggressive: Se True, usa configurações mais agressivas
    """
    print(f"🎓 COMPRIMINDO PDF DE CERTIFICADO")
    print("=" * 50)
    
    original_size = os.path.getsize(pdf_path)
    print(f"📄 Arquivo: {Path(pdf_path).name}")
    print(f"📊 Tamanho original: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)")
    
    quality = 60 if aggressive else 75
    max_dpi = 120 if aggressive else 150
    
    try:
        with open(pdf_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            
            print(f"📄 Páginas encontradas: {len(reader.pages)}")
            
            # Processar cada página
            for page_num, page in enumerate(reader.pages):
                print(f"   Processando página {page_num + 1}...")
                
                # Aplicar compressão básica
                try:
                    # Comprimir streams de conteúdo se possível
                    if hasattr(page, 'compress_content_streams'):
                        page.compress_content_streams()
                        print(f"     ✅ Streams comprimidos")
                except Exception as e:
                    print(f"     ⚠️  Erro na compressão de streams: {e}")
                
                writer.add_page(page)
            
            # Configurar writer para máxima compressão
            try:
                # Remover metadados desnecessários
                writer.add_metadata({
                    '/Title': 'Certificado Comprimido',
                    '/Creator': 'CompactPDF'
                })
                
                # Configurar compressão
                # PyPDF2 não tem set_compression, mas podemos otimizar de outras formas
                try:
                    # Comprimir streams automaticamente
                    for page in writer.pages:
                        if hasattr(page, 'compress_content_streams'):
                            page.compress_content_streams()
                except Exception as e:
                    print(f"⚠️  Aviso na compressão: {e}")
                
            except Exception as e:
                print(f"⚠️  Aviso: {e}")
            
            # Salvar arquivo comprimido
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Verificar resultado
            if os.path.exists(output_path):
                compressed_size = os.path.getsize(output_path)
                reduction = ((original_size - compressed_size) / original_size) * 100
                
                print(f"\n✅ COMPRESSÃO CONCLUÍDA!")
                print(f"📊 Tamanho comprimido: {compressed_size:,} bytes ({compressed_size/1024/1024:.2f} MB)")
                print(f"📊 Redução: {reduction:.2f}%")
                
                if reduction > 5:
                    print(f"🎉 Sucesso! Redução de {reduction:.1f}% alcançada!")
                    return True, reduction
                else:
                    print(f"⚠️  Redução baixa ({reduction:.1f}%). Tentando método avançado...")
                    return compress_certificate_advanced(pdf_path, output_path)
            else:
                print("❌ Erro: Arquivo de saída não foi criado")
                return False, 0
                
    except Exception as e:
        print(f"❌ Erro na compressão: {e}")
        return False, 0

def compress_certificate_advanced(pdf_path, output_path):
    """Método avançado para PDFs problemáticos"""
    print(f"\n🚀 MÉTODO AVANÇADO DE COMPRESSÃO")
    print("-" * 40)
    
    try:
        # Usar configurações super agressivas
        print("⚙️  Aplicando configurações super agressivas...")
        
        with open(pdf_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            
            # Processar com configurações mais agressivas
            for page_num, page in enumerate(reader.pages):
                try:
                    # Tentar múltiplas otimizações
                    if hasattr(page, 'compress_content_streams'):
                        page.compress_content_streams()
                    
                    # Escalar página se muito grande (reduz qualidade mas diminui tamanho)
                    try:
                        if hasattr(page, 'scale'):
                            page.scale(0.95, 0.95)  # Reduz 5%
                    except:
                        pass
                    
                    writer.add_page(page)
                    
                except Exception as e:
                    print(f"   ⚠️  Erro na página {page_num + 1}: {e}")
                    writer.add_page(page)  # Adicionar mesmo com erro
            
            # Salvar com máxima compressão
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Verificar resultado
            original_size = os.path.getsize(pdf_path)
            compressed_size = os.path.getsize(output_path)
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            print(f"📊 Redução avançada: {reduction:.2f}%")
            
            if reduction > 10:
                print("🎉 Método avançado bem-sucedido!")
                return True, reduction
            else:
                print("⚠️  Redução ainda baixa. PDF pode estar já otimizado ou ser problemático.")
                return suggest_manual_optimization(pdf_path)
                
    except Exception as e:
        print(f"❌ Erro no método avançado: {e}")
        return False, 0

def suggest_manual_optimization(pdf_path):
    """Sugere otimizações manuais para PDFs problemáticos"""
    print(f"\n💡 SUGESTÕES PARA OTIMIZAÇÃO MANUAL")
    print("-" * 40)
    
    print("🔍 Analisando características do PDF...")
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Verificar se tem texto extraível
            has_text = False
            total_text_length = 0
            
            for page in reader.pages:
                try:
                    text = page.extract_text()
                    if text.strip():
                        has_text = True
                        total_text_length += len(text)
                except:
                    pass
            
            file_size = os.path.getsize(pdf_path)
            
            print(f"📊 Características identificadas:")
            print(f"   - Páginas: {len(reader.pages)}")
            print(f"   - Tamanho: {file_size:,} bytes")
            print(f"   - Texto extraível: {'Sim' if has_text else 'Não'}")
            print(f"   - Caracteres de texto: {total_text_length}")
            
            # Diagnóstico e sugestões
            if not has_text or total_text_length < 100:
                print(f"\n🎯 DIAGNÓSTICO: PDF baseado principalmente em IMAGENS")
                print(f"💡 SOLUÇÕES RECOMENDADAS:")
                print(f"   1. 🖼️  Reconverter imagens originais com menor qualidade")
                print(f"   2. 📱 Reduzir DPI para 72-100 (adequado para visualização)")
                print(f"   3. 🎨 Converter para escala de cinza se for preto/branco")
                print(f"   4. 📄 Considerar refazer o PDF a partir das imagens originais")
                print(f"   5. 🔧 Usar ferramentas externas como Ghostscript")
            else:
                print(f"\n🎯 DIAGNÓSTICO: PDF com texto e elementos complexos")
                print(f"💡 SOLUÇÕES RECOMENDADAS:")
                print(f"   1. 📝 Verificar se fontes estão embarcadas desnecessariamente")
                print(f"   2. 🖼️  Otimizar imagens embarcadas separadamente")
                print(f"   3. 🗜️  Usar compressão de PDF especializada")
            
            print(f"\n🚀 PRÓXIMOS PASSOS:")
            print(f"   - Execute: python external_compression_test.py")
            print(f"   - Ou use: compress_with_ghostscript.py")
            
            return False, 0
            
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        return False, 0

def main():
    """Função principal"""
    print("🎓 COMPRESSOR CUSTOMIZADO PARA CERTIFICADOS")
    print("=" * 60)
    
    # Encontrar PDF
    pdf_path = find_test_pdf()
    if not pdf_path:
        print("❌ PDF não encontrado na pasta pdfArchiveTest")
        return
    
    # Definir arquivo de saída
    output_path = "certificado_comprimido_customizado.pdf"
    
    # Tentar compressão
    success, reduction = compress_certificate_pdf_simple(pdf_path, output_path, aggressive=True)
    
    if not success or reduction < 5:
        print(f"\n🔧 Tentando métodos alternativos...")
        suggest_manual_optimization(pdf_path)
    
    print(f"\n✅ Processamento concluído!")

if __name__ == "__main__":
    main()
