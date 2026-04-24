import json
import os
import sys

from cli.commands import add_problem
from cli.commands import add_solution
from cli.commands import manage_structures
from cli.commands import list_problems
from cli.utils.config_manager import ConfigManager
from cli.utils.ui import (
    print_banner, print_small_banner, print_info, print_error, 
    separator, console
)

def load_config():
    config_manager = ConfigManager()
    return config_manager.config

def show_help():
    """Show help with beautiful formatting"""
    print_banner()
    console.print("[bold yellow]Hey! Use 'leet <command>' to get started[/bold yellow]\n")

    console.print("[bold white]Available Commands:[/bold white]\n")
    
    commands = [
        ("add", "Create a new problem"),
        ("add-sol", "Add a solution to a problem"),
        ("manage-structures", "Manage data structures"),
        ("list", "List all problems"),
        ("help", "Show this help message"),
    ]
    
    for cmd, desc in commands:
        console.print(f"  [bold cyan]{cmd:<20}[/bold cyan] {desc}")
    
    console.print()

def main():
    config = load_config()

    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1]

    if cmd == "add":
        print()
        add_problem.main(config)
    elif cmd == "add-sol":
        print()
        add_solution.main(config)
    elif cmd == "manage-structures":
        print()
        manage_structures.main(config)
    elif cmd == "list":
        print()
        list_problems.main(config)
    elif cmd == "help":
        show_help()  # Fixed typo from 'show' to 'show_help'
