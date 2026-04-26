import os
import re
from typing import Any, Dict, List

from cli.utils.file_utils import count_solutions, get_all_cpp_files
from cli.utils.ui import (
    console,
    print_command_banner,
    print_error,
    print_info,
    print_list_item,
    print_section,
    print_warning,
    styled_confirm,
    styled_select,
)


def detect_structure(file_path: str, data_structures: Dict[str, str]) -> str:
    """Infer structure name from file path using configured folder names."""
    normalized_path = os.path.normpath(file_path).lower()

    for name, folder in data_structures.items():
        token = f"{os.sep}{folder}{os.sep}".lower()
        if token in normalized_path:
            return name

    return "unmatched"


def collect_problems(base_dir: str, data_structures: Dict[str, str]) -> List[Dict[str, Any]]:
    """Collect all problem files with detected structure and solution count."""
    files = get_all_cpp_files(base_dir)
    records: List[Dict[str, Any]] = []

    for file_path in files:
        solutions = 0
        try:
            with open(file_path, "r", encoding="utf-8") as file_obj:
                solutions = count_solutions(file_obj.read())
        except OSError:
            # Keep the file in listing even if it cannot be read.
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


def filter_problems(
    records: List[Dict[str, Any]],
    selected_structure: str,
    unsolved_only: bool,
) -> List[Dict[str, Any]]:
    """Filter by structure and solved state."""
    filtered: List[Dict[str, Any]] = []

    for record in records:
        if selected_structure != "All" and record["structure"] != selected_structure:
            continue

        if unsolved_only and record["solutions"] > 0:
            continue

        filtered.append(record)

    return filtered


def main(config: Dict[str, Any]):
    print_command_banner("List Problems")

    base_dir = config.get("base_dir", "")
    data_structures = config.get("data_structures", {})

    if not base_dir:
        print_error("Missing 'base_dir' in config")
        return

    if not os.path.isdir(base_dir):
        print_warning(f"Base directory does not exist: {base_dir}")
        return

    records = collect_problems(base_dir, data_structures)

    if not records:
        print_info("No problem files found")
        return

    available_structures = sorted({record["structure"] for record in records})
    selected_structure = styled_select(
        "Filter by data structure",
        ["All"] + available_structures,
    )
    unsolved_only = styled_confirm("Show only unsolved problems?", default=False)

    filtered = filter_problems(records, selected_structure, unsolved_only)

    print_section("Overview")
    print_list_item("Total problems", str(len(records)))
    print_list_item("After filters", str(len(filtered)))
    if selected_structure != "All":
        print_list_item("Structure", selected_structure)
    print_list_item("Mode", "Unsolved only" if unsolved_only else "All")
    console.print()

    if not filtered:
        print_info("No problems match selected filters")
        return

    print_section("Problems")
    for index, record in enumerate(filtered, start=1):
        status = "unsolved" if record["solutions"] == 0 else f"{record['solutions']} solution(s)"
        console.print(
            f"  [cyan]{index:>2}.[/cyan] [white]{record['file_name']}[/white] [dim]({record['structure']}, {status})[/dim]"
        )
        console.print(f"      [dim]{record['file_path']}[/dim]")

    console.print()
