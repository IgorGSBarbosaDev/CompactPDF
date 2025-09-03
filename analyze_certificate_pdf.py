#!/usr/bin/env python3
"""
Análise detalhada do PDF de certificado para identificar problemas de compactação
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

def analyze_pdf_structure(pdf_path):
    """Analisa a estrutura detalhada do PDF"""
    print(f"🔍 Analisando PDF: {pdf_path}")
    print("=" * 60)
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Informações básicas
            print(f"📄 Número de páginas: {len(reader.pages)}")
            print(f"📊 Tamanho do arquivo: {os.path.getsize(pdf_path):,} bytes")
            
            # Metadados
            if reader.metadata:
                print("\n📋 Metadados:")
                for key, value in reader.metadata.items():
                    print(f"  {key}: {value}")
            
            # Análise por página
            total_images = 0
            total_text_objects = 0
            
            for page_num, page in enumerate(reader.pages):
                print(f"\n📄 Página {page_num + 1}:")
                
                # Verificar se há imagens
                try:
                    resources = page['/Resources']
                    if '/XObject' in resources:
                        xobjects = resources['/XObject'].get_object()
                    images_on_page = 0
                    
                    for obj_name, obj_ref in xobjects.items():
                        obj = obj_ref.get_object()
                        if obj.get('/Subtype') == '/Image':
                            images_on_page += 1
                            total_images += 1
                            
                            # Analisar propriedades da imagem
                            width = obj.get('/Width', 'N/A')
                            height = obj.get('/Height', 'N/A')
                            color_space = obj.get('/ColorSpace', 'N/A')
                            bits_per_component = obj.get('/BitsPerComponent', 'N/A')
                            filter_type = obj.get('/Filter', 'N/A')
                            
                            print(f"  🖼️  Imagem {obj_name}:")
                            print(f"    - Dimensões: {width}x{height}")
                            print(f"    - Espaço de cor: {color_space}")
                            print(f"    - Bits por componente: {bits_per_component}")
                            print(f"    - Filtro: {filter_type}")
                            
                            # Tentar extrair e analisar a imagem
                            try:
                                if '/Filter' in obj and obj['/Filter'] == '/DCTDecode':
                                    # JPEG image
                                    img_data = obj._data
                                    print(f"    - Tamanho dos dados: {len(img_data):,} bytes")
                                    
                                    # Tentar abrir com PIL para mais detalhes
                                    try:
                                        img = Image.open(io.BytesIO(img_data))
                                        print(f"    - Formato PIL: {img.format}")
                                        print(f"    - Modo: {img.mode}")
                                        print(f"    - Tamanho real: {img.size}")
                                    except Exception as e:
                                        print(f"    - Erro ao abrir com PIL: {e}")
                                        
                            except Exception as e:
                                print(f"    - Erro ao extrair dados: {e}")
                    
                    print(f"  📊 Total de imagens nesta página: {images_on_page}")
                
                # Contar objetos de texto (aproximação)
                if '/Contents' in page:
                    try:
                        content = page.extract_text()
                        text_length = len(content.strip())
                        print(f"  📝 Texto extraído: {text_length} caracteres")
                        if text_length > 0:
                            total_text_objects += 1
                    except:
                        print("  📝 Não foi possível extrair texto")
            
            print(f"\n📊 RESUMO GERAL:")
            print(f"  Total de imagens: {total_images}")
            print(f"  Páginas com texto: {total_text_objects}")
            
            # Verificar se é principalmente baseado em imagens
            if total_images > 0 and total_text_objects == 0:
                print("  🎯 DIAGNÓSTICO: PDF baseado principalmente em IMAGENS")
                print("  💡 SOLUÇÃO: Necessário otimização de imagens específica")
            elif total_images > total_text_objects:
                print("  🎯 DIAGNÓSTICO: PDF com muitas IMAGENS e pouco texto")
                print("  💡 SOLUÇÃO: Foco na compactação de imagens")
            else:
                print("  🎯 DIAGNÓSTICO: PDF com mais texto que imagens")
                print("  💡 SOLUÇÃO: Foco na otimização de texto e estrutura")
                
    except Exception as e:
        print(f"❌ Erro ao analisar PDF: {e}")
        return False
    
    return True

def extract_images_for_analysis(pdf_path):
    """Extrai imagens do PDF para análise separada"""
    print(f"\n🔧 Extraindo imagens para análise...")
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            image_count = 0
            output_dir = Path("extracted_images")
            output_dir.mkdir(exist_ok=True)
            
            for page_num, page in enumerate(reader.pages):
                if '/XObject' in page['/Resources']:
                    xobjects = page['/Resources']['/XObject'].get_object()
                    
                    for obj_name, obj_ref in xobjects.items():
                        obj = obj_ref.get_object()
                        if obj.get('/Subtype') == '/Image':
                            try:
                                img_data = obj._data
                                filename = output_dir / f"page_{page_num+1}_{obj_name}.jpg"
                                
                                with open(filename, 'wb') as img_file:
                                    img_file.write(img_data)
                                
                                print(f"  ✅ Extraída: {filename}")
                                image_count += 1
                                
                                # Analisar com PIL
                                try:
                                    img = Image.open(filename)
                                    file_size = os.path.getsize(filename)
                                    print(f"    - Tamanho: {img.size}, Arquivo: {file_size:,} bytes")
                                    
                                    # Simular compactação
                                    compressed_filename = output_dir / f"compressed_{filename.name}"
                                    img.save(compressed_filename, "JPEG", quality=85, optimize=True)
                                    compressed_size = os.path.getsize(compressed_filename)
                                    reduction = ((file_size - compressed_size) / file_size) * 100
                                    print(f"    - Compactada: {compressed_size:,} bytes (redução: {reduction:.1f}%)")
                                    
                                except Exception as e:
                                    print(f"    - Erro na análise PIL: {e}")
                                    
                            except Exception as e:
                                print(f"  ❌ Erro ao extrair {obj_name}: {e}")
            
            print(f"\n📊 Total de imagens extraídas: {image_count}")
            
    except Exception as e:
        print(f"❌ Erro na extração: {e}")

def main():
    print("🔍 ANÁLISE DETALHADA DO PDF DE CERTIFICADO")
    print("=" * 60)
    
    # Encontrar o PDF
    pdf_path = find_test_pdf()
    if not pdf_path:
        print("❌ PDF não encontrado na pasta pdfArchiveTest")
        return
    
    # Analisar estrutura
    if analyze_pdf_structure(pdf_path):
        # Extrair imagens para análise
        extract_images_for_analysis(pdf_path)
    
    print("\n✅ Análise concluída!")

if __name__ == "__main__":
    main()
