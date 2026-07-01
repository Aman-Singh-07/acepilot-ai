# 🚀 AcePilot AI: The Agentic Career Accelerator
**Capstone Project - Google AI Agents Intensive Course**

## 📖 Overview
AcePilot AI is a multi-agent system built with the **Google ADK** designed to help users bridge the gap between their current skills and their dream career. It falls under the **Agents for Good** track.

## 🛠️ Tech Stack
- **Orchestration:** Google ADK (Agent Development Kit)
- **Model:** Gemini 1.5 Pro & Flash
- **MCP:** Custom GitHub Repository Search Tool
- **Frontend:** Streamlit

## 🤖 The Agent Team
1. **Resume Agent:** Critiques and scores resumes.
2. **Project Mentor:** Uses MCP to find real GitHub projects.
3. **Learning Path Agent:** Generates 30-day roadmap.
4. **Interview Coach:** Provides 30 tailored questions.
5. **Coordinator:** The central brain managing context handoffs.

## 🔒 Security
- Includes a **Prompt Injection Guard** to prevent unauthorized system overrides and data leaks.

## 🚀 Installation
1. `pip install -r requirements.txt`
2. Add your keys to `.env`
3. `streamlit run frontend/streamlit_app.py`