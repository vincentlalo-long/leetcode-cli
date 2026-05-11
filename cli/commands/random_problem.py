import os
import random
from typing import Any, Dict
try:
    import markdownify
except ImportError:
    markdownify = None

from cli.utils.leetcode_api import get_all_problems, get_problem_details, slugify
from cli.utils.file_utils import create_problem_directory
from cli.utils.config_manager import ConfigManager
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_info, print_warning,
    print_path, styled_text_input, styled_select, styled_confirm,
    print_section, separator, console
)

def main(config: Dict[str, Any]):
    """Fetch a random LeetCode problem based on difficulty preference."""
    print_command_banner("Random LeetCode Problem")
    
    difficulty_choices = ["Any", "Easy", "Medium", "Hard"]
    selected_difficulty = styled_select("Select difficulty level", difficulty_choices)
    
    print_info("Fetching problems...")
    data = get_all_problems()
    
    if not data or "stat_status_pairs" not in data:
        print_error("Could not fetch problems. Please check your connection.")
        return
        
    problems = data["stat_status_pairs"]
    
    # Map selection to LeetCode API difficulty levels (1=Easy, 2=Medium, 3=Hard)
    diff_map = {"Easy": 1, "Medium": 2, "Hard": 3}
    
    # Filter for unpaid problems
    candidates = [p for p in problems if not p.get("paid_only")]
    
    if selected_difficulty != "Any":
        target_level = diff_map[selected_difficulty]
        candidates = [p for p in candidates if p.get("difficulty", {}).get("level") == target_level]
        
    if not candidates:
        print_error(f"No free {selected_difficulty} problems found.")
        return
        
    problem = random.choice(candidates)
    
    problem_num = str(problem["stat"]["frontend_question_id"])
    problem_name = problem["stat"]["question__title"]
    slug = problem["stat"]["question__title_slug"]
    
    # LeetCode difficulty names mapping
    level_to_name = {1: "Easy", 2: "Medium", 3: "Hard"}
    difficulty = level_to_name.get(problem.get("difficulty", {}).get("level"), "Unknown")
    
    link = f"https://leetcode.com/problems/{slug}/"
    
    print_section("Your Random Problem")
    console.print(f"  [bold white]{problem_num}. {problem_name}[/bold white]")
    console.print(f"  [dim]Difficulty:[/dim] [bold]{difficulty}[/bold]")
    console.print(f"  [dim]Link:[/dim] [blue]{link}[/blue]")
    console.print()
    
    if not styled_confirm("Add this problem to your workspace?", default=True):
        return
        
    config_manager = ConfigManager()
    base_dir = config["base_dir"]
    data_structures = config_manager.get_data_structures()
    
    if not data_structures:
        print_error("No data structures found. Add one first!")
        return
        
    choices = list(data_structures.keys()) + ["Add new data structure"]
    selected = styled_select("Select data structure", choices)
    
    if selected == "Add new data structure":
        from cli.commands.manage_structures import add_new_structure
        if not add_new_structure(config_manager):
            return
        data_structures = config_manager.get_data_structures()
        selected = styled_select("Select data structure", list(data_structures.keys()))
        
    ds_folder = data_structures[selected]
    folder_name = f"{problem_num}-{slug}"
    problem_dir = create_problem_directory(base_dir, ds_folder, folder_name)
    
    if not os.path.exists(problem_dir):
        os.makedirs(problem_dir, exist_ok=True)
        
    problem_file = os.path.join(problem_dir, f"{problem_num}_{problem_name}.cpp")
    
    if os.path.exists(problem_file):
        print_warning("Problem file already exists!")
        print_path("Path", problem_file)
        return
        
    # Get full details for tags and description
    print_info("Fetching full problem details...")
    details = get_problem_details(slug)
    
    tags_str = "None"
    if details:
        tags = [tag.get("name") for tag in details.get("topicTags", [])]
        tags_str = ", ".join(tags) if tags else "None"
        
    # Content template
    content = f"""/*
LeetCode Problem {problem_num}: {problem_name}
Link: {link}
Difficulty: {difficulty}
Tags: {tags_str}
Data Structure: {selected}
*/
"""
    
    with open(problem_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    if details and details.get("content"):
        readme_path = os.path.join(problem_dir, "README.md")
        raw_content = details.get('content')
        md_content = raw_content
        if markdownify:
            try:
                md_content = markdownify.markdownify(raw_content, heading_style="ATX")
            except Exception as e:
                print_warning(f"Could not convert HTML to Markdown: {e}")
                
        clean_num = str(int(problem_num)) if problem_num.isdigit() else problem_num
        readme_content = f"# [{clean_num}. {problem_name}]({link})\n\n- **Difficulty:** {difficulty}\n- **Tags:** {tags_str}\n\n## Description\n\n{md_content.strip()}"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print_success("Saved problem description to README.md")

    print_success("Created problem directory and files")
    print_path("Path", problem_file)
    console.print()
