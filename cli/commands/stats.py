import os
from typing import Dict, Any

from cli.utils.file_utils import count_solutions, get_all_cpp_files
from cli.utils.ui import (
    print_command_banner,
    print_error,
    print_info,
    print_list_item,
    print_section,
    print_warning,
    console,
)


def collect_stats(base_dir: str, data_structures: Dict[str, str]) -> Dict[str, Any]:
    files = get_all_cpp_files(base_dir)

    by_structure = {name: 0 for name in data_structures}
    unmatched_problems = 0
    total_solutions = 0

    structure_tokens = {
        name: f"{os.sep}{folder}{os.sep}"
        for name, folder in data_structures.items()
    }

    for file_path in files:
        normalized_path = os.path.normpath(file_path)
        normalized_lower = normalized_path.lower()

        matched = False
        for name, token in structure_tokens.items():
            if token.lower() in normalized_lower:
                by_structure[name] += 1
                matched = True
                break

        if not matched:
            unmatched_problems += 1

        try:
            with open(file_path, "r", encoding="utf-8") as file_obj:
                total_solutions += count_solutions(file_obj.read())
        except OSError:
            continue

    return {
        "total_problems": len(files),
        "total_solutions": total_solutions,
        "by_structure": by_structure,
        "unmatched_problems": unmatched_problems,
    }


def main(config: Dict[str, Any]):
    print_command_banner("Problem Statistics")

    base_dir = config.get("base_dir", "")
    data_structures = config.get("data_structures", {})

    if not base_dir:
        print_error("Missing 'base_dir' in config")
        return

    if not os.path.isdir(base_dir):
        print_warning(f"Base directory does not exist: {base_dir}")
        return

    stats = collect_stats(base_dir, data_structures)

    print_section("Overview")
    print_list_item("Base directory", base_dir)
    print_list_item("Total problems", str(stats["total_problems"]))
    print_list_item("Total solutions", str(stats["total_solutions"]))
    console.print()

    print_section("By Data Structure")
    if not data_structures:
        print_info("No data structures configured")
    else:
        for name in sorted(data_structures.keys()):
            print_list_item(name, str(stats["by_structure"].get(name, 0)))

    if stats["unmatched_problems"] > 0:
        console.print()
        print_info(
            f"Unmatched problems: {stats['unmatched_problems']}"
        )
    console.print()