# AcePilot AI — Complete Setup Guide
# Run these commands in your Ubuntu/WSL terminal, step by step.

## ─────────────────────────────────────────────
## STEP 1: Navigate to your project folder
## ─────────────────────────────────────────────

cd ~/acepilot-ai

## ─────────────────────────────────────────────
## STEP 2: Select the right Python interpreter in VS Code
## ─────────────────────────────────────────────
## Press Ctrl+Shift+P → "Python: Select Interpreter"
## Choose: Python 3.10.12 (.venv) ← the one marked "Recommended"
## This removes all yellow squiggly import errors.

## ─────────────────────────────────────────────
## STEP 3: Activate venv and install requirements
## ─────────────────────────────────────────────

source .venv/bin/activate
pip install -r requirements.txt

## ─────────────────────────────────────────────
## STEP 4: Create your .env file
## ─────────────────────────────────────────────

cp .env.example .env

# Then open .env in VS Code and fill in:
# GOOGLE_API_KEY=AIza...    ← from aistudio.google.com (free)
# GITHUB_TOKEN=ghp_...      ← from github.com/settings/tokens (classic, repo scope)

## ─────────────────────────────────────────────
## STEP 5: Run security tests (no API key needed)
## ─────────────────────────────────────────────

python -m evaluation.test_cases
# Expected: Security: 7/7 passed

## ─────────────────────────────────────────────
## STEP 6: Run the CLI (requires GOOGLE_API_KEY)
## ─────────────────────────────────────────────

python main.py

## ─────────────────────────────────────────────
## STEP 7: Run the Streamlit app
## ─────────────────────────────────────────────

streamlit run frontend/streamlit_app.py
# Opens at: http://localhost:8501

## ─────────────────────────────────────────────
## STEP 8: Push to GitHub
## ─────────────────────────────────────────────

# First, go to github.com → New Repository
# Name it: AcePilot-AI
# Set to: Public
# Do NOT initialize with README (you already have one)
# Copy the repo URL, then run:

git init
git add .
git commit -m "Initial commit: AcePilot AI capstone project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/AcePilot-AI.git
git push -u origin main

## ─────────────────────────────────────────────
## STEP 9: Deploy to Streamlit Cloud (free, 5 mins)
## ─────────────────────────────────────────────

# 1. Go to: https://share.streamlit.io
# 2. Sign in with GitHub
# 3. Click "New app"
# 4. Repository: YOUR_USERNAME/AcePilot-AI
# 5. Branch: main
# 6. Main file path: frontend/streamlit_app.py
# 7. Click "Advanced settings" → Secrets → paste:
#    GOOGLE_API_KEY = "your_key_here"
#    GITHUB_TOKEN = "your_token_here"
# 8. Click "Deploy!" → done in ~2 minutes

## ─────────────────────────────────────────────
## WHAT TO DELETE FROM YOUR CURRENT PROJECT
## ─────────────────────────────────────────────

## These files from your OLD structure should be REPLACED by the new ones:
## - agents/coordinator_agent.py   → REPLACE (new version is correct)
## - agents/resume_agent.py        → REPLACE (new version uses real ADK)
## - agents/project_agent.py       → REPLACE (new version has MCP tool)
## - agents/interview_agent.py     → REPLACE (new version)
## - agents/learning_agent.py      → REPLACE (new version)
## - security/input_guard.py       → REPLACE (improved version)
## - frontend/streamlit_app.py     → REPLACE (fully working version)
## - main.py                       → REPLACE (new CLI)
## - mcp_server.py                 → REPLACE (corrected version)
## - requirements.txt              → REPLACE (correct packages)

## KEEP these (they're fine):
## - .env (your keys are in there)
## - .gitignore
## - README.md (replace with new version)
## - evaluation/test_cases.py (replace with new version)
## - skills/ (replace with new versions)
## - memory/ (replace with new version)

## DELETE entirely:
## - mentor_agent.py (merged into coordinator)
## - docs/ (optional, can keep for screenshots)
