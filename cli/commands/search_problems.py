"""Search for problems by name or number"""
import os
import re
from typing import Any, Dict, List

from cli.utils.config_manager import ConfigManager
from cli.utils.file_utils import get_all_solution_files
from cli.utils.ui import (
    console,
    print_header,
    print_error,
    print_info,
    print_list_item,
    separator,
    styled_text_input,
)


def detect_structure(file_path: str, data_structures: Dict[str, str]) -> str:
    """Infer structure name from file path using configured folder names."""
    normalized_path = os.path.normpath(file_path).lower()

    for name, folder in data_structures.items():
        token = f"{os.sep}{folder}{os.sep}".lower()
        if token in normalized_path:
            return name

    return "unmatched"


def count_solutions(content: str) -> int:
    """Count number of solutions in file content"""
    pattern = r'\bSolution\s+\d+'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return len(matches)


def collect_all_problems(
    base_dir: str,
    data_structures: Dict[str, str],
    extensions: List[str] = None,
) -> List[Dict[str, Any]]:
    """Collect all problem files with detected structure and solution count."""
    if extensions is None:
        extensions = ["cpp"]
    files = get_all_solution_files(base_dir, extensions)
    records: List[Dict[str, Any]] = []

    for file_path in files:
        solutions = 0
        try:
            with open(file_path, "r", encoding="utf-8") as file_obj:
                solutions = count_solutions(file_obj.read())
        except OSError:
            pass

        records.append(
            {
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
                "structure": detect_structure(file_path, data_structures),
                "solutions": solutions,
            }
        )

    def sort_key(record: Dict[str, Any]):
        match = re.match(r"(\d+)", record["file_name"])
        problem_number = int(match.group(1)) if match else float("inf")
        return problem_number, record["file_name"].lower()

    return sorted(records, key=sort_key)


def search_problems(
    records: List[Dict[str, Any]],
    query: str,
) -> List[Dict[str, Any]]:
    """Search problems by name or number."""
    query_lower = query.lower().strip()
    results = []

    for record in records:
        file_name = record["file_name"].lower()
        
        # Try to extract problem number from filename
        match = re.match(r"(\d+)", file_name)
        problem_number = match.group(1) if match else ""

        # Search by problem number
        if problem_number and query_lower in problem_number:
            results.append(record)
        # Search by filename
        elif query_lower in file_name:
            results.append(record)

    return results


def display_results(results: List[Dict[str, Any]]) -> None:
    """Display search results in a formatted table."""
    if not results:
        print_error("No problems found matching your search.")
        return

    console.print(f"\n[bold cyan]Found {len(results)} problem(s):[/bold cyan]\n")

    for record in results:
        status = "✔ solved" if record["solutions"] > 0 else "✘ unsolved"
        status_color = "green" if record["solutions"] > 0 else "red"

        line = f"  [bold cyan]{record['file_name']:<40}[/bold cyan]"
        line += f" [{status_color}]{status}[/{status_color}]"
        line += f" [yellow]({record['structure']})[/yellow]"

        console.print(line)

    console.print()


def main(config: Dict[str, Any]) -> None:
    """Main function for search command"""
    print_header("🔍 Search Problems")

    base_dir = config.get("base_dir", ".")
    data_structures = config.get("data_structures", {})

    # Check if base_dir exists
    if not os.path.isdir(base_dir):
        print_error(f"Base directory not found: {base_dir}")
        return

    # Get search query from user
    query = styled_text_input("Enter problem name or number to search")

    if not query.strip():
        print_error("Search query cannot be empty.")
        return

    # Collect all problems
    print_info("Searching problems...")
    config_manager = ConfigManager()
    languages = config_manager.get_languages()
    extensions = [info["ext"] for info in languages.values()]
    all_problems = collect_all_problems(base_dir, data_structures, extensions)

    if not all_problems:
        print_error("No problems found in the base directory.")
        return

    # Perform search
    results = search_problems(all_problems, query)

    # Display results
    display_results(results)
