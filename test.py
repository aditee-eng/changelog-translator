from dotenv import load_dotenv
import os
load_dotenv()
print("Token loaded:", os.getenv("GITHUB_TOKEN") is not None)
print("Groq key loaded:", os.getenv("GROQ_API_KEY") is not None)

from github_fetcher import get_commits_between_tags
from classifier import classify_commits
from translator import generate_changelog

commits = get_commits_between_tags("expressjs", "express", "4.18.1", "4.18.2")
categories = classify_commits(commits)
changelogs = generate_changelog(categories, "Express.js")

print("=== DEVELOPER ===")
print(changelogs["developer"])
print("\n=== USER ===")
print(changelogs["user"])
print("\n=== SECURITY ===")
print(changelogs["security"])