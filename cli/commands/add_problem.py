import os
import questionary
from rich import print
from cli.utils.config_manager import ConfigManager
from cli.utils.file_utils import create_problem_directory

def main(config: dict):
    """Add a new LeetCode problem"""
    config_manager = ConfigManager()
    base_dir = config["base_dir"]
    
    problem_num = questionary.text("Problem number:").ask()
    problem_name = questionary.text("Problem name:").ask()
    
    # Get or manage data structures
    data_structures = config_manager.get_data_structures()
    
    if not data_structures:
        print("[red]No data structures found. Add one first![/red]")
        return
    
    choices = list(data_structures.keys()) + ["[ADD NEW DATA STRUCTURE]"]
    selected = questionary.select(
        "Data structure:",
        choices=choices
    ).ask()
    
    # If user wants to add new data structure
    if selected == "[ADD NEW DATA STRUCTURE]":
        from cli.commands.manage_structures import add_new_structure
        if not add_new_structure(config_manager):
            return
        # Reload data structures and ask again
        data_structures = config_manager.get_data_structures()
        selected = questionary.select(
            "Data structure:",
            choices=list(data_structures.keys())
        ).ask()
    
    ds_folder = data_structures[selected]
    problem_dir = create_problem_directory(base_dir, ds_folder, problem_num)
    
    if not os.path.exists(problem_dir):
        os.makedirs(problem_dir, exist_ok=True)
    
    problem_file = os.path.join(problem_dir, f"{problem_num}_{problem_name}.cpp")
    
    if os.path.exists(problem_file):
        print("[red]Problem file already exists![/red]")
        return
    
    with open(problem_file, "w") as f:
        f.write(f"""/*
LeetCode Problem {problem_num}: {problem_name}
Data Structure: {selected}
*/

// Solution 1
/*
Method: 
Time Complexity: 
Space Complexity: 
*/
""")
    
    print(f"\n[green]✔ Created problem directory and file[/green]\n")
    print(f"[cyan]Path: {problem_file}[/cyan]\n")
