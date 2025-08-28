# 🚀 Guia de Início Rápido - CompactPDF

Este guia te ajudará a começar a usar o CompactPDF em poucos minutos.

---

## 📋 **Pré-requisitos**

- **Python 3.9+** instalado
- **pip** (gerenciador de pacotes Python)
- **PDFs para testar** (ou use nossos exemplos)

---

## ⚡ **Instalação em 3 Passos**

### **1. Clone o Repositório**
```bash
git clone https://github.com/IgorGSBarbosaDev/CompactPDF.git
cd CompactPDF
```

### **2. Instale Dependências**
```bash
pip install -r requirements.txt
```

### **3. Teste a Instalação**
```bash
python demo.py
```

Se tudo funcionou, você verá o menu interativo da demonstração! 🎉

---

## 🎮 **Primeiro Uso - 30 Segundos**

### **Compressão Automática (Mais Simples)**
```bash
# Comprime um PDF automaticamente
python main.py meu_documento.pdf

# Resultado: meu_documento_compressed.pdf
```

### **Com Arquivo de Saída Específico**
```bash
python main.py meu_documento.pdf --output documento_comprimido.pdf
```

### **Com Perfil Otimizado**
```bash
# Para web (máxima compressão)
python main.py meu_documento.pdf --profile web

# Para impressão (alta qualidade)  
python main.py meu_documento.pdf --profile print
```

---

## 📊 **Resultados Típicos**

Após a compressão, você verá algo como:

```
✅ Compressão concluída!
📊 Resultados:
   📁 Original: 2,450,000 bytes
   🗜️ Comprimido: 1,225,000 bytes  
   📉 Redução: 50.0%
   💾 Economia: 1,225,000 bytes
```

---

## 🎯 **Casos de Uso Comuns**

### **📧 Para Email (Tamanho Mínimo)**
```bash
python main.py documento.pdf --profile maximum
```

### **🌐 Para Web (Balanceado)**
```bash
python main.py documento.pdf --profile web --cache
```

### **🖨️ Para Impressão (Alta Qualidade)**
```bash
python main.py documento.pdf --profile print --backup
```

### **📁 Múltiplos Arquivos**
```bash
python main.py *.pdf --batch --output-dir comprimidos/
```

---

## 🧪 **Teste com Exemplos**

### **Demonstração Interativa**
```bash
python demo.py
```
*Menu interativo com exemplos prontos*

### **Exemplos Avançados**
```bash
python examples/advanced_usage.py
```
*6 exemplos completos das funcionalidades*

### **Exemplos Básicos**
```bash
python examples/usage_examples.py  
```
*Uso programático simples*

---

## 🔧 **Personalização Rápida**

### **Qualidade de Imagem**
```bash
# Qualidade alta (menos compressão)
python main.py doc.pdf --quality 90

# Qualidade baixa (mais compressão)
python main.py doc.pdf --quality 50
```

### **Tamanho Máximo de Imagens**
```bash
python main.py doc.pdf --max-width 800 --max-height 600
```

### **Meta de Compressão**
```bash
# Tentar comprimir para 30% do tamanho original
python main.py doc.pdf --target-ratio 0.3
```

---

## 🚀 **Funcionalidades Avançadas**

### **Cache (Performance)**
```bash
python main.py doc.pdf --cache
# Muito mais rápido em compressões repetidas
```

### **Backup (Segurança)**
```bash
python main.py doc.pdf --backup
# Cria backup automático antes de comprimir
```

### **Analytics (Relatórios)**
```bash
python main.py doc.pdf --analytics --verbose
# Gera relatórios detalhados de performance
```

### **Combinado (Recomendado)**
```bash
python main.py doc.pdf --cache --backup --analytics --verbose
```

---

## 📱 **Uso Programático Simples**

```python
# Salve como: meu_script.py
from src.pdf_compressor import PDFCompressor
from src.config import CompressionConfig

# Configuração automática
compressor = PDFCompressor()
result = compressor.compress_file("input.pdf", "output.pdf")

print(f"Compressão: {result['compression_ratio']:.1%}")
print(f"Economia: {result['space_saved']:,} bytes")
```

Execute com:
```bash
python meu_script.py
```

---

## ❓ **Problemas Comuns**

### **Erro de Import**
```bash
# Certifique-se de estar no diretório do projeto
cd CompactPDF
python main.py documento.pdf
```

### **Arquivo Não Encontrado**
```bash
# Use caminho completo ou relativo correto
python main.py "C:\Documentos\meu_arquivo.pdf"
```

### **Dependências em Falta**
```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

### **Permissões**
```bash
# No Windows, execute como administrador se necessário
# No Linux/Mac: sudo python main.py documento.pdf
```

---

## 🎯 **Próximos Passos**

### **Aprender Mais**
- 📖 [Manual Completo](USER_GUIDE.md) - Todas as funcionalidades
- 🏗️ [Guia do Desenvolvedor](DEVELOPER_GUIDE.md) - Extensão e customização
- 📚 [Exemplos](EXAMPLES.md) - Casos de uso específicos

### **Ajuda**
- ❓ [FAQ](FAQ.md) - Perguntas frequentes
- 🔧 [Solução de Problemas](TROUBLESHOOTING.md) - Problemas técnicos
- 💬 [Issues no GitHub](../../issues) - Reportar bugs

---

## ⏰ **Cronometro - Você Deve Estar Funcionando em < 5 Minutos**

- ✅ **Minuto 1-2**: Clone e instalação
- ✅ **Minuto 3**: Primeiro teste com `python demo.py`
- ✅ **Minuto 4**: Primeira compressão real
- ✅ **Minuto 5**: Resultado na tela! 🎉

---

<div align="center">

**🎉 Parabéns! Você já está usando o CompactPDF!**

*Próximo passo: Explore os perfis e funcionalidades avançadas*

[📖 Manual Completo](USER_GUIDE.md) | [🚀 Exemplos](EXAMPLES.md) | [❓ Ajuda](FAQ.md)

</div>
