import os
import requests
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

def search_github_repos(topic: str, language: str = "") -> list:
    """Search GitHub repositories by topic and optional language.
    Args:
        topic: GitHub topic tag e.g. machine-learning, android, python, dsa.
        language: Optional programming language filter e.g. python, kotlin.
    Returns:
        List of repos with name, description, url, stars.
    """
    query = f"topic:{topic}"
    if language:
        query += f" language:{language}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        resp = requests.get(
            "https://api.github.com/search/repositories",
            params={"q": query, "sort": "stars", "order": "desc", "per_page": 5},
            headers=headers, timeout=10,
        )
        resp.raise_for_status()
        return [{"name": r["full_name"], "description": r.get("description") or "No description",
                 "url": r["html_url"], "stars": r["stargazers_count"]}
                for r in resp.json().get("items", [])]
    except Exception as e:
        return [{"error": str(e)}]

github_tool = FunctionTool(func=search_github_repos)

project_agent = LlmAgent(
    name="ProjectMentor",
    model="gemini-2.0-flash",
    instruction="""You are the AcePilot Project Mentor.
Use the search_github_repos tool to find 2-3 relevant GitHub repositories.
Then suggest 3 original portfolio projects: 1 beginner, 1 intermediate, 1 portfolio-ready.
For each project provide: title, tech stack, what they will learn, why it matters.""",
    description="Searches GitHub and suggests portfolio projects matched to user skills.",
    tools=[github_tool],
)
