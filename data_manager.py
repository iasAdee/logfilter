# ============================================================================
# data_manager.py
import uuid
from typing import Dict, Optional, Any
import pandas as pd


class DataManager:
    """Central data manager for storing and retrieving uploaded files."""
    
    def __init__(self, cache):
        self.cache = cache
    
    def store_data(self, data: Any, metadata: Dict[str, Any] = None) -> str:
        """
        Store data in cache and return a unique key.
        
        Args:
            data: The data to store (DataFrame, dict, etc.)
            metadata: Optional metadata about the data
        
        Returns:
            Cache key for retrieval
        """
        key = str(uuid.uuid4())
        
        storage_obj = {
            "data": data,
            "metadata": metadata or {}
        }
        
        self.cache.set(key, storage_obj)
        return key
    
    def get_data(self, key: str) -> Optional[Any]:
        """
        Retrieve data from cache by key.
        
        Args:
            key: Cache key
        
        Returns:
            The stored data or None if not found
        """
        obj = self.cache.get(key)
        if obj is None:
            return None
        
        # Handle both old format (direct data) and new format (with metadata)
        if isinstance(obj, dict) and "data" in obj:
            return obj["data"]
        return obj
    
    def get_full_object(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve full object including metadata.
        
        Args:
            key: Cache key
        
        Returns:
            Dictionary with 'data' and 'metadata' or None
        """
        obj = self.cache.get(key)
        if obj is None:
            return None
        
        # Ensure consistent format
        if isinstance(obj, dict) and "data" in obj:
            return obj
        return {"data": obj, "metadata": {}}
    
    def clear_cache(self):
        """Clear all cached data."""
        self.cache.clear()
    
    def get_dataframe(self, key: str) -> Optional[pd.DataFrame]:
        """
        Convenience method to get DataFrame specifically.
        
        Args:
            key: Cache key
        
        Returns:
            DataFrame or None
        """
        data = self.get_data(key)
        if isinstance(data, pd.DataFrame):
            return data
        return None
