import json
import os
import sys

from cli.commands import add_problem
from cli.commands import add_solution
from cli.commands import list_problems
from cli.commands import manage_structures
from cli.commands import search_problems
from cli.commands import stats
from cli.commands import theme
from cli.utils.config_manager import ConfigManager
from cli.utils.ui import (
    print_banner, print_small_banner, print_info, print_error, 
    separator, console, render_header, render_info_section, 
    render_status_bar, get_styled_input, set_theme
)

def load_config():
    config_manager = ConfigManager()
    return config_manager.config

COMMANDS = [
    ("add", "Create a new problem"),
    ("add-sol", "Add a solution to a problem"),
    ("list", "List and filter problems"),
    ("search", "Search problems by name or number"),
    ("manage-structures", "Manage data structures"),
    ("stats", "Show problem statistics"),
    ("theme", "Change the UI theme"),
    ("exit", "Exit the CLI"),
    ("quit", "Exit the CLI"),
    ("/help", "Show this help message"),
]


def show_help():
    """Show help with beautiful formatting"""
    console.print()
    console.print("[bold yellow]Usage: leet <command> [options][/bold yellow]\n")
    console.print("[bold white]Available Commands:[/bold white]\n")

    for cmd, desc in COMMANDS:
        console.print(f"  [bold cyan]{cmd:<20}[/bold cyan] {desc}")

    console.print()

def handle_command(config, cmd_string):
    parts = cmd_string.strip().split()
    if not parts:
        return True
    
    cmd = parts[0].lower()
    
    if cmd in ["exit", "quit", "q"]:
        console.print("[bold cyan]Goodbye![/bold cyan]")
        return False
        
    if cmd == "add":
        print()
        sys.argv = parts
        add_problem.main(config)
    elif cmd == "add-sol":
        print()
        sys.argv = parts
        add_solution.main(config)
    elif cmd == "list":
        print()
        sys.argv = parts
        list_problems.main(config)
    elif cmd == "search":
        print()
        sys.argv = parts
        search_problems.main(config)
    elif cmd == "manage-structures":
        print()
        sys.argv = parts
        manage_structures.main(config)
    elif cmd == "stats":
        print()
        sys.argv = parts
        stats.main(config)
    elif cmd == "theme":
        print()
        sys.argv = parts
        theme.main(config)
    elif cmd in ["help", "/help"]:
        show_help()
    else:
        print()
        print_error(f"Unknown command: '{cmd}'")
        print()
        show_help()
    return True

def main():
    config = load_config()
    
    # Set UI theme based on config
    theme_name = config.get("theme", "claude")
    set_theme(theme_name)

    # If arguments are provided (e.g. `leet add`), run once and exit
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            # Print legacy banner for direct help call
            render_header()
        handle_command(config, " ".join(sys.argv[1:]))
        return

    # Check if stdin is interactive (terminal) or piped/test
    if not sys.stdin.isatty():
        # Non-interactive environment (tests, pipes, etc.) - show help and exit
        show_help()
        return

    # Interactive UI Loop (only in terminal)
    render_header()
    render_info_section()

    while True:
        try:
            render_status_bar()
            available_commands = [cmd for cmd, _ in COMMANDS]
            command = get_styled_input(available_commands=available_commands)
            if not command.strip():
                continue
                
            should_continue = handle_command(config, command)
            if not should_continue:
                break
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold cyan]Exiting...[/bold cyan]")
            break

if __name__ == "__main__":
    main()