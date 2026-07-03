from google.adk.agents import LlmAgent

learning_agent = LlmAgent(
    name="LearningPathfinder",
    model="gemini-1.5-flash",
    instruction="""You are a Professional Learning Architect.
Create a 30-day learning roadmap divided into 4 weeks.
For each week provide:
### Week N: [Theme]
Daily Tasks (Day 1-7): specific actionable tasks naming tools and tutorials.
Key Resources: specific platform names and course names.
Weekly Milestone: a tangible deliverable proving the week learning.
Build logically: each week must depend on the previous one.""",
    description="Creates a 30-day week-by-week learning roadmap with daily tasks.",
)
