from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def format_commits_for_prompt(categories: dict) -> str:
    lines = []
    for category, commits in categories.items():
        if commits:
            lines.append(f"\n{category.upper()}:")
            for c in commits:
                lines.append(f"  - {c['message']}")
    return "\n".join(lines)


def generate_changelog(categories: dict, repo_name: str) -> dict:
    commit_summary = format_commits_for_prompt(categories)

    dev_prompt = f"""
    You are a senior developer writing release notes for {repo_name}.
    Below are categorized commits from a new release.
    Write a technical changelog for other developers.
    Be specific. Include breaking changes prominently at the top.
    Use markdown formatting. Be concise — no fluff.

    Commits:
    {commit_summary}
    """

    user_prompt = f"""
    You are writing release notes for regular users of {repo_name} who are not developers.
    Explain only what changed from the user's perspective in plain English.
    No technical jargon. Focus on what works better, what's new, what might look different.
    Keep it short — 3 to 5 bullet points max.

    Commits:
    {commit_summary}
    """

    security_prompt = f"""
    You are a security analyst writing a security-focused changelog for {repo_name}.
    Focus ONLY on security-relevant changes: vulnerabilities fixed, authentication changes,
    data handling updates, dependency updates that affect security.
    If there are no security-relevant changes, say so clearly.

    Commits:
    {commit_summary}
    """

    return {
        "developer": ask(dev_prompt),
        "user": ask(user_prompt),
        "security": ask(security_prompt)
    }
