import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("GitHub-Search-Server")

GITHUB_API_URL = "https://api.github.com/search/repositories"

@mcp.tool()
def search_github_repositories(topic: str, language: str = "") -> list:
    """
    Searches GitHub for repositories based on a topic and programming language.
    Topics: ai, android, python, dsa.
    """
    query = f"topic:{topic}"
    if language:
        query += f" language:{language}"
    
    # Simple GitHub Search API Call
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 5
    }
    
    try:
        response = requests.get(GITHUB_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for repo in data.get("items", []):
            results.append({
                "name": repo["full_name"],
                "description": repo["description"],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"]
            })
        return results
    except Exception as e:
        return [f"Error searching GitHub: {str(e)}"]

if __name__ == "__main__":
    mcp.run()