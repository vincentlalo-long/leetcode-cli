import argparse
import sys
from cli.utils.leetcode_api import get_user_profile
from cli.utils.ui import console, print_error, print_info, print_command_banner, print_section

def main(config):
    parser = argparse.ArgumentParser(description="Fetch and display a LeetCode user profile")
    parser.add_argument("username", help="LeetCode username")
    
    try:
        args = parser.parse_args(sys.argv[1:])
    except SystemExit:
        return

    username = args.username
    
    print_command_banner("LeetCode User Profile")

    with console.status(f"[bold green]Fetching profile for {username}...", spinner="dots"):
        profile_data = get_user_profile(username)
        
    if not profile_data:
        print_error(f"User '{username}' not found or an error occurred.")
        return
        
    stats = profile_data.get("submitStats", {}).get("acSubmissionNum", [])
    profile_info = profile_data.get("profile", {})
    
    # Extract counts
    counts = {stat["difficulty"]: stat["count"] for stat in stats}
    all_count = counts.get("All", 0)
    easy_count = counts.get("Easy", 0)
    medium_count = counts.get("Medium", 0)
    hard_count = counts.get("Hard", 0)
    
    # Extract profile info
    ranking = profile_info.get("ranking", "N/A")
    reputation = profile_info.get("reputation", 0)
    
    # Formatting the output
    print_section(f"👤 Profile for {username}")
    console.print(f"  [bold]Ranking:[/bold]    {ranking}")
    console.print(f"  [bold]Reputation:[/bold] {reputation}")
    console.print()
    print_section("📊 Solved Problems")
    console.print(f"  [bold]Total:[/bold]  {all_count}")
    console.print(f"  [green]Easy:[/green]   {easy_count}")
    console.print(f"  [yellow]Medium:[/yellow] {medium_count}")
    console.print(f"  [red]Hard:[/red]   {hard_count}")
    print()
