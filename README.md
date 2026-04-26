# Changelog Translator

> Turn raw GitHub commits into changelogs for any audience — instantly.

**Live demo → [changelog-translator.onrender.com](https://changelog-translator.onrender.com)**

---

## The problem

When software updates, developers write commit messages for themselves — technical, abbreviated, full of jargon. Nobody translates these into something a regular user or a security team can actually act on.

This tool does that automatically.

---

## What it does

Give it any public GitHub repo and two version tags. It fetches every commit between them, classifies each change by type, and generates three completely different changelogs depending on who's reading.

- **Developers** — technical detail, breaking changes, dependency updates, migration notes
- **Users** — plain English, no jargon, focused on what actually changed for them  
- **Security teams** — only security-relevant changes, vulnerable dependencies, auth updates

Same raw data. Three completely different outputs. Each one written for its audience.

---

## How it works
GitHub API → fetch commits between two tags
↓
Classifier → sort by type (bug fix, feature, security, performance)
↓
Groq LLM (LLaMA 3.3 70B) → three audience-specific prompts
↓
Three changelogs rendered in the browser

The key design decision: three separate prompts instead of one. Audience-specific instructions produce dramatically better output than asking for multiple formats in a single call.

---

## Tech stack

- **Backend** — Python, Flask
- **AI** — Groq API (LLaMA 3.3 70B)
- **Data** — GitHub REST API
- **Frontend** — HTML, CSS, JavaScript
- **Deployment** — Render

---

## Run locally

1. Clone the repo
```bash
   git clone https://github.com/aditee-eng/changelog-translator.git
   cd changelog-translator
```

2. Create a virtual environment
```bash
   python -m venv venv
   source venv/bin/activate
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Create a `.env` file
GITHUB_TOKEN=your_github_token
GROQ_API_KEY=your_groq_api_key

5. Run
```bash
   python app.py
```

6. Open `http://localhost:5000`

---

## Example

**Input:** `https://github.com/expressjs/express` · `4.18.1` → `4.18.2`

**Developer output:**
> Fixed regression routing large stack in single route. body-parser updated to 1.20.1, qs to 6.11.0. Breaking: removed unused function arguments in examples.

**User output:**
> Routes with lots of layers now work more smoothly. Behind-the-scenes tools updated to keep things secure and stable.

**Security output:**
> body-parser@1.20.1 and qs@6.11.0 updated — both may include security fixes. No direct CVEs patched in this release.

---

## Get API keys

- GitHub token — github.com → Settings → Developer Settings → Personal Access Tokens
- Groq API key — [console.groq.com](https://console.groq.com)