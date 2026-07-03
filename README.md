# 🚀 AcePilot AI: Multi-Agent Career Copilot

**Capstone Project - Google AI Agents Intensive Course**

## 📖 Overview
Career coaching is expensive and inaccessible for most students. AcePilot AI democratizes career guidance by providing a free, personalized AI career coach. Built for the **Agents for Good** track, it uses a coordinated team of specialist agents to bridge the gap between a student's current skills and their dream career.

## 🛠️ Tech Stack
* **Orchestration:** Google ADK (Agent Development Kit)
* **Model:** Gemini 2.0 Flash
* **External Tool (MCP):** GitHub API Repository Search
* **Frontend:** Streamlit Cloud
* **Language:** Python

## 🤖 The Agent Team
The system uses a central **Coordinator Agent** to manage four specialists:
1. **Resume Expert:** Analyzes ATS scores, finds missing keywords, and rewrites weak bullet points.
2. **Project Mentor:** Uses a GitHub MCP tool to fetch live repositories and suggests 3 portfolio projects.
3. **Learning Pathfinder:** Generates a structured, day-by-day 30-day learning roadmap.
4. **Interview Coach:** Prepares 15 targeted questions (DSA, Technical, and Behavioral) with model answers.

## 🔒 Security Guardrail
All user input passes through a strict regex-based security layer (`input_guard.py`) before reaching any agent. It successfully detects and blocks:
* Prompt Injection & Instruction Overrides
* Data Exfiltration Attempts
* Command Injection
* Jailbreak Frameworks (e.g., DAN)

## 🚀 Live Demo
**Try it here:** [AcePilot AI Streamlit App](https://acepilot-ai-6kkhfyjhsyzgh7n46n2rhb.streamlit.app)

## 💻 Local Installation
```bash
git clone [https://github.com/Aman-Singh-07/acepilot-ai.git](https://github.com/Aman-Singh-07/acepilot-ai.git)
cd acepilot-ai
pip install -r requirements.txt
