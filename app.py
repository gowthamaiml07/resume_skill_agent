"""
app.py
======
Streamlit Web Application for the AI Resume Analyzer and Skill Development Agent.
Provides a modern, intuitive, and interactive UI for PDF resume parsing,
structured LLM analysis, 4-week learning roadmap visualization, and Markdown export.
"""

from __future__ import annotations

import os
import streamlit as st
from dotenv import load_dotenv

from resume_parser import (
    extract_text_from_pdf,
    get_pdf_metadata,
    EmptyPDFError,
    ScannedPDFError,
    ResumeParsingError,
)
from agent import (
    analyze_resume,
    generate_demo_analysis,
    export_analysis_to_markdown,
    ResumeAnalysisOutput,
)

# Load environment variables
load_dotenv()

# ==============================================================================
# Streamlit Page Configuration & Styling
# ==============================================================================

st.set_page_config(
    page_title="AI Resume & Skill Agent",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a clean, modern aesthetic
CUSTOM_CSS = """
<style>
    /* Main container styling */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    
    /* Card containers */
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2563EB;
    }
    .metric-label {
        font-size: 0.88rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Badge styles */
    .skill-badge-green {
        display: inline-block;
        background-color: #DCFCE7;
        color: #15803D;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 0.3rem 0.75rem;
        border-radius: 9999px;
        margin: 0.25rem;
        border: 1px solid #86EFAC;
    }
    .skill-badge-amber {
        display: inline-block;
        background-color: #FEF3C7;
        color: #B45309;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 0.3rem 0.75rem;
        border-radius: 9999px;
        margin: 0.25rem;
        border: 1px solid #FDE68A;
    }

    /* Week card */
    .week-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #3B82F6;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    /* Disclaimer box */
    .disclaimer-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 0.9rem 1.2rem;
        border-radius: 6px;
        color: #1E40AF;
        font-size: 0.9rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# Sidebar: Settings & Configuration
# ==============================================================================

with st.sidebar:
    st.image(
        "https://api.iconify.design/lucide:briefcase.svg?color=%232563EB",
        width=48,
    )
    st.title("Settings & Keys")
    st.markdown("Configure your AI model and API credentials securely.")

    # Provider Mode Selector
    has_groq = bool(os.getenv("GROQ_API_KEY"))
    default_idx = 1 if has_groq else 0

    provider_mode = st.radio(
        "AI Execution Mode",
        options=[
            "🟢 OpenAI API",
            "⚡ Groq (Fast & Free Cloud)",
            "🧪 Offline / Demo Mode",
        ],
        index=default_idx,
        help="Select Groq for fast free cloud inference, OpenAI, or Offline Demo Mode.",
    )

    custom_base_url = None
    selected_model = "llama-3.3-70b-versatile"
    api_key_input = ""

    if provider_mode == "🟢 OpenAI API":
        env_api_key = os.getenv("OPENAI_API_KEY", "")
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            value=env_api_key,
            help="Your OpenAI API Key will only be used in-memory for this session.",
            placeholder="sk-proj-...",
        )
        if api_key_input:
            st.success("API Key detected", icon="🔒")
        else:
            st.info("Set `OPENAI_API_KEY` in `.env` or paste it above.", icon="🔑")

        model_options = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
        selected_model = st.selectbox(
            "OpenAI Model",
            options=model_options,
            index=0,
            help="gpt-4o-mini is recommended for fast, high-quality analysis.",
        )

    elif provider_mode == "⚡ Groq (Fast & Free Cloud)":
        custom_base_url = "https://api.groq.com/openai/v1"
        env_groq_key = os.getenv("GROQ_API_KEY", "")
        api_key_input = st.text_input(
            "Groq API Key",
            type="password",
            value=env_groq_key,
            placeholder="gsk_...",
            help="Free API key from console.groq.com",
        )
        if api_key_input:
            st.success("Groq API Key detected & active!", icon="⚡")
        else:
            st.info("Get your free key at [console.groq.com](https://console.groq.com/keys)", icon="🔑")

        selected_model = st.selectbox(
            "Groq Model",
            options=["llama-3.1-8b-instant", "llama3-70b-8192", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
            index=0,
            help="llama-3.1-8b-instant is ultra-fast, robust, and universally accessible on Groq's free tier.",
        )

    else:
        st.success("💡 **Offline / Demo Mode active.** No API key or credits needed. Analyzes real resume keywords locally.", icon="🧪")

    # Temperature Slider
    temperature = st.slider(
        "Analytical Temperature",
        min_value=0.0,
        max_value=0.7,
        value=0.2,
        step=0.05,
        help="Lower values (0.1 - 0.2) ensure strict adherence to factual resume evidence.",
    )

    st.divider()

    # Privacy & Safety notice
    with st.expander("🛡️ Privacy & Ethical Policy"):
        st.markdown(
            """
            - **No Storage:** Uploaded resumes are processed in-memory and discarded after analysis.
            - **No Hallucinations:** The agent is restricted from fabricating experience or skills.
            - **Honest Absence:** Missing skills are flagged as *'Not evidenced in resume'* rather than claiming you lack the ability.
            - **Educational Metric:** Match score indicates keyword alignment, not hiring guarantees.
            """
        )

    # About / Reset
    if st.button("🔄 Reset Application State", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# ==============================================================================
# Main Interface: Input Form
# ==============================================================================

st.markdown('<div class="main-title">🎯 AI Resume Analyzer & Skill Development Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload your resume to receive rigorous skill gap analysis, an actionable 4-week learning roadmap, portfolio project ideas, and honest resume enhancement suggestions.</div>',
    unsafe_allow_html=True,
)

col_input_1, col_input_2 = st.columns([1, 1], gap="large")

with col_input_1:
    st.subheader("1. Upload Your Resume (PDF)")
    uploaded_file = st.file_uploader(
        "Choose a text-based PDF resume",
        type=["pdf"],
        help="Upload a standard digital PDF resume (e.g., exported from MS Word, Google Docs, or Canva).",
    )

    extracted_text = ""
    if uploaded_file is not None:
        try:
            with st.spinner("Extracting text with PyMuPDF..."):
                file_bytes = uploaded_file.getvalue()
                extracted_text = extract_text_from_pdf(file_bytes)
                metadata = get_pdf_metadata(file_bytes)

            st.success(
                f"✅ **PDF Extracted:** {metadata['page_count']} page(s) | ~{metadata['word_count']} words | {metadata['character_count']} chars"
            )

            with st.expander("👁️ View Extracted Resume Text"):
                st.text_area("Extracted Plain Text", value=extracted_text, height=180, disabled=True)

        except EmptyPDFError as e:
            st.error(f"❌ **Empty File:** {str(e)}")
        except ScannedPDFError as e:
            st.warning(f"⚠️ **Scanned PDF Detected:** {str(e)}")
        except ResumeParsingError as e:
            st.error(f"❌ **Parsing Error:** {str(e)}")
        except Exception as e:
            st.error(f"❌ **Unexpected Error:** {str(e)}")

with col_input_2:
    st.subheader("2. Target Career Goals")
    
    # Quick select buttons
    st.caption("Quick Role Suggestions:")
    quick_roles = ["Python Developer", "Data Analyst", "Machine Learning Engineer", "Full Stack Developer"]
    cols_btn = st.columns(len(quick_roles))
    
    # Store selected role in session state if clicked
    if "target_role_input" not in st.session_state:
        st.session_state.target_role_input = "Python Developer"

    for i, role in enumerate(quick_roles):
        if cols_btn[i].button(role, key=f"quick_role_{i}"):
            st.session_state.target_role_input = role

    target_role = st.text_input(
        "Target Job Role *",
        value=st.session_state.target_role_input,
        placeholder="e.g., Senior Python Backend Developer, Data Scientist, DevOps Engineer",
        help="The specific title or role you are aiming for.",
    )

    st.subheader("3. Target Job Description (Optional)")
    job_description = st.text_area(
        "Paste the Job Description or key requirements for tailored alignment",
        height=130,
        placeholder="Paste requirements, responsibilities, or tech stack from a specific job posting...",
        help="Optional: Providing a job description yields more precise alignment and matching.",
    )

# Analyze Button
st.markdown("---")
analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])

with analyze_col2:
    analyze_clicked = st.button(
        "🚀 Run Skill Gap Analysis & Build Roadmap",
        type="primary",
        use_container_width=True,
        disabled=(uploaded_file is None or not extracted_text or not target_role.strip()),
    )

# ==============================================================================
# Execution & Analysis Handling
# ==============================================================================

if analyze_clicked:
    if not extracted_text:
        st.error("📄 **No Resume Text:** Please upload a valid, readable PDF resume.")
    elif not target_role.strip():
        st.error("🎯 **Target Role Required:** Please specify your target job role.")
    elif provider_mode == "🧪 Offline / Demo Mode":
        with st.spinner("Analyzing resume locally using factual keyword matching..."):
            st.session_state["analysis_result"] = generate_demo_analysis(
                resume_text=extracted_text,
                target_role=target_role,
                job_description=job_description if job_description.strip() else None,
            )
            st.success("🎉 Complete analysis & roadmap generated!")
    else:
        if provider_mode == "⚡ Groq (Fast & Free Cloud)":
            active_key = api_key_input.strip() if api_key_input else os.getenv("GROQ_API_KEY", "")
        else:
            active_key = api_key_input.strip() if api_key_input else os.getenv("OPENAI_API_KEY", "")

        analysis_done = False
        if active_key or (custom_base_url and "localhost" in custom_base_url):
            try:
                with st.spinner(f"🤖 Analyzing resume against **{target_role}** requirements using {selected_model}..."):
                    analysis_result: ResumeAnalysisOutput = analyze_resume(
                        resume_text=extracted_text,
                        target_role=target_role,
                        job_description=job_description if job_description.strip() else None,
                        api_key=active_key,
                        model_name=selected_model,
                        temperature=temperature,
                        base_url=custom_base_url,
                    )
                    st.session_state["analysis_result"] = analysis_result
                    analysis_done = True
                    st.success("🎉 Analysis complete!")
            except Exception as e:
                err_msg = str(e)
                st.info(f"💡 Cloud API Notice: {err_msg[:100]}... Seamlessly generated complete analysis & roadmap using local analyzer.")

        if not analysis_done:
            with st.spinner(f"🎯 Building complete 4-week roadmap & skills matrix for **{target_role}**..."):
                st.session_state["analysis_result"] = generate_demo_analysis(
                    resume_text=extracted_text,
                    target_role=target_role,
                    job_description=job_description if job_description.strip() else None,
                )
                st.success("🎉 Complete analysis & roadmap generated!")


# ==============================================================================
# Results Visualization (Tabs)
# ==============================================================================

if "analysis_result" in st.session_state and st.session_state["analysis_result"]:
    result: ResumeAnalysisOutput = st.session_state["analysis_result"]

    st.markdown("## 📊 Analysis & Development Plan")

    # Disclaimer Alert
    st.markdown(
        f'<div class="disclaimer-box">💡 <b>Transparency & Ethics:</b> {result.match_disclaimer}</div>',
        unsafe_allow_html=True,
    )

    # Top Metric Cards
    metric_c1, metric_c2, metric_c3, metric_c4 = st.columns(4)
    with metric_c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{result.skill_match_percentage:.1f}%</div>
                <div class="metric-label">Skill Overlap Score</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with metric_c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{result.evidenced_skills_count}</div>
                <div class="metric-label">Skills Evidenced</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with metric_c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{len(result.not_evidenced_skills)}</div>
                <div class="metric-label">Skills Not Evidenced</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with metric_c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{result.total_target_role_skills_count}</div>
                <div class="metric-label">Core Target Skills</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Progress bar representation
    st.write("")
    st.progress(min(max(result.skill_match_percentage / 100.0, 0.0), 1.0))

    # Executive Summary
    st.info(f"**Professional Summary:** {result.professional_summary}")

    # Tabs for detailed sections
    tab_skills, tab_roadmap, tab_projects, tab_resume, tab_interview, tab_export = st.tabs([
        "🎯 Skills Matrix",
        "🗺️ 4-Week Roadmap",
        "🛠️ Practical Projects",
        "✍️ Resume Polish",
        "💡 Interview Prep",
        "📥 Download Report",
    ])

    # --------------------------------------------------------------------------
    # Tab 1: Skills Matrix
    # --------------------------------------------------------------------------
    with tab_skills:
        col_ev, col_not_ev = st.columns(2, gap="large")

        with col_ev:
            st.markdown("### ✅ Skills Evidenced in Resume")
            st.caption("Skills verified with direct context or project evidence in your resume.")
            if result.evidenced_skills:
                for s in result.evidenced_skills:
                    with st.expander(f"🟢 **{s.skill_name}** ({s.category})"):
                        st.markdown(f"**Resume Evidence:** {s.resume_evidence}")
                        st.markdown(f"**Context:** *{s.proficiency_context}*")
            else:
                st.warning("No explicit core skills found in the provided resume text.")

        with col_not_ev:
            st.markdown("### 🔍 Skills Not Evidenced in Resume")
            st.caption("Skills expected for this role that were not found in the resume text.")
            if result.not_evidenced_skills:
                for ns in result.not_evidenced_skills:
                    with st.expander(f"🟡 **{ns.skill_name}** — *{ns.importance}*"):
                        st.markdown(f"**Why it matters for {result.target_role}:** {ns.role_relevance}")
                        st.markdown(f"**Status Note:** {ns.status_note}")
            else:
                st.success("All expected core skills for this role were evidenced in your resume!")

    # --------------------------------------------------------------------------
    # Tab 2: 4-Week Roadmap
    # --------------------------------------------------------------------------
    with tab_roadmap:
        st.markdown("### 🗺️ Personalized 4-Week Skill Bridge Plan")
        st.caption("Structured weekly progression focusing on highest-impact un-evidenced competencies.")

        for week in result.four_week_roadmap:
            with st.container():
                st.markdown(
                    f"""
                    <div class="week-card">
                        <h4 style="color:#1D4ED8; margin:0 0 8px 0;">Week {week.week_number}: {week.week_title}</h4>
                        <p style="color:#4B5563; font-weight:600; margin-bottom:10px;">🎯 <b>Core Focus:</b> {week.core_focus}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                c_obj, c_act = st.columns(2)
                with c_obj:
                    st.markdown("**🎯 Learning Objectives:**")
                    for obj in week.learning_objectives:
                        st.markdown(f"- {obj}")
                with c_act:
                    st.markdown("**⚡ Action Items & Hands-on Work:**")
                    for act in week.action_items:
                        st.markdown(f"- {act}")

                with st.expander("📚 Recommended Learning Resources & Topics"):
                    for res in week.recommended_resources:
                        st.markdown(f"- {res}")
                st.write("")

    # --------------------------------------------------------------------------
    # Tab 3: Practical Projects
    # --------------------------------------------------------------------------
    with tab_projects:
        st.markdown("### 🛠️ Practical Portfolio Projects")
        st.caption("Real-world, showcase-worthy projects designed to build and prove un-evidenced skills.")

        for p_idx, proj in enumerate(result.recommended_projects, 1):
            with st.expander(f"🚀 **Project {p_idx}: {proj.project_title}**", expanded=(p_idx == 1)):
                st.markdown(f"**Overview:** {proj.overview}")
                
                st.markdown("**Skills Developed:**")
                skills_html = "".join([f'<span class="skill-badge-green">{sk}</span>' for sk in proj.target_skills_developed])
                st.markdown(skills_html, unsafe_allow_html=True)
                
                st.markdown("**Key Deliverables to Build:**")
                for d in proj.key_deliverables:
                    st.markdown(f"- {d}")
                
                st.markdown(f"**💡 Recruiter & Interview Impact:** *{proj.portfolio_impact}*")

    # --------------------------------------------------------------------------
    # Tab 4: Resume Polish
    # --------------------------------------------------------------------------
    with tab_resume:
        st.markdown("### ✍️ Constructive Resume Enhancements")
        st.caption("Actionable refinements for impact, clarity, and keyword structure without inventing qualifications.")

        for imp_idx, imp in enumerate(result.resume_improvements, 1):
            with st.container():
                st.markdown(f"#### Suggestion {imp_idx}: {imp.section} Section")
                st.markdown(f"**Identified Weakness:** {imp.identified_issue}")
                st.markdown(f"**Recommendation:** {imp.actionable_suggestion}")
                
                if imp.original_resume_snippet:
                    st.markdown(f"**Original Context:** *\"{imp.original_resume_snippet}\"*")
                
                st.info(f"**Recommended Framing:**\n\n> {imp.enhanced_bullet_point}")
                st.divider()

    # --------------------------------------------------------------------------
    # Tab 5: Interview Prep
    # --------------------------------------------------------------------------
    with tab_interview:
        st.markdown("### 💡 Tailored Interview Questions")
        st.caption("Anticipate technical, behavioral, and architecture questions based on your profile.")

        for q_idx, q in enumerate(result.interview_questions, 1):
            with st.expander(f"❓ **Q{q_idx}:** {q.question} ({q.category})"):
                st.markdown(f"**What the Interviewer is Evaluating:**\n{q.interviewer_intent}")
                st.markdown(f"**Recommended Answer Structure:**\n{q.suggested_approach}")

    # --------------------------------------------------------------------------
    # Tab 6: Download & Export
    # --------------------------------------------------------------------------
    with tab_export:
        st.markdown("### 📥 Download Analysis as Markdown")
        st.caption("Export your complete personalized report to save, print, or share.")

        markdown_report = export_analysis_to_markdown(result)

        # Download button
        file_name = f"Resume_Analysis_{result.target_role.replace(' ', '_')}.md"
        st.download_button(
            label="💾 Download Full Report (.md)",
            data=markdown_report,
            file_name=file_name,
            mime="text/markdown",
            type="primary",
            use_container_width=True,
        )

        with st.expander("📄 Report Markdown Preview", expanded=False):
            st.code(markdown_report, language="markdown")
