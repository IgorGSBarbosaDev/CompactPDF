"""
Backup and recovery system for PDF compression operations.
Ensures data safety and provides rollback capabilities.
"""

import os
import shutil
import json
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class BackupEntry:
    """Represents a backup entry."""
    backup_id: str
    original_file: str
    backup_file: str
    operation: str
    timestamp: float
    metadata: Dict[str, Any]


class BackupManager:
    """
    Manages backup and recovery operations for PDF compression.
    Provides automatic backup, recovery, and cleanup functionality.
    """
    
    def __init__(self, backup_dir: Optional[str] = None, max_backups: int = 10):
        """
        Initialize backup manager.
        
        Args:
            backup_dir: Directory for backup files (auto-created if None)
            max_backups: Maximum number of backups to keep per file
        """
        if backup_dir is None:
            backup_dir = os.path.join(os.path.expanduser("~"), ".compactpdf", "backups")
        
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_backups = max_backups
        self.registry_file = self.backup_dir / "backup_registry.json"
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load backup registry from file."""
        try:
            if self.registry_file.exists():
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return {}
    
    def _save_registry(self) -> None:
        """Save backup registry to file."""
        try:
            with open(self.registry_file, 'w') as f:
                json.dump(self.registry, f, indent=2)
        except Exception:
            pass
    
    def _generate_backup_id(self) -> str:
        """Generate unique backup ID."""
        timestamp = str(int(time.time()))
        return f"backup_{timestamp}_{os.getpid()}"
    
    def _get_backup_filename(self, original_file: str, backup_id: str) -> str:
        """Generate backup filename."""
        original_name = Path(original_file).stem
        return f"{original_name}_{backup_id}.pdf"
    
    def create_backup(
        self,
        file_path: str,
        operation: str = "compression",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Create backup of a file before operation.
        
        Args:
            file_path: Path to file to backup
            operation: Description of operation being performed
            metadata: Additional metadata to store
            
        Returns:
            Backup ID if successful, None otherwise
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            # Generate backup info
            backup_id = self._generate_backup_id()
            backup_filename = self._get_backup_filename(file_path, backup_id)
            backup_path = self.backup_dir / backup_filename
            
            # Copy file to backup location
            shutil.copy2(file_path, backup_path)
            
            # Create backup entry
            backup_entry = BackupEntry(
                backup_id=backup_id,
                original_file=os.path.abspath(file_path),
                backup_file=str(backup_path),
                operation=operation,
                timestamp=time.time(),
                metadata=metadata or {}
            )
            
            # Add to registry
            file_key = os.path.abspath(file_path)
            if file_key not in self.registry:
                self.registry[file_key] = []
            
            self.registry[file_key].append(asdict(backup_entry))
            
            # Cleanup old backups
            self._cleanup_old_backups(file_key)
            
            # Save registry
            self._save_registry()
            
            return backup_id
            
        except Exception:
            return None
    
    def restore_backup(self, backup_id: str, target_path: Optional[str] = None) -> bool:
        """
        Restore a file from backup.
        
        Args:
            backup_id: ID of backup to restore
            target_path: Target path for restored file (original path if None)
            
        Returns:
            True if restoration successful, False otherwise
        """
        try:
            # Find backup entry
            backup_entry = None
            original_file = None
            
            for file_path, backups in self.registry.items():
                for backup in backups:
                    if backup['backup_id'] == backup_id:
                        backup_entry = backup
                        original_file = file_path
                        break
                if backup_entry:
                    break
            
            if not backup_entry:
                return False
            
            backup_file = backup_entry['backup_file']
            if not os.path.exists(backup_file):
                return False
            
            # Determine target path
            if target_path is None:
                target_path = original_file
            
            # Ensure target path is not None
            if target_path is None:
                return False
            
            # Restore file
            shutil.copy2(backup_file, target_path)
            
            return True
            
        except Exception:
            return False
    
    def list_backups(self, file_path: Optional[str] = None) -> List[BackupEntry]:
        """
        List available backups.
        
        Args:
            file_path: Path to specific file (all files if None)
            
        Returns:
            List of backup entries
        """
        backups = []
        
        try:
            if file_path:
                file_key = os.path.abspath(file_path)
                if file_key in self.registry:
                    for backup_data in self.registry[file_key]:
                        backups.append(BackupEntry(**backup_data))
            else:
                for file_backups in self.registry.values():
                    for backup_data in file_backups:
                        backups.append(BackupEntry(**backup_data))
            
            # Sort by timestamp (newest first)
            backups.sort(key=lambda x: x.timestamp, reverse=True)
            
        except Exception:
            pass
        
        return backups
    
    def delete_backup(self, backup_id: str) -> bool:
        """
        Delete a specific backup.
        
        Args:
            backup_id: ID of backup to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            # Find and remove backup entry
            for file_path, backups in self.registry.items():
                for i, backup in enumerate(backups):
                    if backup['backup_id'] == backup_id:
                        # Delete backup file
                        backup_file = backup['backup_file']
                        if os.path.exists(backup_file):
                            os.unlink(backup_file)
                        
                        # Remove from registry
                        backups.pop(i)
                        self._save_registry()
                        
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _cleanup_old_backups(self, file_key: str) -> None:
        """Clean up old backups for a specific file."""
        try:
            if file_key not in self.registry:
                return
            
            backups = self.registry[file_key]
            
            # Sort by timestamp (newest first)
            backups.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Remove excess backups
            while len(backups) > self.max_backups:
                old_backup = backups.pop()
                backup_file = old_backup['backup_file']
                
                if os.path.exists(backup_file):
                    os.unlink(backup_file)
            
            self.registry[file_key] = backups
            
        except Exception:
            pass
    
    def cleanup_orphaned_backups(self) -> int:
        """
        Clean up orphaned backup files (files without registry entries).
        
        Returns:
            Number of orphaned files cleaned up
        """
        try:
            # Get all backup files referenced in registry
            referenced_files = set()
            for backups in self.registry.values():
                for backup in backups:
                    referenced_files.add(backup['backup_file'])
            
            # Find orphaned files
            orphaned_count = 0
            for backup_file in self.backup_dir.glob("*.pdf"):
                if str(backup_file) not in referenced_files:
                    backup_file.unlink()
                    orphaned_count += 1
            
            return orphaned_count
            
        except Exception:
            return 0
    
    def get_backup_statistics(self) -> Dict[str, Any]:
        """Get backup system statistics."""
        try:
            total_backups = sum(len(backups) for backups in self.registry.values())
            total_files = len(self.registry)
            
            # Calculate total backup size
            total_size = 0
            for backup_file in self.backup_dir.glob("*.pdf"):
                try:
                    total_size += backup_file.stat().st_size
                except Exception:
                    pass
            
            # Find oldest and newest backups
            all_timestamps = []
            for backups in self.registry.values():
                for backup in backups:
                    all_timestamps.append(backup['timestamp'])
            
            oldest_backup = None
            newest_backup = None
            if all_timestamps:
                oldest_backup = datetime.fromtimestamp(min(all_timestamps)).isoformat()
                newest_backup = datetime.fromtimestamp(max(all_timestamps)).isoformat()
            
            return {
                'total_backups': total_backups,
                'total_files_backed_up': total_files,
                'total_size_mb': total_size / (1024 * 1024),
                'backup_directory': str(self.backup_dir),
                'max_backups_per_file': self.max_backups,
                'oldest_backup': oldest_backup,
                'newest_backup': newest_backup
            }
            
        except Exception:
            return {
                'error': 'Failed to calculate backup statistics'
            }


