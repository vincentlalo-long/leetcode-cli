import os
import questionary
from rich import print
from cli.utils.config_manager import ConfigManager

def add_new_structure(config_manager: ConfigManager) -> bool:
    """Add a new data structure to the configuration"""
    
    name = questionary.text(
        "Enter data structure name (e.g., 'tree', 'hash_table'):"
    ).ask()
    
    if not name:
        print("[red]Data structure name cannot be empty![/red]")
        return False
    
    folder = questionary.text(
        f"Enter folder name (default: '{name}'):"
    ).ask() or name
    
    if config_manager.add_data_structure(name, folder):
        print(f"\n[green]✔ Added data structure: {name} -> {folder}[/green]\n")
        return True
    else:
        print(f"[red]Data structure '{name}' already exists![/red]")
        return False

def list_structures(config_manager: ConfigManager):
    """List all available data structures"""
    structures = config_manager.get_data_structures()
    
    if not structures:
        print("[yellow]No data structures found![/yellow]")
        return
    
    print("\n[cyan]Available Data Structures:[/cyan]")
    for name, folder in structures.items():
        print(f"  • {name} -> {folder}")
    print()

def remove_structure(config_manager: ConfigManager):
    """Remove a data structure"""
    structures = config_manager.get_data_structures()
    
    if not structures:
        print("[yellow]No data structures to remove![/yellow]")
        return
    
    name = questionary.select(
        "Select data structure to remove:",
        choices=list(structures.keys())
    ).ask()
    
    confirm = questionary.confirm(
        f"Are you sure you want to remove '{name}'?"
    ).ask()
    
    if confirm and config_manager.remove_data_structure(name):
        print(f"\n[green]✔ Removed data structure: {name}[/green]\n")
    else:
        print("[yellow]Operation cancelled[/yellow]")

def main(config: dict):
    """Manage data structures"""
    config_manager = ConfigManager()
    
    action = questionary.select(
        "What would you like to do?",
        choices=[
            "List all data structures",
            "Add new data structure",
            "Remove data structure"
        ]
    ).ask()
    
    if action == "List all data structures":
        list_structures(config_manager)
    elif action == "Add new data structure":
        add_new_structure(config_manager)
    elif action == "Remove data structure":
        remove_structure(config_manager)
