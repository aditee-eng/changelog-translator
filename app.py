import os
from flask import Flask, request, jsonify, render_template
from github_fetcher import get_commits_between_tags
from classifier import classify_commits
from translator import generate_changelog

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    repo_url = data.get("repo_url")
    base_tag = data.get("base_tag")
    head_tag = data.get("head_tag")

    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    commits = get_commits_between_tags(owner, repo, base_tag, head_tag)
    if not commits:
        return jsonify({"error": "No commits found between these tags"}), 400

    categories = classify_commits(commits)
    changelogs = generate_changelog(categories, repo)

    return jsonify({
        "repo": f"{owner}/{repo}",
        "commit_count": len(commits),
        "changelogs": changelogs
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)