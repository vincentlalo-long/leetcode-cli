"""
Modern UI utilities for beautiful CLI styling - Claude Code inspired
"""
import questionary
from questionary import Style
from prompt_toolkit.completion import WordCompleter
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from typing import List, Optional
import os

console = Console()
DIVIDER_WIDTH = 56

# Claude Code inspired color scheme - remove ? and use > instead
CLAUDE_STYLE = Style([
    ('qmark', 'fg:#00D9FF bold'),           # Cyan for question marks → use as >
    ('question', 'fg:#FFFFFF bold'),        # White for questions
    ('answer', 'fg:#00D9FF bold'),          # Cyan for answers
    ('pointer', 'fg:#00D9FF bold'),         # Cyan pointer
    ('highlighted', 'fg:#000000 bg:#00D9FF'),  # Highlight
    ('selected', 'fg:#00D9FF bold'),        # Selected
    ('separator', 'fg:#404040'),            # Dark separator
    ('instruction', 'fg:#808080'),          # Gray instruction
])

def print_header(title: str, subtitle: Optional[str] = None):
    """Print a clean, aligned header panel."""
    content = Text(title, style="bold white")
    if subtitle:
        content.append("\n")
        content.append(subtitle, style="dim")

    panel = Panel.fit(
        content,
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 2),
    )
    console.print(panel)


def print_success(message: str):
    """Print success message"""
    console.print(f"[green]✔[/green] [bold green]{message}[/bold green]")


def print_error(message: str):
    """Print error message"""
    console.print(f"[red]✘[/red] [bold red]{message}[/bold red]")


def print_warning(message: str):
    """Print warning message"""
    console.print(f"[yellow]⚠[/yellow] [bold yellow]{message}[/bold yellow]")


def print_info(message: str):
    """Print info message"""
    console.print(f"[cyan]ℹ[/cyan] [cyan]{message}[/cyan]")


def print_path(label: str, path: str):
    """Print file path with nice formatting"""
    console.print(f"[dim]{label}:[/dim] [bold cyan]{path}[/bold cyan]")


def styled_text_input(message: str, default: Optional[str] = None) -> str:
    """
    Get text input with styled prompt (using > instead of ?)
    """
    return questionary.text(
        message,
        default=default or "",
        style=CLAUDE_STYLE,
        qmark=">"
    ).ask()


def styled_select(message: str, choices: List[str], use_pointer: bool = True) -> str:
    """
    Get selection with styled prompt (using > instead of ?)
    """
    return questionary.select(
        message,
        choices=choices,
        style=CLAUDE_STYLE,
        use_shortcuts=True,
        qmark=">"
    ).ask()


def styled_confirm(message: str, default: bool = False) -> bool:
    """
    Get confirmation with styled prompt (using > instead of ?)
    """
    return questionary.confirm(
        message,
        default=default,
        style=CLAUDE_STYLE,
        qmark=">"
    ).ask()


def print_section(title: str):
    """Print a section divider"""
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    separator()


def print_list_item(label: str, value: str):
    """Print a formatted list item"""
    console.print(f"  [dim]{label:<20}[/dim] [cyan]{value}[/cyan]")


def print_code_block(code: str, language: str = "cpp", title: Optional[str] = None):
    """Print a syntax-highlighted code block"""
    syntax = Syntax(code, language, theme="monokai", line_numbers=False)
    if title:
        panel = Panel(syntax, title=title, border_style="cyan")
        console.print(panel)
    else:
        console.print(syntax)


def separator():
    """Print a separator line"""
    width = max(24, min(DIVIDER_WIDTH, console.width - 2))
    console.print("[dim]" + "-" * width + "[/dim]")


def print_menu_header(title: str):
    """Print a menu header"""
    print_section(title)


def print_menu_footer():
    """Print a menu footer"""
    separator()
    console.print()


