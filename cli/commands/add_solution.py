import os

from cli.utils.config_manager import ConfigManager
from cli.utils.file_utils import get_all_solution_files, count_solutions
from cli.utils.language_support import build_solution_block, get_language_by_extension
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_info,
    print_section, styled_select, styled_text_input,
    separator, console
)

def main(config: dict):
    """Add a new solution to an existing LeetCode problem"""
    print_command_banner("Add New Solution")
    
    config_manager = ConfigManager()
    base_dir = config["base_dir"]
    
    languages = config_manager.get_languages()
    extensions = [info["ext"] for info in languages.values()]

    # Get all solution files
    files = get_all_solution_files(base_dir, extensions)
    
    if not files:
        print_error("No problem files found!")
        return
    
    file_path = styled_select("Select problem file", files)
    
    if not file_path:
        print_error("No file selected")
        return
    
    with open(file_path, "r") as f:
        content = f.read()
    
    sol_num = count_solutions(content) + 1
    
    print_info(f"Adding Solution {sol_num} to {file_path.split('/')[-1]}")
    console.print()
    
    method = styled_text_input("Method/Approach")
    time = styled_text_input("Time complexity")
    space = styled_text_input("Space complexity")
    separator()
    
    print_info("Paste your code (end with EOF):")
    
    lines = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        lines.append(line)
    
    code = "\n".join(lines)
    
    _, ext = os.path.splitext(file_path)
    language_key = get_language_by_extension(languages, ext)
    if not language_key:
        language_key = config_manager.get_default_language()

    new_block = build_solution_block(
        language_key,
        sol_num,
        method,
        time,
        space,
        code,
    )
    
    with open(file_path, "a") as f:
        f.write(new_block)
    
    console.print()
    print_success(f"Added Solution {sol_num}")
    print_info(f"File: {file_path}")
    console.print()
