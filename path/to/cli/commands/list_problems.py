import os
from cli.utils.config_manager import ConfigManager
from cli.utils.ui import print_error, print_info  # Added imports

def main(config: dict):
    config_manager = ConfigManager()
    base_dir = config_manager.get('base_dir', '')
    if not base_dir:
        print_error("Base directory not found in config.")
        return
    try:
        problems = os.listdir(base_dir)
        if not problems:
            print_info("No problems found.")
            return
        print_info("List of problems:")
        for problem in problems:
            print(f" - {problem}")
    except Exception as e:
        print_error(f"Error listing problems: {e}")
