"""
Advanced reporting and analytics system for PDF compression operations.
Provides detailed insights, performance metrics, and optimization recommendations.
"""

import json
import time
import statistics
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path

from ..services import CompressionResult


@dataclass
class CompressionSession:
    """Represents a compression session with multiple operations."""
    session_id: str
    start_time: float
    end_time: Optional[float]
    operations: List[CompressionResult]
    session_metadata: Dict[str, Any]


class CompressionAnalytics:
    """
    Advanced analytics engine for PDF compression operations.
    Tracks performance, identifies patterns, and provides optimization insights.
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize analytics engine.
        
        Args:
            data_dir: Directory for analytics data storage
        """
        if data_dir is None:
            import tempfile
            data_dir = str(Path(tempfile.gettempdir()) / "compactpdf_analytics")
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.sessions_file = self.data_dir / "compression_sessions.json"
        self.metrics_file = self.data_dir / "performance_metrics.json"
        
        self.sessions = self._load_sessions()
        self.current_session = None
    
    def _load_sessions(self) -> List[CompressionSession]:
        """Load compression sessions from storage."""
        try:
            if self.sessions_file.exists():
                with open(self.sessions_file, 'r') as f:
                    data = json.load(f)
                
                sessions = []
                for session_data in data:
                    operations = [
                        CompressionResult(**op) for op in session_data['operations']
                    ]
                    session = CompressionSession(
                        session_id=session_data['session_id'],
                        start_time=session_data['start_time'],
                        end_time=session_data.get('end_time'),
                        operations=operations,
                        session_metadata=session_data.get('session_metadata', {})
                    )
                    sessions.append(session)
                
                return sessions
        except Exception:
            pass
        
        return []
    
    def _save_sessions(self) -> None:
        """Save compression sessions to storage."""
        try:
            data = []
            for session in self.sessions:
                session_data = {
                    'session_id': session.session_id,
                    'start_time': session.start_time,
                    'end_time': session.end_time,
                    'operations': [asdict(op) for op in session.operations],
                    'session_metadata': session.session_metadata
                }
                data.append(session_data)
            
            with open(self.sessions_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    def start_session(self, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Start a new compression session.
        
        Args:
            metadata: Optional session metadata
            
        Returns:
            Session ID
        """
        session_id = f"session_{int(time.time())}_{len(self.sessions)}"
        
        self.current_session = CompressionSession(
            session_id=session_id,
            start_time=time.time(),
            end_time=None,
            operations=[],
            session_metadata=metadata or {}
        )
        
        return session_id
    
    def end_session(self) -> None:
        """End the current compression session."""
        if self.current_session:
            self.current_session.end_time = time.time()
            self.sessions.append(self.current_session)
            self._save_sessions()
            self.current_session = None
    
    def record_operation(self, result: CompressionResult) -> None:
        """
        Record a compression operation result.
        
        Args:
            result: Compression result to record
        """
        if self.current_session:
            self.current_session.operations.append(result)
    
    def generate_performance_report(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate comprehensive performance report.
        
        Args:
            days: Number of days to include in report
            
        Returns:
            Performance report dictionary
        """
        try:
            cutoff_time = time.time() - (days * 24 * 3600)
            recent_sessions = [
                s for s in self.sessions 
                if s.start_time >= cutoff_time
            ]
            
            if not recent_sessions:
                return {'error': 'No data available for specified period'}
            
            # Collect all operations
            all_operations = []
            for session in recent_sessions:
                all_operations.extend(session.operations)
            
            successful_ops = [op for op in all_operations if op.success]
            failed_ops = [op for op in all_operations if not op.success]
            
            # Calculate metrics
            report = {
                'period_days': days,
                'total_sessions': len(recent_sessions),
                'total_operations': len(all_operations),
                'successful_operations': len(successful_ops),
                'failed_operations': len(failed_ops),
                'success_rate': (len(successful_ops) / len(all_operations) * 100) if all_operations else 0,
                
                'compression_metrics': self._calculate_compression_metrics(successful_ops),
                'performance_metrics': self._calculate_performance_metrics(successful_ops),
                'strategy_analysis': self._analyze_strategies(successful_ops),
                'file_size_analysis': self._analyze_file_sizes(successful_ops),
                'recommendations': self._generate_recommendations(recent_sessions)
            }
            
            return report
            
        except Exception as e:
            return {'error': f'Failed to generate report: {str(e)}'}
    
    def _calculate_compression_metrics(self, operations: List[CompressionResult]) -> Dict[str, Any]:
        """Calculate compression-related metrics."""
        if not operations:
            return {}
        
        ratios = [op.compression_ratio for op in operations]
        original_sizes = [op.original_size for op in operations]
        compressed_sizes = [op.compressed_size for op in operations]
        
        total_original = sum(original_sizes)
        total_compressed = sum(compressed_sizes)
        overall_ratio = 1 - (total_compressed / total_original) if total_original > 0 else 0
        
        return {
            'average_compression_ratio': statistics.mean(ratios),
            'median_compression_ratio': statistics.median(ratios),
            'best_compression_ratio': max(ratios),
            'worst_compression_ratio': min(ratios),
            'overall_compression_ratio': overall_ratio,
            'total_space_saved_mb': (total_original - total_compressed) / (1024 * 1024),
            'compression_ratio_std_dev': statistics.stdev(ratios) if len(ratios) > 1 else 0
        }
    
    def _calculate_performance_metrics(self, operations: List[CompressionResult]) -> Dict[str, Any]:
        """Calculate performance-related metrics."""
        if not operations:
            return {}
        
        times = [op.time_taken for op in operations]
        sizes = [op.original_size for op in operations]
        
        # Calculate throughput (MB/s)
        throughputs = []
        for op in operations:
            if op.time_taken > 0:
                mb_size = op.original_size / (1024 * 1024)
                throughput = mb_size / op.time_taken
                throughputs.append(throughput)
        
        return {
            'average_processing_time': statistics.mean(times),
            'median_processing_time': statistics.median(times),
            'fastest_operation': min(times),
            'slowest_operation': max(times),
            'average_throughput_mb_per_sec': statistics.mean(throughputs) if throughputs else 0,
            'processing_time_std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }
    
    def _analyze_strategies(self, operations: List[CompressionResult]) -> Dict[str, Any]:
        """Analyze strategy effectiveness."""
        strategy_stats = {}
        
        for op in operations:
            strategy = op.strategy_used
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {
                    'count': 0,
                    'ratios': [],
                    'times': [],
                    'success_count': 0
                }
            
            stats = strategy_stats[strategy]
            stats['count'] += 1
            stats['ratios'].append(op.compression_ratio)
            stats['times'].append(op.time_taken)
            
            if op.success:
                stats['success_count'] += 1
        
        # Calculate summary for each strategy
        strategy_analysis = {}
        for strategy, stats in strategy_stats.items():
            strategy_analysis[strategy] = {
                'total_uses': stats['count'],
                'success_rate': (stats['success_count'] / stats['count'] * 100) if stats['count'] > 0 else 0,
                'average_compression_ratio': statistics.mean(stats['ratios']) if stats['ratios'] else 0,
                'average_processing_time': statistics.mean(stats['times']) if stats['times'] else 0,
                'effectiveness_score': self._calculate_strategy_effectiveness(stats)
            }
        
        return strategy_analysis
    
    def _calculate_strategy_effectiveness(self, stats: Dict[str, Any]) -> float:
        """Calculate overall effectiveness score for a strategy."""
        if not stats['ratios'] or not stats['times']:
            return 0.0
        
        avg_ratio = statistics.mean(stats['ratios'])
        avg_time = statistics.mean(stats['times'])
        success_rate = stats['success_count'] / stats['count'] if stats['count'] > 0 else 0
        
        # Weighted score: compression (40%), speed (30%), reliability (30%)
        # Normalize time to 0-1 scale (assuming 60s is very slow)
        time_score = max(0, 1 - (avg_time / 60))
        
        effectiveness = (0.4 * avg_ratio) + (0.3 * time_score) + (0.3 * success_rate)
        return min(1.0, max(0.0, effectiveness))
    
    def _analyze_file_sizes(self, operations: List[CompressionResult]) -> Dict[str, Any]:
        """Analyze compression effectiveness by file size ranges."""
        size_ranges = {
            'small': (0, 1 * 1024 * 1024),      # < 1MB
            'medium': (1 * 1024 * 1024, 10 * 1024 * 1024),   # 1-10MB
            'large': (10 * 1024 * 1024, 100 * 1024 * 1024),  # 10-100MB
            'very_large': (100 * 1024 * 1024, float('inf'))   # > 100MB
        }
        
        range_stats = {}
        
        for range_name, (min_size, max_size) in size_ranges.items():
            range_ops = [
                op for op in operations 
                if min_size <= op.original_size < max_size
            ]
            
            if range_ops:
                ratios = [op.compression_ratio for op in range_ops]
                times = [op.time_taken for op in range_ops]
                
                range_stats[range_name] = {
                    'file_count': len(range_ops),
                    'average_compression_ratio': statistics.mean(ratios),
                    'average_processing_time': statistics.mean(times),
                    'size_range_mb': f"{min_size/(1024*1024):.1f} - {max_size/(1024*1024):.1f}" if max_size != float('inf') else f"> {min_size/(1024*1024):.1f}"
                }
        
        return range_stats
    
    def _generate_recommendations(self, sessions: List[CompressionSession]) -> List[str]:
        """Generate optimization recommendations based on analysis."""
        recommendations = []
        
        try:
            all_operations = []
            for session in sessions:
                all_operations.extend(session.operations)
            
            successful_ops = [op for op in all_operations if op.success]
            
            if not successful_ops:
                return ["Insufficient data for recommendations"]
            
            # Analyze compression ratios
            ratios = [op.compression_ratio for op in successful_ops]
            avg_ratio = statistics.mean(ratios)
            
            if avg_ratio < 0.3:
                recommendations.append("Consider using more aggressive compression settings to achieve better ratios")
            elif avg_ratio > 0.7:
                recommendations.append("Excellent compression achieved - current settings are optimal")
            
            # Analyze processing times
            times = [op.time_taken for op in successful_ops]
            avg_time = statistics.mean(times)
            
            if avg_time > 30:
                recommendations.append("Processing times are high - consider optimizing for speed over compression ratio")
            
            # Analyze strategy effectiveness
            strategy_stats = {}
            for op in successful_ops:
                strategy = op.strategy_used
                if strategy not in strategy_stats:
                    strategy_stats[strategy] = []
                strategy_stats[strategy].append(op.compression_ratio)
            
            best_strategy = max(
                strategy_stats.items(),
                key=lambda x: statistics.mean(x[1])
            )[0] if strategy_stats else None
            
            if best_strategy:
                recommendations.append(f"Strategy '{best_strategy}' shows best results - consider prioritizing it")
            
            # Check for failed operations
            failed_ops = [op for op in all_operations if not op.success]
            failure_rate = len(failed_ops) / len(all_operations) if all_operations else 0
            
            if failure_rate > 0.1:  # > 10% failure rate
                recommendations.append("High failure rate detected - review input file quality and compression settings")
            
        except Exception:
            recommendations.append("Unable to generate recommendations due to data analysis error")
        
        return recommendations
    
    def export_data(self, format: str = 'json') -> str:
        """
        Export analytics data in specified format.
        
        Args:
            format: Export format ('json', 'csv')
            
        Returns:
            Exported data as string
        """
        try:
            if format.lower() == 'json':
                return self._export_json()
            elif format.lower() == 'csv':
                return self._export_csv()
            else:
                raise ValueError(f"Unsupported export format: {format}")
        except Exception as e:
            return f"Export failed: {str(e)}"
    
    def _export_json(self) -> str:
        """Export data as JSON."""
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'total_sessions': len(self.sessions),
            'sessions': []
        }
        
        for session in self.sessions:
            session_data = {
                'session_id': session.session_id,
                'start_time': datetime.fromtimestamp(session.start_time).isoformat(),
                'end_time': datetime.fromtimestamp(session.end_time).isoformat() if session.end_time else None,
                'duration_seconds': (session.end_time - session.start_time) if session.end_time else None,
                'operations_count': len(session.operations),
                'metadata': session.session_metadata,
                'operations': [asdict(op) for op in session.operations]
            }
            export_data['sessions'].append(session_data)
        
        return json.dumps(export_data, indent=2)
    
    def _export_csv(self) -> str:
        """Export data as CSV."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        header = [
            'session_id', 'operation_timestamp', 'original_size', 'compressed_size',
            'compression_ratio', 'time_taken', 'strategy_used', 'success', 'error_message'
        ]
        writer.writerow(header)
        
        # Write data
        for session in self.sessions:
            for op in session.operations:
                row = [
                    session.session_id,
                    datetime.fromtimestamp(session.start_time).isoformat(),
                    op.original_size,
                    op.compressed_size,
                    op.compression_ratio,
                    op.time_taken,
                    op.strategy_used,
                    op.success,
                    op.error_message or ''
                ]
                writer.writerow(row)
        
        return output.getvalue()
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics across all sessions."""
        try:
            all_operations = []
            for session in self.sessions:
                all_operations.extend(session.operations)
            
            successful_ops = [op for op in all_operations if op.success]
            
            if not all_operations:
                return {'message': 'No operations recorded yet'}
            
            total_original_size = sum(op.original_size for op in successful_ops)
            total_compressed_size = sum(op.compressed_size for op in successful_ops)
            
            return {
                'total_sessions': len(self.sessions),
                'total_operations': len(all_operations),
                'successful_operations': len(successful_ops),
                'overall_success_rate': len(successful_ops) / len(all_operations) * 100,
                'total_files_processed_mb': total_original_size / (1024 * 1024),
                'total_space_saved_mb': (total_original_size - total_compressed_size) / (1024 * 1024),
                'average_compression_ratio': statistics.mean([op.compression_ratio for op in successful_ops]) if successful_ops else 0,
                'average_processing_time': statistics.mean([op.time_taken for op in successful_ops]) if successful_ops else 0,
                'data_collection_period': {
                    'start': datetime.fromtimestamp(min(s.start_time for s in self.sessions)).isoformat() if self.sessions else None,
                    'end': datetime.fromtimestamp(max(s.end_time or s.start_time for s in self.sessions)).isoformat() if self.sessions else None
                }
            }
        except Exception as e:
            return {'error': f'Failed to calculate statistics: {str(e)}'}
