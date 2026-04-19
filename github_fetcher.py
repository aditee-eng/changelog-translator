import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_commits_between_tags(owner: str, repo: str, base_tag: str, head_tag: str) -> list:
    """
    Fetch all commits between two version tags.
    owner: e.g. "facebook"
    repo:  e.g. "react"
    base_tag: e.g. "v18.0.0"
    head_tag: e.g. "v18.1.0"
    """

    # Step 1: compare the two tags
    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{base_tag}...{head_tag}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error: {response.status_code} — {response.json().get('message')}")
        return []

    data = response.json()
    commits = data.get("commits", [])

    # Step 2: extract what matters from each commit
    cleaned = []
    for c in commits:
        cleaned.append({
            "message": c["commit"]["message"].split("\n")[0],  # first line only
            "author": c["commit"]["author"]["name"],
            "date": c["commit"]["author"]["date"],
            "sha": c["sha"][:7]  # short hash
        })

    return cleaned


if __name__ == "__main__":
    # Test with a real public repo
    commits = get_commits_between_tags(
        owner="expressjs",
        repo="express",
        base_tag="4.18.1",
        head_tag="4.18.2"
    )

    print(f"Found {len(commits)} commits:\n")
    for c in commits:
        print(f"[{c['sha']}] {c['author']}: {c['message']}")