class OperationRecovery:
    """
    Handles recovery from failed compression operations.
    Provides transaction-like behavior for file operations.
    """
    
    def __init__(self, backup_manager: BackupManager):
        """
        Initialize operation recovery.
        
        Args:
            backup_manager: Backup manager instance
        """
        self.backup_manager = backup_manager
        self.active_operations = {}
    
    def begin_operation(
        self,
        file_path: str,
        operation_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Begin a recoverable operation.
        
        Args:
            file_path: Path to file being operated on
            operation_type: Type of operation
            metadata: Additional operation metadata
            
        Returns:
            Operation ID if successful, None otherwise
        """
        try:
            # Create backup
            backup_id = self.backup_manager.create_backup(
                file_path,
                operation_type,
                metadata
            )
            
            if backup_id:
                operation_id = f"op_{backup_id}"
                self.active_operations[operation_id] = {
                    'backup_id': backup_id,
                    'file_path': file_path,
                    'operation_type': operation_type,
                    'start_time': time.time(),
                    'metadata': metadata or {}
                }
                
                return operation_id
            
            return None
            
        except Exception:
            return None
    
    def commit_operation(self, operation_id: str) -> bool:
        """
        Commit a successful operation (remove from active operations).
        
        Args:
            operation_id: ID of operation to commit
            
        Returns:
            True if committed successfully, False otherwise
        """
        try:
            if operation_id in self.active_operations:
                del self.active_operations[operation_id]
                return True
            
            return False
            
        except Exception:
            return False
    
    def rollback_operation(self, operation_id: str) -> bool:
        """
        Rollback a failed operation (restore from backup).
        
        Args:
            operation_id: ID of operation to rollback
            
        Returns:
            True if rollback successful, False otherwise
        """
        try:
            if operation_id not in self.active_operations:
                return False
            
            operation = self.active_operations[operation_id]
            backup_id = operation['backup_id']
            file_path = operation['file_path']
            
            # Restore from backup
            success = self.backup_manager.restore_backup(backup_id, file_path)
            
            if success:
                del self.active_operations[operation_id]
            
            return success
            
        except Exception:
            return False
    
    def get_active_operations(self) -> List[Dict[str, Any]]:
        """Get list of currently active operations."""
        return list(self.active_operations.values())
