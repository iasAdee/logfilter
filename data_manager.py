# ============================================================================
# data_manager.py
import uuid
from typing import Dict, Optional, Any
import pandas as pd
import logging
import pickle


class DataManager:
    """Central data manager for storing and retrieving uploaded files."""
    
    def __init__(self, cache):
        self.cache = cache
    
    def store_data(self, data: Any, metadata: Dict[str, Any] = None) -> str:
        """
        Store data in cache and return a unique key.
        """
        key = str(uuid.uuid4())
        
        storage_obj = {
            "data": pickle.dumps(data),
            "metadata": metadata or {}
        }
        
        self.cache.set(key, storage_obj)
        return key
    
    def get_data(self, key: str) -> Optional[Any]:
        """
        Retrieve data from cache by key.
        """
        obj = self.cache.get(key)
        if obj is None:
            logging.info("Cache key is returning nothing")
            return None
        
        if isinstance(obj, dict) and "data" in obj:
            return pickle.loads(obj["data"])
        
        return obj
    
    def get_full_object(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve full object including metadata.
        """
        obj = self.cache.get(key)
        if obj is None:
            logging.info("Cache key is returning nothing")
            return None
        
        if isinstance(obj, dict) and "data" in obj:
            return {
                "data": pickle.loads(obj["data"]),
                "metadata": obj.get("metadata", {})
            }
        
        return {"data": obj, "metadata": {}}
    
    def clear_cache(self):
        """Clear all cached data."""
        self.cache.clear()
    
    def get_dataframe(self, key: str) -> Optional[pd.DataFrame]:
        """
        Convenience method to get DataFrame specifically.
        """
        data = self.get_data(key)
        
        if isinstance(data, pd.DataFrame):
            return data
        
        logging.info("Data is not instance of DataFrame")
        return None