def render_header():
    """Renders the stylized 'IDEAL' logo with ASCII art and gradient colors."""
    # Brighter, multi-tone palette for a more colorful banner
    lines = [
        " [bold blue]██╗[/bold blue]  [bold magenta]██████╗ [/bold magenta] [bold magenta]███████╗ [/bold magenta] [bold yellow]█████╗ [/bold yellow]  [bold yellow]██╗ [/bold yellow]",
        " [bold blue]██║[/bold blue]  [bold magenta]██╔══██╗[/bold magenta] [bold magenta]██╔════╝ [/bold magenta] [bold yellow]██╔══██╗[/bold yellow] [bold yellow]██║ [/bold yellow]",
        " [bold blue]██║[/bold blue]  [bold magenta]██║  ██║[/bold magenta] [bold magenta]█████╗   [/bold magenta] [bold green]███████║[/bold green] [bold green]██║ [/bold green]",
        " [bold blue]██║[/bold blue]  [bold magenta]██║  ██║[/bold magenta] [bold magenta]██╔══╝   [/bold magenta] [bold green]██╔══██║[/bold green] [bold green]██║ [/bold green]",
        " [bold cyan]██║[/bold cyan]  [bold cyan]██████╔╝[/bold cyan] [bold magenta]███████╗ [/bold magenta] [bold cyan]██║  ██║[/bold cyan] [bold cyan]███████╗[/bold cyan]",
        " [bold cyan]╚═╝[/bold cyan]  [bold cyan]╚═════╝ [/bold cyan] [bold magenta]╚══════╝ [/bold magenta] [bold cyan]╚═╝  ╚═╝[/bold cyan] [bold cyan]╚══════╝[/bold cyan]",
    ]
    for line in lines:
        console.print(line)
    console.print()


def render_info_section():
    """Renders the helpful tips box."""
    tips_text = (
        "[white]Tips for getting started:[/white]\n"
        "[white]1. Ask questions, edit files, or run commands.[/white]\n"
        "[white]2. Be specific for the best results.[/white]\n"
        "[white]3. [bold magenta]/help[/bold magenta] for more information.[/white]"
    )
    console.print(tips_text + "\n")


def render_status_bar(mode="no sandbox", active_model="IDEAL-core (100%)"):
    """Renders the three-column status bar below the input."""
    # Get short path representation (e.g. ~/project)
    home = os.path.expanduser("~")
    cwd = os.getcwd().replace(home, "~")
    
    # Left, Center, Right aligned elements
    left = Text(cwd, style="bold cyan")
    center = Text(mode, style="red")
    right = Text(active_model, style="magenta")
    
    # Use Columns to auto-space items across the terminal width
    columns = Columns([
        Align(left, align="left"),
        Align(center, align="center"),
        Align(right, align="right")
    ], expand=True)
    
    # Draw separation line and columns
    console.print("[dim]" + "─" * console.width + "[/dim]")
    console.print(columns)
    console.print()


def get_styled_input(available_commands: Optional[List[str]] = None) -> str:
    """Renders the input prompt with integrated footer and autocomplete."""
    # Top divider
    console.print("[dim]" + "─" * console.width + "[/dim]")

    completer = None
    if available_commands:
        completer = WordCompleter(available_commands, ignore_case=True)

    # Styled input request with suggestions
    cmd = questionary.text(
        "",
        style=CLAUDE_STYLE,
        qmark=">",
        completer=completer,
    ).ask()

    # Bottom footer integrated with input box
    footer_text = (
        "[dim]Ctrl+C to exit[/dim] • "
        "[dim]/help for commands[/dim] • "
        "[dim]Type a command to start[/dim]"
    )
    console.print("[dim]" + "─" * console.width + "[/dim]")
    console.print(Align(footer_text, align="center"))
    console.print()

    return cmd or ""


def print_banner():
    """Print a balanced Claude-like welcome frame."""
    content = Text()
    content.append("LeetCode CLI\n", style="bold white")
    content.append("Problem Tracker\n", style="bold cyan")
    content.append("Track problems, solutions, and progress.\n", style="dim")
    content.append("Run ", style="dim")
    content.append("leet help", style="bold cyan")
    content.append(" to get started.", style="dim")

    panel = Panel.fit(
        content,
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2),
    )
    console.print(panel)


def print_small_banner():
    """Print a compact banner"""
    panel = Panel.fit(
        Text("LeetCode CLI", style="bold white"),
        border_style="bright_black",
        box=box.SQUARE,
        padding=(0, 1),
    )
    console.print(panel)


def print_command_banner(title: str):
    """Print a command banner"""
    console.print()
    panel = Panel.fit(
        Text(title, style="bold white"),
        border_style="cyan",
        box=box.SQUARE,
        padding=(0, 2),
    )
    console.print(panel)
    separator()
