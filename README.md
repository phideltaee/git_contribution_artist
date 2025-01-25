# Git Contribution Artist

Git Contribution Artist is a Python tool designed to create custom “art” in your GitHub contribution history by manipulating commit dates and frequencies. This allows you to form patterns, words, or designs in your GitHub contributions graph.

# How it works
GitHub’s contributions graph is a 7×52 grid (7 rows × 52 weeks = ~1 year). Each cell in that grid corresponds to a specific day. By default, the color/“intensity” in each cell is determined by how many commits you made on that date.

This tool automates the process of creating empty commits with manually set commit dates. When pushed to GitHub, these backdated commits appear in your contribution graph, effectively “drawing” a pattern.

Important: If you already have an active history, adding more commits on specific days can “override” or heighten that day’s intensity, effectively painting over existing commits.

Contributions work on the basis of a `<less>` to `<more>` heatmap, thus, if you have a very active commit history already, you can always "paint over it" by having more commits on given days. 

### Use cases
1. Creative art ideas
2. Custom marketing on your git page (e.g., display a 7x42 QR codes)

### Not endorsed uses
1. Lying on your job search pretending to have more experience than you have. 
2. Pretending you are at work. 
3. Any other ethically-questionable use, at your discretion. 

## Workflow
- Prompts/reads user input (or command-line arguments) for the word/pattern, start date, etc.
- Pushes commits to GitHub
- Simplifies the commit and push workflow

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/phideltaee/git_contribution_artist.git
    ```
2. Navigate to the project directory:
    ```sh
    cd git_contribution_artist
    ```
3. Create a conda environment to manage dependencies
    ```sh
    conda env create -f config/environment.yml
    conda activate git_artist_env

4. Ensure you have the Github CLI (`gh`) installed and authenticated, so the script can create/view repos if needed:
    ```bash 
    gh auth login

## Usage

You have two main ways to use this tool:

1) Interactive Script
The easiest way for most users is via the interactive script, which prompts you step-by-step for each setting (like repo name, word, etc.), and shows a preview of the contribution art before committing.

1. Run the interactive script:

    ```bash
    python interactive_contribution_art.py

2. Answer the prompts:
    - Word or phrase (e.g., "HELLO")
    - Start date (in YYYY-MM-DD format)
    - GitHub repo name (e.g., username/repo_name)
    - Number of times you want the pattern repeated
    - Target directory where your new repository is created
    - Push to GitHub or not (yes/no)

3. Preview: You’ll see a 7-row ASCII map of your planned commits (█ = a day with commits, . = no commits).

4. Confirm: If you choose to proceed, the script creates (or cleans) a .git repo in your target directory and commits.

5. Enjoy: If you opted to push, your design will appear in your contributions graph on GitHub shortly.

## Cleaning Up Your Contribution Timeline - Deleting Repos

To cleanup the timeline, the only option is to delete the repo which "painted" it. At the moment, it's not possible to use the GH CLI to delete repos (and perhaps you shouldn't be able to!). You can follow these steps:
1. Go to github.com
2. Navigate to your arts repo (created by this script)
3. Go to settings -> Danger Zone (at the bottom) -> Delete this repository

Tip: make triple sure you are deleting the right repo!

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Create a new feature branch (git checkout -b feature/something).
3. Commit your changes.
4. Push your feature branch (git push origin feature/something).
5. Submit a Pull Request with a clear description of your changes.

## License

This project is licensed under the MIT License.


