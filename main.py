"""Tidy up a messy folder by sorting its files into subfolders by type.

    python main.py ~/Downloads             # show the plan, then ask before moving
    python main.py ~/Downloads --dry-run   # only show the plan
    python main.py ~/Downloads --yes       # move without asking
    python main.py ~/Downloads --undo      # put everything from the last run back
"""
import argparse
from collections import defaultdict
from pathlib import Path

import organizer


def show_plan(folder, moves):
    groups = defaultdict(list)
    for source, destination in moves:
        groups[destination.parent.name].append((source.name, destination.name))
    print(f"Found {len(moves)} files to organise in {folder}\n")
    for group in sorted(groups):
        print(f"{group}/ ({len(groups[group])})")
        for old, new in groups[group]:
            print(f"  {old}" + (f"  ->  {new} (renamed, name already taken)" if new != old else ""))
    print()


def main():
    parser = argparse.ArgumentParser(description="Sort the files in a folder into subfolders by type.")
    parser.add_argument("folder", nargs="?", help="folder to organise (asked for if left out)")
    parser.add_argument("--dry-run", action="store_true", help="only show what would be moved")
    parser.add_argument("--yes", "-y", action="store_true", help="don't ask for confirmation")
    parser.add_argument("--undo", action="store_true", help="reverse the last run in this folder")
    args = parser.parse_args()

    folder = Path(args.folder or input("Folder to organise: ").strip().strip('"')).expanduser()
    if not folder.is_dir():
        print(f"{folder} is not a folder.")
        return

    if args.undo:
        try:
            print(f"Restored {organizer.undo(folder)} files.")
        except FileNotFoundError as e:
            print(e)
        return

    moves = organizer.plan(folder)
    if not moves:
        print("Nothing to organise.")
        return
    show_plan(folder, moves)
    if args.dry_run:
        return
    if not args.yes and input(f"Move {len(moves)} files? (y/n): ").strip().lower() != "y":
        print("Nothing was moved.")
        return

    count = organizer.apply(folder, moves)
    print(f"Moved {count} files. Run again with --undo to put them back.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
