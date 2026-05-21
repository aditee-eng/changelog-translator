import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_commits_between_tags(owner: str, repo: str, base_tag: str, head_tag: str) -> list:
    
    # moved inside function so token is read fresh every call
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}
    
    print(f"Token present: {token is not None}")  # debug line
    
    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{base_tag}...{head_tag}"
    response = requests.get(url, headers=headers)
    print(f"GitHub API response: {response.status_code} — {response.text[:200]}")

    if response.status_code != 200:
        print(f"Error: {response.status_code} — {response.json().get('message')}")
        return []

    data = response.json()
    commits = data.get("commits", [])

    cleaned = []
    for c in commits:
        cleaned.append({
            "message": c["commit"]["message"].split("\n")[0],
            "author": c["commit"]["author"]["name"],
            "date": c["commit"]["author"]["date"],
            "sha": c["sha"][:7]
        })

    return cleaned


if __name__ == "__main__":
    commits = get_commits_between_tags(
        owner="expressjs",
        repo="express",
        base_tag="4.18.1",
        head_tag="4.18.2"
    )
    print(f"Found {len(commits)} commits:\n")
    for c in commits:
        print(f"[{c['sha']}] {c['author']}: {c['message']}")