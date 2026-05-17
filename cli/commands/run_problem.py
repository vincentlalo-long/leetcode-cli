import os
import subprocess
import tempfile
import platform
import sys
from typing import Any, Dict

from cli.utils.config_manager import ConfigManager
from cli.utils.file_utils import get_all_solution_files
from cli.utils.language_support import get_language_by_extension
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_info, print_warning,
    styled_text_input, console
)

def _matches_problem_number(filename: str, problem_num: str) -> bool:
    if filename.startswith(f"{problem_num}_"):
        return True
    if problem_num.isdigit():
        num = int(problem_num)
        return filename.startswith(f"{num:03d}_") or filename.startswith(f"{num:04d}_")
    return False


def main(config: Dict[str, Any]):
    """Compile and run a problem file locally."""
    print_command_banner("Run Code")
    
    problem_num = styled_text_input("Enter problem number to run")
    base_dir = config.get("base_dir", "")
    
    if not base_dir or not os.path.isdir(base_dir):
        print_error(f"Invalid base directory in config: {base_dir}")
        return
        
    print_info("Searching for problem...")
    config_manager = ConfigManager()
    normalized_languages = config_manager.get_languages()
    extensions = [info["ext"] for info in normalized_languages.values()]
    all_files = get_all_solution_files(base_dir, extensions)

    matches = []
    for file_path in all_files:
        basename = os.path.basename(file_path)
        if _matches_problem_number(basename, problem_num):
            matches.append(file_path)

    target_file = None
    target_dir = None
            
    if not matches:
        print_error(f"Could not find local file for problem {problem_num}.")
        return

    if len(matches) == 1:
        target_file = matches[0]
    else:
        choices = [os.path.basename(path) for path in matches]
        selected = styled_select("Multiple matches found. Select file to run", choices)
        target_file = matches[choices.index(selected)]

    target_dir = os.path.dirname(target_file)

    print_success(f"Found problem: {os.path.basename(target_file)}")
    
    # Check if there is a main function
    _, ext = os.path.splitext(target_file)
    language_key = get_language_by_extension(normalized_languages, ext)
    if not language_key:
        print_error("Unsupported file extension for running.")
        return

    if language_key in ["cpp", "c"]:
        with open(target_file, "r", encoding="utf-8") as rf:
            content = rf.read()
            if "main(" not in content:
                print_warning("No main() function detected in your code.")
                print_info("To run the code locally, please add a main() function to test your Solution class.")
                print_info("Example:\nint main() {\n    // test here\n    return 0;\n}")
                print_info("We will attempt to compile it anyway to check for syntax errors.")
    
    # We will output the executable to a temporary directory so we don't clutter the workspace
    tmp_dir = tempfile.gettempdir()
    exe_name = f"leet_run_{problem_num}"
    if platform.system() == "Windows":
        exe_name += ".exe"
    exe_path = os.path.join(tmp_dir, exe_name)
    
    if language_key in ["cpp", "c"]:
        compiler = "g++" if language_key == "cpp" else "gcc"
        std_flag = "-std=c++17" if language_key == "cpp" else "-std=c11"
        print_info(f"Compiling with {compiler} ...")
        compile_cmd = [compiler, std_flag, "-O2", "-Wall", target_file, "-o", exe_path]
    
    if language_key in ["cpp", "c"]:
        try:
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)

            if compile_result.returncode != 0:
                print_error("Compilation failed!")
                console.print(f"[red]{compile_result.stderr}[/red]")
                return

            if compile_result.stderr:
                print_warning("Compiled with warnings:")
                console.print(f"[yellow]{compile_result.stderr}[/yellow]")
            else:
                print_success("Compiled successfully.")

        except FileNotFoundError:
            print_error(f"{compiler} compiler not found.")
            print_info("Please install GCC (MinGW on Windows, build-essential on Linux/Mac) and add it to your PATH.")
            return

        print_info("Running executable...")
        console.print("\n[bold cyan]--- Output ---[/bold cyan]\n")

        try:
            subprocess.run([exe_path])
        except Exception as e:
            print_error(f"Execution failed: {e}")
        finally:
            console.print("\n[bold cyan]--------------[/bold cyan]\n")
            try:
                if os.path.exists(exe_path):
                    os.remove(exe_path)
            except OSError:
                pass
        return

    print_info("Running script...")
    console.print("\n[bold cyan]--- Output ---[/bold cyan]\n")

    try:
        if language_key == "python":
            subprocess.run([sys.executable, target_file])
        elif language_key == "go":
            subprocess.run(["go", "run", target_file])
        else:
            print_error(f"Running '{language_key}' files is not supported yet.")
            return
    except FileNotFoundError as e:
        print_error(f"Execution failed: {e}")
    finally:
        console.print("\n[bold cyan]--------------[/bold cyan]\n")
