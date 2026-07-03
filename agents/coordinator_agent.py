import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import google.genai.types as types

from agents.resume_agent import resume_agent
from agents.project_agent import project_agent
from agents.interview_agent import interview_agent
from agents.learning_agent import learning_agent

coordinator_agent = LlmAgent(
    name="AcePilotCoordinator",
    model="gemini-1.5-flash",
    instruction="""You are AcePilot, an AI career accelerator.
When given a resume, skills, and career goal, coordinate with your sub-agents:
1. Ask ResumeExpert to analyze the resume for ATS score and improvements.
2. Ask ProjectMentor to find GitHub repos and suggest portfolio projects.
3. Ask LearningPathfinder to create a 30-day learning roadmap.
4. Ask InterviewCoach to prepare 15 interview questions.
Then synthesize all outputs into one complete Career Development Report.""",
    description="Orchestrates all AcePilot sub-agents to produce a unified career report.",
    sub_agents=[resume_agent, project_agent, interview_agent, learning_agent],
)

async def run_coordinator(prompt: str, session_id: str = "default") -> str:
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="acepilot", user_id="user", session_id=session_id)
    runner = Runner(agent=coordinator_agent, session_service=session_service, app_name="acepilot")
    message = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    parts = []
    async for event in runner.run_async(user_id="user", session_id=session_id, new_message=message):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    parts.append(part.text)
    return "".join(parts)

def generate_career_report(resume_text: str, skills: str, career_goal: str, session_id: str = "default") -> str:
    prompt = f"""RESUME:\n{resume_text}\n\nCURRENT SKILLS:\n{skills}\n\nCAREER GOAL:\n{career_goal}\n\nGenerate a complete Career Development Report with Resume Analysis, GitHub Recommendations, 30-Day Roadmap, and Interview Prep."""
    return asyncio.run(run_coordinator(prompt, session_id))
