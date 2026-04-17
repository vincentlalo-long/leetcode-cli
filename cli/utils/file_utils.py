import os
from typing import List

def get_all_cpp_files(base_dir: str) -> List[str]:
    """Get all .cpp files recursively from base directory"""
    files = []
    for root, _, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith(".cpp"):
                files.append(os.path.join(root, filename))
    return sorted(files)

def create_problem_directory(base_dir: str, ds_folder: str, problem_num: str) -> str:
    """Create problem directory and return the path"""
    problem_dir = os.path.join(base_dir, ds_folder, problem_num)
    os.makedirs(problem_dir, exist_ok=True)
    return problem_dir

def count_solutions(content: str) -> int:
    """Count number of solutions in file content"""
    return content.count("Solution")
