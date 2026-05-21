import os
import subprocess
from datetime import datetime

from cli.utils.ui import print_command_banner, print_success, print_error, print_info, console

def run_command(command, cwd=None):
    """Run a shell command and return its success status and output"""
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=True, 
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main(config: dict):
    """Sync LeetCode workspace with remote git repository"""
    print_command_banner("Sync LeetCode Workspace")
    
    base_dir = config.get("base_dir")
    
    if not base_dir or not os.path.exists(base_dir):
        print_error(f"Base directory '{base_dir}' does not exist.")
        return
        
    # Check if base_dir is a git repository
    is_git, _, _ = run_command("git rev-parse --is-inside-work-tree", cwd=base_dir)
    if not is_git:
        print_error(f"'{base_dir}' is not a Git repository.")
        print_info("Please initialize git and set up a remote repository first:")
        print_info(f"  cd {base_dir}")
        print_info("  git init")
        print_info("  git remote add origin <your-repo-url>")
        return
        
    print_info(f"Syncing workspace: {base_dir}")
    console.print()
    
    # 1. Add all changes
    print_info("Staging changes...")
    success, out, err = run_command("git add .", cwd=base_dir)
    if not success:
        print_error("Failed to stage changes.")
        if err: console.print(err)
        return
        
    # Check if there are changes to commit
    has_changes, out, _ = run_command("git status --porcelain", cwd=base_dir)
    if not out.strip():
        print_info("No changes to sync. Workspace is up to date.")
        return
        
    # 2. Commit changes
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"LeetCode Sync: {timestamp}"
    print_info(f"Committing changes...")
    
    success, out, err = run_command(f'git commit -m "{commit_msg}"', cwd=base_dir)
    if not success:
        print_error("Failed to commit changes.")
        if err: console.print(err)
        return
        
    # 3. Pull latest changes (optional, but good practice)
    print_info("Pulling latest changes from remote (if any)...")
    run_command("git pull --rebase", cwd=base_dir) # Don't fail if pull fails (might not have tracking branch)
        
    # 4. Push changes
    print_info("Pushing to remote...")
    success, out, err = run_command("git push", cwd=base_dir)
    if not success:
        print_error("Failed to push changes.")
        print_info("You might need to set upstream branch manually the first time:")
        print_info("  cd " + base_dir)
        print_info("  git push -u origin main")
        if err: console.print(err)
        return
        
    console.print()
    print_success("Successfully synced LeetCode workspace!")
