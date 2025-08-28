# 🗜️ CompactPDF - Sistema Inteligente de Compressão de PDF

<div align="center">

**Um sistema avançado de compressão de PDF construído com princípios SOLID**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-SOLID-orange.svg)](#-arquitetura-solid)
[![Compression](https://img.shields.io/badge/Compression-Up%20to%2060%25-success.svg)](#-resultados)

*Compacte seus PDFs em até 60% mantendo qualidade visual superior*

</div>

---

## 🎯 **Visão Geral**

O **CompactPDF** é uma ferramenta profissional de compressão de PDF que combina **inteligência artificial**, **análise de conteúdo** e **múltiplas estratégias** para alcançar a máxima compressão com mínima perda de qualidade.

### **✨ Características Principais**

- 🧠 **Compressão Inteligente**: Análise automática do conteúdo para otimização personalizada
- 📊 **Múltiplas Estratégias**: 4 estratégias de compressão especializadas
- 🎯 **Alta Performance**: Cache inteligente e otimizações automáticas
- 🛡️ **Segurança Total**: Sistema completo de backup e recuperação
- 📈 **Analytics Avançado**: Relatórios detalhados e métricas de performance
- 🏗️ **Arquitetura SOLID**: Código limpo, extensível e mantível

---

## 🚀 **Início Rápido**

### **Instalação Simples**

```bash
# 1. Clone o repositório
git clone https://github.com/IgorGSBarbosaDev/CompactPDF.git
cd CompactPDF

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute o exemplo
python demo.py
```

### **Uso Básico**

```bash
# Compressão automática inteligente
python main.py documento.pdf --output comprimido.pdf

# Resultado típico: 50-60% de redução mantendo qualidade
```

---

## 📁 **Estrutura Organizada**

```
CompactPDF/
├── 🎯 ENTRADA PRINCIPAL
│   ├── main.py                    # 🖥️ Interface CLI completa
│   └── demo.py                    # 🚀 Demonstração rápida
│
├── 📦 CÓDIGO FONTE (src/)
│   ├── pdf_compressor.py         # 🎯 Facade principal
│   │
│   ├── 🔌 INTERFACES (interfaces/)
│   │   └── __init__.py            # Contratos e abstrações
│   │
│   ├── 🎯 ESTRATÉGIAS (strategies/)
│   │   ├── image_compression.py   # 🖼️ Otimização de imagens
│   │   ├── font_optimization.py   # 🔤 Otimização de fontes  
│   │   ├── content_optimization.py # 📄 Otimização de conteúdo
│   │   └── adaptive_compression.py # 🧠 Estratégia inteligente
│   │
│   ├── 🛠️ SERVIÇOS (services/)
│   │   ├── pdf_file_service.py    # 📁 Operações de arquivo
│   │   ├── compression_metrics.py  # 📊 Métricas e análise
│   │   └── progress_service.py     # ⏳ Controle de progresso
│   │
│   ├── ⚙️ CONFIGURAÇÃO (config/)
│   │   └── __init__.py            # Configurações e perfis
│   │
│   └── 🔧 UTILITÁRIOS (utils/)
│       ├── image_quality.py       # 🎯 Avaliação de qualidade
│       ├── cache.py               # ⚡ Sistema de cache
│       ├── backup.py              # 🛡️ Backup e recuperação
│       ├── analytics.py           # 📈 Analytics e relatórios
│       ├── adaptive_optimizer.py  # 🧠 Otimizador inteligente
│       ├── logger.py              # 📝 Sistema de logs
│       └── file_utils.py          # 📁 Utilitários de arquivo
│
├── 📚 EXEMPLOS E DOCUMENTAÇÃO
│   ├── examples/
│   │   ├── usage_examples.py      # 📖 Exemplos básicos
│   │   ├── advanced_usage.py      # 🚀 Funcionalidades avançadas
│   │   └── sample_pdfs/           # 📄 PDFs para teste
│   │
│   ├── tests/                     # 🧪 Testes automatizados
│   ├── README.md                  # 📖 Esta documentação
│   ├── MELHORIAS_IMPLEMENTADAS.md # 📋 Log de melhorias
│   └── requirements.txt           # 📦 Dependências
```

---

## 🎯 **Estratégias de Compressão**

### **1. 🖼️ Compressão de Imagens**
- **Redução de qualidade** inteligente (JPEG optimization)
- **Redimensionamento** automático baseado em uso
- **Métricas de qualidade** PSNR e SSIM

### **2. 🔤 Otimização de Fontes**
- **Subsetting** de fontes (remove caracteres não usados)
- **Remoção de fontes** duplicadas ou não utilizadas
- **Otimização de encoding** de fontes

### **3. 📄 Otimização de Conteúdo**
- **Compressão de streams** de conteúdo
- **Remoção de objetos** não utilizados
- **Limpeza de metadados** desnecessários

### **4. 🧠 Estratégia Adaptativa (NOVA!)**
- **Análise automática** do tipo de conteúdo
- **Seleção inteligente** de técnicas de compressão
- **Configuração automática** baseada no documento

---

## 🎮 **Formas de Uso**

### **🖥️ Interface de Linha de Comando**

```bash
# Compressão automática (recomendado)
python main.py documento.pdf

# Escolher perfil específico
python main.py documento.pdf --profile web_optimized

# Configuração personalizada
python main.py documento.pdf --quality 70 --max-width 1200

# Modo verboso com métricas
python main.py documento.pdf --verbose --analytics

# Usar cache para performance
python main.py documento.pdf --cache --backup
```

### **🐍 Uso Programático**

```python
from src.pdf_compressor import PDFCompressor
from src.config import CompressionConfig
from src.strategies import AdaptiveCompressionStrategy

# Compressão simples
compressor = PDFCompressor()
result = compressor.compress_file("input.pdf", "output.pdf")

# Compressão inteligente
strategy = AdaptiveCompressionStrategy()
config = CompressionConfig.get_balanced_config()
result = compressor.compress_file("input.pdf", "output.pdf", config, strategy)

# Resultados detalhados
print(f"📊 Compressão: {result['compression_ratio']:.1%}")
print(f"💾 Economia: {result['space_saved']:,} bytes")
print(f"⏱️ Tempo: {result['processing_time']:.2f}s")
```

---

## 📊 **Resultados e Performance**

### **🎯 Métricas Típicas**

| Tipo de Documento | Compressão | Qualidade Preservada | Tempo/MB |
|-------------------|------------|---------------------|----------|
| 📄 Texto com imagens | 45-60% | >90% | 3-5s |
| 🖼️ Rico em imagens | 60-75% | >85% | 5-8s |
| 📋 Documentos técnicos | 35-50% | >95% | 2-4s |
| 📊 Apresentações | 50-65% | >88% | 4-7s |

### **⚡ Performance do Cache**

- **Cache Hit**: ~10x mais rápido
- **Economia de CPU**: 80-90%
- **Armazenamento**: Compressão automática de cache

---

## 🧪 **Testes e Exemplos**

### **🔍 Testes Automatizados**

```bash
# Executar todos os testes
python -m pytest tests/ -v

# Testes de performance
python tests/test_performance.py

# Testes de qualidade
python tests/test_quality_metrics.py
```

### **📚 Exemplos Práticos**

```bash
# Exemplos básicos
python examples/usage_examples.py

# Funcionalidades avançadas (6 exemplos completos)
python examples/advanced_usage.py

# Demonstração com PDFs reais
python demo.py
```

---

## 🔧 **Configuração e Personalização**

### **📋 Perfis Predefinidos**

```python
# Máxima compressão (web, email)
config = CompressionConfig.get_maximum_compression_config()

# Balanceado (uso geral)
config = CompressionConfig.get_balanced_config()

# Preservação de qualidade (impressão)
config = CompressionConfig.get_quality_preserving_config()
```

### **⚙️ Configuração Personalizada**

```python
config = CompressionConfig(
    # Qualidade de imagem (0-100)
    image_quality=75,
    
    # Dimensões máximas
    max_image_width=1200,
    max_image_height=1200,
    
    # Otimizações
    optimize_fonts=True,
    remove_metadata=False,
    compress_streams=True,
    
    # Meta de compressão
    target_compression_ratio=0.5
)
```

---

## 🏗️ **Arquitetura SOLID**

O projeto implementa rigorosamente os **5 princípios SOLID**:

### **S** - Single Responsibility Principle
- `PDFCompressor`: Coordenação de compressão
- `ImageQualityAssessor`: Avaliação de qualidade
- `CompressionCache`: Gerenciamento de cache

### **O** - Open/Closed Principle
- Sistema de **estratégias plugáveis**
- Novas estratégias sem modificar código existente

### **L** - Liskov Substitution Principle
- Todas as estratégias são **intercambiáveis**
- Comportamento consistente entre implementações

### **I** - Interface Segregation Principle
- Interfaces **específicas** para cada responsabilidade

### **D** - Dependency Inversion Principle
- Dependências por **abstrações**, não implementações
- **Injeção de dependências** em toda aplicação

---

## 🤝 **Contribuição**

### **🔄 Processo de Contribuição**

1. **Fork** o repositório
2. **Crie** uma branch (`git checkout -b feature/nova-funcionalidade`)
3. **Implemente** seguindo os princípios SOLID
4. **Teste** suas mudanças (`python -m pytest`)
5. **Documente** as alterações
6. **Commit** (`git commit -m 'feat: adiciona nova funcionalidade'`)
7. **Push** (`git push origin feature/nova-funcionalidade`)
8. **Abra** um Pull Request

---

## 📄 **Licença**

Este projeto está sob a **Licença MIT** - veja [LICENSE](LICENSE) para detalhes.

---

<div align="center">

**⭐ Gostou do projeto? Deixe uma estrela!**

**🐛 Encontrou um bug? [Abra uma issue](../../issues)**

**💡 Tem uma ideia? [Inicie uma discussão](../../discussions)**

---

*Desenvolvido com ❤️ para a comunidade Python*

</div>
