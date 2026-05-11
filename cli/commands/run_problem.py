import os
import subprocess
import tempfile
import platform
from typing import Any, Dict

from cli.utils.file_utils import get_all_cpp_files
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_info, print_warning,
    styled_text_input, console
)

def main(config: Dict[str, Any]):
    """Compile and run a C++ problem file locally."""
    print_command_banner("Run C++ Code")
    
    problem_num = styled_text_input("Enter problem number to run")
    base_dir = config.get("base_dir", "")
    
    if not base_dir or not os.path.isdir(base_dir):
        print_error(f"Invalid base directory in config: {base_dir}")
        return
        
    print_info("Searching for problem...")
    cpp_files = get_all_cpp_files(base_dir)
    
    target_file = None
    target_dir = None
    
    for f in cpp_files:
        basename = os.path.basename(f)
        if basename.startswith(f"{problem_num}_") or basename.startswith(f"{int(problem_num):03d}_") or basename.startswith(f"{int(problem_num):04d}_"):
            target_file = f
            target_dir = os.path.dirname(f)
            break
            
    if not target_file:
        print_error(f"Could not find local file for problem {problem_num}.")
        return
        
    print_success(f"Found problem: {os.path.basename(target_file)}")
    
    # Check if there is a main function
    with open(target_file, "r", encoding="utf-8") as rf:
        content = rf.read()
        if "int main" not in content and "void main" not in content:
            print_warning("No main() function detected in your code.")
            print_info("To run the code locally, please add a main() function to test your Solution class.")
            print_info("Example:\nint main() {\n    Solution sol;\n    // test here\n    return 0;\n}")
            # We still try to compile it to check for syntax errors
            print_info("We will attempt to compile it anyway to check for syntax errors.")
    
    # We will output the executable to a temporary directory so we don't clutter the workspace
    tmp_dir = tempfile.gettempdir()
    exe_name = f"leet_run_{problem_num}"
    if platform.system() == "Windows":
        exe_name += ".exe"
    exe_path = os.path.join(tmp_dir, exe_name)
    
    print_info("Compiling with g++ ...")
    
    compile_cmd = ["g++", "-std=c++17", "-O2", "-Wall", target_file, "-o", exe_path]
    
    try:
        # We capture output to check for warnings/errors
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
        print_error("g++ compiler not found.")
        print_info("Please install GCC (MinGW on Windows, build-essential on Linux/Mac) and add it to your PATH.")
        return
        
    print_info("Running executable...")
    console.print("\n[bold cyan]--- Output ---[/bold cyan]\n")
    
    try:
        # Run the executable, output goes directly to terminal
        subprocess.run([exe_path])
    except Exception as e:
        print_error(f"Execution failed: {e}")
    finally:
        console.print("\n[bold cyan]--------------[/bold cyan]\n")
        # Cleanup
        try:
            if os.path.exists(exe_path):
                os.remove(exe_path)
        except OSError:
            pass # Windows might still lock the file momentarily
