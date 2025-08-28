"""
Utilities module.
Contains helper functions, utilities, and advanced features.
Enhanced with performance optimizations and memory management.
"""

from .logger import SimpleLogger, NullLogger
from .logger_optimized import (
    BufferedLogger, OptimizedSimpleLogger, get_logger, 
    get_global_logger, set_global_logger
)
from .file_utils import (
    is_pdf_file,
    validate_output_path,
    get_safe_filename,
    generate_output_filename,
    get_unique_filename,
    find_pdf_files,
    estimate_compression_time
)
from .image_quality import ImageQualityAssessor
from .cache import CompressionCache, InMemoryCache
from .backup import BackupManager, OperationRecovery
from .analytics import CompressionAnalytics
from .adaptive_optimizer import AdaptiveCompressionOptimizer
from .memory_optimizer import (
    MemoryManager, SmartCache, memory_optimized, cached_property,
    global_memory_manager, global_cache, get_memory_info, cleanup_all
)

__all__ = [
    # Basic utilities
    'SimpleLogger',
    'NullLogger',
    'is_pdf_file',
    'validate_output_path',
    'get_safe_filename',
    'generate_output_filename',
    'get_unique_filename',
    'find_pdf_files',
    'estimate_compression_time',
    
    # Advanced features
    'ImageQualityAssessor',
    'AdaptiveCompressionOptimizer',
    'CompressionCache',
    'InMemoryCache',
    'BackupManager',
    'OperationRecovery',
    'CompressionAnalytics',
    
    # Performance optimizations
    'BufferedLogger',
    'OptimizedSimpleLogger',
    'get_logger',
    'get_global_logger',
    'set_global_logger',
    'MemoryManager',
    'SmartCache',
    'memory_optimized',
    'cached_property',
    'global_memory_manager',
    'global_cache',
    'get_memory_info',
    'cleanup_all'
]
