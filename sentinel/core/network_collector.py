"""
Real network collector using psutil to gather network connection information.
"""
import psutil
from typing import List, Dict, Any
from .base_collector import BaseCollector


class NetworkCollector(BaseCollector):
    """
    Collects real network connection information using psutil.
    
    This collector gathers information about active network connections
    including local/remote addresses, ports, status, and process info.
    """
    
    def collect(self) -> List[Dict[str, Any]]:
        """
        Collect real network connection data from the system using psutil.
        
        Returns:
            List[Dict[str, Any]]: List of network connection data dictionaries
        """
        connections = []
        
        try:
            # Try to get network connections, but handle permission issues gracefully
            net_connections = psutil.net_connections(kind='inet')
            
            for conn in net_connections:
                try:
                    # Extract connection details with safe access
                    local_addr = None
                    remote_addr = None
                    
                    if hasattr(conn, 'laddr') and conn.laddr:
                        local_addr = f"{conn.laddr.ip}:{conn.laddr.port}"
                    if hasattr(conn, 'raddr') and conn.raddr:
                        remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}"
                    
                    # Create normalized connection data
                    connection_data = {
                        'family': str(getattr(conn, 'family', 'unknown')),
                        'type': str(getattr(conn, 'type', 'unknown')),
                        'local_addr': local_addr,
                        'remote_addr': remote_addr,
                        'status': str(getattr(conn, 'status', 'unknown')),
                        'pid': getattr(conn, 'pid', None),
                        'fd': getattr(conn, 'fd', None)
                    }
                    
                    # Only add connections with valid addresses
                    if local_addr or remote_addr:
                        connections.append(connection_data)
                        
                except (AttributeError, TypeError, Exception):
                    # Skip problematic connections
                    continue
                    
        except (psutil.AccessDenied, psutil.ZombieProcess, Exception) as e:
            # On macOS, network connections might require elevated permissions
            # Return empty list instead of failing
            print(f"Network collection limited due to permissions: {e}")
            return []
        
        return connections 