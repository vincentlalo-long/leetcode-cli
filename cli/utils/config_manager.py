import json
import os
from typing import Dict, Any

class ConfigManager:
    """Manages configuration file for LeetCode CLI"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "../../config.json")
        self.config_path = os.path.abspath(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def save_config(self):
        """Save configuration to JSON file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value by key"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value and save"""
        self.config[key] = value
        self.save_config()
    
    def get_theme(self) -> str:
        """Get the current UI theme"""
        return self.config.get("theme", "claude")
    
    def set_theme(self, theme_name: str) -> bool:
        """Set the UI theme"""
        self.config["theme"] = theme_name
        self.save_config()
        return True

    
    def get_data_structures(self) -> Dict[str, str]:
        """Get all data structures"""
        return self.config.get("data_structures", {})
    
    def add_data_structure(self, name: str, folder: str) -> bool:
        """Add a new data structure to config"""
        if name in self.config["data_structures"]:
            return False
        self.config["data_structures"][name] = folder
        self.save_config()
        return True
    
    def remove_data_structure(self, name: str) -> bool:
        """Remove a data structure from config"""
        if name not in self.config["data_structures"]:
            return False
        del self.config["data_structures"][name]
        self.save_config()
        return True
