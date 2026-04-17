import questionary
from rich import print
from cli.utils.config_manager import ConfigManager
from cli.utils.file_utils import get_all_cpp_files, count_solutions

def main(config: dict):
    """Add a new solution to an existing LeetCode problem"""
    config_manager = ConfigManager()
    base_dir = config["base_dir"]
    
    # Get all .cpp files
    files = get_all_cpp_files(base_dir)
    
    if not files:
        print("[red]No problem files found![/red]")
        return
    
    file_path = questionary.select(
        "Select file:",
        choices=files
    ).ask()
    
    if not file_path:
        print("[red]No file selected[/red]")
        return
    
    with open(file_path, "r") as f:
        content = f.read()
    
    sol_num = count_solutions(content) + 1
    
    print(f"\n[cyan]Adding Solution {sol_num}[/cyan]\n")
    
    method = questionary.text("Method:").ask()
    time = questionary.text("Time complexity:").ask()
    space = questionary.text("Space complexity:").ask()
    
    print("\n[yellow]Paste code (end with EOF):[/yellow]")
    
    lines = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        lines.append(line)
    
    code = "\n".join(lines)
    
    new_block = f"""

/// ================== Solution {sol_num} ==================
/*
Method: {method}
Time Complexity: {time}
Space Complexity: {space}
*/

{code}
"""
    
    with open(file_path, "a") as f:
        f.write(new_block)
    
    print(f"\n[green]✔ Added Solution {sol_num}[/green]\n")
