import os
try:
    import markdownify
except ImportError:
    markdownify = None

from cli.utils.config_manager import ConfigManager
from cli.utils.file_utils import create_problem_directory
from cli.utils.leetcode_api import get_problem_details, slugify, get_problem_by_id
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_info, print_warning,
    print_path, styled_text_input, styled_select, styled_confirm,
    print_section, separator, console
)

def main(config: dict):
    """Add a new LeetCode problem"""
    print_command_banner("Add New Problem")
    
    config_manager = ConfigManager()
    base_dir = config["base_dir"]
    
    # Get problem information
    problem_num = styled_text_input("Problem number")
    
    # Try to fetch problem name by ID
    suggested_name = ""
    print_info("Looking up problem details...")
    problem_data = get_problem_by_id(problem_num)
    if problem_data:
        suggested_name = problem_data["title"]
        print_success(f"Found: {suggested_name}")
    else:
        print_warning(f"Could not find problem with ID {problem_num}")
        
    problem_name = styled_text_input("Problem name", default=suggested_name)
    
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
    slug = slugify(problem_name)
    folder_name = f"{problem_num}-{slug}"
    problem_dir = create_problem_directory(base_dir, ds_folder, folder_name)
    
    if not os.path.exists(problem_dir):
        os.makedirs(problem_dir, exist_ok=True)
    
    problem_file = os.path.join(problem_dir, f"{problem_num}_{problem_name}.cpp")
    
    if os.path.exists(problem_file):
        print_error("Problem file already exists!")
        return
    
    # Ask if user wants to add solution now
    add_sol_now = styled_confirm("Add solution now?", default=False)
    
    print_info(f"Fetching problem details from LeetCode...")
    details = get_problem_details(slug)
    
    if details:
        difficulty = details.get("difficulty", "Unknown")
        tags = [tag.get("name") for tag in details.get("topicTags", [])]
        tags_str = ", ".join(tags) if tags else "None"
        link = f"https://leetcode.com/problems/{slug}/"
        actual_title = details.get("title", problem_name)
        
        content = f"""/*
LeetCode Problem {problem_num}: {actual_title}
Link: {link}
Difficulty: {difficulty}
Tags: {tags_str}
Data Structure: {selected}
*/
"""
        print_success(f"Found: {actual_title} ({difficulty})")
    else:
        content = f"""/*
LeetCode Problem {problem_num}: {problem_name}
Data Structure: {selected}
*/
"""
        print_error(f"Could not fetch problem details for '{problem_name}'. Using basic template.")
    
    if add_sol_now:
        console.print()
        print_section("Solution Details")
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
        
        content += f"""\n/// ================== Solution 1 ==================
/*
Method: {method}
Time Complexity: {time}
Space Complexity: {space}
*/

{code}
"""
    
    with open(problem_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    if details and details.get("content"):
        readme_path = os.path.join(problem_dir, "README.md")
        
        # Convert HTML content to Markdown if markdownify is available
        raw_content = details.get('content')
        md_content = raw_content
        if markdownify:
            try:
                md_content = markdownify.markdownify(raw_content, heading_style="ATX")
            except Exception as e:
                print_warning(f"Could not convert HTML to Markdown: {e}")
                
        # Clean problem number to strip leading zeros if any for display
        clean_num = str(int(problem_num)) if problem_num.isdigit() else problem_num
        
        readme_content = f"# [{clean_num}. {actual_title}]({link})\n\n- **Difficulty:** {difficulty}\n- **Tags:** {tags_str}\n\n## Description\n\n{md_content.strip()}"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print_success("Saved problem description to README.md")
    
    console.print()
    print_success("Created problem directory and files")
    print_path("Path", problem_file)
    console.print()
