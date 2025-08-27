"""
Real collector service to orchestrate data collection from multiple collectors.
"""
from typing import List, Dict, Any
from ..core.base_collector import BaseCollector
from .rule_engine import RuleEngine


class CollectorService:
    """
    Orchestrates real data collection from multiple collectors.

    This service manages a list of collectors and coordinates
    the collection of system data from all sources.
    """
    
    def __init__(self, collectors: List[BaseCollector], rules_file: str = "rules/default.json"):
        """
        Initialize the collector service.
        
        Args:
            collectors: List of collector instances to use
            rules_file: Path to rules configuration file
        """
        self.collectors = collectors
        self.rule_engine = RuleEngine(rules_file)
    
    def collect_all(self) -> List[Dict[str, Any]]:
        """
        Run all collectors and return merged events with event_type field.

        Returns:
            List[Dict[str, Any]]: Combined events from all collectors
        """
        all_events = []

        try:
            for collector in self.collectors:
                # Get collector name for event type
                collector_name = collector.__class__.__name__.lower().replace('collector', '')

                # Collect data from this collector
                events = collector.collect()

                # Add event_type field to each event
                for event in events:
                    event['event_type'] = collector_name
                    all_events.append(event)

        except Exception as e:
            print(f"Error in collector service: {e}")
            return []

        return all_events
    
    def collect_and_alert(self) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Collect data and generate alerts based on rules.
        
        Returns:
            tuple: (events, alerts) - collected events and generated alerts
        """
        # Collect all events
        events = self.collect_all()
        
        # Evaluate events against rules to generate alerts
        alerts = self.rule_engine.evaluate_events(events)
        
        return events, alerts
    
    def get_collector_status(self) -> Dict[str, Any]:
        """
        Get status of all collectors.

        Returns:
            Dict[str, Any]: Status information for each collector
        """
        status = {}

        for collector in self.collectors:
            collector_name = collector.__class__.__name__
            try:
                # Test collection to check if collector is working
                sample_data = collector.collect()
                status[collector_name] = {
                    'status': 'active',
                    'sample_count': len(sample_data),
                    'working': True
                }
            except Exception as e:
                status[collector_name] = {
                    'status': 'error',
                    'error': str(e),
                    'working': False
                }

        return status
    
    def get_rule_engine_status(self) -> Dict[str, Any]:
        """
        Get status of the rule engine.
        
        Returns:
            Dict[str, Any]: Rule engine status and configuration
        """
        return self.rule_engine.get_rules_summary()
    
    def reload_rules(self) -> bool:
        """
        Reload rules from the configuration file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        return self.rule_engine.reload_rules() 