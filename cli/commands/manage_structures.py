import os
from cli.utils.config_manager import ConfigManager
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_warning,
    print_info, print_section, print_list_item,
    styled_text_input, styled_select, styled_confirm,
    separator, console
)

def add_new_structure(config_manager: ConfigManager) -> bool:
    """Add a new data structure to the configuration"""
    
    name = styled_text_input("Data structure name (e.g., tree)")
    
    if not name:
        print_error("Data structure name cannot be empty!")
        return False
    
    folder = styled_text_input(
        f"Folder name (press Enter for '{name}')",
        default=name
    ) or name
    
    if config_manager.add_data_structure(name, folder):
        separator()
        console.print()
        print_success(f"Added data structure: {name} → {folder}")
        console.print()
        return True
    else:
        print_error(f"Data structure '{name}' already exists!")
        return False

def list_structures(config_manager: ConfigManager):
    """List all available data structures"""
    structures = config_manager.get_data_structures()
    
    if not structures:
        print_warning("No data structures found!")
        return
    
    print_section("Available Data Structures")
    for name, folder in structures.items():
        print_list_item(name, folder)
    console.print()

def remove_structure(config_manager: ConfigManager):
    """Remove a data structure"""
    structures = config_manager.get_data_structures()
    
    if not structures:
        print_warning("No data structures to remove!")
        return
    
    name = styled_select(
        "Select data structure to remove",
        list(structures.keys())
    )
    
    confirm = styled_confirm(
        f"Remove '{name}'?",
        default=False
    )
    
    if confirm and config_manager.remove_data_structure(name):
        separator()
        console.print()
        print_success(f"Removed data structure: {name}")
        console.print()
    else:
        print_warning("Operation cancelled")

def main(config: dict):
    """Manage data structures"""
    print_command_banner("Manage Data Structures")
    console.print()
    
    config_manager = ConfigManager()
    
    action = styled_select(
        "What would you like to do?",
        [
            "List all data structures",
            "Add new data structure",
            "Remove data structure"
        ]
    )
    
    separator()
    console.print()
    
    if "List" in action:
        list_structures(config_manager)
    elif "Add" in action:
        add_new_structure(config_manager)
    elif "Remove" in action:
        remove_structure(config_manager)

