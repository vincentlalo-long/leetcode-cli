import json
from typing import Any, Dict

from cli.utils.leetcode_api import get_problem_by_id, get_problem_details
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_info, print_warning,
    styled_text_input, print_section, console
)

def main(config: Dict[str, Any]):
    """Fetch and display similar problems for a LeetCode problem."""
    print_command_banner("Find Similar Problems")
    
    problem_num = styled_text_input("Enter problem number")
    
    print_info("Looking up problem...")
    problem_data = get_problem_by_id(problem_num)
    
    if not problem_data:
        print_error(f"Could not find problem with ID {problem_num}")
        return
        
    problem_name = problem_data["title"]
    slug = problem_data["slug"]
    
    print_success(f"Found: {problem_name}")
    print_info("Fetching similar problems...")
    
    details = get_problem_details(slug)
    
    if not details:
        print_error("Failed to fetch problem details from LeetCode.")
        return
        
    similar_json = details.get("similarQuestions")
    
    if not similar_json:
        print_warning("No similar problems available for this problem.")
        return
        
    try:
        similar_problems = json.loads(similar_json)
    except json.JSONDecodeError:
        print_error("Failed to parse similar problems data.")
        return
        
    if not similar_problems:
        print_warning("No similar problems found for this problem.")
        return
        
    print_section(f"Similar Problems to {problem_name} ({len(similar_problems)} total)")
    
    for i, prob in enumerate(similar_problems, 1):
        diff_color = {
            "Easy": "green",
            "Medium": "yellow",
            "Hard": "red"
        }.get(prob.get("difficulty"), "white")
        
        console.print(f"  [bold cyan]{i}.[/bold cyan] [white]{prob.get('title')}[/white] - [{diff_color}]{prob.get('difficulty')}[/{diff_color}] [dim](Slug: {prob.get('titleSlug')})[/dim]")
        
    console.print()
    print_success("Finished showing similar problems.")
