"""
main.py
-------
CLI entry point for AcePilot AI.
Use this to test the full agent pipeline from the terminal.

Usage:
    python main.py

The Streamlit frontend is the main user interface.
Run it with:
    streamlit run frontend/streamlit_app.py
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load .env before importing agents (agents need GOOGLE_API_KEY at import time)
load_dotenv()

from security.input_guard import validate_input
from agents.coordinator_agent import run_coordinator


BANNER = """
╔══════════════════════════════════════════════════╗
║         🚀  AcePilot AI — Career Copilot         ║
║   Powered by Google ADK + Gemini 2.0 Flash       ║
╚══════════════════════════════════════════════════╝
"""


def get_input(prompt: str, field_name: str) -> str:
    """Get validated user input, checking for injection attacks."""
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"  ⚠️  {field_name} cannot be empty. Try again.")
            continue
        guard = validate_input(value)
        if not guard:
            print(f"  🛡️  Security alert: {guard.threat_type}. Please enter valid {field_name}.")
            continue
        return value


async def main():
    print(BANNER)

    if not os.getenv("GOOGLE_API_KEY"):
        print("❌  GOOGLE_API_KEY not found.")
        print("    Create a .env file with: GOOGLE_API_KEY=your_key_here")
        print("    Get your free key at: https://aistudio.google.com/")
        sys.exit(1)

    print("Enter your details to generate your Career Report.\n")

    resume = get_input("📄 Paste your resume text (one line, or press Enter for demo):\n> ", "resume")
    if resume.lower() in ("demo", ""):
        resume = "Software Developer with 2 years experience in Python and Java. Built REST APIs and worked on SQL databases."

    skills = get_input("\n🛠️  Your current skills (comma-separated):\n> ", "skills")
    goal = get_input("\n🎯  Your career goal:\n> ", "career goal")

    prompt = f"""
RESUME:
{resume}

CURRENT SKILLS:
{skills}

CAREER GOAL:
{goal}

Please generate a complete Career Development Report with:
1. Resume Analysis (ATS score + improvements)
2. GitHub Repository Recommendations + Portfolio Projects
3. 30-Day Learning Roadmap
4. Interview Preparation Guide
"""

    print("\n⏳ AcePilot agents are working on your report...\n")
    print("(This usually takes 30–90 seconds)\n")

    try:
        report = await run_coordinator(prompt)
        print("=" * 60)
        print("CAREER DEVELOPMENT REPORT")
        print("=" * 60)
        print(report)
        print("=" * 60)
        print("\n✅ Report complete! Run 'streamlit run frontend/streamlit_app.py' for the full UI.")
    except Exception as exc:
        print(f"❌ Error: {exc}")
        print("\nCheck that your GOOGLE_API_KEY is valid.")


if __name__ == "__main__":
    asyncio.run(main())
