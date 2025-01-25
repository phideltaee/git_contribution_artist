#!/usr/bin/env python3

"""
Create custom art using your git history commits! 
Author: phideltaee
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta

# Import your existing utilities
from utils.utils import cleanup_git_repository, initialize_and_set_upstream
from utils.characters import characters

def interactive_input(prompt, default=None, required=False, cast_type=str):
    """
    Prompt the user for input.
    - If `default` is provided, show it in parentheses.
    - If the user hits Enter with no input, return the `default`.
    - If `required` is True, re-prompt until something is entered.
    - Use `cast_type` to cast the result (e.g. int, str).
    """
    while True:
        if default is not None:
            user_input = input(f"{prompt} (leave blank for '{default}'): ").strip()
        else:
            user_input = input(f"{prompt}: ").strip()
        
        # If no input given, use default (if there is one)
        if not user_input and default is not None:
            return cast_type(default)
        
        # If required but user_input is empty and no default
        if not user_input and required:
            print("This value is required. Please try again.")
            continue
        
        # If user_input is non-empty, cast it if needed
        if user_input:
            try:
                return cast_type(user_input)
            except ValueError:
                print(f"Invalid input. Expected type: {cast_type.__name__}. Please try again.")
                continue
        
        # If we get here, it means user_input is empty, but not required
        return None

def make_commit(commit_date, message):
    """
    Create an empty commit for a specific date with a given message.
    """
    formatted_date = commit_date.strftime("%a %b %d %H:%M:%S %Y %z")
    subprocess.run(
        ["git", "commit", "--allow-empty", "--date", formatted_date, "-m", message],
        check=True
    )

def build_heatmap_grid(word):
    """
    Build a 7-row "heatmap" (ASCII-based) for the word (including a leading '*').
    Each character is 5 columns wide + 1 column spacing => 6 columns total.
    
    Returns: A 2D list of '0' and '1' (strings), 7 rows × total columns needed.
    """
    full_word = f"{word}"
    
    # For each character, we have 5 columns + 1 spacing => 6 columns
    total_chars = len(full_word)
    total_columns = 6 * total_chars
    rows = 7
    
    # Initialize grid with '0'
    grid = [["0" for _ in range(total_columns)] for _ in range(rows)]
    
    # Fill in '1' where needed
    current_col_offset = 0
    for letter in full_word:
        char_grid = characters[letter]  # 7 x 5 matrix
        for r in range(rows):
            for c in range(5):
                if char_grid[r][c] == "1":
                    grid[r][current_col_offset + c] = "1"
        current_col_offset += 6  # 5 used + 1 spacing

    return grid

def print_heatmap(grid):
    """
    Print the 7-row heatmap using '█' for '1' and '.' for '0'.
    """
    for row in grid:
        line = "".join("█" if cell == "1" else "." for cell in row)
        print(line)

def show_progress_bar(iteration, total, length=50, prefix='Progress', suffix=''):
    """
    Simple console-based progress bar.
    `iteration`: current step (1-based)
    `total`: total steps
    """
    # Ensure iteration doesn't exceed total
    iteration = min(iteration, total)
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    percent = (iteration / total) * 100
    sys.stdout.write(f"\r{prefix} |{bar}| {percent:5.1f}% {suffix}")
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')  # Newline on completion

def main():
    print("=== Interactive Git Contribution Art ===\n")
    
    # 1) Gather parameters interactively
    word = interactive_input("1) Word or phrase to 'paint'", default="UpCircle.ai")
    start_date_str = interactive_input("2) Start date (YYYY-MM-DD)", default="2024-01-01")
    repeat_count = interactive_input("3) Number of times to repeat pattern", default="3", cast_type=int)
    repo_name = interactive_input("4) GitHub repo name", default=f"git_artist_paintword_{word}")
    target_dir = interactive_input("5) Target directory for the new repo", default="../git_artist_repo_v1")
    
    # For push, let's do a simple yes/no prompt
    push_input = interactive_input("6) Push commits to remote? (yes/no)", default="no")
    push = push_input.lower().startswith('y')
    

    # 2) Convert/validate the start date
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Invalid date format: '{start_date_str}'. Aborting.")
        return
    
    # Adjust to next Sunday if not already Sunday
    if start_date.weekday() != 6:  # 6 = Sunday
        start_date += timedelta(days=(6 - start_date.weekday()))
    
    # 3) Build and display a preview heatmap
    print("\n=== Preview of your contribution pattern ===")
    preview_grid = build_heatmap_grid(word)
    print_heatmap(preview_grid)
    
    # Show summary
    print(f"\nRepo Name: {repo_name}")
    print(f"Start Date (adjusted to Sunday if needed): {start_date.strftime('%Y-%m-%d')}")
    print(f"Word/Phrase: {word}")
    print(f"Repeat Count: {repeat_count}")
    print(f"Push to remote: {push}")
    print(f"Target Directory: {target_dir}\n")
    
    # 4) Ask user to proceed or cancel
    proceed_input = interactive_input("Proceed with commit creation? (yes/no)", default="no")
    if not proceed_input.lower().startswith('y'):
        print("Cancelled. No commits were made.")
        return
    
    # 5) Create/move to the target directory
    os.makedirs(target_dir, exist_ok=True)
    os.chdir(target_dir)
    
    # 6) Create/clean the repo in the target directory
    cleanup_git_repository()
    initialize_and_set_upstream(repo_name)
    
    # 7) Make commits with a progress bar
    print("\nCreating commits...")
    # Count total commits for progress bar
    commits_per_cycle = sum(cell == "1" for row in preview_grid for cell in row)
    total_commits = commits_per_cycle * repeat_count
    
    iteration = 0
    letters = word 
    for _ in range(repeat_count):
        current_week = 0
        for letter in letters:
            char_grid = characters[letter]  # 7 x 5
            for day in range(7):
                for week_offset in range(5):
                    if char_grid[day][week_offset] == "1":
                        commit_date = start_date + timedelta(weeks=current_week + week_offset, days=day)
                        make_commit(commit_date, f"Commit for {letter} at ({day}, {week_offset})")
                        iteration += 1
                        show_progress_bar(iteration, total_commits, prefix='Creating')
            current_week += 6  # spacing after each character

    # 8) Optionally push
    if push:
        print("\nPushing commits to remote...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print(f"Pattern '{word}' created and pushed to GitHub.")
    else:
        print(f"\nPattern '{word}' created locally (not pushed).")

if __name__ == "__main__":
    main()
