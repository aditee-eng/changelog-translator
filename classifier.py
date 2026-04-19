def classify_commits(commits: list) -> dict:
    categories = {
        "features": [],
        "bug_fixes": [],
        "security": [],
        "performance": [],
        "breaking": [],
        "other": []
    }

    feature_words = ["feat", "add", "new", "implement", "introduce"]
    bug_words = ["fix", "bug", "patch", "resolve", "correct", "repair"]
    security_words = ["security", "cve", "vulnerability", "auth", "xss", "injection", "csrf"]
    perf_words = ["perf", "performance", "speed", "optimize", "cache", "faster"]
    breaking_words = ["breaking", "deprecat", "remove", "drop support", "migration"]

    for commit in commits:
        msg = commit["message"].lower()

        if any(w in msg for w in breaking_words):
            categories["breaking"].append(commit)
        elif any(w in msg for w in security_words):
            categories["security"].append(commit)
        elif any(w in msg for w in perf_words):
            categories["performance"].append(commit)
        elif any(w in msg for w in feature_words):
            categories["features"].append(commit)
        elif any(w in msg for w in bug_words):
            categories["bug_fixes"].append(commit)
        else:
            categories["other"].append(commit)

    return categories


if __name__ == "__main__":
    # test with fake commits so you can see it working
    test_commits = [
        {"message": "fix null pointer in auth flow", "author": "someone", "sha": "abc1234"},
        {"message": "add new payment endpoint", "author": "someone", "sha": "def5678"},
        {"message": "security: patch XSS vulnerability", "author": "someone", "sha": "ghi9012"},
        {"message": "deps: qs@6.11.0", "author": "someone", "sha": "jkl3456"},
    ]

    result = classify_commits(test_commits)
    for category, commits in result.items():
        if commits:
            print(f"\n{category.upper()}:")
            for c in commits:
                print(f"  - {c['message']}")