import os
import subprocess
import platform
import shutil
from typing import Any, Dict

from cli.utils.file_utils import get_all_cpp_files
from cli.utils.config_manager import ConfigManager
from cli.utils.ui import (
    print_command_banner, print_success, print_error, print_info, print_warning,
    styled_text_input, styled_confirm, styled_select, console
)

def main(config: Dict[str, Any]):
    """Open a problem in the configured editor and display its description."""
    print_command_banner("Open Problem")
    
    problem_num = styled_text_input("Enter problem number to open")
    base_dir = config.get("base_dir", "")
    
    if not base_dir or not os.path.isdir(base_dir):
        print_error(f"Invalid base directory in config: {base_dir}")
        return
        
    print_info("Searching for problem...")
    cpp_files = get_all_cpp_files(base_dir)
    
    target_file = None
    target_dir = None
    
    # We look for a file starting with '{problem_num}_' or having '{problem_num}' in the filename
    for f in cpp_files:
        basename = os.path.basename(f)
        if basename.startswith(f"{problem_num}_") or basename.startswith(f"{int(problem_num):03d}_") or basename.startswith(f"{int(problem_num):04d}_"):
            target_file = f
            target_dir = os.path.dirname(f)
            break
            
    if not target_file:
        print_error(f"Could not find local file for problem {problem_num}.")
        print_info("Try running 'leet add' or 'leet daily' first.")
        return
        
    print_success(f"Found problem: {os.path.basename(target_file)}")
    
    # Print the description if README.md exists
    readme_path = os.path.join(target_dir, "README.md")
    if os.path.exists(readme_path):
        console.print("\n[bold cyan]--- Problem Description ---[/bold cyan]\n")
        with open(readme_path, "r", encoding="utf-8") as rf:
            from rich.markdown import Markdown
            md = Markdown(rf.read())
            console.print(md)
        console.print("\n[bold cyan]---------------------------[/bold cyan]\n")
    else:
        print_warning("No README.md found for this problem.")
        
    config_manager = ConfigManager()
    editor = config_manager.get_editor()
    
    # Check for split layout support
    has_wt = platform.system() == "Windows" and shutil.which("wt") is not None
    has_tmux = platform.system() != "Windows" and shutil.which("tmux") is not None
    
    if (has_wt or has_tmux) and styled_confirm("Open in split-terminal layout? (Left: Editor, Right: Tests & Terminal)", default=True):
        if editor.lower() == "code":
            print_warning("VS Code ('code') opens a separate GUI. For split-terminal, 'nvim', 'vim', or 'nano' is recommended.")
            
        # On Windows, we can choose the shell for the panes
        shell_cmd = "powershell"
        if platform.system() == "Windows":
            shell_choices = ["PowerShell", "Git Bash (bash)", "Ubuntu (wsl)"]
            selected_shell = styled_select("Select shell for the split panes", shell_choices)
            if "wsl" in selected_shell.lower():
                shell_cmd = "wsl"
                if editor.lower() in ["code", "nvim", "vim", "nano"]:
                    editor = f"wsl {editor}" # Use wsl version of the editor
            elif "bash" in selected_shell.lower():
                shell_cmd = "bash"
                
        # Ask for editor if it's still default or if user wants to change
        if editor.lower() == "code" or styled_confirm(f"Use '{editor}' as editor?", default=True) is False:
            editor = styled_text_input("Enter CLI editor to use (e.g., nvim, wsl nvim)", default="nvim")
            
        read_cmd = ""
        if os.path.exists(readme_path):
            if shell_cmd == "powershell":
                read_cmd = f"type README.md ; "
            else:
                read_cmd = f"cat README.md ; "
                
        target_basename = os.path.basename(target_file)
        
        if has_tmux:
            # (tmux logic remains same)
            print_info(f"Launching Tmux split layout with {editor}...")
            try:
                if os.environ.get("TMUX"):
                    subprocess.run(["tmux", "split-window", "-h", "-c", target_dir, f"{read_cmd} echo ''; echo '--- READY ---'; exec bash"])
                    subprocess.run(["tmux", "split-window", "-v", "-c", target_dir, "bash"])
                    subprocess.run(["tmux", "select-pane", "-L"])
                    os.execlp(editor, editor, target_file)
                else:
                    session_name = f"leet_{problem_num}"
                    subprocess.run(["tmux", "new-session", "-d", "-s", session_name, "-c", target_dir, f"{editor} '{target_basename}'"])
                    subprocess.run(["tmux", "split-window", "-h", "-t", session_name, "-c", target_dir, f"{read_cmd} echo ''; echo '--- READY ---'; exec bash"])
                    subprocess.run(["tmux", "split-window", "-v", "-t", session_name, "-c", target_dir, "bash"])
                    os.execlp("tmux", "tmux", "attach", "-t", session_name)
            except Exception as e:
                print_error(f"Failed to launch Tmux: {e}")
        elif has_wt:
            print_info(f"Launching Windows Terminal split layout ({shell_cmd}) with {editor}...")
            
            # For Windows Terminal, if using wsl, we need to handle paths carefully
            # but wt -d . wsl works fine as it starts in the directory.
            
            wt_args = [
                "wt", "-d", target_dir, "powershell", "-Command", f"{editor} {target_basename}",
                ";", "split-pane", "-V", "-d", target_dir, shell_cmd, "-Command" if shell_cmd == "powershell" else "-c",
                f"{read_cmd} echo ''; echo '--- READY ---'; {'pause' if shell_cmd == 'powershell' else 'exec bash'}",
                ";", "split-pane", "-H", "-d", target_dir, shell_cmd
            ]
            
            try:
                subprocess.Popen(wt_args)
                print_success("Split terminal launched successfully!")
            except Exception as e:
                print_error(f"Failed to launch Windows Terminal: {e}")
            
    else:
        print_info(f"Opening with {editor}...")
        try:
            if platform.system() == "Windows":
                subprocess.Popen([editor, target_file], shell=True)
            else:
                subprocess.Popen([editor, target_file])
            print_success("Problem opened in editor!")
        except Exception as e:
            print_error(f"Failed to open editor '{editor}': {e}")
            print_info(f"You can change your editor in config.json or manually open: {target_file}")
