# Changelog Translator

Turns raw GitHub commit history into audience-specific changelogs using AI.

Give it any public GitHub repo and two version tags — it fetches every change between them and generates three completely different explanations depending on who's reading.

## The problem

When software updates, developers write commit messages for themselves — technical, abbreviated, full of jargon. Nobody translates these into something a regular user or a security team can actually act on. This tool does that automatically.

## What it generates

- **Developer changelog** — technical detail, breaking changes, migration notes
- **User changelog** — plain English, no jargon, focused on what changed for them
- **Security changelog** — only security-relevant changes, dependency updates, vulnerabilities fixed

## How it works

1. Fetches commits between two version tags using the GitHub API
2. Classifies each commit by type (bug fix, feature, security, performance)
3. Sends the classified commits to an LLM with three different audience-specific prompts
4. Returns three completely different changelogs from the same raw data

## Tech stack

- Python
- GitHub REST API
- Groq API (LLaMA 3.3 70B)
- Flask (coming in v2)

## Setup

1. Clone the repo
```bash
   git clone https://github.com/yourusername/changelog-translator.git
   cd changelog-translator
```

2. Create a virtual environment
```bash
   python -m venv venv
   source venv/bin/activate
```

3. Install dependencies
```bash
   pip install requests groq python-dotenv
```

4. Create a `.env` file in the root folder
GITHUB_TOKEN=your_github_token
GROQ_API_KEY=your_groq_api_key

5. Run it
```bash
   python test.py
```

## Example output

**Input:** `expressjs/express` from `4.18.1` to `4.18.2`

**Developer changelog:**
> Fixed regression routing a large stack in a single route. Updated body-parser to 1.20.1, qs to 6.11.0. Breaking: removed unused function arguments in examples.

**User changelog:**
> Routes with a lot of layers now work more smoothly. Behind-the-scenes tools updated to keep Express.js secure and stable.

**Security changelog:**
> body-parser updated to 1.20.1 and qs updated to 6.11.0 — both may include security fixes. No direct vulnerabilities patched in this release.

## What's next

- Flask API with web frontend
- Support for private repos
- Side-by-side diff view between versions

## Get API keys

- GitHub token: github.com → Settings → Developer Settings → Personal Access Tokens
- Groq API key: console.groq.com