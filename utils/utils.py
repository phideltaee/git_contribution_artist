"""
Utility functions for the git-contribution-artist tool. 
Author: phideltaee
"""

import subprocess
from datetime import datetime, timedelta
import os
import shutil

def cleanup_git_repository():
    """
    Completely removes the existing Git repository in the current directory, 
    and reinitializes it as a new Git repository.
    """
    # Path to the .git directory
    git_dir = ".git"
    
    # Step 1: Remove the .git directory if it exists
    if os.path.isdir(git_dir):
        shutil.rmtree(git_dir)
        print("Removed existing .git directory and all Git history.")
    else:
        print("No existing .git directory found.")

    # Example usage
    # cleanup_git_repository()

def fill_contributions_calendar(start_date_str, end_date_str):
    """
    Fills every date between the start and end dates with an empty commit.
    
    Parameters:
    - start_date_str (str): Start date in 'YYYY-MM-DD' format.
    - end_date_str (str): End date in 'YYYY-MM-DD' format.

    """
    # Parse start and end dates
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Check if start date is before end date
    if start_date > end_date:
        print("Start date must be before end date.")
        return
    
    # Iterate over each date in the range
    current_date = start_date
    while current_date <= end_date:
        # Format date as required by git commit
        formatted_date = current_date.strftime("%a %b %d %H:%M:%S %Y %z")
        
        # Make an empty commit for the current date
        subprocess.run([
            "git", "commit", "--allow-empty",
            "--date", formatted_date,
            "-m", f"Commit for {current_date.strftime('%Y-%m-%d')}"
        ])
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    # Push all commits to GitHub
    subprocess.run(["git", "push", "origin", "main"])
    print(f"Filled contributions calendar from {start_date_str} to {end_date_str}.")

    # Example usage
    # fill_contributions_calendar("2023-10-29", "2024-11-02")
        
def initialize_and_set_upstream(repo_name):
    """
    Initializes a git repository in the current directory if it doesn't exist,
    checks if the repository exists on GitHub, creates it if necessary,
    sets the remote to origin (if not already set), and pushes the initial commit to GitHub.

    Parameters:
    - repo_name (str): The name of the repository to create and push (in format 'username/repo_name').
    """
    # Check if there's already a Git repository initialized
    if not os.path.isdir(".git"):
        subprocess.run(["git", "init", "-b", "main"])
        print("Initialized a new git repository with 'main' as the default branch.")
    else:
        print("Git repository already initialized.")

    # Check if the GitHub repository already exists
    repo_exists = subprocess.run(
        ["gh", "repo", "view", repo_name],
        capture_output=True,
        text=True
    )

    if repo_exists.returncode == 0:
        print(f"Repository '{repo_name}' already exists on GitHub.")
    else:
        # Attempt to create the repository on GitHub
        result = subprocess.run(
            ["gh", "repo", "create", repo_name, "--private", "--confirm"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("Failed to create the GitHub repository.")
            print(result.stderr)
            return  # Exit if repo creation fails
        print(f"Created GitHub repository '{repo_name}'.")

    # Check if the remote 'origin' is already set, and only add it if it doesn't exist
    remote_check = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    if remote_check.returncode != 0:  # If 'origin' doesn't exist
        # Set the SSH URL for the GitHub repository
        remote_url = f"git@github.com:{repo_name}.git"
        subprocess.run(["git", "remote", "add", "origin", remote_url])
        print(f"Remote 'origin' set to {remote_url}.")
    else:
        print("Remote 'origin' already exists.")

    # Verify remote access
    remote_verify = subprocess.run(["git", "ls-remote", "origin"], capture_output=True, text=True)
    if remote_verify.returncode != 0:
        print("ERROR: Could not access the remote repository. Please check your access rights.")
        print(remote_verify.stderr)
        return  # Exit if remote verification fails

    # Check if there are any commits; if not, make an initial commit
    commit_check = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    if commit_check.returncode != 0:
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Initial commit"])
        print("Created an initial commit.")
    else:
        print("Initial commit already exists.")

    # Push to GitHub and set the upstream branch to origin/main
    push_result = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
    if push_result.returncode == 0:
        print("Pushed to GitHub and set upstream to origin/main.")
    else:
        # Handle the case if the branch is already pushed and upstream is set
        if "up to date" in push_result.stderr:
            print("Branch is already up to date on GitHub.")
        else:
            print("Failed to push to GitHub. Please check your remote access rights and repository existence.")
            print(push_result.stderr)

    # Example usage
    # initialize_and_set_upstream("your_username/your_repo_name")


