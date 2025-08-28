# 📚 Referência da API - CompactPDF

Documentação completa da API do sistema CompactPDF.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Classes Principais](#classes-principais)
3. [Interfaces](#interfaces)
4. [Estratégias](#estratégias)
5. [Modelos de Dados](#modelos-de-dados)
6. [Serviços](#serviços)
7. [Utilitários](#utilitários)
8. [Configurações](#configurações)
9. [Exceções](#exceções)
10. [Exemplos de Uso](#exemplos-de-uso)

---

## 🌟 Visão Geral

A API do CompactPDF é projetada para ser intuitiva, flexível e extensível. Todas as funcionalidades principais são acessíveis através da classe `PDFCompressorFacade`, que atua como ponto de entrada único para o sistema.

### Importação Principal

```python
from src.pdf_compressor_facade import PDFCompressorFacade
from src.config.compression_config import CompressionConfig
from src.models.compression_result import CompressionResult
```

---

## 🏛️ Classes Principais

### PDFCompressorFacade

**Descrição:** Classe principal que orquestra todo o processo de compressão.

```python
class PDFCompressorFacade:
    """
    Facade principal para operações de compressão de PDF.
    
    Esta classe simplifica o acesso a todo o sistema de compressão,
    fornecendo uma interface unificada para diferentes estratégias
    e funcionalidades.
    """
```

#### **Construtor**

```python
def __init__(
    self,
    strategies: Optional[List[ICompressionStrategy]] = None,
    file_service: Optional[IPDFFileService] = None,
    metrics_service: Optional[ICompressionMetrics] = None,
    cache: Optional[ICompressionCache] = None,
    backup_manager: Optional[IBackupManager] = None,
    analytics: Optional[ICompressionAnalytics] = None,
    logger: Optional[ILogger] = None
)
```

**Parâmetros:**
- `strategies` (List[ICompressionStrategy], opcional): Lista de estratégias de compressão
- `file_service` (IPDFFileService, opcional): Serviço para operações de arquivo
- `metrics_service` (ICompressionMetrics, opcional): Serviço de cálculo de métricas
- `cache` (ICompressionCache, opcional): Sistema de cache
- `backup_manager` (IBackupManager, opcional): Gerenciador de backups
- `analytics` (ICompressionAnalytics, opcional): Sistema de analytics
- `logger` (ILogger, opcional): Sistema de logging

#### **Métodos Principais**

##### compress_pdf()

```python
def compress_pdf(
    self,
    input_path: str,
    output_path: str,
    config: Optional[CompressionConfig] = None,
    progress_callback: Optional[Callable[[float, str], None]] = None
) -> CompressionResult:
    """
    Comprime um arquivo PDF usando configuração especificada.
    
    Args:
        input_path (str): Caminho para o arquivo PDF de entrada
        output_path (str): Caminho para o arquivo PDF de saída
        config (CompressionConfig, opcional): Configuração de compressão
        progress_callback (Callable, opcional): Callback para progresso
    
    Returns:
        CompressionResult: Resultado da compressão com métricas
    
    Raises:
        FileNotFoundError: Se arquivo de entrada não existir
        PermissionError: Se não houver permissão para escrever
        InvalidPDFError: Se arquivo não for um PDF válido
        CompressionError: Se compressão falhar
    
    Example:
        >>> facade = PDFCompressorFacade()
        >>> config = CompressionConfig(strategy='adaptive', quality=80)
        >>> result = facade.compress_pdf('input.pdf', 'output.pdf', config)
        >>> print(f"Compressão: {result.compression_ratio:.1%}")
    """
```

##### compress_with_preset()

```python
def compress_with_preset(
    self,
    input_path: str,
    output_path: str,
    preset: str,
    progress_callback: Optional[Callable[[float, str], None]] = None
) -> CompressionResult:
    """
    Comprime PDF usando preset predefinido.
    
    Args:
        input_path (str): Caminho para arquivo de entrada
        output_path (str): Caminho para arquivo de saída
        preset (str): Nome do preset ('web', 'print', 'maximum', 'balanced', 'quality')
        progress_callback (Callable, opcional): Callback para progresso
    
    Returns:
        CompressionResult: Resultado da compressão
    
    Example:
        >>> result = facade.compress_with_preset('doc.pdf', 'compressed.pdf', 'web')
    """
```

##### batch_compress()

```python
def batch_compress(
    self,
    input_patterns: List[str],
    output_dir: str,
    config: Optional[CompressionConfig] = None,
    progress_callback: Optional[Callable[[float, str], None]] = None,
    preserve_structure: bool = True
) -> List[CompressionResult]:
    """
    Comprime múltiplos arquivos PDF em lote.
    
    Args:
        input_patterns (List[str]): Padrões de arquivos (glob patterns)
        output_dir (str): Diretório de saída
        config (CompressionConfig, opcional): Configuração de compressão
        progress_callback (Callable, opcional): Callback para progresso
        preserve_structure (bool): Preservar estrutura de diretórios
    
    Returns:
        List[CompressionResult]: Lista de resultados para cada arquivo
    
    Example:
        >>> patterns = ['docs/*.pdf', 'reports/**/*.pdf']
        >>> results = facade.batch_compress(patterns, 'compressed/', config)
    """
```

##### analyze_pdf()

```python
def analyze_pdf(
    self,
    file_path: str
) -> PDFAnalysis:
    """
    Analisa estrutura e conteúdo de um PDF.
    
    Args:
        file_path (str): Caminho para o arquivo PDF
    
    Returns:
        PDFAnalysis: Análise detalhada do PDF
    
    Example:
        >>> analysis = facade.analyze_pdf('document.pdf')
        >>> print(f"Páginas: {analysis.page_count}")
        >>> print(f"Imagens: {analysis.image_count}")
    """
```

##### get_compression_recommendations()

```python
def get_compression_recommendations(
    self,
    file_path: str
) -> CompressionRecommendations:
    """
    Obtém recomendações de compressão para um PDF.
    
    Args:
        file_path (str): Caminho para o arquivo PDF
    
    Returns:
        CompressionRecommendations: Recomendações de estratégias e configurações
    
    Example:
        >>> recommendations = facade.get_compression_recommendations('doc.pdf')
        >>> print(f"Estratégia recomendada: {recommendations.best_strategy}")
    """
```

---

## 🔌 Interfaces

### ICompressionStrategy

**Descrição:** Interface base para todas as estratégias de compressão.

```python
class ICompressionStrategy(ABC):
    """Interface para estratégias de compressão de PDF."""
    
    @abstractmethod
    def compress(
        self,
        pdf_data: bytes,
        config: CompressionConfig
    ) -> CompressionResult:
        """
        Aplica compressão aos dados do PDF.
        
        Args:
            pdf_data (bytes): Dados binários do PDF
            config (CompressionConfig): Configuração de compressão
        
        Returns:
            CompressionResult: Resultado da compressão
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Retorna o nome identificador da estratégia.
        
        Returns:
            str: Nome da estratégia
        """
        pass
    
    @abstractmethod
    def can_handle(self, pdf_analysis: PDFAnalysis) -> bool:
        """
        Verifica se a estratégia pode processar o PDF.
        
        Args:
            pdf_analysis (PDFAnalysis): Análise do PDF
        
        Returns:
            bool: True se pode processar, False caso contrário
        """
        pass
    
    def get_estimated_compression(
        self,
        pdf_analysis: PDFAnalysis
    ) -> float:
        """
        Estima taxa de compressão para o PDF.
        
        Args:
            pdf_analysis (PDFAnalysis): Análise do PDF
        
        Returns:
            float: Taxa estimada de compressão (0.0 a 1.0)
        """
        return 0.5  # Implementação padrão
```

### IPDFFileService

**Descrição:** Interface para operações com arquivos PDF.

```python
class IPDFFileService(ABC):
    """Interface para operações com arquivos PDF."""
    
    @abstractmethod
    def read_pdf(self, file_path: str) -> bytes:
        """
        Lê arquivo PDF e retorna dados binários.
        
        Args:
            file_path (str): Caminho para o arquivo
        
        Returns:
            bytes: Dados binários do PDF
        """
        pass
    
    @abstractmethod
    def write_pdf(self, file_path: str, pdf_data: bytes) -> None:
        """
        Escreve dados binários em arquivo PDF.
        
        Args:
            file_path (str): Caminho para o arquivo de saída
            pdf_data (bytes): Dados binários do PDF
        """
        pass
    
    @abstractmethod
    def validate_pdf(self, file_path: str) -> bool:
        """
        Valida se arquivo é um PDF válido.
        
        Args:
            file_path (str): Caminho para o arquivo
        
        Returns:
            bool: True se válido, False caso contrário
        """
        pass
```

### ICompressionMetrics

**Descrição:** Interface para cálculo de métricas de compressão.

```python
class ICompressionMetrics(ABC):
    """Interface para cálculo de métricas de compressão."""
    
    @abstractmethod
    def calculate_compression_ratio(
        self,
        original_size: int,
        compressed_size: int
    ) -> float:
        """
        Calcula taxa de compressão.
        
        Args:
            original_size (int): Tamanho original em bytes
            compressed_size (int): Tamanho comprimido em bytes
        
        Returns:
            float: Taxa de compressão (0.0 a 1.0)
        """
        pass
    
    @abstractmethod
    def calculate_space_saved(
        self,
        original_size: int,
        compressed_size: int
    ) -> int:
        """
        Calcula espaço economizado.
        
        Args:
            original_size (int): Tamanho original em bytes
            compressed_size (int): Tamanho comprimido em bytes
        
        Returns:
            int: Bytes economizados
        """
        pass
```

---

## ⚡ Estratégias

### ImageCompressionStrategy

**Descrição:** Estratégia focada na compressão de imagens dentro do PDF.

```python
class ImageCompressionStrategy(ICompressionStrategy):
    """
    Estratégia para compressão de imagens em PDFs.
    
    Otimiza imagens através de:
    - Redimensionamento baseado em DPI
    - Recompressão JPEG com qualidade ajustável
    - Conversão para formatos mais eficientes
    - Remoção de canais alpha desnecessários
    """
    
    def __init__(
        self,
        quality: int = 80,
        max_dpi: int = 150,
        convert_to_jpeg: bool = True
    ):
        """
        Inicializa estratégia de compressão de imagens.
        
        Args:
            quality (int): Qualidade JPEG (0-100)
            max_dpi (int): DPI máximo para imagens
            convert_to_jpeg (bool): Converter imagens para JPEG
        """
        self.quality = quality
        self.max_dpi = max_dpi
        self.convert_to_jpeg = convert_to_jpeg
```

**Métodos Específicos:**

```python
def optimize_image(
    self,
    image_data: bytes,
    image_format: str
) -> bytes:
    """
    Otimiza uma imagem individual.
    
    Args:
        image_data (bytes): Dados da imagem
        image_format (str): Formato da imagem
    
    Returns:
        bytes: Imagem otimizada
    """
    pass

def calculate_optimal_dpi(
    self,
    image_width: int,
    image_height: int,
    page_width: float,
    page_height: float
) -> int:
    """
    Calcula DPI ótimo baseado no tamanho da página.
    
    Args:
        image_width (int): Largura da imagem em pixels
        image_height (int): Altura da imagem em pixels
        page_width (float): Largura da página em pontos
        page_height (float): Altura da página em pontos
    
    Returns:
        int: DPI recomendado
    """
    pass
```

### FontOptimizationStrategy

**Descrição:** Estratégia para otimização de fontes no PDF.

```python
class FontOptimizationStrategy(ICompressionStrategy):
    """
    Estratégia para otimização de fontes em PDFs.
    
    Otimiza fontes através de:
    - Subset de fontes (manter apenas caracteres usados)
    - Remoção de fontes não utilizadas
    - Merge de fontes similares
    - Compressão de dados de fonte
    """
    
    def __init__(
        self,
        create_subset: bool = True,
        remove_unused: bool = True,
        merge_similar: bool = False
    ):
        """
        Inicializa estratégia de otimização de fontes.
        
        Args:
            create_subset (bool): Criar subset das fontes
            remove_unused (bool): Remover fontes não usadas
            merge_similar (bool): Fazer merge de fontes similares
        """
        self.create_subset = create_subset
        self.remove_unused = remove_unused
        self.merge_similar = merge_similar
```

### ContentOptimizationStrategy

**Descrição:** Estratégia para otimização da estrutura e conteúdo do PDF.

```python
class ContentOptimizationStrategy(ICompressionStrategy):
    """
    Estratégia para otimização de conteúdo e estrutura do PDF.
    
    Otimiza através de:
    - Remoção de objetos não utilizados
    - Compressão de streams de conteúdo
    - Otimização da estrutura do documento
    - Deduplicação de recursos
    """
    
    def __init__(
        self,
        remove_unused_objects: bool = True,
        compress_streams: bool = True,
        optimize_structure: bool = True,
        deduplicate_resources: bool = True
    ):
        """
        Inicializa estratégia de otimização de conteúdo.
        
        Args:
            remove_unused_objects (bool): Remover objetos não usados
            compress_streams (bool): Comprimir streams
            optimize_structure (bool): Otimizar estrutura
            deduplicate_resources (bool): Deduplicar recursos
        """
        self.remove_unused_objects = remove_unused_objects
        self.compress_streams = compress_streams
        self.optimize_structure = optimize_structure
        self.deduplicate_resources = deduplicate_resources
```

### AdaptiveCompressionStrategy

**Descrição:** Estratégia inteligente que combina múltiplas técnicas.

```python
class AdaptiveCompressionStrategy(ICompressionStrategy):
    """
    Estratégia adaptativa que seleciona automaticamente
    as melhores técnicas baseado no conteúdo do PDF.
    
    Combina:
    - Análise automática de conteúdo
    - Seleção inteligente de estratégias
    - Aplicação sequencial otimizada
    - Validação de qualidade em tempo real
    """
    
    def __init__(
        self,
        available_strategies: List[ICompressionStrategy],
        quality_threshold: float = 0.95,
        max_strategies: int = 3
    ):
        """
        Inicializa estratégia adaptativa.
        
        Args:
            available_strategies (List[ICompressionStrategy]): Estratégias disponíveis
            quality_threshold (float): Limite mínimo de qualidade
            max_strategies (int): Número máximo de estratégias a aplicar
        """
        self.available_strategies = available_strategies
        self.quality_threshold = quality_threshold
        self.max_strategies = max_strategies
```

---

## 📊 Modelos de Dados

### CompressionResult

**Descrição:** Modelo que encapsula o resultado de uma operação de compressão.

```python
@dataclass
class CompressionResult:
    """
    Resultado de uma operação de compressão de PDF.
    
    Contém todas as informações sobre o processo de compressão,
    incluindo métricas, tempo de execução e metadados.
    """
    
    # Informações básicas
    input_path: str
    output_path: str
    success: bool
    
    # Métricas de tamanho
    original_size: int
    compressed_size: int
    compression_ratio: float
    space_saved: int
    
    # Métricas de tempo
    processing_time: float
    start_time: datetime
    end_time: datetime
    
    # Estratégias aplicadas
    strategies_used: List[str]
    strategy_results: Dict[str, Any]
    
    # Métricas de qualidade
    quality_score: Optional[float] = None
    quality_metrics: Optional[Dict[str, float]] = None
    
    # Informações do arquivo
    page_count: Optional[int] = None
    has_images: Optional[bool] = None
    has_fonts: Optional[bool] = None
    has_forms: Optional[bool] = None
    
    # Metadados
    backup_created: bool = False
    backup_path: Optional[str] = None
    cache_hit: bool = False
    error_message: Optional[str] = None
    
    def __post_init__(self):
        """Calcula campos derivados após inicialização."""
        if self.compressed_size > 0:
            self.compression_ratio = 1 - (self.compressed_size / self.original_size)
            self.space_saved = self.original_size - self.compressed_size
    
    @property
    def compression_percentage(self) -> float:
        """Retorna porcentagem de compressão."""
        return self.compression_ratio * 100
    
    @property
    def size_reduction_mb(self) -> float:
        """Retorna redução de tamanho em MB."""
        return self.space_saved / (1024 * 1024)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte resultado para dicionário."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Converte resultado para JSON."""
        return json.dumps(self.to_dict(), default=str, indent=2)
```

### CompressionConfig

**Descrição:** Configuração para operações de compressão.

```python
@dataclass
class CompressionConfig:
    """
    Configuração para compressão de PDF.
    
    Define todos os parâmetros necessários para personalizar
    o processo de compressão.
    """
    
    # Estratégia principal
    strategy: str = 'adaptive'
    
    # Configurações de qualidade
    quality: int = 80  # 0-100
    preserve_quality: bool = True
    quality_threshold: float = 0.95
    
    # Configurações de imagem
    image_quality: int = 80
    max_image_dpi: int = 150
    convert_images_to_jpeg: bool = True
    resize_large_images: bool = True
    
    # Configurações de fonte
    subset_fonts: bool = True
    remove_unused_fonts: bool = True
    merge_similar_fonts: bool = False
    
    # Configurações de conteúdo
    remove_unused_objects: bool = True
    compress_streams: bool = True
    optimize_structure: bool = True
    
    # Configurações de sistema
    use_cache: bool = True
    create_backup: bool = True
    parallel_processing: bool = True
    max_workers: int = 4
    
    # Configurações de saída
    overwrite_existing: bool = False
    preserve_metadata: bool = True
    preserve_bookmarks: bool = True
    preserve_annotations: bool = True
    
    def validate(self) -> List[str]:
        """
        Valida configuração e retorna lista de erros.
        
        Returns:
            List[str]: Lista de mensagens de erro (vazia se válida)
        """
        errors = []
        
        if not 0 <= self.quality <= 100:
            errors.append("Quality deve estar entre 0 e 100")
        
        if not 0 <= self.image_quality <= 100:
            errors.append("Image quality deve estar entre 0 e 100")
        
        if self.max_image_dpi < 50:
            errors.append("Max image DPI deve ser pelo menos 50")
        
        if not 0 < self.quality_threshold <= 1:
            errors.append("Quality threshold deve estar entre 0 e 1")
        
        return errors
    
    @classmethod
    def from_preset(cls, preset_name: str) -> 'CompressionConfig':
        """
        Cria configuração a partir de preset.
        
        Args:
            preset_name (str): Nome do preset
        
        Returns:
            CompressionConfig: Configuração do preset
        """
        presets = {
            'web': cls(
                strategy='adaptive',
                quality=60,
                image_quality=60,
                max_image_dpi=96,
                convert_images_to_jpeg=True
            ),
            'print': cls(
                strategy='adaptive',
                quality=85,
                image_quality=85,
                max_image_dpi=300,
                convert_images_to_jpeg=False
            ),
            'maximum': cls(
                strategy='adaptive',
                quality=50,
                image_quality=50,
                max_image_dpi=72,
                convert_images_to_jpeg=True
            ),
            'balanced': cls(
                strategy='adaptive',
                quality=75,
                image_quality=75,
                max_image_dpi=150,
                convert_images_to_jpeg=True
            ),
            'quality': cls(
                strategy='adaptive',
                quality=95,
                image_quality=95,
                max_image_dpi=300,
                preserve_quality=True
            )
        }
        
        if preset_name not in presets:
            raise ValueError(f"Preset '{preset_name}' não encontrado")
        
        return presets[preset_name]
```

### PDFAnalysis

**Descrição:** Análise detalhada de um arquivo PDF.

```python
@dataclass
class PDFAnalysis:
    """
    Análise detalhada de um arquivo PDF.
    
    Contém informações sobre estrutura, conteúdo e
    características do PDF para otimizar compressão.
    """
    
    # Informações básicas
    file_path: str
    file_size: int
    page_count: int
    
    # Análise de conteúdo
    image_count: int
    image_total_size: int
    font_count: int
    font_total_size: int
    
    # Tipos de conteúdo
    has_images: bool
    has_text: bool
    has_forms: bool
    has_annotations: bool
    has_bookmarks: bool
    has_javascript: bool
    
    # Análise de imagens
    image_formats: Dict[str, int]  # formato -> quantidade
    average_image_dpi: Optional[float]
    max_image_size: Optional[int]
    
    # Análise de fontes
    font_types: Dict[str, int]  # tipo -> quantidade
    embedded_fonts: int
    subset_fonts: int
    
    # Estimativas de compressão
    estimated_image_reduction: float
    estimated_font_reduction: float
    estimated_content_reduction: float
    estimated_total_reduction: float
    
    # Recomendações
    recommended_strategies: List[str]
    complexity_score: float  # 0-1, onde 1 é mais complexo
    
    def get_content_distribution(self) -> Dict[str, float]:
        """
        Retorna distribuição do conteúdo por tipo.
        
        Returns:
            Dict[str, float]: Porcentagem por tipo de conteúdo
        """
        total_size = self.file_size
        return {
            'images': (self.image_total_size / total_size) * 100,
            'fonts': (self.font_total_size / total_size) * 100,
            'other': ((total_size - self.image_total_size - self.font_total_size) / total_size) * 100
        }
    
    def get_optimization_potential(self) -> str:
        """
        Avalia potencial de otimização.
        
        Returns:
            str: 'alto', 'médio' ou 'baixo'
        """
        if self.estimated_total_reduction > 0.5:
            return 'alto'
        elif self.estimated_total_reduction > 0.2:
            return 'médio'
        else:
            return 'baixo'
```

---

## 🛠️ Serviços

### PDFFileService

**Descrição:** Serviço para operações com arquivos PDF.

```python
class PDFFileService(IPDFFileService):
    """
    Serviço para operações com arquivos PDF.
    
    Gerencia leitura, escrita e validação de arquivos PDF
    com tratamento robusto de erros e otimizações de memória.
    """
    
    def __init__(self, logger: Optional[ILogger] = None):
        """
        Inicializa serviço de arquivos PDF.
        
        Args:
            logger (ILogger, opcional): Sistema de logging
        """
        self.logger = logger or SimpleLogger()
    
    def read_pdf(self, file_path: str) -> bytes:
        """
        Lê arquivo PDF com otimizações de memória.
        
        Args:
            file_path (str): Caminho para o arquivo
        
        Returns:
            bytes: Dados binários do PDF
        
        Raises:
            FileNotFoundError: Se arquivo não existir
            PermissionError: Se não houver permissão de leitura
            InvalidPDFError: Se arquivo não for PDF válido
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        if not self.validate_pdf(file_path):
            raise InvalidPDFError(f"Arquivo não é um PDF válido: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except PermissionError:
            raise PermissionError(f"Sem permissão para ler: {file_path}")
    
    def write_pdf(self, file_path: str, pdf_data: bytes) -> None:
        """
        Escreve dados PDF com verificações de segurança.
        
        Args:
            file_path (str): Caminho para arquivo de saída
            pdf_data (bytes): Dados binários do PDF
        
        Raises:
            PermissionError: Se não houver permissão de escrita
            DiskSpaceError: Se não houver espaço em disco
        """
        # Verificar espaço em disco
        available_space = shutil.disk_usage(os.path.dirname(file_path)).free
        if len(pdf_data) > available_space:
            raise DiskSpaceError("Espaço insuficiente em disco")
        
        # Criar diretórios se necessário
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            with open(file_path, 'wb') as file:
                file.write(pdf_data)
        except PermissionError:
            raise PermissionError(f"Sem permissão para escrever: {file_path}")
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Obtém informações detalhadas do arquivo.
        
        Args:
            file_path (str): Caminho para o arquivo
        
        Returns:
            Dict[str, Any]: Informações do arquivo
        """
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'permissions': oct(stat.st_mode)[-3:],
            'is_readable': os.access(file_path, os.R_OK),
            'is_writable': os.access(file_path, os.W_OK)
        }
```

### CompressionMetricsService

**Descrição:** Serviço para cálculo de métricas de compressão.

```python
class CompressionMetricsService(ICompressionMetrics):
    """
    Serviço para cálculo de métricas de compressão.
    
    Calcula várias métricas de performance e qualidade
    para avaliar eficácia da compressão.
    """
    
    def calculate_comprehensive_metrics(
        self,
        original_data: bytes,
        compressed_data: bytes,
        processing_time: float
    ) -> Dict[str, float]:
        """
        Calcula métricas abrangentes de compressão.
        
        Args:
            original_data (bytes): Dados originais
            compressed_data (bytes): Dados comprimidos
            processing_time (float): Tempo de processamento
        
        Returns:
            Dict[str, float]: Dicionário com todas as métricas
        """
        original_size = len(original_data)
        compressed_size = len(compressed_data)
        
        return {
            'compression_ratio': self.calculate_compression_ratio(original_size, compressed_size),
            'space_saved_bytes': self.calculate_space_saved(original_size, compressed_size),
            'space_saved_percentage': (original_size - compressed_size) / original_size * 100,
            'compression_speed_mbps': (original_size / (1024 * 1024)) / processing_time,
            'efficiency_score': self._calculate_efficiency_score(original_size, compressed_size, processing_time),
            'quality_preservation': self._estimate_quality_preservation(original_data, compressed_data)
        }
    
    def _calculate_efficiency_score(
        self,
        original_size: int,
        compressed_size: int,
        processing_time: float
    ) -> float:
        """
        Calcula score de eficiência (compressão vs. tempo).
        
        Returns:
            float: Score de eficiência (0-100)
        """
        compression_ratio = 1 - (compressed_size / original_size)
        time_penalty = min(processing_time / 10, 1)  # Penalidade por tempo > 10s
        return max(0, (compression_ratio * 100) - (time_penalty * 20))
```

---

## 🔧 Utilitários

### CompressionCache

**Descrição:** Sistema de cache para resultados de compressão.

```python
class CompressionCache(ICompressionCache):
    """
    Cache inteligente para resultados de compressão.
    
    Implementa cache LRU com expiração baseada em tempo
    e validação de integridade.
    """
    
    def __init__(
        self,
        max_size: int = 100,
        ttl: int = 3600,  # 1 hora
        cache_dir: Optional[str] = None
    ):
        """
        Inicializa cache de compressão.
        
        Args:
            max_size (int): Número máximo de entradas
            ttl (int): Tempo de vida em segundos
            cache_dir (str, opcional): Diretório para cache persistente
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache_dir = cache_dir or self._get_default_cache_dir()
        self._cache: OrderedDict = OrderedDict()
        self._load_persistent_cache()
    
    def get(self, key: str) -> Optional[CompressionResult]:
        """
        Obtém resultado do cache.
        
        Args:
            key (str): Chave do cache
        
        Returns:
            CompressionResult: Resultado cacheado ou None
        """
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        # Verificar expiração
        if self._is_expired(entry):
            del self._cache[key]
            return None
        
        # Mover para final (LRU)
        self._cache.move_to_end(key)
        
        return entry['result']
    
    def set(self, key: str, result: CompressionResult) -> None:
        """
        Armazena resultado no cache.
        
        Args:
            key (str): Chave do cache
            result (CompressionResult): Resultado a armazenar
        """
        # Remover mais antigo se necessário
        if len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)
        
        entry = {
            'result': result,
            'timestamp': time.time(),
            'access_count': 0
        }
        
        self._cache[key] = entry
        self._save_to_persistent_cache(key, entry)
    
    def generate_key(
        self,
        file_path: str,
        config: CompressionConfig
    ) -> str:
        """
        Gera chave única para combinação arquivo/config.
        
        Args:
            file_path (str): Caminho do arquivo
            config (CompressionConfig): Configuração
        
        Returns:
            str: Chave única
        """
        # Usar hash do arquivo + configuração
        file_hash = self._calculate_file_hash(file_path)
        config_hash = self._calculate_config_hash(config)
        return f"{file_hash}_{config_hash}"
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtém estatísticas do cache.
        
        Returns:
            Dict[str, Any]: Estatísticas do cache
        """
        total_accesses = sum(entry['access_count'] for entry in self._cache.values())
        
        return {
            'size': len(self._cache),
            'max_size': self.max_size,
            'hit_rate': self._calculate_hit_rate(),
            'total_accesses': total_accesses,
            'oldest_entry': self._get_oldest_entry_age(),
            'cache_size_mb': self._calculate_cache_size_mb()
        }
```

---

## ⚙️ Configurações

### Presets de Compressão

```python
# Preset para Web (máxima compressão)
WEB_PRESET = CompressionConfig(
    strategy='adaptive',
    quality=60,
    image_quality=60,
    max_image_dpi=96,
    convert_images_to_jpeg=True,
    subset_fonts=True,
    remove_unused_fonts=True,
    compress_streams=True
)

# Preset para Impressão (qualidade alta)
PRINT_PRESET = CompressionConfig(
    strategy='adaptive',
    quality=85,
    image_quality=85,
    max_image_dpi=300,
    convert_images_to_jpeg=False,
    preserve_quality=True,
    subset_fonts=True
)

# Preset Balanceado
BALANCED_PRESET = CompressionConfig(
    strategy='adaptive',
    quality=75,
    image_quality=75,
    max_image_dpi=150,
    convert_images_to_jpeg=True,
    subset_fonts=True,
    remove_unused_fonts=True
)
```

---

## ❌ Exceções

### Exceções Personalizadas

```python
class CompressionError(Exception):
    """Erro base para operações de compressão."""
    pass

class InvalidPDFError(CompressionError):
    """Erro para arquivos PDF inválidos."""
    pass

class CompressionFailedError(CompressionError):
    """Erro quando compressão falha."""
    
    def __init__(self, message: str, strategy: str = None):
        super().__init__(message)
        self.strategy = strategy

class QualityThresholdError(CompressionError):
    """Erro quando qualidade fica abaixo do threshold."""
    
    def __init__(self, message: str, quality_score: float, threshold: float):
        super().__init__(message)
        self.quality_score = quality_score
        self.threshold = threshold

class CacheError(Exception):
    """Erro relacionado ao cache."""
    pass

class BackupError(Exception):
    """Erro relacionado ao backup."""
    pass

class DiskSpaceError(Exception):
    """Erro de espaço insuficiente em disco."""
    pass
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Compressão Básica

```python
from src.pdf_compressor_facade import PDFCompressorFacade
from src.config.compression_config import CompressionConfig

# Criar facade
facade = PDFCompressorFacade()

# Compressão simples
result = facade.compress_pdf('document.pdf', 'compressed.pdf')
print(f"Compressão: {result.compression_percentage:.1f}%")
print(f"Espaço economizado: {result.size_reduction_mb:.2f} MB")
```

### Exemplo 2: Configuração Personalizada

```python
# Configuração personalizada
config = CompressionConfig(
    strategy='adaptive',
    quality=85,
    image_quality=80,
    max_image_dpi=200,
    use_cache=True,
    create_backup=True
)

# Compressão com callback de progresso
def progress_callback(progress: float, message: str):
    print(f"[{progress:.1%}] {message}")

result = facade.compress_pdf(
    'large_document.pdf',
    'optimized.pdf',
    config=config,
    progress_callback=progress_callback
)
```

### Exemplo 3: Processamento em Lote

```python
# Compressão em lote
patterns = [
    'documents/*.pdf',
    'reports/**/*.pdf',
    'presentations/2024/*.pdf'
]

results = facade.batch_compress(
    input_patterns=patterns,
    output_dir='compressed/',
    config=config,
    preserve_structure=True
)

# Relatório de resultados
total_saved = sum(r.space_saved for r in results)
avg_compression = sum(r.compression_ratio for r in results) / len(results)

print(f"Arquivos processados: {len(results)}")
print(f"Espaço total economizado: {total_saved / (1024*1024):.2f} MB")
print(f"Compressão média: {avg_compression:.1%}")
```

### Exemplo 4: Análise Detalhada

```python
# Analisar PDF antes da compressão
analysis = facade.analyze_pdf('document.pdf')

print(f"Páginas: {analysis.page_count}")
print(f"Imagens: {analysis.image_count}")
print(f"Fontes: {analysis.font_count}")
print(f"Potencial de otimização: {analysis.get_optimization_potential()}")

# Obter recomendações
recommendations = facade.get_compression_recommendations('document.pdf')
print(f"Estratégia recomendada: {recommendations.best_strategy}")
print(f"Compressão estimada: {recommendations.estimated_reduction:.1%}")

# Aplicar recomendações
config = recommendations.to_config()
result = facade.compress_pdf('document.pdf', 'optimized.pdf', config)
```

### Exemplo 5: Integração com Sistema Existente

```python
class DocumentProcessor:
    """Integração do CompactPDF em sistema existente."""
    
    def __init__(self):
        self.compressor = PDFCompressorFacade()
    
    def process_uploaded_file(self, file_path: str) -> Dict[str, Any]:
        """Processa arquivo enviado pelo usuário."""
        try:
            # Analisar arquivo
            analysis = self.compressor.analyze_pdf(file_path)
            
            # Selecionar preset baseado no tipo
            if analysis.has_images and analysis.image_count > 10:
                preset = 'web'  # Muitas imagens = otimizar para web
            elif analysis.complexity_score > 0.7:
                preset = 'balanced'  # Complexo = balanceado
            else:
                preset = 'quality'  # Simples = manter qualidade
            
            # Comprimir
            output_path = file_path.replace('.pdf', '_compressed.pdf')
            result = self.compressor.compress_with_preset(
                file_path, output_path, preset
            )
            
            return {
                'success': True,
                'compressed_file': output_path,
                'original_size': result.original_size,
                'compressed_size': result.compressed_size,
                'compression_ratio': result.compression_ratio,
                'processing_time': result.processing_time
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
```

---

*📝 Esta documentação da API é mantida atualizada com cada versão do CompactPDF.*
