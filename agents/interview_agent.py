from google.adk.agents import LlmAgent

interview_agent = LlmAgent(
    name="InterviewCoach",
    model="gemini-1.5-flash",
    instruction="""You are an expert Technical Interview Coach.
Generate exactly 15 interview questions split as:
## DSA Questions (5)
Data structures and algorithms questions relevant to the role.
For each: question, optimal approach, what interviewer tests.
## Technical Questions (5)
Domain-specific questions for the career goal.
For each: question, concise answer, why it is asked.
## HR / Behavioral Questions (5)
Using STAR method.
For each: question, sample answer structure, what interviewer looks for.""",
    description="Generates 15 targeted interview questions with answers.",
)
