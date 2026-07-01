import os, sys, time, asyncio
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from security.input_guard import validate_input

st.set_page_config(
    page_title="AcePilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── Remove Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 3rem 3rem; max-width: 1100px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}
section[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem; }

.sidebar-logo {
    font-size: 1.1rem;
    font-weight: 600;
    color: #111827;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
}
.sidebar-sub {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-bottom: 1.5rem;
}
.sidebar-divider {
    border: none;
    border-top: 1px solid #f3f4f6;
    margin: 1.2rem 0;
}
.sidebar-section-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9ca3af;
    margin-bottom: 0.75rem;
}

/* Agent list */
.agent-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #f9fafb;
}
.agent-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #10b981;
    flex-shrink: 0;
}
.agent-name { font-size: 0.85rem; font-weight: 500; color: #374151; }
.agent-desc { font-size: 0.75rem; color: #9ca3af; }

/* Status pill */
.pill-green {
    display: inline-flex; align-items: center; gap: 5px;
    background: #f0fdf4; color: #15803d;
    border: 1px solid #bbf7d0;
    border-radius: 20px; padding: 3px 10px;
    font-size: 0.75rem; font-weight: 500;
}
.pill-amber {
    display: inline-flex; align-items: center; gap: 5px;
    background: #fffbeb; color: #b45309;
    border: 1px solid #fde68a;
    border-radius: 20px; padding: 3px 10px;
    font-size: 0.75rem; font-weight: 500;
}

/* ── Main page ── */
.page-title {
    font-size: 1.75rem;
    font-weight: 600;
    color: #111827;
    letter-spacing: -0.03em;
    margin-bottom: 4px;
}
.page-sub {
    font-size: 0.95rem;
    color: #6b7280;
    margin-bottom: 2rem;
}

/* Section labels */
.field-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 6px;
    display: block;
}
.field-hint {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 4px;
}

/* Inputs */
.stTextArea textarea {
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    color: #111827 !important;
    background: #fafafa !important;
    resize: vertical !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
    background: #fff !important;
}
.stTextInput input {
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    color: #111827 !important;
    background: #fafafa !important;
    height: 42px !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
    background: #fff !important;
}

/* Generate button */
div.stButton > button {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
    transition: background 0.15s !important;
}
div.stButton > button:hover {
    background: #1e40af !important;
}

/* Divider */
.page-divider {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 2rem 0;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: transparent;
    border-bottom: 1px solid #e5e7eb;
    padding: 0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #6b7280 !important;
    padding: 10px 18px !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #1d4ed8 !important;
    border-bottom: 2px solid #1d4ed8 !important;
    background: transparent !important;
}

/* Report content */
.report-content {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.75rem 2rem;
    font-size: 0.9rem;
    line-height: 1.8;
    color: #374151;
    margin-top: 1rem;
}

/* Stats row */
.stats-row {
    display: flex;
    gap: 1px;
    background: #e5e7eb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.stat-cell {
    flex: 1;
    background: #fff;
    padding: 14px 20px;
    text-align: center;
}
.stat-num { font-size: 1.4rem; font-weight: 600; color: #111827; }
.stat-lbl { font-size: 0.72rem; color: #9ca3af; margin-top: 2px; font-weight: 500; }

/* Empty state */
.empty-state {
    background: #f9fafb;
    border: 1px dashed #d1d5db;
    border-radius: 10px;
    padding: 3rem 2rem;
    text-align: center;
    margin-top: 1rem;
    color: #6b7280;
    font-size: 0.9rem;
    line-height: 1.7;
}
.empty-title {
    font-size: 1rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 0.5rem;
}

/* Info note */
.info-note {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 0.8rem;
    color: #1e40af;
    margin-top: 12px;
    line-height: 1.6;
}

/* Architecture box */
.arch-block {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 0.82rem;
    color: #374151;
    line-height: 2;
}
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">AcePilot AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Google ADK · Gemini 2.0 Flash</div>', unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Agents</div>', unsafe_allow_html=True)

    agents = [
        ("Resume Expert",       "ATS analysis & rewrites"),
        ("Project Mentor",      "GitHub search & portfolio ideas"),
        ("Learning Pathfinder", "30-day study roadmap"),
        ("Interview Coach",     "DSA, technical & HR questions"),
    ]
    for name, desc in agents:
        st.markdown(f"""
        <div class="agent-item">
            <div class="agent-dot"></div>
            <div>
                <div class="agent-name">{name}</div>
                <div class="agent-desc">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">API Key</div>', unsafe_allow_html=True)

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key and hasattr(st, "secrets"):
        api_key = st.secrets.get("GOOGLE_API_KEY", "")

    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.markdown('<span class="pill-green">&#10003;&nbsp; Key loaded</span>', unsafe_allow_html=True)
    else:
        user_key = st.text_input("Google API Key", type="password",
                                  placeholder="Paste your key here",
                                  label_visibility="collapsed")
        if user_key:
            os.environ["GOOGLE_API_KEY"] = user_key
            api_key = user_key
            st.markdown('<span class="pill-green">&#10003;&nbsp; Key set</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="pill-amber">Key required</span>', unsafe_allow_html=True)
            st.markdown(
                '<a href="https://aistudio.google.com/" target="_blank" '
                'style="font-size:0.78rem;color:#2563eb;">Get a free key at aistudio.google.com</a>',
                unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Security</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.78rem; color:#6b7280; line-height:2">
        Prompt injection detection<br>
        Jailbreak pattern blocking<br>
        Command injection guard<br>
        Data exfiltration prevention
    </div>""", unsafe_allow_html=True)


# ── MAIN ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Career Development Report</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-sub">Fill in your background and target role. '
    'Four AI agents will analyse your profile and generate a personalised action plan.</div>',
    unsafe_allow_html=True)

with st.expander("How it works"):
    col_a, col_b = st.columns([1, 1], gap="large")
    with col_a:
        st.markdown("""
        <div class="arch-block">
Your input (resume + skills + goal)
          |
          v
Security validation
          |
          v
AcePilot Coordinator (Google ADK)
     |         |         |        |
     v         v         v        v
  Resume   Project  Learning  Interview
  Expert   Mentor   Pathfndr  Coach
          |
          v
Unified career report
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""
**What the report includes**

**Resume analysis** — ATS compatibility score (0–100), missing keywords, and specific before/after rewrites for weak sections.

**GitHub recommendations** — Live search of real repositories relevant to your goal, plus three portfolio project ideas graded by difficulty.

**30-day roadmap** — Week-by-week plan with daily tasks, curated resources, and a milestone project each Friday.

**Interview preparation** — Five DSA questions, five technical questions, and five behavioural questions, each with a model answer.
        """)

st.markdown('<hr class="page-divider">', unsafe_allow_html=True)

# ── INPUT FORM ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<span class="field-label">Resume</span>', unsafe_allow_html=True)
    resume_text = st.text_area(
        "Resume",
        placeholder="Paste your resume text here — work experience, skills, education, and any projects.",
        height=220,
        label_visibility="collapsed",
    )
    st.markdown('<span class="field-hint">Plain text works best. No need to format it perfectly.</span>',
                unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="field-label">Current skills</span>', unsafe_allow_html=True)
    skills = st.text_input(
        "Skills",
        placeholder="e.g.  Python, Java, SQL, Docker, REST APIs, Git",
        label_visibility="collapsed",
    )
    st.markdown('<span class="field-hint">Separate each skill with a comma.</span>',
                unsafe_allow_html=True)

with col2:
    st.markdown('<span class="field-label">Target role</span>', unsafe_allow_html=True)
    career_goal = st.text_input(
        "Career goal",
        placeholder="e.g.  Senior ML Engineer at a product-based company",
        label_visibility="collapsed",
    )
    st.markdown('<span class="field-hint">Be as specific as you can — seniority, domain, and company type all help.</span>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="info-note">
        <strong>Good examples</strong><br>
        Android Developer specialising in on-device AI<br>
        Senior DevOps Engineer at a cloud-first startup<br>
        Data Engineer with AWS and Apache Airflow
    </div>""", unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)
generate = st.button("Generate report", use_container_width=True)


# ── RUN ───────────────────────────────────────────────────────────────────────
if generate:
    errors = []
    if not resume_text.strip():
        errors.append("Resume text is required.")
    if not skills.strip():
        errors.append("Please list your current skills.")
    if not career_goal.strip():
        errors.append("Please enter your target role.")
    if not os.getenv("GOOGLE_API_KEY"):
        errors.append("A Google API key is required. Add it in the sidebar.")
    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    for field_name, value in [("resume", resume_text), ("skills", skills), ("goal", career_goal)]:
        guard = validate_input(value)
        if not guard:
            st.error(f"Security check failed on {field_name}: {guard.threat_type}.")
            st.stop()

    prompt = f"""
RESUME:
{resume_text}

CURRENT SKILLS:
{skills}

CAREER GOAL:
{career_goal}

Generate a comprehensive Career Development Report with four sections:
1. Resume Analysis — ATS score, missing keywords, and specific before/after rewrites
2. GitHub Recommendations — real repository names and three portfolio project ideas
3. 30-Day Learning Roadmap — four weeks with daily tasks, resources, and milestones
4. Interview Preparation — 5 DSA, 5 technical, and 5 behavioural questions with model answers
"""

    st.markdown('<hr class="page-divider">', unsafe_allow_html=True)

    with st.status("Generating your report — this usually takes 30–60 seconds.", expanded=True) as status:
        st.write("Resume Expert is analysing your profile...")
        time.sleep(0.5)
        st.write("Project Mentor is searching GitHub...")
        time.sleep(0.5)
        st.write("Learning Pathfinder is building your roadmap...")
        time.sleep(0.5)
        st.write("Interview Coach is preparing your questions...")

        try:
            from agents.coordinator_agent import run_coordinator
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                report = loop.run_until_complete(run_coordinator(prompt))
            finally:
                loop.close()
            status.update(label="Report ready.", state="complete", expanded=False)
        except Exception as exc:
            status.update(label="Something went wrong.", state="error")
            err = str(exc)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                st.error(
                    "The Gemini API free-tier quota has been reached for today. "
                    "Please wait a few minutes and try again, or create a new API key at aistudio.google.com."
                )
            else:
                st.error(f"Agent error: {exc}")
            st.stop()

    # ── Stats ──
    word_count = len(report.split())
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-cell"><div class="stat-num">{word_count:,}</div><div class="stat-lbl">Words generated</div></div>
        <div class="stat-cell"><div class="stat-num">4</div><div class="stat-lbl">Agents used</div></div>
        <div class="stat-cell"><div class="stat-num">15</div><div class="stat-lbl">Interview questions</div></div>
        <div class="stat-cell"><div class="stat-num">30</div><div class="stat-lbl">Day roadmap</div></div>
    </div>""", unsafe_allow_html=True)

    # ── Section splitter ──
    def extract(text, keywords):
        lines = text.split("\n")
        out, active = [], False
        for line in lines:
            hit = any(k.lower() in line.lower() for k in keywords)
            if hit:
                active = True
            elif active and line.startswith("# ") and not hit:
                break
            if active:
                out.append(line)
        result = "\n".join(out).strip()
        return result if len(result) > 100 else ""

    s_resume    = extract(report, ["resume", "ats", "missing skill", "keyword", "weak section"])
    s_projects  = extract(report, ["project", "github", "portfolio", "repository"])
    s_roadmap   = extract(report, ["roadmap", "week", "30-day", "daily", "milestone"])
    s_interview = extract(report, ["interview", "dsa", "behavioural", "behavioral", "hr", "technical question"])

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Resume analysis",
        "Projects & GitHub",
        "30-day roadmap",
        "Interview prep",
        "Full report",
    ])

    with tab1:
        st.markdown(f'<div class="report-content">{s_resume or report}</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown(f'<div class="report-content">{s_projects or report}</div>', unsafe_allow_html=True)
    with tab3:
        st.markdown(f'<div class="report-content">{s_roadmap or report}</div>', unsafe_allow_html=True)
    with tab4:
        st.markdown(f'<div class="report-content">{s_interview or report}</div>', unsafe_allow_html=True)
    with tab5:
        st.markdown(f'<div class="report-content">{report}</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "Download as text",
            data=report,
            file_name=f"acepilot_{career_goal[:25].replace(' ','_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "Download as Markdown",
            data=f"# Career Development Report\n**Target role:** {career_goal}\n\n{report}",
            file_name=f"acepilot_{career_goal[:25].replace(' ','_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-title">No report generated yet</div>
        Fill in your resume, skills, and target role above, then click <strong>Generate report</strong>.<br>
        The process takes 30–60 seconds. You will be able to download the result when it is ready.
    </div>""", unsafe_allow_html=True)
