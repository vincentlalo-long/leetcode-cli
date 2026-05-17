import json
import os
from typing import Dict, Any

from cli.utils.language_support import DEFAULT_LANGUAGES, normalize_languages, get_default_language_key

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

    def get_editor(self) -> str:
        """Get the configured editor, default to code (VS Code)"""
        return self.config.get("editor", "code")

    def set_editor(self, editor: str) -> bool:
        """Set the configured editor"""
        self.config["editor"] = editor
        self.save_config()
        return True
    
    def get_data_structures(self) -> Dict[str, str]:
        """Get all data structures"""
        return self.config.get("data_structures", {})

    def get_languages(self) -> Dict[str, Dict[str, str]]:
        """Get configured languages with normalized labels/extensions"""
        languages = self.config.get("languages", DEFAULT_LANGUAGES)
        return normalize_languages(languages)

    def get_default_language(self) -> str:
        """Get the default language key"""
        languages = self.get_languages()
        default_key = self.config.get("default_language", "cpp")
        return get_default_language_key(languages, default_key)

    def set_default_language(self, language_key: str) -> bool:
        """Set the default language key"""
        self.config["default_language"] = language_key
        self.save_config()
        return True
    
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
