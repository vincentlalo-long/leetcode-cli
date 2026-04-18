"""
Modern UI utilities for beautiful CLI styling - Claude Code inspired
"""
import questionary
from questionary import Style
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from typing import List, Optional

console = Console()

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

# Icons for various purposes
ICONS = {
    'question': '?',
    'success': '✔',
    'error': '✘',
    'warning': '⚠',
    'info': 'ℹ',
    'arrow': '→',
    'bullet': '•',
    'star': '★',
}


def print_header(title: str, subtitle: Optional[str] = None):
    """Print a beautiful header"""
    title_text = Text(title, style="bold cyan")
    
    if subtitle:
        subtitle_text = Text(subtitle, style="dim white")
        panel_content = f"{title_text}\n{subtitle_text}"
    else:
        panel_content = title_text
    
    panel = Panel(
        panel_content,
        border_style="cyan",
        padding=(1, 2)
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
        qmark="›"  # Use › instead of ?
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
        qmark="›"  # Use › instead of ?
    ).ask()


def styled_confirm(message: str, default: bool = False) -> bool:
    """
    Get confirmation with styled prompt (using > instead of ?)
    """
    return questionary.confirm(
        message,
        default=default,
        style=CLAUDE_STYLE,
        qmark="›"  # Use › instead of ?
    ).ask()


def print_section(title: str):
    """Print a section divider"""
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    console.print("[dim]" + "─" * 50 + "[/dim]")


def print_list_item(label: str, value: str):
    """Print a formatted list item"""
    console.print(f"  [white]{label}:[/white] [cyan]{value}[/cyan]")


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
    console.print("[dim]" + "─" * 50 + "[/dim]")


def print_menu_header(title: str):
    """Print a menu header"""
    console.print(f"\n[bold cyan]╭─ {title} ─╮[/bold cyan]")


def print_menu_footer():
    """Print a menu footer"""
    console.print(f"[bold cyan]╰─────────────────────────╯[/bold cyan]\n")


def print_banner():
    """Print a beautiful ASCII art banner inspired by Claude"""
    banner = """
[bold cyan]
    ╔════════════════════════════════════════╗
    ║                                        ║
    ║      LeetCode Problem Tracker          ║
    ║                                        ║
    ║   Master Your Coding Challenges       ║
    ║                                        ║
    ╚════════════════════════════════════════╝
[/bold cyan]
"""
    console.print(banner)


def print_small_banner():
    """Print a compact banner"""
    banner = """[dim cyan]
  ┌─────────────────────────────────┐
  │  LeetCode CLI  v1.0             │
  └─────────────────────────────────┘
[/dim cyan]"""
    console.print(banner)


def print_command_banner(title: str):
    """Print a command banner"""
    banner = f"\n[bold cyan]{title}[/bold cyan]"
    console.print(banner)
    console.print("[dim cyan]" + "─" * 40 + "[/dim cyan]")
