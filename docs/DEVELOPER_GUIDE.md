# 🏗️ Guia do Desenvolvedor - CompactPDF

Guia completo para desenvolvedores que querem contribuir, estender ou integrar o CompactPDF.

## 📋 Índice

1. [Arquitetura do Sistema](#arquitetura-do-sistema)
2. [Princípios SOLID](#princípios-solid)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Configuração do Ambiente](#configuração-do-ambiente)
5. [APIs e Interfaces](#apis-e-interfaces)
6. [Estratégias de Compressão](#estratégias-de-compressão)
7. [Sistema de Plugin](#sistema-de-plugin)
8. [Testes e Qualidade](#testes-e-qualidade)
9. [Performance e Otimização](#performance-e-otimização)
10. [Contribuindo](#contribuindo)

---

## 🏛️ Arquitetura do Sistema

### Visão Geral
O CompactPDF segue uma arquitetura modular baseada nos princípios SOLID, utilizando patterns como Strategy, Factory, e Facade para máxima flexibilidade e manutenibilidade.

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface                        │
│                     (main.py)                          │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                PDFCompressorFacade                      │
│              (Facade Pattern)                          │
└─────────────────────┬───────────────────────────────────┘
                      │
      ┌───────────────┼───────────────┐
      │               │               │
┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
│Strategies │  │ Services  │  │   Utils   │
│           │  │           │  │           │
│ • Image   │  │ • PDF     │  │ • Cache   │
│ • Font    │  │ • Metrics │  │ • Backup  │
│ • Content │  │ • Progress│  │ • Logger  │
│ • Adaptive│  │           │  │ • Memory  │
└───────────┘  └───────────┘  └───────────┘
```

### Componentes Principais

#### 1. **PDFCompressorFacade** - Orquestrador Principal
```python
from src import PDFCompressorFacade, CompressionConfig

# Interface simplificada para o usuário
compressor = PDFCompressorFacade()
result = compressor.compress_pdf("input.pdf", "output.pdf", config)
```

#### 2. **Strategy Pattern** - Algoritmos Intercambiáveis
```python
from src.strategies import (
    ImageCompressionStrategy,
    FontOptimizationStrategy,
    ContentOptimizationStrategy,
    AdaptiveCompressionStrategy
)

# Estratégias podem ser trocadas dinamicamente
strategy = AdaptiveCompressionStrategy()
compressor.set_strategy(strategy)
```

#### 3. **Service Layer** - Lógica de Negócio
```python
from src.services import (
    PDFFileService,
    CompressionMetricsService,
    ProgressTracker
)
```

#### 4. **Utilities** - Funcionalidades Transversais
```python
from src.utils import (
    CompressionCache,
    BackupManager,
    CompressionAnalytics,
    MemoryManager
)
```

---

## 🎯 Princípios SOLID

### **S** - Single Responsibility Principle
Cada classe tem uma única responsabilidade bem definida:

```python
# ✅ Correto: Responsabilidade única
class ImageCompressionStrategy:
    """Responsável apenas por comprimir imagens."""
    def compress(self, pdf_data: bytes) -> bytes:
        # Lógica específica de compressão de imagens
        pass

class FontOptimizationStrategy:
    """Responsável apenas por otimizar fontes."""
    def optimize(self, pdf_data: bytes) -> bytes:
        # Lógica específica de otimização de fontes
        pass
```

### **O** - Open/Closed Principle
Sistema aberto para extensão, fechado para modificação:

```python
# Nova estratégia pode ser adicionada sem modificar código existente
class NovelCompressionStrategy(ICompressionStrategy):
    """Nova estratégia implementada sem modificar código existente."""
    
    def compress(self, pdf_data: bytes, config: CompressionConfig) -> CompressionResult:
        # Implementação da nova estratégia
        pass
    
    def get_strategy_name(self) -> str:
        return "novel_strategy"
```

### **L** - Liskov Substitution Principle
Subtipos podem substituir tipos base sem quebrar funcionalidade:

```python
# Qualquer estratégia pode substituir a interface base
def use_strategy(strategy: ICompressionStrategy, data: bytes) -> bytes:
    return strategy.compress(data)  # Funciona com qualquer implementação

# Todas funcionam igualmente
image_strategy = ImageCompressionStrategy()
font_strategy = FontOptimizationStrategy()
adaptive_strategy = AdaptiveCompressionStrategy()

# Intercambiáveis sem problemas
use_strategy(image_strategy, pdf_data)
use_strategy(font_strategy, pdf_data)
use_strategy(adaptive_strategy, pdf_data)
```

### **I** - Interface Segregation Principle
Interfaces específicas e focadas:

```python
# ✅ Interfaces segregadas e específicas
class ICompressionStrategy(ABC):
    """Interface específica para estratégias de compressão."""
    @abstractmethod
    def compress(self, pdf_data: bytes, config: CompressionConfig) -> CompressionResult:
        pass

class ICompressionMetrics(ABC):
    """Interface específica para métricas."""
    @abstractmethod
    def calculate_compression_ratio(self, original_size: int, compressed_size: int) -> float:
        pass

class IProgressTracker(ABC):
    """Interface específica para tracking de progresso."""
    @abstractmethod
    def update_progress(self, percentage: float, message: str) -> None:
        pass
```

### **D** - Dependency Inversion Principle
Dependência de abstrações, não de implementações concretas:

```python
class PDFCompressorFacade:
    def __init__(
        self,
        strategies: List[ICompressionStrategy],  # Depende da abstração
        file_service: IPDFFileService,           # Não da implementação
        metrics_service: ICompressionMetrics,
        cache: ICompressionCache = None
    ):
        self.strategies = strategies
        self.file_service = file_service
        self.metrics_service = metrics_service
        self.cache = cache
```

---

## 📁 Estrutura do Projeto

### Organização Hierárquica
```
CompactPDF/
├── main.py                     # 🎯 CLI Interface
├── requirements.txt            # 📦 Dependencies
├── .env.example               # ⚙️ Environment template
├── .gitignore                 # 🚫 Git exclusions
│
├── src/                       # 💼 Core source code
│   ├── __init__.py           # 📤 Main exports
│   ├── pdf_compressor.py     # 🏗️ Facade implementation
│   │
│   ├── interfaces/           # 🔌 Abstract interfaces
│   │   ├── __init__.py
│   │   ├── compression.py    # ICompressionStrategy, etc.
│   │   ├── services.py       # Service interfaces
│   │   └── utils.py          # Utility interfaces
│   │
│   ├── strategies/           # ⚡ Compression strategies
│   │   ├── __init__.py
│   │   ├── base.py          # Base strategy class
│   │   ├── image_compression.py
│   │   ├── font_optimization.py
│   │   ├── content_optimization.py
│   │   └── adaptive.py      # AI-powered adaptive strategy
│   │
│   ├── services/            # 🛠️ Business logic services
│   │   ├── __init__.py
│   │   ├── pdf_file_service.py
│   │   ├── compression_metrics.py
│   │   └── progress_tracker.py
│   │
│   ├── utils/               # 🔧 Utilities and helpers
│   │   ├── __init__.py
│   │   ├── cache.py         # Intelligent caching
│   │   ├── backup.py        # Backup management
│   │   ├── analytics.py     # Performance analytics
│   │   ├── logger.py        # Logging utilities
│   │   ├── memory_optimizer.py  # Memory management
│   │   └── file_utils.py    # File operations
│   │
│   └── config/              # ⚙️ Configuration management
│       ├── __init__.py
│       ├── compression_config.py
│       └── optimized_config.py
│
├── tests/                   # 🧪 Test suite
│   ├── __init__.py
│   ├── test_strategies/
│   ├── test_services/
│   ├── test_utils/
│   └── test_integration/
│
├── docs/                    # 📚 Documentation
│   ├── README.md
│   ├── GETTING_STARTED.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md   # 👈 Este arquivo
│   └── API_REFERENCE.md
│
├── examples/                # 💡 Usage examples
│   ├── basic_usage.py
│   ├── advanced_config.py
│   ├── batch_processing.py
│   └── custom_strategy.py
│
└── tools/                   # 🛠️ Development tools
    ├── benchmark.py
    ├── profiler.py
    └── setup_dev.py
```

### Convenções de Nomenclatura

#### **Classes**
- `PascalCase` para classes: `PDFCompressorFacade`
- `I` prefix para interfaces: `ICompressionStrategy`
- Sufixos descritivos: `Strategy`, `Service`, `Manager`

#### **Métodos e Funções**
- `snake_case` para métodos: `compress_pdf()`, `get_strategy_name()`
- Verbos descritivos: `calculate_`, `generate_`, `process_`

#### **Constantes**
- `UPPER_SNAKE_CASE`: `DEFAULT_QUALITY`, `MAX_FILE_SIZE`

#### **Arquivos e Módulos**
- `snake_case.py`: `compression_strategy.py`
- Nomes descritivos e específicos

---

## ⚙️ Configuração do Ambiente

### Desenvolvimento Local

#### 1. **Pré-requisitos**
```bash
# Python 3.8+ required
python --version  # Deve ser 3.8+

# Git para versionamento
git --version
```

#### 2. **Clone e Setup**
```bash
# Clone do repositório
git clone https://github.com/IgorGSBarbosaDev/CompactPDF.git
cd CompactPDF

# Ambiente virtual
python -m venv .venv

# Ativação (Windows)
.venv\Scripts\activate

# Ativação (Linux/Mac)
source .venv/bin/activate

# Instalação de dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dependências de desenvolvimento
```

#### 3. **Configuração IDE**

**VS Code:**
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

**PyCharm:**
```ini
# PyCharm project settings
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Ferramentas de Desenvolvimento

#### **Linting e Formatação**
```bash
# Black - Code formatting
black src/ tests/ main.py

# isort - Import sorting
isort src/ tests/ main.py

# flake8 - Linting
flake8 src/ tests/ main.py

# mypy - Type checking
mypy src/ main.py
```

#### **Testes**
```bash
# Executar todos os testes
pytest

# Com coverage
pytest --cov=src tests/

# Testes específicos
pytest tests/test_strategies/

# Testes com marcadores
pytest -m "not slow"
```

#### **Profiling e Benchmark**
```bash
# Profile de performance
python tools/profiler.py

# Benchmark de estratégias
python tools/benchmark.py

# Análise de memória
python tools/memory_analysis.py
```

---

## 🔌 APIs e Interfaces

### Interface Principal - PDFCompressorFacade

```python
from src import PDFCompressorFacade, CompressionConfig
from src.strategies import AdaptiveCompressionStrategy

class PDFCompressorFacade:
    """
    Interface principal para compressão de PDF.
    Implementa o pattern Facade para simplificar o uso.
    """
    
    def __init__(self, strategies: List[ICompressionStrategy] = None):
        """
        Inicializa o compressor com estratégias opcionais.
        
        Args:
            strategies: Lista de estratégias a serem usadas
        """
        
    def compress_pdf(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        config: Optional[CompressionConfig] = None
    ) -> CompressionResult:
        """
        Comprime um arquivo PDF usando as estratégias configuradas.
        
        Args:
            input_path: Caminho do arquivo PDF de entrada
            output_path: Caminho do arquivo de saída (opcional)
            config: Configuração de compressão (opcional)
            
        Returns:
            CompressionResult com métricas da operação
            
        Raises:
            FileNotFoundError: Se arquivo de entrada não existir
            PermissionError: Se não houver permissão para escrever
            CompressionError: Se houver erro na compressão
        """
        
    def compress_with_preset(
        self,
        input_path: str,
        output_path: str,
        preset: str = 'balanced'
    ) -> CompressionResult:
        """
        Comprime usando preset predefinido.
        
        Args:
            input_path: Arquivo de entrada
            output_path: Arquivo de saída  
            preset: Nome do preset ('web', 'print', 'maximum', etc.)
            
        Returns:
            CompressionResult com métricas
        """
        
    def batch_compress(
        self,
        input_patterns: List[str],
        output_dir: str,
        config: Optional[CompressionConfig] = None
    ) -> List[CompressionResult]:
        """
        Comprime múltiplos arquivos em lote.
        
        Args:
            input_patterns: Padrões de arquivos (wildcards aceitos)
            output_dir: Diretório de saída
            config: Configuração opcional
            
        Returns:
            Lista de CompressionResult para cada arquivo
        """
```

### Interface de Estratégia

```python
from abc import ABC, abstractmethod
from typing import Optional
from src.config import CompressionConfig
from src.services import CompressionResult

class ICompressionStrategy(ABC):
    """
    Interface base para todas as estratégias de compressão.
    Implementa o Strategy Pattern.
    """
    
    @abstractmethod
    def compress(
        self, 
        pdf_data: bytes, 
        config: CompressionConfig
    ) -> CompressionResult:
        """
        Comprime os dados do PDF usando a estratégia específica.
        
        Args:
            pdf_data: Dados binários do PDF
            config: Configuração de compressão
            
        Returns:
            CompressionResult com dados comprimidos e métricas
        """
        pass
        
    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Retorna o nome identificador da estratégia.
        
        Returns:
            Nome único da estratégia (ex: 'adaptive', 'image', 'font')
        """
        pass
        
    def can_handle(self, pdf_analysis: dict) -> bool:
        """
        Verifica se a estratégia é adequada para o PDF analisado.
        
        Args:
            pdf_analysis: Análise do conteúdo do PDF
            
        Returns:
            True se a estratégia é recomendada para este PDF
        """
        return True  # Implementação padrão aceita qualquer PDF
        
    def estimate_compression(self, pdf_analysis: dict) -> float:
        """
        Estima a taxa de compressão esperada.
        
        Args:
            pdf_analysis: Análise do PDF
            
        Returns:
            Taxa de compressão estimada (0.0 a 1.0)
        """
        return 0.5  # Implementação padrão estima 50%
```

### Interface de Serviços

```python
class IPDFFileService(ABC):
    """Interface para operações com arquivos PDF."""
    
    @abstractmethod
    def read_pdf(self, file_path: str) -> bytes:
        """Lê arquivo PDF e retorna dados binários."""
        pass
        
    @abstractmethod
    def write_pdf(self, file_path: str, pdf_data: bytes) -> None:
        """Escreve dados binários em arquivo PDF."""
        pass
        
    @abstractmethod
    def analyze_pdf(self, pdf_data: bytes) -> dict:
        """Analisa estrutura e conteúdo do PDF."""
        pass

class ICompressionMetrics(ABC):
    """Interface para cálculo de métricas."""
    
    @abstractmethod
    def calculate_compression_ratio(
        self, 
        original_size: int, 
        compressed_size: int
    ) -> float:
        """Calcula taxa de compressão."""
        pass
        
    @abstractmethod
    def calculate_quality_score(
        self, 
        original_data: bytes, 
        compressed_data: bytes
    ) -> float:
        """Calcula score de qualidade mantida."""
        pass
```

---

## ⚡ Estratégias de Compressão

### Criando Nova Estratégia

#### 1. **Implementar Interface**
```python
# src/strategies/custom_strategy.py
from src.interfaces.compression import ICompressionStrategy
from src.config import CompressionConfig
from src.services import CompressionResult

class CustomCompressionStrategy(ICompressionStrategy):
    """
    Estratégia personalizada de compressão.
    Exemplo de implementação de nova estratégia.
    """
    
    def __init__(self, custom_param: float = 0.8):
        """
        Inicializa estratégia com parâmetros específicos.
        
        Args:
            custom_param: Parâmetro personalizado da estratégia
        """
        self.custom_param = custom_param
        self._compression_cache = {}
    
    def compress(
        self, 
        pdf_data: bytes, 
        config: CompressionConfig
    ) -> CompressionResult:
        """
        Implementa lógica específica de compressão.
        """
        # 1. Análise do PDF
        analysis = self._analyze_pdf_structure(pdf_data)
        
        # 2. Aplicar transformações específicas
        compressed_data = self._apply_custom_compression(pdf_data, analysis, config)
        
        # 3. Calcular métricas
        metrics = self._calculate_metrics(pdf_data, compressed_data)
        
        # 4. Retornar resultado
        return CompressionResult(
            original_size=len(pdf_data),
            compressed_size=len(compressed_data),
            compression_ratio=metrics['ratio'],
            time_taken=metrics['time'],
            strategy_used=self.get_strategy_name(),
            success=True,
            compressed_data=compressed_data
        )
    
    def get_strategy_name(self) -> str:
        """Identificador único da estratégia."""
        return "custom_strategy"
    
    def can_handle(self, pdf_analysis: dict) -> bool:
        """
        Verifica se PDF é adequado para esta estratégia.
        """
        # Exemplo: apenas PDFs com muitas imagens
        image_ratio = pdf_analysis.get('image_content_ratio', 0)
        return image_ratio > 0.3
    
    def estimate_compression(self, pdf_analysis: dict) -> float:
        """
        Estima compressão baseado na análise.
        """
        # Lógica personalizada de estimativa
        base_ratio = 0.6
        
        # Ajustar baseado no conteúdo
        if pdf_analysis.get('has_images', False):
            base_ratio += 0.2
        
        if pdf_analysis.get('has_redundant_content', False):
            base_ratio += 0.1
            
        return min(base_ratio, 0.9)  # Máximo 90% de compressão
    
    def _analyze_pdf_structure(self, pdf_data: bytes) -> dict:
        """Análise específica da estratégia."""
        # Implementar análise personalizada
        return {
            'total_objects': 0,
            'image_objects': 0,
            'font_objects': 0,
            'content_streams': 0
        }
    
    def _apply_custom_compression(
        self, 
        pdf_data: bytes, 
        analysis: dict, 
        config: CompressionConfig
    ) -> bytes:
        """Aplicar compressão específica."""
        # Implementar lógica de compressão
        return pdf_data  # Placeholder
    
    def _calculate_metrics(self, original: bytes, compressed: bytes) -> dict:
        """Calcular métricas específicas."""
        return {
            'ratio': len(compressed) / len(original),
            'time': 0.0,
            'quality_score': 0.85
        }
```

#### 2. **Registrar Estratégia**
```python
# src/strategies/__init__.py
from .custom_strategy import CustomCompressionStrategy

__all__ = [
    'ImageCompressionStrategy',
    'FontOptimizationStrategy', 
    'ContentOptimizationStrategy',
    'AdaptiveCompressionStrategy',
    'CustomCompressionStrategy',  # Nova estratégia
]

# Registro automático
AVAILABLE_STRATEGIES = {
    'image': ImageCompressionStrategy,
    'font': FontOptimizationStrategy,
    'content': ContentOptimizationStrategy,
    'adaptive': AdaptiveCompressionStrategy,
    'custom': CustomCompressionStrategy,  # Registrar aqui
}
```

#### 3. **Usar Nova Estratégia**
```python
# Exemplo de uso
from src import PDFCompressorFacade
from src.strategies import CustomCompressionStrategy

# Instanciar estratégia personalizada
custom_strategy = CustomCompressionStrategy(custom_param=0.9)

# Usar com facade
compressor = PDFCompressorFacade([custom_strategy])
result = compressor.compress_pdf("input.pdf", "output.pdf")

# Ou via CLI (após registro)
# python main.py input.pdf --strategy custom
```

### Estratégias Existentes

#### **AdaptiveCompressionStrategy** - IA Inteligente
```python
class AdaptiveCompressionStrategy(ICompressionStrategy):
    """
    Estratégia que usa IA para analisar conteúdo e 
    escolher automaticamente a melhor abordagem.
    """
    
    def __init__(self):
        self.sub_strategies = [
            ImageCompressionStrategy(),
            FontOptimizationStrategy(),
            ContentOptimizationStrategy()
        ]
        self.ai_analyzer = ContentAnalyzer()
    
    def compress(self, pdf_data: bytes, config: CompressionConfig) -> CompressionResult:
        # 1. Análise IA do conteúdo
        analysis = self.ai_analyzer.analyze(pdf_data)
        
        # 2. Seleção inteligente de estratégias
        selected_strategies = self._select_strategies(analysis)
        
        # 3. Aplicação sequencial otimizada
        result_data = pdf_data
        for strategy in selected_strategies:
            result_data = strategy.compress(result_data, config).compressed_data
        
        return self._build_result(pdf_data, result_data)
```

#### **ImageCompressionStrategy** - Foco em Imagens
```python
class ImageCompressionStrategy(ICompressionStrategy):
    """
    Estratégia especializada em otimização de imagens.
    """
    
    def compress(self, pdf_data: bytes, config: CompressionConfig) -> CompressionResult:
        # 1. Extrair imagens do PDF
        images = self._extract_images(pdf_data)
        
        # 2. Comprimir cada imagem
        compressed_images = []
        for image in images:
            compressed_img = self._compress_image(image, config.image_quality)
            compressed_images.append(compressed_img)
        
        # 3. Reincorporar imagens comprimidas
        result_data = self._rebuild_pdf_with_images(pdf_data, compressed_images)
        
        return self._build_result(pdf_data, result_data)
    
    def _compress_image(self, image_data: bytes, quality: int) -> bytes:
        """Comprime imagem individual."""
        # Implementação específica de compressão de imagem
        pass
```

---

## 🔌 Sistema de Plugin

### Arquitetura de Plugins

O CompactPDF suporta plugins para estender funcionalidades sem modificar o core:

```python
# src/plugins/base.py
from abc import ABC, abstractmethod

class IPlugin(ABC):
    """Interface base para plugins."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Nome único do plugin."""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Versão do plugin."""
        pass
    
    @abstractmethod
    def initialize(self, context: dict) -> None:
        """Inicializa plugin com contexto."""
        pass
    
    @abstractmethod
    def execute(self, data: any) -> any:
        """Executa funcionalidade do plugin."""
        pass

class ICompressionPlugin(IPlugin):
    """Interface específica para plugins de compressão."""
    
    @abstractmethod
    def get_strategy(self) -> ICompressionStrategy:
        """Retorna estratégia implementada pelo plugin."""
        pass
```

### Criando Plugin

```python
# plugins/watermark_plugin.py
from src.plugins.base import ICompressionPlugin
from src.interfaces.compression import ICompressionStrategy

class WatermarkCompressionStrategy(ICompressionStrategy):
    """Estratégia que remove marcas d'água durante compressão."""
    
    def compress(self, pdf_data: bytes, config: CompressionConfig) -> CompressionResult:
        # 1. Detectar marcas d'água
        watermarks = self._detect_watermarks(pdf_data)
        
        # 2. Remover marcas d'água
        clean_data = self._remove_watermarks(pdf_data, watermarks)
        
        # 3. Aplicar compressão padrão
        compressed_data = self._standard_compression(clean_data, config)
        
        return CompressionResult(...)
    
    def get_strategy_name(self) -> str:
        return "watermark_removal"

class WatermarkPlugin(ICompressionPlugin):
    """Plugin para remoção de marcas d'água."""
    
    def get_name(self) -> str:
        return "watermark_plugin"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def initialize(self, context: dict) -> None:
        self.strategy = WatermarkCompressionStrategy()
    
    def execute(self, data: any) -> any:
        return self.strategy.compress(data['pdf_data'], data['config'])
    
    def get_strategy(self) -> ICompressionStrategy:
        return self.strategy
```

### Carregamento de Plugins

```python
# src/plugins/manager.py
import importlib
import os
from typing import List, Dict
from .base import IPlugin

class PluginManager:
    """Gerenciador de plugins do sistema."""
    
    def __init__(self, plugin_dir: str = "plugins/"):
        self.plugin_dir = plugin_dir
        self.loaded_plugins: Dict[str, IPlugin] = {}
    
    def discover_plugins(self) -> List[str]:
        """Descobre plugins disponíveis."""
        plugins = []
        if os.path.exists(self.plugin_dir):
            for file in os.listdir(self.plugin_dir):
                if file.endswith('_plugin.py'):
                    plugins.append(file[:-3])  # Remove .py
        return plugins
    
    def load_plugin(self, plugin_name: str) -> IPlugin:
        """Carrega plugin específico."""
        try:
            module = importlib.import_module(f"plugins.{plugin_name}")
            plugin_class = getattr(module, f"{plugin_name.title()}Plugin")
            
            plugin = plugin_class()
            plugin.initialize({'plugin_dir': self.plugin_dir})
            
            self.loaded_plugins[plugin_name] = plugin
            return plugin
            
        except Exception as e:
            raise PluginLoadError(f"Erro ao carregar plugin {plugin_name}: {e}")
    
    def get_available_strategies(self) -> Dict[str, ICompressionStrategy]:
        """Retorna estratégias de todos os plugins carregados."""
        strategies = {}
        for plugin in self.loaded_plugins.values():
            if hasattr(plugin, 'get_strategy'):
                strategy = plugin.get_strategy()
                strategies[strategy.get_strategy_name()] = strategy
        return strategies
```

---

## 🧪 Testes e Qualidade

### Estrutura de Testes

```python
# tests/test_strategies/test_image_strategy.py
import pytest
from unittest.mock import Mock, patch
from src.strategies import ImageCompressionStrategy
from src.config import CompressionConfig

class TestImageCompressionStrategy:
    """Suite de testes para estratégia de compressão de imagens."""
    
    @pytest.fixture
    def strategy(self):
        """Fixture que fornece instância da estratégia."""
        return ImageCompressionStrategy()
    
    @pytest.fixture
    def sample_pdf_data(self):
        """Fixture com dados de PDF de teste."""
        return b"sample_pdf_data_with_images"
    
    @pytest.fixture
    def compression_config(self):
        """Fixture com configuração padrão."""
        return CompressionConfig(image_quality=80, resize_images=True)
    
    def test_compress_basic(self, strategy, sample_pdf_data, compression_config):
        """Testa compressão básica."""
        result = strategy.compress(sample_pdf_data, compression_config)
        
        assert result.success is True
        assert result.compressed_size < result.original_size
        assert result.strategy_used == "image_compression"
        assert 0 < result.compression_ratio < 1
    
    @patch('src.strategies.image_compression.extract_images')
    def test_extract_images_called(self, mock_extract, strategy, sample_pdf_data, compression_config):
        """Testa se extração de imagens é chamada."""
        mock_extract.return_value = []
        
        strategy.compress(sample_pdf_data, compression_config)
        
        mock_extract.assert_called_once_with(sample_pdf_data)
    
    @pytest.mark.parametrize("quality,expected_size_range", [
        (100, (0.8, 1.0)),  # Alta qualidade = menos compressão
        (50, (0.4, 0.7)),   # Média qualidade = compressão moderada
        (10, (0.1, 0.4)),   # Baixa qualidade = alta compressão
    ])
    def test_quality_impact(self, strategy, sample_pdf_data, quality, expected_size_range):
        """Testa impacto da qualidade na compressão."""
        config = CompressionConfig(image_quality=quality)
        result = strategy.compress(sample_pdf_data, config)
        
        min_expected, max_expected = expected_size_range
        assert min_expected <= result.compression_ratio <= max_expected
    
    def test_can_handle_image_rich_pdf(self, strategy):
        """Testa se estratégia aceita PDFs ricos em imagens."""
        analysis = {
            'image_content_ratio': 0.8,
            'total_images': 50,
            'image_size_mb': 15.5
        }
        
        assert strategy.can_handle(analysis) is True
    
    def test_cannot_handle_text_only_pdf(self, strategy):
        """Testa se estratégia rejeita PDFs apenas com texto."""
        analysis = {
            'image_content_ratio': 0.05,
            'total_images': 1,
            'image_size_mb': 0.1
        }
        
        assert strategy.can_handle(analysis) is False
    
    def test_estimate_compression_accuracy(self, strategy):
        """Testa precisão da estimativa de compressão."""
        analysis = {
            'image_content_ratio': 0.6,
            'image_quality_avg': 85,
            'total_images': 25
        }
        
        estimate = strategy.estimate_compression(analysis)
        
        assert 0.3 <= estimate <= 0.8  # Estimativa razoável
        assert isinstance(estimate, float)

# tests/test_integration/test_full_workflow.py
class TestFullWorkflow:
    """Testes de integração do workflow completo."""
    
    def test_end_to_end_compression(self, temp_pdf_file):
        """Teste end-to-end completo."""
        from src import PDFCompressorFacade
        from src.config import CompressionConfig
        
        # Setup
        compressor = PDFCompressorFacade()
        config = CompressionConfig(image_quality=75)
        
        # Execute
        result = compressor.compress_pdf(
            input_path=temp_pdf_file,
            output_path=temp_pdf_file.replace('.pdf', '_compressed.pdf'),
            config=config
        )
        
        # Verify
        assert result.success is True
        assert result.compression_ratio > 0
        assert os.path.exists(temp_pdf_file.replace('.pdf', '_compressed.pdf'))
```

### Executando Testes

```bash
# Todos os testes
pytest

# Testes com coverage
pytest --cov=src --cov-report=html tests/

# Testes específicos
pytest tests/test_strategies/

# Testes por marcadores
pytest -m "not slow" -v

# Testes paralelos
pytest -n auto tests/

# Testes com output detalhado
pytest -v -s tests/
```

### Qualidade de Código

#### **Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
    -   id: black
        language_version: python3.8

-   repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
    -   id: isort

-   repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
    -   id: flake8

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
    -   id: mypy
```

#### **Configuração de Qualidade**
```ini
# setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,docs/,old/,build/,dist/

[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --strict-markers --disable-warnings
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

---

## 🚀 Performance e Otimização

### Profiling de Performance

```python
# tools/profiler.py
import cProfile
import pstats
import io
from src import PDFCompressorFacade

def profile_compression():
    """Profile de compressão completa."""
    pr = cProfile.Profile()
    
    # Setup
    compressor = PDFCompressorFacade()
    
    # Profile
    pr.enable()
    result = compressor.compress_pdf("sample.pdf", "output.pdf")
    pr.disable()
    
    # Análise
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    
    print(s.getvalue())
    return result

if __name__ == "__main__":
    profile_compression()
```

### Otimizações de Memória

```python
# src/utils/memory_optimizer.py
import gc
import psutil
import threading
from typing import Any, Callable

class MemoryManager:
    """Gerenciador inteligente de memória."""
    
    def __init__(self, max_memory_mb: int = 512):
        self.max_memory_mb = max_memory_mb
        self.current_usage = 0
        self._lock = threading.RLock()
    
    def monitor_memory(self, func: Callable) -> Callable:
        """Decorator para monitorar uso de memória."""
        def wrapper(*args, **kwargs):
            with self._lock:
                # Memória antes
                mem_before = psutil.Process().memory_info().rss / 1024 / 1024
                
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    # Memória depois
                    mem_after = psutil.Process().memory_info().rss / 1024 / 1024
                    
                    # Cleanup se necessário
                    if mem_after > self.max_memory_mb:
                        self._force_cleanup()
                        
        return wrapper
    
    def _force_cleanup(self):
        """Força limpeza de memória."""
        gc.collect()
        
        # Limpar caches específicos
        if hasattr(self, '_compression_cache'):
            self._compression_cache.clear()

# Uso do decorator
memory_manager = MemoryManager(max_memory_mb=1024)

@memory_manager.monitor_memory
def compress_large_pdf(pdf_data: bytes) -> bytes:
    """Comprime PDF grande com monitoramento de memória."""
    # Processamento em chunks para economizar memória
    chunk_size = 1024 * 1024  # 1MB chunks
    processed_chunks = []
    
    for i in range(0, len(pdf_data), chunk_size):
        chunk = pdf_data[i:i + chunk_size]
        processed_chunk = process_chunk(chunk)
        processed_chunks.append(processed_chunk)
    
    return b''.join(processed_chunks)
```

### Cache Inteligente

```python
# src/utils/cache.py
import hashlib
import pickle
import time
from pathlib import Path
from typing import Any, Optional

class SmartCache:
    """Cache inteligente com LRU e expiração."""
    
    def __init__(self, cache_dir: str, max_size_mb: int = 100, ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_size_mb = max_size_mb
        self.ttl_seconds = ttl_hours * 3600
        self._access_times = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera item do cache."""
        cache_file = self._get_cache_file(key)
        
        if not cache_file.exists():
            return None
        
        # Verificar expiração
        if self._is_expired(cache_file):
            cache_file.unlink()
            return None
        
        # Atualizar tempo de acesso
        self._access_times[key] = time.time()
        
        # Carregar dados
        try:
            with cache_file.open('rb') as f:
                return pickle.load(f)
        except Exception:
            cache_file.unlink()  # Remove cache corrompido
            return None
    
    def set(self, key: str, value: Any) -> None:
        """Armazena item no cache."""
        # Verificar espaço disponível
        self._ensure_space()
        
        cache_file = self._get_cache_file(key)
        
        try:
            with cache_file.open('wb') as f:
                pickle.dump(value, f)
            
            self._access_times[key] = time.time()
            
        except Exception as e:
            if cache_file.exists():
                cache_file.unlink()
            raise CacheError(f"Erro ao salvar cache: {e}")
    
    def _get_cache_file(self, key: str) -> Path:
        """Gera caminho do arquivo de cache."""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.cache"
    
    def _is_expired(self, cache_file: Path) -> bool:
        """Verifica se cache expirou."""
        age = time.time() - cache_file.stat().st_mtime
        return age > self.ttl_seconds
    
    def _ensure_space(self) -> None:
        """Garante espaço disponível removendo itens LRU."""
        current_size = self._get_cache_size_mb()
        
        if current_size > self.max_size_mb:
            # Ordenar por tempo de acesso (LRU primeiro)
            sorted_files = sorted(
                self.cache_dir.glob("*.cache"),
                key=lambda f: self._access_times.get(f.stem, 0)
            )
            
            # Remover até ter espaço
            for cache_file in sorted_files:
                cache_file.unlink()
                current_size = self._get_cache_size_mb()
                
                if current_size <= self.max_size_mb * 0.8:  # 80% do limite
                    break
    
    def _get_cache_size_mb(self) -> float:
        """Calcula tamanho atual do cache em MB."""
        total_size = sum(
            f.stat().st_size 
            for f in self.cache_dir.glob("*.cache")
        )
        return total_size / 1024 / 1024
```

---

## 🤝 Contribuindo

### Processo de Contribuição

#### 1. **Fork e Clone**
```bash
# Fork no GitHub
# Depois clone seu fork
git clone https://github.com/SEU_USUARIO/CompactPDF.git
cd CompactPDF

# Adicionar upstream
git remote add upstream https://github.com/IgorGSBarbosaDev/CompactPDF.git
```

#### 2. **Branch de Feature**
```bash
# Criar branch para nova funcionalidade
git checkout -b feature/nova-estrategia-ia

# Ou para correção de bug
git checkout -b fix/corrigir-cache-memoria
```

#### 3. **Desenvolvimento**
```bash
# Instalar dependências de dev
pip install -r requirements-dev.txt

# Executar testes frequentemente
pytest

# Verificar qualidade do código
black src/ tests/
flake8 src/ tests/
mypy src/
```

#### 4. **Commit e Push**
```bash
# Commits semânticos
git commit -m "feat: adicionar estratégia de IA para PDFs técnicos"
git commit -m "fix: corrigir vazamento de memória no cache"
git commit -m "docs: atualizar guia do desenvolvedor"

# Push da branch
git push origin feature/nova-estrategia-ia
```

#### 5. **Pull Request**
- Criar PR no GitHub
- Preencher template de PR
- Aguardar review
- Aplicar correções solicitadas

### Convenções de Commit

```bash
# Tipos de commit
feat:     # Nova funcionalidade
fix:      # Correção de bug
docs:     # Documentação
style:    # Formatação (não afeta lógica)
refactor: # Refatoração de código
test:     # Adição/correção de testes
chore:    # Tarefas de manutenção

# Exemplos
git commit -m "feat(strategies): adicionar estratégia de compressão neural"
git commit -m "fix(cache): corrigir race condition no LRU cache"
git commit -m "docs(api): atualizar documentação da interface principal"
```

### Checklist de PR

- [ ] Código segue padrões do projeto (Black, flake8)
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Nenhum teste quebrado
- [ ] Performance não foi degradada
- [ ] Compatibilidade mantida
- [ ] Changelog atualizado (se necessário)

### Reportando Bugs

Use o template de issue:

```markdown
## Descrição do Bug
Descrição clara e concisa do problema.

## Passos para Reproduzir
1. Executar comando '...'
2. Com arquivo '...'
3. Observar erro '...'

## Comportamento Esperado
O que deveria acontecer.

## Comportamento Atual
O que está acontecendo.

## Ambiente
- OS: [Windows/Linux/Mac]
- Python: [3.8/3.9/3.10/3.11]
- CompactPDF: [versão]

## Arquivos de Exemplo
Anexar PDF de teste se possível.

## Logs
```
Logs relevantes
```
```

---

## 📚 Recursos Adicionais

### Documentação Relacionada
- **Arquitetura:** [`ARCHITECTURE.md`](ARCHITECTURE.md)
- **API Reference:** [`API_REFERENCE.md`](API_REFERENCE.md)
- **Exemplos:** [`EXAMPLES.md`](EXAMPLES.md)
- **Troubleshooting:** [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)

### Ferramentas Recomendadas
- **IDE:** VS Code ou PyCharm
- **Debugger:** pdb, ipdb ou IDE debugger
- **Profiler:** cProfile, py-spy
- **Memory:** memory_profiler, pympler
- **Tests:** pytest, coverage
- **Docs:** sphinx, mkdocs

### Comunidade
- **Issues:** GitHub Issues para bugs e features
- **Discussions:** GitHub Discussions para perguntas
- **Wiki:** Documentação colaborativa
- **Examples:** Repositório de exemplos da comunidade

---

*📝 Este guia é atualizado constantemente. Contribuições são bem-vindas!*
