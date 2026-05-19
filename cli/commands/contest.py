from typing import Any, Dict
from datetime import datetime

from cli.utils.leetcode_api import get_upcoming_contests
from cli.utils.ui import (
    print_command_banner, print_error, print_info, print_section, console
)

def main(config: Dict[str, Any]):
    """Fetch and display upcoming LeetCode contests"""
    print_command_banner("Upcoming LeetCode Contests")
    
    print_info("Fetching contest information...")
    contests = get_upcoming_contests()
    
    if not contests:
        print_error("Could not fetch contest information. Please check your connection.")
        return
        
    print_section("Upcoming Contests")
    
    for contest in contests:
        title = contest.get("title")
        slug = contest.get("titleSlug")
        start_time_unix = contest.get("startTime", 0)
        duration_sec = contest.get("duration", 0)
        
        start_time = datetime.fromtimestamp(start_time_unix)
        duration_hrs = duration_sec / 3600
        
        link = f"https://leetcode.com/contest/{slug}/"
        
        console.print(f"  [bold white]{title}[/bold white]")
        console.print(f"  [dim]Start Time:[/dim] [bold]{start_time.strftime('%Y-%m-%d %H:%M:%S')}[/bold]")
        console.print(f"  [dim]Duration:[/dim]   {duration_hrs} hours")
        console.print(f"  [dim]Link:[/dim]       [blue]{link}[/blue]")
        console.print()
