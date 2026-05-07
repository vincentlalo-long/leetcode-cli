import sys
from typing import Any, Dict

from cli.utils.ui import (
    THEMES,
    console,
    print_command_banner,
    print_success,
    print_error,
    styled_select,
    set_theme
)
from cli.utils.config_manager import ConfigManager

def main(config: Dict[str, Any]) -> None:
    """Command to change the UI theme"""
    print_command_banner("Select UI Theme")
    
    current_theme = config.get("theme", "claude")
    available_themes = list(THEMES.keys())
    
    # Capitalize for display, keeping original as value
    choices = [t.capitalize() + (" (Current)" if t == current_theme else "") for t in available_themes]
    
    selection = styled_select("Choose a theme for the CLI", choices)
    
    # Extract the base theme name (remove " (Current)" and lowercase)
    selected_theme = selection.split(" ")[0].lower()
    
    if selected_theme == current_theme:
        print_success(f"Theme is already set to {selected_theme}")
        return
        
    if selected_theme in available_themes:
        # Update config
        cm = ConfigManager()
        cm.set_theme(selected_theme)
        
        # Apply theme immediately
        set_theme(selected_theme)
        
        print_success(f"Theme successfully changed to {selected_theme.capitalize()}!")
        console.print("[cyan]The new colors are now active.[/cyan]")
    else:
        print_error("Invalid theme selected")
