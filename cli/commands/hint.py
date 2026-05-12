import re
from typing import Any, Dict
try:
    import markdownify
except ImportError:
    markdownify = None

from cli.utils.leetcode_api import get_problem_by_id, get_problem_details
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_info, print_warning,
    styled_text_input, print_section, console
)

def main(config: Dict[str, Any]):
    """Fetch and display hints for a LeetCode problem."""
    print_command_banner("Get Problem Hints")
    
    problem_num = styled_text_input("Enter problem number")
    
    print_info("Looking up problem...")
    problem_data = get_problem_by_id(problem_num)
    
    if not problem_data:
        print_error(f"Could not find problem with ID {problem_num}")
        return
        
    problem_name = problem_data["title"]
    slug = problem_data["slug"]
    
    print_success(f"Found: {problem_name}")
    print_info("Fetching hints...")
    
    details = get_problem_details(slug)
    
    if not details:
        print_error("Failed to fetch problem details from LeetCode.")
        return
        
    hints = details.get("hints", [])
    
    if not hints:
        print_warning("No official hints available for this problem.")
        return
        
    print_section(f"Hints for {problem_name} ({len(hints)} total)")
    
    for i, hint_html in enumerate(hints, 1):
        # Convert HTML hints to Markdown if markdownify is available, else strip tags basically
        if markdownify:
            try:
                hint_text = markdownify.markdownify(hint_html).strip()
            except Exception:
                hint_text = re.sub(r'<[^>]+>', '', hint_html).strip()
        else:
            hint_text = re.sub(r'<[^>]+>', '', hint_html).strip()
            
        console.print(f"  [bold cyan]Hint {i}:[/bold cyan] {hint_text}")
        
        if i < len(hints):
            console.print()
            user_input = input("  Press Enter for next hint (or 'q' to quit)... ")
            if user_input.strip().lower() == 'q':
                break
                
    console.print()
    print_success("Finished showing hints.")
