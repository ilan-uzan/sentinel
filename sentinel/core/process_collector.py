"""
Real process collector using psutil to gather system process information.
"""
import psutil
from typing import List, Dict, Any
from .base_collector import BaseCollector


class ProcessCollector(BaseCollector):
    """
    Collects real system process information using psutil.
    
    This collector gathers information about running processes including
    PID, name, CPU usage, memory usage, and other relevant metrics.
    """
    
    def collect(self) -> List[Dict[str, Any]]:
        """
        Collect real process data from the system using psutil.
        
        Returns:
            List[Dict[str, Any]]: List of process data dictionaries
        """
        processes = []
        
        try:
            # Get all running processes
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'create_time']):
                try:
                    # Get process info
                    proc_info = proc.info
                    
                    # Calculate memory usage in MB
                    memory_mb = proc_info['memory_info'].rss / (1024 * 1024) if proc_info['memory_info'] else 0
                    
                    # Create normalized process data
                    process_data = {
                        'pid': proc_info['pid'],
                        'name': proc_info['name'] or 'unknown',
                        'cpu_percent': round(proc_info['cpu_percent'] or 0, 2),
                        'memory_mb': round(memory_mb, 2),
                        'status': proc_info['status'] or 'unknown',
                        'create_time': proc_info['create_time']
                    }
                    
                    processes.append(process_data)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Skip processes we can't access
                    continue
                    
        except Exception as e:
            print(f"Error collecting process data: {e}")
            return []
        
        return processes 