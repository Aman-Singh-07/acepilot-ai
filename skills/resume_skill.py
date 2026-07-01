import os
from typing import Dict, Any
from google_adk import Agent, ModelConfig, Task

class ResumeSkill:
    """
    A reusable ADK Skill that evaluates resumes for ATS compatibility.
    Can be used standalone or registered as a tool for a Coordinator.
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.model_cfg = ModelConfig(
            model_name=model_name,
            api_key=api_key,
            temperature=0.1, # Low temperature for consistent scoring
            response_mime_type="application/json"
        )
        
        self.system_instructions = """
        You are a specialized ATS (Applicant Tracking System) Evaluation Skill.
        Your goal is to parse resume text and provide a objective score and feedback.
        
        OUTPUT FORMAT (JSON):
        {
            "ats_score": number (0-100),
            "critical_fail_points": ["list of major issues"],
            "keyword_optimization": ["missing industry keywords"],
            "formatting_suggestions": ["advice on layout and parsing"],
            "content_suggestions": ["advice on bullet points and metrics"]
        }
        """
        
        # Internal agent that powers the skill
        self._engine = Agent(
            name="ResumeSkillEngine",
            instructions=self.system_instructions,
            model_config=self.model_cfg
        )

    async def run(self, resume_text: str) -> Dict[str, Any]:
        """
        Executes the skill logic.
        """
        if not resume_text or len(resume_text.strip()) < 50:
            return {"error": "Resume text is too short or empty."}

        task = Task(
            input_data=f"Analyze this resume: {resume_text}",
            expected_output="JSON object with ATS score and detailed suggestions."
        )

        try:
            import json
            response = await self._engine.run(task)
            return json.loads(response.text)
        except Exception as e:
            return {"error": f"ResumeSkill execution failed: {str(e)}"}

# --- Example of Reusability ---

async def main():
    # 1. Initialize the reusable skill
    resume_skill = ResumeSkill(api_key=os.getenv("GOOGLE_API_KEY"))

    # 2. Sample Data
    raw_resume = """
    Alex Smith
    Software person. 
    I know Java and I worked at a place for 5 years.
    I like coding and fixing things.
    """

    # 3. Use the skill
    result = await resume_skill.run(raw_resume)

    # 4. Handle Output
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"ATS Score: {result['ats_score']}/100")
        print(f"Suggestions: {result['content_suggestions']}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())