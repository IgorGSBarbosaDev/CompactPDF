# 📖 Manual Completo do Usuário - CompactPDF

Guia completo para usar todas as funcionalidades do CompactPDF de forma eficiente.

## 📋 Índice

1. [Introdução](#introdução)
2. [Interface de Linha de Comando](#interface-de-linha-de-comando)
3. [Perfis de Compressão](#perfis-de-compressão)
4. [Estratégias de Compressão](#estratégias-de-compressão)
5. [Configurações Personalizadas](#configurações-personalizadas)
6. [Funcionalidades Avançadas](#funcionalidades-avançadas)
7. [Processamento em Lote](#processamento-em-lote)
8. [Monitoramento e Analytics](#monitoramento-e-analytics)
9. [Integração com Scripts](#integração-com-scripts)
10. [Casos de Uso Comuns](#casos-de-uso-comuns)

---

## 🎯 Introdução

O CompactPDF é um sistema inteligente de compressão de PDF que utiliza múltiplas estratégias para otimizar documentos mantendo a qualidade visual. O sistema segue princípios SOLID e oferece:

- **🧠 Compressão Inteligente** - Análise automática do conteúdo
- **📊 4 Estratégias Especializadas** - Cada uma otimizada para diferentes tipos de conteúdo
- **⚡ Alta Performance** - Cache e otimizações avançadas
- **🛡️ Segurança** - Sistema completo de backup e recuperação
- **📈 Analytics** - Relatórios detalhados de performance

---

## 🖥️ Interface de Linha de Comando

### Sintaxe Básica
```bash
python main.py [arquivo(s)] [opções]
```

### Argumentos Obrigatórios
- `input` - Um ou mais arquivos PDF para comprimir

### Argumentos Opcionais

#### **📁 Entrada e Saída**
```bash
-o, --output ARQUIVO        # Arquivo de saída específico
--output-dir DIRETÓRIO      # Diretório de saída para lote
--batch                     # Modo de processamento em lote
```

#### **🎯 Configuração de Compressão**
```bash
--profile {web,print,maximum,balanced,quality}  # Perfil predefinido
--strategy {adaptive,image,font,content}        # Estratégia específica
--quality 0-100                                 # Qualidade de imagem (%)
--max-width PIXELS                              # Largura máxima de imagens
--max-height PIXELS                             # Altura máxima de imagens
--target-ratio 0.0-1.0                          # Meta de compressão
```

#### **🚀 Funcionalidades Avançadas**
```bash
--cache                     # Ativar sistema de cache
--cache-dir DIRETÓRIO       # Pasta do cache
--backup                    # Criar backup antes da compressão
--backup-dir DIRETÓRIO      # Pasta de backups
--analytics                 # Ativar relatórios de analytics
--analytics-dir DIRETÓRIO   # Pasta de dados analytics
```

#### **🔧 Opções de Execução**
```bash
-v, --verbose               # Modo verboso com progresso
--quiet                     # Modo silencioso
--dry-run                   # Simular sem modificar arquivos
--force                     # Sobrescrever arquivos existentes
--version                   # Mostrar versão
--list-profiles             # Listar perfis disponíveis
--list-strategies           # Listar estratégias disponíveis
```

---

## 🎨 Perfis de Compressão

### 🌐 **Web** - Otimizado para Internet
```bash
python main.py documento.pdf --profile web
```

**Características:**
- **Compressão:** Alta (60-70% de redução)
- **Qualidade:** Boa para visualização em tela
- **Velocidade:** Rápida
- **Uso ideal:** Sites, emails, compartilhamento online

**Configurações:**
- Qualidade de imagem: 70%
- Redimensionamento agressivo
- Otimização de fontes moderada
- Remoção de metadados completa

### 🖨️ **Print** - Otimizado para Impressão
```bash
python main.py documento.pdf --profile print
```

**Características:**
- **Compressão:** Moderada (30-40% de redução)
- **Qualidade:** Excelente para impressão
- **Velocidade:** Moderada
- **Uso ideal:** Documentos profissionais, impressão

**Configurações:**
- Qualidade de imagem: 85%
- Preservação de alta resolução
- Otimização conservadora de fontes
- Manutenção de metadados importantes

### 🗜️ **Maximum** - Máxima Compressão
```bash
python main.py documento.pdf --profile maximum
```

**Características:**
- **Compressão:** Máxima (70-80% de redução)
- **Qualidade:** Reduzida mas legível
- **Velocidade:** Mais lenta
- **Uso ideal:** Arquivamento, armazenamento limitado

**Configurações:**
- Qualidade de imagem: 50%
- Redimensionamento máximo
- Otimização agressiva de fontes
- Remoção completa de elementos desnecessários

### ⚖️ **Balanced** - Equilibrado (Padrão)
```bash
python main.py documento.pdf --profile balanced
```

**Características:**
- **Compressão:** Equilibrada (50-60% de redução)
- **Qualidade:** Muito boa
- **Velocidade:** Boa
- **Uso ideal:** Uso geral, documentos do dia a dia

**Configurações:**
- Qualidade de imagem: 75%
- Redimensionamento moderado
- Otimização balanceada de fontes
- Preservação seletiva de metadados

### 💎 **Quality** - Prioriza Qualidade
```bash
python main.py documento.pdf --profile quality
```

**Características:**
- **Compressão:** Baixa (20-30% de redução)
- **Qualidade:** Máxima
- **Velocidade:** Rápida
- **Uso ideal:** Documentos críticos, portfolios

**Configurações:**
- Qualidade de imagem: 95%
- Preservação de resolução original
- Otimização mínima
- Manutenção completa de metadados

---

## ⚡ Estratégias de Compressão

### 🧠 **Adaptive** - Inteligência Artificial (Padrão)
```bash
python main.py documento.pdf --strategy adaptive
```

**Como funciona:**
- Analisa automaticamente o conteúdo do PDF
- Seleciona a melhor estratégia para cada seção
- Combina múltiplas técnicas conforme necessário
- Otimiza baseado no tipo de conteúdo predominante

**Ideal para:**
- Documentos mistos (texto + imagens)
- Uso geral quando não se conhece o conteúdo
- Máxima eficiência automática

### 🖼️ **Image** - Foco em Imagens
```bash
python main.py documento.pdf --strategy image
```

**Como funciona:**
- Prioriza otimização de imagens
- Aplica compressão avançada em fotos e gráficos
- Redimensiona imagens para tamanhos ideais
- Converte formatos para otimização

**Ideal para:**
- Catálogos de produtos
- Portfolios fotográficos
- Documentos com muitas imagens
- Revistas e brochuras

### 🔤 **Font** - Foco em Fontes
```bash
python main.py documento.pdf --strategy font
```

**Como funciona:**
- Otimiza e comprime fontes incorporadas
- Remove fontes não utilizadas
- Faz subset de fontes para caracteres usados
- Mescla fontes similares

**Ideal para:**
- Documentos com muitas fontes diferentes
- E-books e textos longos
- Documentos multilíngues
- Apresentações com fontes especiais

### 📄 **Content** - Foco em Conteúdo
```bash
python main.py documento.pdf --strategy content
```

**Como funciona:**
- Remove conteúdo redundante
- Otimiza estrutura interna do PDF
- Comprime streams de dados
- Remove objetos não utilizados

**Ideal para:**
- Documentos gerados automaticamente
- PDFs com estrutura complexa
- Documentos com muito conteúdo vetorial
- Formulários e documentos técnicos

---

## ⚙️ Configurações Personalizadas

### Qualidade de Imagem
```bash
# Qualidade específica (0-100)
python main.py documento.pdf --quality 80

# Combinado com perfil
python main.py documento.pdf --profile web --quality 65
```

**Guia de Qualidade:**
- **90-100:** Qualidade máxima, arquivo grande
- **80-90:** Qualidade excelente, tamanho razoável
- **70-80:** Qualidade muito boa, bom equilíbrio
- **60-70:** Qualidade boa, arquivo menor
- **50-60:** Qualidade aceitável, compressão alta
- **30-50:** Qualidade baixa, arquivo muito pequeno

### Redimensionamento de Imagens
```bash
# Tamanho máximo específico
python main.py documento.pdf --max-width 1920 --max-height 1080

# Para web (menor)
python main.py documento.pdf --max-width 800 --max-height 600

# Para impressão (maior)
python main.py documento.pdf --max-width 2400 --max-height 1800
```

### Meta de Compressão
```bash
# Tentar comprimir para 50% do tamanho original
python main.py documento.pdf --target-ratio 0.5

# Compressão mais agressiva (30%)
python main.py documento.pdf --target-ratio 0.3

# Compressão conservadora (70%)
python main.py documento.pdf --target-ratio 0.7
```

### Combinações Avançadas
```bash
# Configuração personalizada completa
python main.py documento.pdf \
    --profile balanced \
    --strategy adaptive \
    --quality 75 \
    --max-width 1600 \
    --max-height 1200 \
    --target-ratio 0.4 \
    --cache \
    --backup \
    --verbose
```

---

## 🚀 Funcionalidades Avançadas

### 💾 Sistema de Cache
```bash
# Ativar cache básico
python main.py documento.pdf --cache

# Cache com pasta específica
python main.py documento.pdf --cache --cache-dir ./meu-cache/

# Cache para processamento em lote
python main.py *.pdf --batch --cache
```

**Benefícios do Cache:**
- ⚡ **Performance:** Evita reprocessar arquivos idênticos
- 🔄 **Eficiência:** Reutiliza resultados anteriores
- 💾 **Economia:** Reduz uso de CPU e tempo

**Como funciona:**
- Gera hash único para cada combinação arquivo+configuração
- Armazena resultados de compressões anteriores
- Verifica automaticamente se arquivo já foi processado
- Retorna resultado do cache se disponível

### 🛡️ Sistema de Backup
```bash
# Backup automático
python main.py documento.pdf --backup

# Backup com pasta específica
python main.py documento.pdf --backup --backup-dir ./meus-backups/

# Backup para lote
python main.py *.pdf --batch --backup
```

**Recursos do Backup:**
- 🔒 **Segurança:** Cria cópia antes de modificar
- 📂 **Organização:** Estrutura hierárquica de pastas
- 🏷️ **Metadados:** Timestamp e informações de origem
- 🔄 **Recuperação:** Fácil restauração se necessário

### 📊 Sistema de Analytics
```bash
# Analytics básico
python main.py documento.pdf --analytics

# Analytics com pasta específica
python main.py documento.pdf --analytics --analytics-dir ./analytics/

# Relatório detalhado
python main.py documento.pdf --analytics --verbose
```

**Métricas Coletadas:**
- 📈 **Performance:** Tempo de processamento, taxa de compressão
- 📊 **Qualidade:** Comparação antes/depois, métricas de qualidade
- 🎯 **Eficiência:** Hit rate do cache, estratégias mais eficazes
- 🔍 **Diagnósticos:** Erros, warnings, problemas encontrados

---

## 📁 Processamento em Lote

### Básico
```bash
# Todos os PDFs na pasta atual
python main.py *.pdf --batch

# Arquivos específicos
python main.py arquivo1.pdf arquivo2.pdf arquivo3.pdf --batch
```

### Com Diretório de Saída
```bash
# Pasta específica para resultados
python main.py *.pdf --batch --output-dir ./comprimidos/

# Estrutura organizada
python main.py documentos/*.pdf --batch --output-dir ./resultado/
```

### Lote Avançado
```bash
# Lote completo com todas as funcionalidades
python main.py documentos/*.pdf \
    --batch \
    --output-dir ./comprimidos/ \
    --profile web \
    --cache \
    --backup \
    --analytics \
    --verbose
```

### Padrões de Nomenclatura
```bash
# Padrão automático: original_compressed.pdf
python main.py *.pdf --batch

# Com sufixo personalizado
python main.py *.pdf --batch --output "_{}_optimized.pdf"
```

---

## 📈 Monitoramento e Analytics

### Modo Verboso
```bash
# Ver progresso detalhado
python main.py documento.pdf --verbose
```

**Informações Exibidas:**
- 🔄 Progresso de cada etapa
- 📊 Métricas em tempo real
- 🎯 Estratégias aplicadas
- ⏱️ Tempo de cada operação

### Relatórios de Analytics
```bash
# Gerar relatório completo
python main.py documento.pdf --analytics --verbose
```

**Exemplo de Relatório:**
```
📊 Relatório de Compressão
═══════════════════════════
📁 Arquivo: documento.pdf
📏 Tamanho original: 2.5 MB
📦 Tamanho comprimido: 1.2 MB
📉 Compressão: 52% (1.3 MB economizados)
⏱️ Tempo: 3.2s
🎯 Estratégia: adaptive
🏆 Qualidade mantida: 87%
```

### Monitoramento de Performance
```bash
# Monitor detalhado de sistema
python main.py documento.pdf --analytics --verbose --cache
```

---

## 🔗 Integração com Scripts

### Script Bash/Shell
```bash
#!/bin/bash
# Compressão automatizada

PERFIL="web"
PASTA_ORIGEM="./documentos"
PASTA_DESTINO="./comprimidos"

python main.py "${PASTA_ORIGEM}"/*.pdf \
    --batch \
    --profile "${PERFIL}" \
    --output-dir "${PASTA_DESTINO}" \
    --cache \
    --backup \
    --verbose

echo "Compressão concluída!"
```

### Script Python
```python
#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def comprimir_pdfs(pasta_origem, pasta_destino, perfil="balanced"):
    """Comprime todos os PDFs de uma pasta."""
    
    comando = [
        sys.executable, "main.py",
        f"{pasta_origem}/*.pdf",
        "--batch",
        f"--profile={perfil}",
        f"--output-dir={pasta_destino}",
        "--cache",
        "--backup",
        "--verbose"
    ]
    
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print("✅ Compressão concluída com sucesso!")
        print(resultado.stdout)
    else:
        print("❌ Erro na compressão:")
        print(resultado.stderr)
    
    return resultado.returncode

if __name__ == "__main__":
    comprimir_pdfs("./docs", "./docs_comprimidos", "web")
```

### Automação com Cron
```bash
# Executar compressão diariamente às 2h da manhã
0 2 * * * cd /caminho/para/CompactPDF && python main.py /pasta/pdfs/*.pdf --batch --profile web --cache
```

---

## 🎯 Casos de Uso Comuns

### 📧 Email e Compartilhamento
```bash
# PDFs para anexar em emails
python main.py documento.pdf --profile web --target-ratio 0.3

# Múltiplos documentos para compartilhar
python main.py *.pdf --batch --profile web --output-dir ./para_email/
```

### 🌐 Publicação Web
```bash
# Otimizar para carregamento rápido
python main.py catalogo.pdf --profile web --max-width 1200 --quality 70

# Lote para site
python main.py documentos/*.pdf --batch --profile web --cache
```

### 🖨️ Preparação para Impressão
```bash
# Manter qualidade para impressão
python main.py documento.pdf --profile print --quality 85

# Reduzir apenas o que for desnecessário
python main.py *.pdf --batch --profile quality --strategy content
```

### 💾 Arquivamento e Backup
```bash
# Máxima compressão para arquivo
python main.py *.pdf --batch --profile maximum --backup

# Arquivamento com analytics
python main.py documentos_antigos/*.pdf \
    --batch \
    --profile maximum \
    --output-dir ./arquivo_comprimido/ \
    --analytics \
    --cache
```

### 📱 Dispositivos Móveis
```bash
# Otimizar para tablets/celulares
python main.py apresentacao.pdf \
    --profile web \
    --max-width 800 \
    --max-height 600 \
    --quality 65
```

### 🏢 Automação Corporativa
```bash
# Processamento noturno automatizado
python main.py /servidor/documentos/*.pdf \
    --batch \
    --profile balanced \
    --output-dir /servidor/documentos_otimizados/ \
    --cache \
    --backup \
    --analytics \
    --verbose > /logs/compressao_$(date +%Y%m%d).log 2>&1
```

---

## 🔧 Dicas e Melhores Práticas

### ✅ Recomendações

1. **Sempre teste primeiro** com `--dry-run`
2. **Use cache** para processamento repetitivo
3. **Faça backup** de arquivos importantes
4. **Escolha o perfil adequado** para seu caso
5. **Monitor qualidade** com modo verboso
6. **Use analytics** para otimizar workflows

### ⚠️ Cuidados

1. **PDFs já comprimidos** podem não reduzir muito
2. **Qualidade muito baixa** pode tornar texto ilegível
3. **Redimensionamento excessivo** pode degradar imagens
4. **Arquivos corrompidos** podem causar erros

### 🚀 Performance

1. **Use SSD** para cache e temporários
2. **RAM suficiente** para arquivos grandes
3. **CPU multi-core** para processamento em lote
4. **Rede rápida** se arquivos estão em rede

---

## 🆘 Solução de Problemas Rápida

### Erro de Memória
```bash
# Reduzir uso de memória
python main.py documento.pdf --profile web --target-ratio 0.5
```

### Arquivo Muito Grande
```bash
# Processamento em chunks menores
python main.py arquivo_grande.pdf --max-width 1200 --quality 60
```

### Qualidade Ruim
```bash
# Aumentar qualidade preservada
python main.py documento.pdf --profile quality --quality 90
```

### Cache Corrompido
```bash
# Limpar cache
rm -rf ./cache/*
python main.py documento.pdf --cache
```

---

## 📚 Recursos Adicionais

- **Guia do Desenvolvedor:** [`DEVELOPER_GUIDE.md`](DEVELOPER_GUIDE.md)
- **Exemplos Práticos:** [`EXAMPLES.md`](EXAMPLES.md)
- **Solução de Problemas:** [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)
- **Perguntas Frequentes:** [`FAQ.md`](FAQ.md)
- **API Reference:** [`API_REFERENCE.md`](API_REFERENCE.md)

---

*📝 Este manual é atualizado regularmente. Para a versão mais recente, consulte a documentação online.*
