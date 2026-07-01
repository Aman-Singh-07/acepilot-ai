import os
import json
from typing import Dict, Any, Optional
from google_adk import Agent, ModelConfig, Task

class LearningRoadmapSkill:
    """
    A reusable ADK Skill that generates structured 30-day technical 
    learning paths based on a specific career goal.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        # Configuration focused on structure and logical progression
        self.model_cfg = ModelConfig(
            model_name=model_name,
            api_key=api_key,
            temperature=0.3,
            response_mime_type="application/json"
        )

        self.system_instructions = """
        You are a Senior Learning Architect. Your task is to generate a 
        highly structured 30-day learning roadmap for a specific career goal.
        
        STRUCTURE REQUIREMENTS:
        1. Split the roadmap into exactly 4 weeks (7 days per week).
        2. For each week, provide:
           - Theme: The core focus of the week.
           - Daily Tasks: A specific task for each day.
           - Key Resources: High-quality links or names of platforms.
           - Milestone: A mini-project to complete by day 7.
        
        OUTPUT FORMAT (JSON):
        {
            "career_goal": "string",
            "roadmap": [
                {
                    "week": 1,
                    "theme": "string",
                    "daily_plan": ["Day 1: ...", "Day 2: ...", "Day 7: ..."],
                    "resources": ["Resource A", "Resource B"],
                    "milestone_project": "string"
                }
                // ... repeated for weeks 2, 3, and 4
            ]
        }
        """

        self._agent = Agent(
            name="RoadmapEngine",
            instructions=self.system_instructions,
            model_config=self.model_cfg
        )

    async def run(self, career_goal: str) -> Dict[str, Any]:
        """
        Generates the 30-day roadmap based on the input goal.
        """
        if not career_goal or len(career_goal.strip()) < 3:
            return {"error": "Invalid career goal provided."}

        # Define the task for the ADK internal engine
        roadmap_task = Task(
            input_data=f"Create a 30-day roadmap to become a: {career_goal}",
            expected_output="A JSON object with a 4-week structured plan."
        )

        try:
            response = await self._agent.run(roadmap_task)
            # The response is guaranteed to be JSON due to response_mime_type config
            return json.loads(response.text)
        except Exception as e:
            return {
                "error": f"LearningRoadmapSkill failed: {str(e)}",
                "status": "failure"
            }

# --- Usage Example (Standalone or Integration) ---

async def main():
    # Initialize the skill with your API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    roadmap_skill = LearningRoadmapSkill(api_key=api_key)

    # Input goal
    goal = "Cloud Native Developer (Kubernetes & Go)"

    print(f"--- Generating 30-Day Roadmap for: {goal} ---\n")
    
    result = await roadmap_skill.run(goal)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        # Example: Printing Week 1 details
        week1 = result['roadmap'][0]
        print(f"Week 1 Theme: {week1['theme']}")
        print(f"First Task: {week1['daily_plan'][0]}")
        print(f"Resources: {', '.join(week1['resources'])}")
        print(f"Milestone: {week1['milestone_project']}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())