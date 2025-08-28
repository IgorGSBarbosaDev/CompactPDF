"""
Caching system for PDF compression to improve performance.
Implements intelligent caching of compression results and intermediate data.
"""

import os
import json
import hashlib
import pickle
import tempfile
import time
from typing import Any, Dict, Optional, Union
from pathlib import Path
from io import BytesIO


class CompressionCache:
    """
    Intelligent caching system for PDF compression operations.
    Stores compression results and intermediate data to improve performance.
    """
    
    def __init__(self, cache_dir: Optional[str] = None, max_cache_size_mb: int = 100):
        """
        Initialize compression cache.
        
        Args:
            cache_dir: Directory for cache files (uses temp dir if None)
            max_cache_size_mb: Maximum cache size in MB
        """
        if cache_dir is None:
            cache_dir = os.path.join(tempfile.gettempdir(), 'compactpdf_cache')
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_cache_size = max_cache_size_mb * 1024 * 1024  # Convert to bytes
        self.index_file = self.cache_dir / 'cache_index.json'
        self.index = self._load_index()
    
    def _load_index(self) -> Dict[str, Any]:
        """Load cache index from file."""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return {
            'entries': {},
            'last_cleanup': time.time(),
            'total_size': 0
        }
    
    def _save_index(self) -> None:
        """Save cache index to file."""
        try:
            with open(self.index_file, 'w') as f:
                json.dump(self.index, f, indent=2)
        except Exception:
            pass
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate hash of file for cache key."""
        try:
            hasher = hashlib.md5()
            
            # Include file path, size, and modification time
            hasher.update(file_path.encode())
            
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                hasher.update(str(stat.st_size).encode())
                hasher.update(str(stat.st_mtime).encode())
            
            return hasher.hexdigest()
        except Exception:
            return hashlib.md5(file_path.encode()).hexdigest()
    
    def _calculate_config_hash(self, config: Dict[str, Any]) -> str:
        """Calculate hash of configuration for cache key."""
        try:
            # Convert config to JSON string and hash it
            config_str = json.dumps(config, sort_keys=True)
            return hashlib.md5(config_str.encode()).hexdigest()
        except Exception:
            return hashlib.md5(str(config).encode()).hexdigest()
    
    def _generate_cache_key(self, file_path: str, config: Dict[str, Any], strategy: str) -> str:
        """Generate unique cache key for compression operation."""
        file_hash = self._calculate_file_hash(file_path)
        config_hash = self._calculate_config_hash(config)
        strategy_hash = hashlib.md5(strategy.encode()).hexdigest()
        
        return f"{file_hash}_{config_hash}_{strategy_hash}"
    
    def _cleanup_cache(self) -> None:
        """Clean up cache if it exceeds size limit."""
        try:
            # Check if cleanup is needed
            current_time = time.time()
            last_cleanup = self.index.get('last_cleanup', 0)
            
            # Only cleanup every hour or if cache is too large
            if (current_time - last_cleanup < 3600 and 
                self.index.get('total_size', 0) < self.max_cache_size):
                return
            
            # Calculate actual cache size
            total_size = 0
            entries_to_remove = []
            
            for cache_key, entry in self.index['entries'].items():
                cache_file = self.cache_dir / f"{cache_key}.pkl"
                
                if cache_file.exists():
                    total_size += cache_file.stat().st_size
                    entry['file_size'] = cache_file.stat().st_size
                    entry['access_time'] = entry.get('access_time', current_time)
                else:
                    # File doesn't exist, mark for removal
                    entries_to_remove.append(cache_key)
            
            # Remove non-existent entries
            for key in entries_to_remove:
                del self.index['entries'][key]
            
            # If still over limit, remove oldest entries
            if total_size > self.max_cache_size:
                # Sort by access time (oldest first)
                sorted_entries = sorted(
                    self.index['entries'].items(),
                    key=lambda x: x[1].get('access_time', 0)
                )
                
                for cache_key, entry in sorted_entries:
                    cache_file = self.cache_dir / f"{cache_key}.pkl"
                    
                    if cache_file.exists():
                        file_size = entry.get('file_size', 0)
                        cache_file.unlink()
                        total_size -= file_size
                        
                        del self.index['entries'][cache_key]
                        
                        if total_size <= self.max_cache_size * 0.8:  # Leave some buffer
                            break
            
            self.index['total_size'] = total_size
            self.index['last_cleanup'] = current_time
            self._save_index()
            
        except Exception:
            pass  # Fail silently on cleanup errors
    
    def get(self, file_path: str, config: Dict[str, Any], strategy: str) -> Optional[BytesIO]:
        """
        Get cached compression result.
        
        Args:
            file_path: Path to original PDF file
            config: Compression configuration
            strategy: Compression strategy name
            
        Returns:
            Cached compressed PDF data or None if not found
        """
        try:
            cache_key = self._generate_cache_key(file_path, config, strategy)
            
            if cache_key not in self.index['entries']:
                return None
            
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            
            if not cache_file.exists():
                # Remove stale index entry
                del self.index['entries'][cache_key]
                self._save_index()
                return None
            
            # Load cached data
            with open(cache_file, 'rb') as f:
                cached_data = pickle.load(f)
            
            # Update access time
            self.index['entries'][cache_key]['access_time'] = time.time()
            self.index['entries'][cache_key]['hit_count'] = (
                self.index['entries'][cache_key].get('hit_count', 0) + 1
            )
            
            # Return as BytesIO
            result = BytesIO(cached_data['compressed_data'])
            return result
            
        except Exception:
            return None
    
    def put(
        self,
        file_path: str,
        config: Dict[str, Any],
        strategy: str,
        compressed_data: BytesIO,
        compression_ratio: float
    ) -> bool:
        """
        Store compression result in cache.
        
        Args:
            file_path: Path to original PDF file
            config: Compression configuration
            strategy: Compression strategy name
            compressed_data: Compressed PDF data
            compression_ratio: Achieved compression ratio
            
        Returns:
            True if stored successfully, False otherwise
        """
        try:
            cache_key = self._generate_cache_key(file_path, config, strategy)
            
            # Prepare data to cache
            compressed_data.seek(0)
            data_to_cache = {
                'compressed_data': compressed_data.read(),
                'compression_ratio': compression_ratio,
                'original_file': file_path,
                'config': config,
                'strategy': strategy,
                'created_time': time.time()
            }
            
            # Save to cache file
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            with open(cache_file, 'wb') as f:
                pickle.dump(data_to_cache, f)
            
            # Update index
            file_size = cache_file.stat().st_size
            self.index['entries'][cache_key] = {
                'created_time': time.time(),
                'access_time': time.time(),
                'file_size': file_size,
                'compression_ratio': compression_ratio,
                'hit_count': 0
            }
            
            self.index['total_size'] = self.index.get('total_size', 0) + file_size
            self._save_index()
            
            # Cleanup if needed
            self._cleanup_cache()
            
            return True
            
        except Exception:
            return False
    
    def invalidate(self, file_path: str) -> None:
        """
        Invalidate all cache entries for a specific file.
        
        Args:
            file_path: Path to file whose cache entries should be invalidated
        """
        try:
            file_hash = self._calculate_file_hash(file_path)
            keys_to_remove = []
            
            for cache_key in self.index['entries']:
                if cache_key.startswith(file_hash):
                    keys_to_remove.append(cache_key)
            
            for key in keys_to_remove:
                cache_file = self.cache_dir / f"{key}.pkl"
                if cache_file.exists():
                    cache_file.unlink()
                
                if key in self.index['entries']:
                    del self.index['entries'][key]
            
            if keys_to_remove:
                self._save_index()
                
        except Exception:
            pass
    
    def clear(self) -> None:
        """Clear all cache entries."""
        try:
            # Remove all cache files
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()
            
            # Reset index
            self.index = {
                'entries': {},
                'last_cleanup': time.time(),
                'total_size': 0
            }
            self._save_index()
            
        except Exception:
            pass
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get cache usage statistics."""
        try:
            total_entries = len(self.index['entries'])
            total_size = sum(
                entry.get('file_size', 0) 
                for entry in self.index['entries'].values()
            )
            total_hits = sum(
                entry.get('hit_count', 0) 
                for entry in self.index['entries'].values()
            )
            
            avg_compression_ratio = 0
            if total_entries > 0:
                avg_compression_ratio = sum(
                    entry.get('compression_ratio', 0) 
                    for entry in self.index['entries'].values()
                ) / total_entries
            
            return {
                'total_entries': total_entries,
                'total_size_mb': total_size / (1024 * 1024),
                'max_size_mb': self.max_cache_size / (1024 * 1024),
                'usage_percentage': (total_size / self.max_cache_size * 100) if self.max_cache_size > 0 else 0,
                'total_hits': total_hits,
                'average_compression_ratio': avg_compression_ratio,
                'cache_hit_rate': self._calculate_hit_rate()
            }
            
        except Exception:
            return {
                'total_entries': 0,
                'total_size_mb': 0,
                'error': 'Failed to calculate statistics'
            }
    
    def _calculate_hit_rate(self) -> float:
        """Calculate cache hit rate (approximation)."""
        try:
            total_hits = sum(
                entry.get('hit_count', 0) 
                for entry in self.index['entries'].values()
            )
            total_entries = len(self.index['entries'])
            
            # Rough estimation: assume each entry was created once and hit n times
            total_requests = total_entries + total_hits
            
            if total_requests > 0:
                return (total_hits / total_requests) * 100
            
            return 0.0
            
        except Exception:
            return 0.0


class InMemoryCache:
    """
    Simple in-memory cache for frequently accessed data.
    Useful for caching small objects during processing.
    """
    
    def __init__(self, max_entries: int = 50):
        """
        Initialize in-memory cache.
        
        Args:
            max_entries: Maximum number of entries to keep in memory
        """
        self.max_entries = max_entries
        self.cache = {}
        self.access_order = []
    
    def get(self, key: str) -> Any:
        """Get item from cache."""
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, value: Any) -> None:
        """Put item in cache."""
        if key in self.cache:
            # Update existing
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_entries:
            # Remove least recently used
            lru_key = self.access_order.pop(0)
            del self.cache[lru_key]
        
        self.cache[key] = value
        self.access_order.append(key)
    
    def clear(self) -> None:
        """Clear all cached items."""
        self.cache.clear()
        self.access_order.clear()
    
    def size(self) -> int:
        """Get number of cached items."""
        return len(self.cache)
