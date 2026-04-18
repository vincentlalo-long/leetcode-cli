import os
from cli.utils.config_manager import ConfigManager
from cli.utils.file_utils import create_problem_directory
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_info,
    print_path, styled_text_input, styled_select,
    print_section, separator, console
)

def main(config: dict):
    """Add a new LeetCode problem"""
    print_command_banner("Add New Problem")
    
    config_manager = ConfigManager()
    base_dir = config["base_dir"]
    
    # Get problem information
    problem_num = styled_text_input("Problem number")
    problem_name = styled_text_input("Problem name")
    
    # Get or manage data structures
    data_structures = config_manager.get_data_structures()
    
    if not data_structures:
        print_error("No data structures found. Add one first!")
        return
    
    choices = list(data_structures.keys()) + ["Add new data structure"]
    selected = styled_select("Select data structure", choices)
    
    # If user wants to add new data structure
    if selected == "Add new data structure":
        from cli.commands.manage_structures import add_new_structure
        if not add_new_structure(config_manager):
            return
        # Reload data structures and ask again
        data_structures = config_manager.get_data_structures()
        selected = styled_select(
            "Select data structure",
            list(data_structures.keys())
        )
    
    ds_folder = data_structures[selected]
    problem_dir = create_problem_directory(base_dir, ds_folder, problem_num)
    
    if not os.path.exists(problem_dir):
        os.makedirs(problem_dir, exist_ok=True)
    
    problem_file = os.path.join(problem_dir, f"{problem_num}_{problem_name}.cpp")
    
    if os.path.exists(problem_file):
        print_error("Problem file already exists!")
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
    
    console.print()
    print_success("Created problem directory and file")
    print_path("Path", problem_file)
    console.print()
