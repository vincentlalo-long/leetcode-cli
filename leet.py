import json
import os
import sys

from cli.commands import add_problem
from cli.commands import add_solution
from cli.commands import manage_structures
from cli.utils.config_manager import ConfigManager

def load_config():
    config_manager = ConfigManager()
    return config_manager.config

def main():
    config = load_config()

    if len(sys.argv) < 2:
        print("Usage: leet [add | add-sol | manage-structures]")
        return

    cmd = sys.argv[1]

    if cmd == "add":
        add_problem.main(config)
    elif cmd == "add-sol":
        add_solution.main(config)
    elif cmd == "manage-structures":
        manage_structures.main(config)
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()