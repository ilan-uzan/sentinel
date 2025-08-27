"""
Base collector abstract class for system data collection.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseCollector(ABC):
    """
    Abstract base class for all system data collectors.
    
    This class defines the interface that all collectors must implement.
    Each collector is responsible for gathering specific types of system data.
    """
    
    @abstractmethod
    def collect(self) -> List[Dict[str, Any]]:
        """
        Collect system data and return normalized dictionary format.
        
        Returns:
            List[Dict[str, Any]]: List of normalized data dictionaries
        """
        pass 