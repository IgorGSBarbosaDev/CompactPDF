# 💡 Exemplos Práticos - CompactPDF

Coleção de exemplos práticos para usar o CompactPDF em diferentes cenários.

## 📋 Índice

1. [Exemplos Básicos](#exemplos-básicos)
2. [Configurações Avançadas](#configurações-avançadas)
3. [Processamento em Lote](#processamento-em-lote)
4. [Integração com Sistemas](#integração-com-sistemas)
5. [Automação e Scripts](#automação-e-scripts)
6. [Casos de Uso Específicos](#casos-de-uso-específicos)
7. [Tratamento de Erros](#tratamento-de-erros)
8. [Performance e Otimização](#performance-e-otimização)

---

## 🚀 Exemplos Básicos

### Exemplo 1: Primeira Compressão

```python
"""
Exemplo mais simples - comprimir um PDF básico.
"""
from src.pdf_compressor_facade import PDFCompressorFacade

# Criar o compressor
compressor = PDFCompressorFacade()

# Comprimir arquivo
result = compressor.compress_pdf(
    input_path='meu_documento.pdf',
    output_path='documento_comprimido.pdf'
)

# Mostrar resultados
print(f"✅ Compressão concluída!")
print(f"📊 Redução: {result.compression_percentage:.1f}%")
print(f"💾 Espaço economizado: {result.size_reduction_mb:.2f} MB")
print(f"⏱️ Tempo: {result.processing_time:.2f} segundos")
```

### Exemplo 2: Usando Presets

```python
"""
Usar presets predefinidos para diferentes necessidades.
"""
from src.pdf_compressor_facade import PDFCompressorFacade

compressor = PDFCompressorFacade()

# Para web (máxima compressão)
result_web = compressor.compress_with_preset(
    'catalogo_produtos.pdf',
    'catalogo_web.pdf',
    'web'
)

# Para impressão (alta qualidade)
result_print = compressor.compress_with_preset(
    'relatorio_anual.pdf',
    'relatorio_print.pdf',
    'print'
)

# Comparar resultados
print("🌐 Web:", f"{result_web.compression_percentage:.1f}% redução")
print("🖨️ Print:", f"{result_print.compression_percentage:.1f}% redução")
```

### Exemplo 3: Com Callback de Progresso

```python
"""
Monitorar progresso da compressão em tempo real.
"""
from src.pdf_compressor_facade import PDFCompressorFacade

def mostrar_progresso(progresso: float, mensagem: str):
    """Callback para mostrar progresso."""
    barra = "█" * int(progresso * 20)
    espacos = "░" * (20 - int(progresso * 20))
    print(f"\r[{barra}{espacos}] {progresso:.1%} - {mensagem}", end="")

compressor = PDFCompressorFacade()

result = compressor.compress_pdf(
    'arquivo_grande.pdf',
    'arquivo_comprimido.pdf',
    progress_callback=mostrar_progresso
)

print(f"\n✅ Concluído! Redução: {result.compression_percentage:.1f}%")
```

---

## ⚙️ Configurações Avançadas

### Exemplo 4: Configuração Personalizada

```python
"""
Criar configuração personalizada para necessidades específicas.
"""
from src.pdf_compressor_facade import PDFCompressorFacade
from src.config.compression_config import CompressionConfig

# Configuração personalizada para e-books
config_ebook = CompressionConfig(
    strategy='adaptive',
    quality=85,                    # Boa qualidade para leitura
    image_quality=75,              # Imagens um pouco comprimidas
    max_image_dpi=150,             # DPI adequado para telas
    convert_images_to_jpeg=True,   # JPEG para menor tamanho
    subset_fonts=True,             # Reduzir fontes não usadas
    remove_unused_fonts=True,      # Remover fontes desnecessárias
    preserve_bookmarks=True,       # Manter navegação
    preserve_annotations=True,     # Manter anotações
    create_backup=True             # Segurança
)

# Aplicar configuração
compressor = PDFCompressorFacade()
result = compressor.compress_pdf(
    'ebook_original.pdf',
    'ebook_otimizado.pdf',
    config=config_ebook
)

print(f"📚 E-book otimizado - Redução: {result.compression_percentage:.1f}%")
```

### Exemplo 5: Configuração para Diferentes Tipos

```python
"""
Configurações otimizadas para diferentes tipos de documento.
"""
from src.config.compression_config import CompressionConfig

# Para catálogos com muitas imagens
config_catalogo = CompressionConfig(
    strategy='image',              # Foco em imagens
    image_quality=60,              # Compressão agressiva
    max_image_dpi=96,              # Web resolution
    convert_images_to_jpeg=True,
    resize_large_images=True
)

# Para documentos técnicos
config_tecnico = CompressionConfig(
    strategy='content',            # Foco no conteúdo
    quality=90,                    # Alta qualidade
    preserve_quality=True,
    remove_unused_objects=True,
    optimize_structure=True,
    preserve_annotations=True      # Importante para docs técnicos
)

# Para apresentações
config_apresentacao = CompressionConfig(
    strategy='adaptive',           # Estratégia mista
    quality=80,
    image_quality=75,
    max_image_dpi=150,
    preserve_bookmarks=True,       # Navegação importante
    compress_streams=True
)

# Usar configurações
compressor = PDFCompressorFacade()

# Comprimir cada tipo
catalogo = compressor.compress_pdf('catalogo.pdf', 'catalogo_web.pdf', config_catalogo)
tecnico = compressor.compress_pdf('manual.pdf', 'manual_otim.pdf', config_tecnico)
slides = compressor.compress_pdf('slides.pdf', 'slides_final.pdf', config_apresentacao)

print("📊 Resultados:")
print(f"  Catálogo: {catalogo.compression_percentage:.1f}%")
print(f"  Técnico: {tecnico.compression_percentage:.1f}%")
print(f"  Slides: {slides.compression_percentage:.1f}%")
```

---

## 📦 Processamento em Lote

### Exemplo 6: Lote Simples

```python
"""
Comprimir múltiplos arquivos de uma vez.
"""
from src.pdf_compressor_facade import PDFCompressorFacade

compressor = PDFCompressorFacade()

# Padrões de arquivos para processar
padroes = [
    'documentos/*.pdf',
    'relatorios/2024/*.pdf',
    'propostas/**/*.pdf'
]

# Processar em lote
resultados = compressor.batch_compress(
    input_patterns=padroes,
    output_dir='comprimidos/',
    preserve_structure=True  # Manter estrutura de pastas
)

# Relatório geral
total_arquivos = len(resultados)
total_economia = sum(r.space_saved for r in resultados)
compressao_media = sum(r.compression_ratio for r in resultados) / total_arquivos

print(f"📊 Relatório do Lote:")
print(f"  Arquivos processados: {total_arquivos}")
print(f"  Espaço economizado: {total_economia / (1024*1024):.2f} MB")
print(f"  Compressão média: {compressao_media:.1%}")

# Detalhes por arquivo
for result in resultados:
    if result.success:
        print(f"  ✅ {result.input_path}: {result.compression_percentage:.1f}%")
    else:
        print(f"  ❌ {result.input_path}: {result.error_message}")
```

### Exemplo 7: Lote com Callback Personalizado

```python
"""
Processamento em lote com callback detalhado.
"""
import os
from src.pdf_compressor_facade import PDFCompressorFacade

class ProcessadorLote:
    def __init__(self):
        self.compressor = PDFCompressorFacade()
        self.arquivo_atual = 0
        self.total_arquivos = 0
        self.resultados = []
    
    def callback_progresso(self, progresso: float, mensagem: str):
        """Callback personalizado para lote."""
        print(f"[{self.arquivo_atual}/{self.total_arquivos}] "
              f"{progresso:.1%} - {mensagem}")
    
    def processar_diretorio(self, diretorio: str, output_dir: str):
        """Processa todos os PDFs de um diretório."""
        # Encontrar todos os PDFs
        pdfs = []
        for root, dirs, files in os.walk(diretorio):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdfs.append(os.path.join(root, file))
        
        self.total_arquivos = len(pdfs)
        print(f"🔍 Encontrados {self.total_arquivos} arquivos PDF")
        
        # Processar cada arquivo
        for i, pdf_path in enumerate(pdfs, 1):
            self.arquivo_atual = i
            print(f"\n📄 Processando: {os.path.basename(pdf_path)}")
            
            # Definir caminho de saída
            rel_path = os.path.relpath(pdf_path, diretorio)
            output_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            try:
                result = self.compressor.compress_pdf(
                    pdf_path,
                    output_path,
                    progress_callback=self.callback_progresso
                )
                self.resultados.append(result)
                print(f"  ✅ Redução: {result.compression_percentage:.1f}%")
                
            except Exception as e:
                print(f"  ❌ Erro: {e}")
                continue
    
    def gerar_relatorio(self):
        """Gera relatório final."""
        if not self.resultados:
            print("❌ Nenhum arquivo processado com sucesso")
            return
        
        total_original = sum(r.original_size for r in self.resultados)
        total_comprimido = sum(r.compressed_size for r in self.resultados)
        economia_total = total_original - total_comprimido
        
        print(f"\n📊 RELATÓRIO FINAL:")
        print(f"  Arquivos processados: {len(self.resultados)}")
        print(f"  Tamanho original: {total_original / (1024*1024):.2f} MB")
        print(f"  Tamanho comprimido: {total_comprimido / (1024*1024):.2f} MB")
        print(f"  Economia total: {economia_total / (1024*1024):.2f} MB")
        print(f"  Redução média: {(economia_total/total_original):.1%}")

# Usar o processador
processador = ProcessadorLote()
processador.processar_diretorio('documentos/', 'comprimidos/')
processador.gerar_relatorio()
```

---

## 🔧 Integração com Sistemas

### Exemplo 8: Integração com Flask

```python
"""
API Flask para compressão de PDFs via web.
"""
from flask import Flask, request, send_file, jsonify
import os
import tempfile
from src.pdf_compressor_facade import PDFCompressorFacade

app = Flask(__name__)
compressor = PDFCompressorFacade()

@app.route('/compress', methods=['POST'])
def compress_pdf():
    """Endpoint para compressão de PDF."""
    try:
        # Verificar se arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nome de arquivo vazio'}), 400
        
        # Obter parâmetros
        preset = request.form.get('preset', 'balanced')
        
        # Salvar arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_input:
            file.save(temp_input.name)
            input_path = temp_input.name
        
        # Definir arquivo de saída
        output_path = input_path.replace('.pdf', '_compressed.pdf')
        
        # Comprimir
        result = compressor.compress_with_preset(
            input_path, output_path, preset
        )
        
        # Limpar arquivo de entrada
        os.unlink(input_path)
        
        # Retornar arquivo comprimido
        return send_file(
            output_path,
            as_attachment=True,
            download_name='compressed.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_pdf():
    """Endpoint para análise de PDF."""
    try:
        file = request.files['file']
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            file.save(temp_file.name)
            
            # Analisar PDF
            analysis = compressor.analyze_pdf(temp_file.name)
            
            # Limpar arquivo temporário
            os.unlink(temp_file.name)
            
            return jsonify({
                'file_size': analysis.file_size,
                'page_count': analysis.page_count,
                'has_images': analysis.has_images,
                'image_count': analysis.image_count,
                'optimization_potential': analysis.get_optimization_potential(),
                'recommended_strategies': analysis.recommended_strategies
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### Exemplo 9: Integração com Django

```python
"""
Views Django para compressão de PDFs.
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
import json
import tempfile
import os
from src.pdf_compressor_facade import PDFCompressorFacade

compressor = PDFCompressorFacade()

@csrf_exempt
@require_http_methods(["POST"])
def compress_pdf_view(request):
    """View para compressão de PDF."""
    try:
        # Obter arquivo e parâmetros
        pdf_file = request.FILES.get('pdf')
        if not pdf_file:
            return JsonResponse({'error': 'PDF file required'}, status=400)
        
        # Parâmetros de compressão
        preset = request.POST.get('preset', 'balanced')
        create_backup = request.POST.get('backup', 'true').lower() == 'true'
        
        # Salvar arquivo temporariamente
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_input:
            for chunk in pdf_file.chunks():
                temp_input.write(chunk)
            input_path = temp_input.name
        
        # Definir saída
        output_path = input_path.replace('.pdf', '_compressed.pdf')
        
        # Configurar compressão
        from src.config.compression_config import CompressionConfig
        config = CompressionConfig.from_preset(preset)
        config.create_backup = create_backup
        
        # Comprimir
        result = compressor.compress_pdf(input_path, output_path, config)
        
        # Ler arquivo comprimido
        with open(output_path, 'rb') as f:
            compressed_data = f.read()
        
        # Limpar arquivos temporários
        os.unlink(input_path)
        os.unlink(output_path)
        
        # Retornar dados
        response = HttpResponse(compressed_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="compressed_{pdf_file.name}"'
        response['X-Compression-Ratio'] = str(result.compression_ratio)
        response['X-Space-Saved'] = str(result.space_saved)
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def pdf_analysis_view(request):
    """View para análise de PDF."""
    try:
        pdf_file = request.FILES.get('pdf')
        if not pdf_file:
            return JsonResponse({'error': 'PDF file required'}, status=400)
        
        # Salvar temporariamente
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            for chunk in pdf_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name
        
        # Analisar
        analysis = compressor.analyze_pdf(temp_path)
        recommendations = compressor.get_compression_recommendations(temp_path)
        
        # Limpar
        os.unlink(temp_path)
        
        return JsonResponse({
            'analysis': {
                'file_size': analysis.file_size,
                'page_count': analysis.page_count,
                'has_images': analysis.has_images,
                'image_count': analysis.image_count,
                'has_fonts': analysis.font_count > 0,
                'complexity_score': analysis.complexity_score,
                'content_distribution': analysis.get_content_distribution()
            },
            'recommendations': {
                'best_strategy': recommendations.best_strategy,
                'estimated_reduction': recommendations.estimated_reduction,
                'recommended_preset': recommendations.recommended_preset
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

---

## 🤖 Automação e Scripts

### Exemplo 10: Script de Monitoramento

```python
"""
Script para monitorar pasta e comprimir PDFs automaticamente.
"""
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.pdf_compressor_facade import PDFCompressorFacade

class PDFHandler(FileSystemEventHandler):
    def __init__(self, output_dir: str):
        self.compressor = PDFCompressorFacade()
        self.output_dir = output_dir
        
    def on_created(self, event):
        """Chamado quando novo arquivo é criado."""
        if event.is_directory:
            return
            
        if event.src_path.lower().endswith('.pdf'):
            print(f"📄 Novo PDF detectado: {event.src_path}")
            self.processar_pdf(event.src_path)
    
    def processar_pdf(self, file_path: str):
        """Processa um PDF recém-criado."""
        try:
            # Aguardar arquivo ser completamente escrito
            time.sleep(2)
            
            # Definir caminho de saída
            filename = os.path.basename(file_path)
            output_path = os.path.join(self.output_dir, f"compressed_{filename}")
            
            # Analisar e comprimir
            analysis = self.compressor.analyze_pdf(file_path)
            
            # Escolher preset baseado na análise
            if analysis.has_images and analysis.image_count > 5:
                preset = 'web'
            elif analysis.complexity_score > 0.7:
                preset = 'balanced'
            else:
                preset = 'quality'
            
            print(f"🔄 Comprimindo com preset: {preset}")
            
            result = self.compressor.compress_with_preset(
                file_path, output_path, preset
            )
            
            print(f"✅ Comprimido! Redução: {result.compression_percentage:.1f}%")
            print(f"💾 Salvo em: {output_path}")
            
        except Exception as e:
            print(f"❌ Erro ao processar {file_path}: {e}")

def monitorar_pasta(pasta_origem: str, pasta_destino: str):
    """Monitora pasta para novos PDFs."""
    # Criar pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Configurar observer
    event_handler = PDFHandler(pasta_destino)
    observer = Observer()
    observer.schedule(event_handler, pasta_origem, recursive=True)
    
    # Iniciar monitoramento
    observer.start()
    print(f"👀 Monitorando {pasta_origem} para novos PDFs...")
    print(f"📁 Comprimidos serão salvos em {pasta_destino}")
    print("Pressione Ctrl+C para parar")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Monitoramento interrompido")
    
    observer.join()

if __name__ == "__main__":
    monitorar_pasta("documentos_novos/", "documentos_comprimidos/")
```

### Exemplo 11: Script de Otimização Agendada

```python
"""
Script para otimização agendada de PDFs.
"""
import schedule
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from src.pdf_compressor_facade import PDFCompressorFacade

class OtimizadorAgendado:
    def __init__(self, config_email=None):
        self.compressor = PDFCompressorFacade()
        self.config_email = config_email
        self.log_file = 'compression_log.txt'
    
    def log(self, mensagem: str):
        """Registra mensagem no log."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {mensagem}\n"
        
        print(log_entry.strip())
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def otimizar_diretorio(self, diretorio: str, output_dir: str):
        """Otimiza todos os PDFs de um diretório."""
        self.log(f"Iniciando otimização de {diretorio}")
        
        # Encontrar PDFs
        pdfs = []
        for root, dirs, files in os.walk(diretorio):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdfs.append(os.path.join(root, file))
        
        if not pdfs:
            self.log("Nenhum PDF encontrado")
            return
        
        self.log(f"Encontrados {len(pdfs)} PDFs para otimizar")
        
        # Estatísticas
        sucessos = 0
        falhas = 0
        economia_total = 0
        
        # Processar cada PDF
        for pdf_path in pdfs:
            try:
                # Verificar se já foi processado
                rel_path = os.path.relpath(pdf_path, diretorio)
                output_path = os.path.join(output_dir, rel_path)
                
                if os.path.exists(output_path):
                    self.log(f"Pulando {rel_path} (já processado)")
                    continue
                
                # Criar diretório de saída
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Comprimir
                result = self.compressor.compress_with_preset(
                    pdf_path, output_path, 'balanced'
                )
                
                sucessos += 1
                economia_total += result.space_saved
                
                self.log(f"✅ {rel_path}: {result.compression_percentage:.1f}% redução")
                
            except Exception as e:
                falhas += 1
                self.log(f"❌ Erro em {rel_path}: {e}")
        
        # Relatório final
        economia_mb = economia_total / (1024 * 1024)
        self.log(f"Otimização concluída: {sucessos} sucessos, {falhas} falhas")
        self.log(f"Economia total: {economia_mb:.2f} MB")
        
        # Enviar email se configurado
        if self.config_email:
            self.enviar_relatorio(sucessos, falhas, economia_mb)
    
    def enviar_relatorio(self, sucessos: int, falhas: int, economia_mb: float):
        """Envia relatório por email."""
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = self.config_email['from']
            msg['To'] = self.config_email['to']
            msg['Subject'] = 'Relatório de Otimização de PDFs'
            
            # Corpo do email
            corpo = f"""
            Relatório de Otimização de PDFs
            Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            
            Resultados:
            - Arquivos processados com sucesso: {sucessos}
            - Arquivos com falha: {falhas}
            - Economia total de espaço: {economia_mb:.2f} MB
            
            Log completo em anexo.
            """
            
            msg.attach(MIMEText(corpo, 'plain'))
            
            # Enviar email
            server = smtplib.SMTP(self.config_email['smtp_server'], self.config_email['port'])
            server.starttls()
            server.login(self.config_email['user'], self.config_email['password'])
            server.send_message(msg)
            server.quit()
            
            self.log("📧 Relatório enviado por email")
            
        except Exception as e:
            self.log(f"❌ Erro ao enviar email: {e}")

# Configuração
config_email = {
    'from': 'sistema@empresa.com',
    'to': 'admin@empresa.com',
    'smtp_server': 'smtp.empresa.com',
    'port': 587,
    'user': 'sistema@empresa.com',
    'password': 'senha'
}

otimizador = OtimizadorAgendado(config_email)

# Agendar tarefas
schedule.every().day.at("02:00").do(
    otimizador.otimizar_diretorio,
    "documentos_empresa/",
    "documentos_otimizados/"
)

schedule.every().sunday.at("01:00").do(
    otimizador.otimizar_diretorio,
    "arquivos_historicos/",
    "historicos_otimizados/"
)

# Executar scheduler
print("🕐 Scheduler iniciado")
print("📅 Otimização diária às 02:00")
print("📅 Otimização semanal aos domingos 01:00")

while True:
    schedule.run_pending()
    time.sleep(60)  # Verificar a cada minuto
```

---

## 🎯 Casos de Uso Específicos

### Exemplo 12: Sistema de E-commerce

```python
"""
Otimização automática de catálogos para e-commerce.
"""
from src.pdf_compressor_facade import PDFCompressorFacade
from src.config.compression_config import CompressionConfig

class OtimizadorEcommerce:
    def __init__(self):
        self.compressor = PDFCompressorFacade()
    
    def otimizar_catalogo(self, catalogo_path: str):
        """Otimiza catálogo para diferentes canais."""
        # Analisar catálogo original
        analysis = self.compressor.analyze_pdf(catalogo_path)
        
        print(f"📄 Catálogo: {os.path.basename(catalogo_path)}")
        print(f"📊 Páginas: {analysis.page_count}")
        print(f"🖼️ Imagens: {analysis.image_count}")
        print(f"💾 Tamanho: {analysis.file_size / (1024*1024):.2f} MB")
        
        # Configurações para diferentes canais
        configs = {
            'web_mobile': CompressionConfig(
                strategy='image',
                quality=50,
                image_quality=60,
                max_image_dpi=72,
                convert_images_to_jpeg=True,
                resize_large_images=True
            ),
            'web_desktop': CompressionConfig(
                strategy='adaptive',
                quality=70,
                image_quality=75,
                max_image_dpi=96,
                convert_images_to_jpeg=True
            ),
            'email': CompressionConfig(
                strategy='adaptive',
                quality=60,
                image_quality=65,
                max_image_dpi=96,
                convert_images_to_jpeg=True,
                remove_unused_objects=True
            ),
            'impressao': CompressionConfig(
                strategy='content',
                quality=90,
                image_quality=85,
                max_image_dpi=300,
                preserve_quality=True,
                convert_images_to_jpeg=False
            )
        }
        
        # Gerar versões otimizadas
        resultados = {}
        base_name = os.path.splitext(catalogo_path)[0]
        
        for canal, config in configs.items():
            output_path = f"{base_name}_{canal}.pdf"
            
            print(f"\n🔄 Otimizando para {canal}...")
            
            result = self.compressor.compress_pdf(
                catalogo_path, output_path, config
            )
            
            resultados[canal] = {
                'path': output_path,
                'size_mb': result.compressed_size / (1024*1024),
                'reduction': result.compression_percentage,
                'suitable_for': self._get_canal_info(canal)
            }
            
            print(f"  ✅ Redução: {result.compression_percentage:.1f}%")
            print(f"  💾 Tamanho final: {result.compressed_size / (1024*1024):.2f} MB")
        
        # Relatório final
        self._gerar_relatorio_canais(resultados)
        
        return resultados
    
    def _get_canal_info(self, canal: str) -> dict:
        """Informações sobre cada canal."""
        info = {
            'web_mobile': {
                'descricao': 'Dispositivos móveis',
                'max_size_mb': 5,
                'prioridade': 'velocidade'
            },
            'web_desktop': {
                'descricao': 'Navegadores desktop',
                'max_size_mb': 10,
                'prioridade': 'qualidade_velocidade'
            },
            'email': {
                'descricao': 'Anexos de email',
                'max_size_mb': 8,
                'prioridade': 'compatibilidade'
            },
            'impressao': {
                'descricao': 'Impressão profissional',
                'max_size_mb': 50,
                'prioridade': 'qualidade_maxima'
            }
        }
        return info.get(canal, {})
    
    def _gerar_relatorio_canais(self, resultados: dict):
        """Gera relatório das versões criadas."""
        print(f"\n📊 RELATÓRIO DE OTIMIZAÇÃO POR CANAL:")
        print("=" * 60)
        
        for canal, dados in resultados.items():
            info = dados['suitable_for']
            print(f"\n📱 {canal.upper()}")
            print(f"  Descrição: {info.get('descricao', 'N/A')}")
            print(f"  Tamanho: {dados['size_mb']:.2f} MB")
            print(f"  Redução: {dados['reduction']:.1f}%")
            print(f"  Limite recomendado: {info.get('max_size_mb', 'N/A')} MB")
            
            # Verificar se está dentro do limite
            max_size = info.get('max_size_mb')
            if max_size and dados['size_mb'] > max_size:
                print(f"  ⚠️ ATENÇÃO: Excede limite recomendado!")
            else:
                print(f"  ✅ Dentro do limite recomendado")
        
        print("\n🎯 Recomendações:")
        print("  • Mobile: Para carregamento rápido em 3G/4G")
        print("  • Desktop: Balanceamento qualidade/velocidade")
        print("  • Email: Compatibilidade máxima com clientes")
        print("  • Impressão: Qualidade profissional para gráficas")

# Usar otimizador
otimizador = OtimizadorEcommerce()

# Otimizar catálogo de produtos
resultados = otimizador.otimizar_catalogo('catalogo_produtos_2024.pdf')

# Usar resultados para upload automático
for canal, dados in resultados.items():
    print(f"📤 {canal}: {dados['path']} pronto para upload")
```

### Exemplo 13: Sistema Educacional

```python
"""
Otimização de materiais educacionais.
"""
import os
from src.pdf_compressor_facade import PDFCompressorFacade
from src.config.compression_config import CompressionConfig

class OtimizadorEducacional:
    def __init__(self):
        self.compressor = PDFCompressorFacade()
    
    def processar_material_didatico(self, material_path: str, tipo_material: str):
        """Processa material didático baseado no tipo."""
        # Analisar material
        analysis = self.compressor.analyze_pdf(material_path)
        
        # Configurações por tipo de material
        configs = self._get_config_por_tipo(tipo_material, analysis)
        
        # Gerar versões
        base_name = os.path.splitext(material_path)[0]
        resultados = {}
        
        for versao, config in configs.items():
            output_path = f"{base_name}_{versao}.pdf"
            
            print(f"📚 Gerando versão {versao}...")
            
            result = self.compressor.compress_pdf(
                material_path, output_path, config
            )
            
            resultados[versao] = {
                'path': output_path,
                'size_mb': result.compressed_size / (1024*1024),
                'reduction': result.compression_percentage,
                'uso_recomendado': self._get_uso_recomendado(versao)
            }
            
            print(f"  ✅ {result.compression_percentage:.1f}% redução")
            print(f"  💾 {result.compressed_size / (1024*1024):.2f} MB")
        
        return resultados
    
    def _get_config_por_tipo(self, tipo: str, analysis) -> dict:
        """Configurações específicas por tipo de material."""
        if tipo == 'apostila':
            return {
                'estudantes': CompressionConfig(
                    strategy='adaptive',
                    quality=75,
                    image_quality=70,
                    max_image_dpi=150,
                    subset_fonts=True,
                    preserve_bookmarks=True
                ),
                'professores': CompressionConfig(
                    strategy='content',
                    quality=85,
                    image_quality=80,
                    max_image_dpi=200,
                    preserve_quality=True,
                    preserve_annotations=True
                ),
                'impressao': CompressionConfig(
                    strategy='balanced',
                    quality=90,
                    image_quality=85,
                    max_image_dpi=300,
                    convert_images_to_jpeg=False
                )
            }
        
        elif tipo == 'slides':
            return {
                'aula_online': CompressionConfig(
                    strategy='image',
                    quality=65,
                    image_quality=70,
                    max_image_dpi=96,
                    convert_images_to_jpeg=True
                ),
                'download_estudantes': CompressionConfig(
                    strategy='adaptive',
                    quality=75,
                    image_quality=75,
                    max_image_dpi=150
                ),
                'arquivo_professor': CompressionConfig(
                    quality=90,
                    preserve_quality=True,
                    preserve_annotations=True
                )
            }
        
        elif tipo == 'prova':
            return {
                'digital': CompressionConfig(
                    strategy='content',
                    quality=80,
                    preserve_quality=True,
                    remove_unused_objects=True,
                    preserve_forms=True
                ),
                'impressao': CompressionConfig(
                    quality=95,
                    image_quality=90,
                    max_image_dpi=300,
                    preserve_quality=True,
                    convert_images_to_jpeg=False
                )
            }
        
        else:  # material genérico
            return {
                'web': CompressionConfig(strategy='adaptive', quality=75),
                'download': CompressionConfig(strategy='balanced', quality=80),
                'impressao': CompressionConfig(quality=90, preserve_quality=True)
            }
    
    def _get_uso_recomendado(self, versao: str) -> str:
        """Descrição do uso recomendado para cada versão."""
        recomendacoes = {
            'estudantes': 'Download pelos alunos, visualização em dispositivos',
            'professores': 'Uso docente, anotações, preparação de aulas',
            'aula_online': 'Projeção em aulas online, compartilhamento rápido',
            'download_estudantes': 'Download pelos estudantes para estudo',
            'arquivo_professor': 'Arquivo principal do professor com qualidade máxima',
            'digital': 'Aplicação digital, formulários interativos',
            'impressao': 'Impressão profissional, qualidade gráfica',
            'web': 'Visualização web, carregamento rápido',
            'download': 'Download geral, uso offline'
        }
        return recomendacoes.get(versao, 'Uso geral')
    
    def processar_curso_completo(self, diretorio_curso: str):
        """Processa todos os materiais de um curso."""
        print(f"🎓 Processando curso: {diretorio_curso}")
        
        # Mapear tipos de arquivo
        tipos_arquivo = {
            'apostila': ['apostila', 'manual', 'livro'],
            'slides': ['slides', 'apresentacao', 'aula'],
            'prova': ['prova', 'exame', 'teste', 'avaliacao'],
            'exercicio': ['exercicio', 'lista', 'atividade']
        }
        
        resultados_curso = {}
        
        # Processar cada PDF no diretório
        for root, dirs, files in os.walk(diretorio_curso):
            for file in files:
                if not file.lower().endswith('.pdf'):
                    continue
                
                file_path = os.path.join(root, file)
                
                # Determinar tipo baseado no nome
                tipo_detectado = 'generico'
                for tipo, palavras_chave in tipos_arquivo.items():
                    if any(palavra in file.lower() for palavra in palavras_chave):
                        tipo_detectado = tipo
                        break
                
                print(f"\n📄 {file} (tipo: {tipo_detectado})")
                
                # Processar arquivo
                try:
                    resultado = self.processar_material_didatico(file_path, tipo_detectado)
                    resultados_curso[file] = {
                        'tipo': tipo_detectado,
                        'versoes': resultado
                    }
                except Exception as e:
                    print(f"  ❌ Erro: {e}")
                    continue
        
        # Relatório do curso
        self._gerar_relatorio_curso(resultados_curso)
        return resultados_curso
    
    def _gerar_relatorio_curso(self, resultados: dict):
        """Gera relatório completo do curso."""
        print(f"\n📊 RELATÓRIO DO CURSO:")
        print("=" * 50)
        
        total_arquivos = len(resultados)
        total_versoes = sum(len(dados['versoes']) for dados in resultados.values())
        
        print(f"📚 Arquivos processados: {total_arquivos}")
        print(f"📄 Versões geradas: {total_versoes}")
        
        # Estatísticas por tipo
        tipos = {}
        for arquivo, dados in resultados.items():
            tipo = dados['tipo']
            if tipo not in tipos:
                tipos[tipo] = {'arquivos': 0, 'versoes': 0}
            tipos[tipo]['arquivos'] += 1
            tipos[tipo]['versoes'] += len(dados['versoes'])
        
        print(f"\n📋 Por tipo de material:")
        for tipo, stats in tipos.items():
            print(f"  {tipo.title()}: {stats['arquivos']} arquivos, {stats['versoes']} versões")

# Usar otimizador educacional
otimizador = OtimizadorEducacional()

# Processar material específico
resultado_apostila = otimizador.processar_material_didatico(
    'Apostila_Python_Avancado.pdf', 
    'apostila'
)

# Processar curso completo
resultado_curso = otimizador.processar_curso_completo('Curso_Python_2024/')
```

---

## 🚨 Tratamento de Erros

### Exemplo 14: Tratamento Robusto de Erros

```python
"""
Exemplos de tratamento robusto de erros.
"""
import logging
import traceback
from src.pdf_compressor_facade import PDFCompressorFacade
from src.exceptions import (
    CompressionError, InvalidPDFError, 
    QualityThresholdError, DiskSpaceError
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('compression_errors.log'),
        logging.StreamHandler()
    ]
)

class CompressorRobusto:
    def __init__(self):
        self.compressor = PDFCompressorFacade()
        self.logger = logging.getLogger(__name__)
    
    def comprimir_com_fallback(self, input_path: str, output_path: str):
        """Comprime PDF com estratégias de fallback."""
        estrategias = ['adaptive', 'balanced', 'quality']
        
        for i, estrategia in enumerate(estrategias):
            try:
                self.logger.info(f"Tentativa {i+1}: estratégia {estrategia}")
                
                config = CompressionConfig.from_preset(estrategia)
                
                result = self.compressor.compress_pdf(
                    input_path, output_path, config
                )
                
                self.logger.info(f"✅ Sucesso com {estrategia}")
                return result
                
            except QualityThresholdError as e:
                self.logger.warning(f"Qualidade insuficiente com {estrategia}: {e}")
                if i == len(estrategias) - 1:
                    raise CompressionError(f"Todas as estratégias falharam: qualidade abaixo do threshold")
                continue
                
            except InvalidPDFError as e:
                self.logger.error(f"PDF inválido: {e}")
                raise  # Não há fallback para PDF inválido
                
            except DiskSpaceError as e:
                self.logger.error(f"Espaço insuficiente: {e}")
                raise  # Não há fallback para falta de espaço
                
            except CompressionError as e:
                self.logger.warning(f"Falha na compressão com {estrategia}: {e}")
                if i == len(estrategias) - 1:
                    raise CompressionError(f"Todas as estratégias falharam: {e}")
                continue
                
            except Exception as e:
                self.logger.error(f"Erro inesperado com {estrategia}: {e}")
                self.logger.debug(traceback.format_exc())
                if i == len(estrategias) - 1:
                    raise CompressionError(f"Erro inesperado: {e}")
                continue
    
    def processar_lote_robusto(self, arquivos: list, output_dir: str):
        """Processa lote com recuperação de erros."""
        resultados = {
            'sucessos': [],
            'falhas': [],
            'recuperados': []
        }
        
        for arquivo in arquivos:
            try:
                output_path = os.path.join(output_dir, os.path.basename(arquivo))
                
                # Tentativa principal
                result = self.comprimir_com_fallback(arquivo, output_path)
                
                resultados['sucessos'].append({
                    'arquivo': arquivo,
                    'resultado': result
                })
                
            except InvalidPDFError as e:
                self.logger.error(f"PDF inválido {arquivo}: {e}")
                resultados['falhas'].append({
                    'arquivo': arquivo,
                    'erro': 'PDF inválido',
                    'detalhes': str(e)
                })
                
            except DiskSpaceError as e:
                self.logger.error(f"Espaço insuficiente para {arquivo}: {e}")
                resultados['falhas'].append({
                    'arquivo': arquivo,
                    'erro': 'Espaço insuficiente',
                    'detalhes': str(e)
                })
                
            except CompressionError as e:
                # Tentar recuperação com configuração mínima
                try:
                    self.logger.warning(f"Tentando recuperação para {arquivo}")
                    
                    config_minima = CompressionConfig(
                        strategy='content',
                        quality=95,
                        preserve_quality=True,
                        remove_unused_objects=True
                    )
                    
                    output_path_rec = output_path.replace('.pdf', '_minimal.pdf')
                    result = self.compressor.compress_pdf(
                        arquivo, output_path_rec, config_minima
                    )
                    
                    resultados['recuperados'].append({
                        'arquivo': arquivo,
                        'resultado': result,
                        'tipo_recuperacao': 'configuracao_minima'
                    })
                    
                except Exception as e_rec:
                    self.logger.error(f"Recuperação falhou para {arquivo}: {e_rec}")
                    resultados['falhas'].append({
                        'arquivo': arquivo,
                        'erro': 'Compressão falhou',
                        'detalhes': str(e),
                        'recuperacao_falhou': str(e_rec)
                    })
            
            except Exception as e:
                self.logger.error(f"Erro inesperado com {arquivo}: {e}")
                self.logger.debug(traceback.format_exc())
                resultados['falhas'].append({
                    'arquivo': arquivo,
                    'erro': 'Erro inesperado',
                    'detalhes': str(e)
                })
        
        # Gerar relatório
        self._gerar_relatorio_robusto(resultados)
        return resultados
    
    def _gerar_relatorio_robusto(self, resultados: dict):
        """Gera relatório detalhado de processamento robusto."""
        total = len(resultados['sucessos']) + len(resultados['falhas']) + len(resultados['recuperados'])
        
        print(f"\n📊 RELATÓRIO DE PROCESSAMENTO ROBUSTO:")
        print("=" * 50)
        print(f"📁 Total de arquivos: {total}")
        print(f"✅ Sucessos: {len(resultados['sucessos'])}")
        print(f"🔄 Recuperados: {len(resultados['recuperados'])}")
        print(f"❌ Falhas: {len(resultados['falhas'])}")
        print(f"📈 Taxa de sucesso: {((len(resultados['sucessos']) + len(resultados['recuperados'])) / total * 100):.1f}%")
        
        # Detalhes das falhas
        if resultados['falhas']:
            print(f"\n❌ FALHAS DETALHADAS:")
            for falha in resultados['falhas']:
                print(f"  📄 {falha['arquivo']}")
                print(f"    Erro: {falha['erro']}")
                print(f"    Detalhes: {falha['detalhes'][:100]}...")
        
        # Detalhes das recuperações
        if resultados['recuperados']:
            print(f"\n🔄 RECUPERAÇÕES:")
            for rec in resultados['recuperados']:
                result = rec['resultado']
                print(f"  📄 {rec['arquivo']}")
                print(f"    Método: {rec['tipo_recuperacao']}")
                print(f"    Redução: {result.compression_percentage:.1f}%")

# Usar compressor robusto
compressor = CompressorRobusto()

# Teste com arquivo individual
try:
    result = compressor.comprimir_com_fallback(
        'documento_problematico.pdf',
        'documento_recuperado.pdf'
    )
    print(f"✅ Sucesso: {result.compression_percentage:.1f}% redução")
except Exception as e:
    print(f"❌ Falha total: {e}")

# Teste com lote
arquivos_teste = [
    'documento1.pdf',
    'arquivo_corrompido.pdf',
    'pdf_muito_grande.pdf',
    'documento_normal.pdf'
]

resultados = compressor.processar_lote_robusto(arquivos_teste, 'saida_robusta/')
```

---

## ⚡ Performance e Otimização

### Exemplo 15: Processamento Paralelo

```python
"""
Exemplo de processamento paralelo para melhor performance.
"""
import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from src.pdf_compressor_facade import PDFCompressorFacade

class CompressorParalelo:
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(cpu_count(), 8)
        self.compressor = PDFCompressorFacade()
    
    def comprimir_arquivo(self, args: tuple) -> dict:
        """Comprime um único arquivo (para uso em paralelo)."""
        input_path, output_path, config = args
        
        start_time = time.time()
        
        try:
            result = self.compressor.compress_pdf(input_path, output_path, config)
            
            return {
                'sucesso': True,
                'input_path': input_path,
                'output_path': output_path,
                'resultado': result,
                'tempo': time.time() - start_time
            }
            
        except Exception as e:
            return {
                'sucesso': False,
                'input_path': input_path,
                'erro': str(e),
                'tempo': time.time() - start_time
            }
    
    def processar_lote_paralelo(
        self, 
        arquivos: list, 
        output_dir: str, 
        config: CompressionConfig = None,
        use_processes: bool = False
    ):
        """Processa lote de arquivos em paralelo."""
        os.makedirs(output_dir, exist_ok=True)
        
        if config is None:
            config = CompressionConfig.from_preset('balanced')
        
        # Preparar argumentos
        args_list = []
        for input_path in arquivos:
            filename = os.path.basename(input_path)
            output_path = os.path.join(output_dir, filename)
            args_list.append((input_path, output_path, config))
        
        print(f"🚀 Iniciando processamento paralelo")
        print(f"📁 Arquivos: {len(arquivos)}")
        print(f"👥 Workers: {self.max_workers}")
        print(f"⚙️ Método: {'Processes' if use_processes else 'Threads'}")
        
        start_time = time.time()
        resultados = []
        
        # Escolher executor
        ExecutorClass = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
        
        with ExecutorClass(max_workers=self.max_workers) as executor:
            # Submeter todas as tarefas
            future_to_args = {
                executor.submit(self.comprimir_arquivo, args): args 
                for args in args_list
            }
            
            # Coletar resultados conforme completam
            for i, future in enumerate(as_completed(future_to_args), 1):
                resultado = future.result()
                resultados.append(resultado)
                
                # Mostrar progresso
                if resultado['sucesso']:
                    comp_ratio = resultado['resultado'].compression_percentage
                    print(f"[{i}/{len(arquivos)}] ✅ {os.path.basename(resultado['input_path'])}: {comp_ratio:.1f}%")
                else:
                    print(f"[{i}/{len(arquivos)}] ❌ {os.path.basename(resultado['input_path'])}: {resultado['erro']}")
        
        tempo_total = time.time() - start_time
        
        # Relatório de performance
        self._relatorio_performance_paralelo(resultados, tempo_total)
        
        return resultados
    
    def comparar_performance(self, arquivos: list, output_dir: str):
        """Compara performance entre métodos sequencial, threads e processes."""
        config = CompressionConfig.from_preset('balanced')
        
        print("🏁 COMPARAÇÃO DE PERFORMANCE")
        print("=" * 50)
        
        # Teste sequencial
        print("\n1️⃣ Processamento Sequencial:")
        start_seq = time.time()
        resultados_seq = []
        
        for arquivo in arquivos:
            output_path = os.path.join(output_dir, f"seq_{os.path.basename(arquivo)}")
            try:
                result = self.compressor.compress_pdf(arquivo, output_path, config)
                resultados_seq.append({'sucesso': True, 'resultado': result})
            except Exception as e:
                resultados_seq.append({'sucesso': False, 'erro': str(e)})
        
        tempo_seq = time.time() - start_seq
        
        # Teste com threads
        print("\n2️⃣ Processamento com Threads:")
        arquivos_thread = [arquivo for arquivo in arquivos]
        output_thread = os.path.join(output_dir, 'threads')
        resultados_thread = self.processar_lote_paralelo(
            arquivos_thread, output_thread, config, use_processes=False
        )
        tempo_thread = sum(r.get('tempo', 0) for r in resultados_thread)
        
        # Teste com processes
        print("\n3️⃣ Processamento com Processes:")
        arquivos_process = [arquivo for arquivo in arquivos]
        output_process = os.path.join(output_dir, 'processes')
        resultados_process = self.processar_lote_paralelo(
            arquivos_process, output_process, config, use_processes=True
        )
        tempo_process = sum(r.get('tempo', 0) for r in resultados_process)
        
        # Comparação final
        print(f"\n📊 RESULTADOS DA COMPARAÇÃO:")
        print(f"  Sequencial: {tempo_seq:.2f}s")
        print(f"  Threads:    {tempo_thread:.2f}s (speedup: {tempo_seq/tempo_thread:.2f}x)")
        print(f"  Processes:  {tempo_process:.2f}s (speedup: {tempo_seq/tempo_process:.2f}x)")
        
        # Recomendação
        if tempo_thread < tempo_process:
            print(f"🏆 Recomendação: Usar Threads para este workload")
        else:
            print(f"🏆 Recomendação: Usar Processes para este workload")
    
    def _relatorio_performance_paralelo(self, resultados: list, tempo_total: float):
        """Gera relatório de performance do processamento paralelo."""
        sucessos = [r for r in resultados if r['sucesso']]
        falhas = [r for r in resultados if not r['sucesso']]
        
        if sucessos:
            tempos = [r['tempo'] for r in sucessos]
            compressoes = [r['resultado'].compression_percentage for r in sucessos]
            
            tempo_medio = sum(tempos) / len(tempos)
            compressao_media = sum(compressoes) / len(compressoes)
            
            print(f"\n📊 RELATÓRIO DE PERFORMANCE:")
            print(f"  ✅ Sucessos: {len(sucessos)}")
            print(f"  ❌ Falhas: {len(falhas)}")
            print(f"  ⏱️ Tempo total: {tempo_total:.2f}s")
            print(f"  ⏱️ Tempo médio por arquivo: {tempo_medio:.2f}s")
            print(f"  📈 Compressão média: {compressao_media:.1f}%")
            print(f"  🚀 Throughput: {len(sucessos)/tempo_total:.2f} arquivos/segundo")

# Exemplo de uso
compressor_paralelo = CompressorParalelo(max_workers=4)

# Arquivos de teste
arquivos_teste = [
    'documento1.pdf',
    'catalogo.pdf',
    'relatorio.pdf',
    'apostila.pdf',
    'apresentacao.pdf'
]

# Processamento paralelo com threads
resultados = compressor_paralelo.processar_lote_paralelo(
    arquivos_teste,
    'saida_paralela/',
    use_processes=False
)

# Comparação de métodos
compressor_paralelo.comparar_performance(arquivos_teste, 'comparacao_performance/')
```

---

*🎯 Estes exemplos cobrem os principais casos de uso do CompactPDF. Para casos específicos não cobertos, consulte a [API Reference](API_REFERENCE.md) ou abra uma issue no repositório.*
