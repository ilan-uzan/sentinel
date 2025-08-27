"""
Functional rule engine for evaluating events and generating alerts.
"""
import json
import os
from typing import List, Dict, Any
from datetime import datetime, timezone


class RuleEngine:
    """
    Evaluates events against rules and generates alerts.
    """
    
    def __init__(self, rules_file: str = "rules/default.json"):
        """
        Initialize the rule engine with rules from JSON file.
        
        Args:
            rules_file: Path to rules configuration file
        """
        self.rules_file = rules_file
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from JSON file."""
        try:
            with open(self.rules_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load rules from {self.rules_file}: {e}")
            return {
                "blocklisted_ips": [],
                "severity_levels": {"low": "info", "medium": "warning", "high": "critical"}
            }
    
    def evaluate_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Evaluate events against rules and return alerts.
        
        Args:
            events: List of events to evaluate
            
        Returns:
            List[Dict[str, Any]]: List of generated alerts
        """
        alerts = []
        
        for event in events:
            event_alerts = self._evaluate_single_event(event)
            alerts.extend(event_alerts)
        
        return alerts
    
    def _evaluate_single_event(self, event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate a single event and return any alerts generated."""
        alerts = []
        event_type = event.get('event_type', '')
        
        if event_type == 'network':
            # Check network events for blocklisted IPs
            network_alerts = self._check_network_security(event)
            alerts.extend(network_alerts)
        
        elif event_type == 'process':
            # Check process events for suspicious activity
            process_alerts = self._check_process_security(event)
            alerts.extend(process_alerts)
        
        return alerts
    
    def _check_network_security(self, event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check network events for security violations."""
        alerts = []
        blocklisted_ips = self.rules.get('blocklisted_ips', [])
        
        # Check remote address against blocklist
        remote_addr = event.get('remote_addr')
        if remote_addr and ':' in remote_addr:
            ip = remote_addr.split(':')[0]
            if ip in blocklisted_ips:
                alerts.append(self._create_network_alert(
                    event, 
                    f"Blocklisted IP detected: {ip}",
                    "high"
                ))
        
        # Check for suspicious connection patterns
        if self._is_suspicious_connection(event):
            alerts.append(self._create_network_alert(
                event,
                "Suspicious network connection pattern detected",
                "medium"
            ))
        
        return alerts
    
    def _check_process_security(self, event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check process events for security violations."""
        alerts = []
        
        # Check for high CPU usage processes
        cpu_percent = event.get('cpu_percent', 0)
        if cpu_percent > 80:
            alerts.append(self._create_process_alert(
                event,
                f"High CPU usage detected: {cpu_percent}%",
                "medium"
            ))
        
        # Check for high memory usage processes
        memory_mb = event.get('memory_mb', 0)
        if memory_mb > 1000:  # 1GB threshold
            alerts.append(self._create_process_alert(
                event,
                f"High memory usage detected: {memory_mb:.1f}MB",
                "medium"
            ))
        
        return alerts
    
    def _is_suspicious_connection(self, event: Dict[str, Any]) -> bool:
        """Determine if a network connection is suspicious."""
        # Check for connections to non-standard ports
        remote_addr = event.get('remote_addr', '')
        if remote_addr and ':' in remote_addr:
            try:
                port = int(remote_addr.split(':')[1])
                # Flag connections to common suspicious ports
                suspicious_ports = [22, 23, 3389, 5900, 8080, 8443]
                if port in suspicious_ports:
                    return True
            except (ValueError, IndexError):
                pass
        
        return False
    
    def _create_network_alert(self, event: Dict[str, Any], title: str, severity: str) -> Dict[str, Any]:
        """Create a network security alert."""
        return {
            'title': title,
            'severity': severity,
            'details': {
                'event_type': 'network_security',
                'event_data': event,
                'rule_triggered': 'network_security_check',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        }
    
    def _create_process_alert(self, event: Dict[str, Any], title: str, severity: str) -> Dict[str, Any]:
        """Create a process security alert."""
        return {
            'title': title,
            'severity': severity,
            'details': {
                'event_type': 'process_security',
                'event_data': event,
                'rule_triggered': 'process_security_check',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        }
    
    def reload_rules(self) -> bool:
        """Reload rules from the configuration file."""
        try:
            self.rules = self._load_rules()
            return True
        except Exception as e:
            print(f"Error reloading rules: {e}")
            return False
    
    def get_rules_summary(self) -> Dict[str, Any]:
        """Get a summary of loaded rules."""
        return {
            'blocklisted_ips_count': len(self.rules.get('blocklisted_ips', [])),
            'severity_levels': self.rules.get('severity_levels', {}),
            'rules_file': self.rules_file,
            'last_loaded': datetime.now(timezone.utc).isoformat()
        } 