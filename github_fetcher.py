import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_commits_between_tags(owner: str, repo: str, base_tag: str, head_tag: str) -> list:
    
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}

    # Step 1: get the date of each tag
    def get_tag_date(tag: str):
        # try lightweight tag first
        url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/tags/{tag}"
        res = requests.get(url, headers=headers).json()
        
        sha = res.get("object", {}).get("sha")
        tag_type = res.get("object", {}).get("type")
        
        if tag_type == "tag":
            # annotated tag — need one more call
            tag_url = f"https://api.github.com/repos/{owner}/{repo}/git/tags/{sha}"
            tag_data = requests.get(tag_url, headers=headers).json()
            sha = tag_data.get("object", {}).get("sha")
        
        # get commit date
        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
        commit_data = requests.get(commit_url, headers=headers).json()
        return commit_data.get("commit", {}).get("committer", {}).get("date")

    base_date = get_tag_date(base_tag)
    head_date = get_tag_date(head_tag)

    if not base_date or not head_date:
        print(f"Could not resolve tag dates: {base_tag}={base_date}, {head_tag}={head_date}")
        return []

    print(f"Fetching commits between {base_date} and {head_date}")

    # Step 2: fetch commits between those dates
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {
        "since": base_date,
        "until": head_date,
        "per_page": 100
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} — {response.json().get('message')}")
        return []

    commits = response.json()

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