"""
views_analysis.py
=================
Resume Analysis Page: Form input, PDF parsing with PyMuPDF, agent execution, and results overview.
Ensures reliable HTML rendering without accidental code block formatting.
"""

from __future__ import annotations
import streamlit as st
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
from config import (
    get_groq_api_key,
    get_groq_model,
    get_openai_api_key,
    get_openai_model,
)
from components.header import render_header
from components.cards import (
    render_metric_card,
    render_ethical_disclaimer,
    render_skill_badges_html,
)


def render_analysis_view():
    """Renders the Resume Analysis & Results view."""
    has_analysis = bool(st.session_state.get("analysis_result"))
    status_text = "Analysis Ready" if has_analysis else "Input Required"
    status_type = "emerald" if has_analysis else "neutral"

    render_header(
        title="Resume Analysis & Benchmark Evaluation",
        description="Upload your PDF resume and target role to extract verified competencies and identify growth areas.",
        breadcrumb="Workspace • Resume Analysis",
        status_text=status_text,
        status_type=status_type,
    )

    # Input Section Cards
    col_upload, col_target = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown("### 1. Upload Resume (PDF)")
        st.caption("Supports standard digital PDF resumes (max 10MB). Text is extracted in-memory.")

        uploaded_file = st.file_uploader(
            "Upload Resume PDF",
            type=["pdf"],
            help="Select a text-based PDF resume (exported from Google Docs, Word, or Canva).",
            label_visibility="collapsed",
            key="pdf_resume_uploader",
        )

        extracted_text = st.session_state.get("extracted_text", "")

        if uploaded_file is not None:
            # Check if file changed or not yet extracted
            file_bytes = uploaded_file.getvalue()
            current_file_name = uploaded_file.name
            
            if st.session_state.get("last_uploaded_name") != current_file_name or not extracted_text:
                try:
                    with st.spinner("Extracting text with PyMuPDF..."):
                        extracted_text = extract_text_from_pdf(file_bytes)
                        metadata = get_pdf_metadata(file_bytes)
                        st.session_state.extracted_text = extracted_text
                        st.session_state.pdf_metadata = metadata
                        st.session_state.last_uploaded_name = current_file_name
                except EmptyPDFError as e:
                    st.error(f"❌ **Empty File:** {str(e)}")
                    st.session_state.extracted_text = ""
                except ScannedPDFError as e:
                    st.warning(f"⚠️ **Scanned Document:** {str(e)}")
                    st.session_state.extracted_text = ""
                except ResumeParsingError as e:
                    st.error(f"❌ **Parsing Issue:** {str(e)}")
                    st.session_state.extracted_text = ""
                except Exception as e:
                    st.error(f"❌ **Error:** {str(e)}")
                    st.session_state.extracted_text = ""

        if st.session_state.get("extracted_text"):
            metadata = st.session_state.get("pdf_metadata", {})
            p_count = metadata.get("page_count", 1)
            w_count = metadata.get("word_count", 0)
            c_count = metadata.get("character_count", 0)
            
            extract_badge_html = (
                '<div style="background-color:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; '
                'padding:0.7rem 0.9rem; margin-top:0.5rem; font-size:0.88rem; color:#065F46; font-weight:600;">'
                f'✅ <b>Text Extracted:</b> {p_count} page(s) • ~{w_count} words • {c_count} characters'
                '</div>'
            )
            st.markdown(extract_badge_html, unsafe_allow_html=True)

            with st.expander("👁️ View Extracted Text Preview"):
                st.text_area("Extracted Plain Text", value=st.session_state.extracted_text, height=140, disabled=True)

    with col_target:
        st.markdown("### 2. Target Role & Details")
        st.caption("Specify your target position and optional job description for precise alignment.")

        # Quick Role Suggestions
        quick_roles = ["Python Developer", "Data Analyst", "Machine Learning Engineer", "DevOps Engineer"]
        if "target_role_input" not in st.session_state:
            st.session_state.target_role_input = "Python Developer"

        st.caption("Quick Suggestions:")
        cols_btn = st.columns(len(quick_roles))
        for i, role in enumerate(quick_roles):
            if cols_btn[i].button(role, key=f"analysis_quick_role_{i}"):
                st.session_state.target_role_input = role

        target_role = st.text_input(
            "Target Job Role *",
            value=st.session_state.target_role_input,
            placeholder="e.g., Senior Python Backend Developer, Data Scientist",
            key="target_role_field",
        )
        st.session_state.target_role_input = target_role

        job_description = st.text_area(
            "Target Job Description (Optional)",
            height=100,
            placeholder="Paste requirements or tech stack from a specific job description for fine-grained alignment...",
            key="job_description_field",
        )

    st.write("")

    # Provider status and action button
    provider_mode = st.session_state.get("provider_mode", "⚡ Groq (Fast & Free Cloud)")
    
    # Check key configuration status
    has_groq = bool(get_groq_api_key() or st.session_state.get("groq_api_key_override"))
    has_openai = bool(get_openai_api_key() or st.session_state.get("openai_api_key_override"))
    
    if provider_mode == "⚡ Groq (Fast & Free Cloud)" and not has_groq:
        provider_badge = "⚠️ Groq Key Not Detected (Add key in .streamlit/secrets.toml or Settings)"
    elif provider_mode == "⚡ Groq (Fast & Free Cloud)":
        provider_badge = f"⚡ Groq Cloud AI Active ({st.session_state.get('selected_model', get_groq_model())})"
    elif provider_mode == "🟢 OpenAI API" and not has_openai:
        provider_badge = "⚠️ OpenAI Key Not Detected (Add key in .streamlit/secrets.toml or Settings)"
    elif provider_mode == "🟢 OpenAI API":
        provider_badge = f"🟢 OpenAI Active ({st.session_state.get('selected_model', get_openai_model())})"
    else:
        provider_badge = "🧪 Offline / Demo Keyword Analyzer Active"

    col_btn_l, col_btn_mid, col_btn_r = st.columns([1, 2, 1])
    with col_btn_mid:
        badge_html = f'<div style="text-align:center; font-size:0.86rem; font-weight:700; color:#047857; margin-bottom:0.5rem;">{provider_badge}</div>'
        st.markdown(badge_html, unsafe_allow_html=True)

        can_analyze = bool(st.session_state.get("extracted_text") and target_role.strip())
        analyze_clicked = st.button(
            "🚀 Run AI Resume Analysis",
            type="primary",
            use_container_width=True,
            disabled=not can_analyze,
            key="run_analysis_action_btn",
        )
        if not can_analyze:
            st.caption("Upload a valid PDF resume and enter a target role to enable analysis.")

    # --------------------------------------------------------------------------
    # Execution Logic
    # --------------------------------------------------------------------------
    if analyze_clicked:
        extracted = st.session_state.get("extracted_text", "")
        role = target_role.strip()
        jd = job_description.strip() if job_description and job_description.strip() else None

        if not extracted:
            st.error("Please upload a valid, readable PDF resume.")
        elif not role:
            st.error("Please provide a target job role.")
        elif provider_mode == "🧪 Offline / Demo Mode":
            with st.spinner(f"Analyzing resume locally for {role} role requirements..."):
                res = generate_demo_analysis(
                    resume_text=extracted,
                    target_role=role,
                    job_description=jd,
                )
                st.session_state.analysis_result = res
                st.success("🎉 Complete analysis & roadmap generated!")
                st.rerun()
        else:
            is_groq = (provider_mode == "⚡ Groq (Fast & Free Cloud)")
            active_model = st.session_state.get("selected_model", get_groq_model() if is_groq else get_openai_model())
            temperature = float(st.session_state.get("temperature", 0.2))

            active_key = (
                (st.session_state.get("groq_api_key_override") or get_groq_api_key())
                if is_groq
                else (st.session_state.get("openai_api_key_override") or get_openai_api_key())
            )

            if not active_key:
                prov_label = "Groq" if is_groq else "OpenAI"
                secret_var = "GROQ_API_KEY" if is_groq else "OPENAI_API_KEY"
                st.error(
                    f"❌ **{prov_label} API Key Missing:** Please add your key to `.streamlit/secrets.toml` "
                    f"(`{secret_var} = \"...\"`) or set the `{secret_var}` environment variable in `.env`. "
                    f"Alternatively, switch to **Offline / Demo Mode** in the sidebar settings."
                )
            else:
                try:
                    with st.spinner(f"Analyzing resume against {role} requirements using {active_model}..."):
                        res = analyze_resume(
                            resume_text=extracted,
                            target_role=role,
                            job_description=jd,
                            api_key=active_key,
                            model_name=active_model,
                            temperature=temperature,
                            is_groq=is_groq,
                        )
                        st.session_state.analysis_result = res
                        st.success("🎉 Analysis completed successfully!")
                        st.rerun()
                except Exception as e:
                    err_msg = str(e)
                    st.error(f"❌ **Analysis Error:** {err_msg}")
                    st.info(
                        "💡 **Troubleshooting Tip:** If you are testing without API credits, switch to "
                        "**Offline / Demo Mode** in Settings & About to test the full analysis pipeline instantly."
                    )

    # --------------------------------------------------------------------------
    # Results Display
    # --------------------------------------------------------------------------
    if "analysis_result" in st.session_state and st.session_state["analysis_result"]:
        result: ResumeAnalysisOutput = st.session_state["analysis_result"]

        st.markdown("---")
        st.markdown("## 📊 Executive Results Overview")

        # Metric Cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card(f"{result.skill_match_percentage:.1f}%", "Skill Overlap Score")
        with c2:
            render_metric_card(str(result.evidenced_skills_count), "Skills Evidenced")
        with c3:
            render_metric_card(str(len(result.not_evidenced_skills)), "Skills Not Evidenced")
        with c4:
            render_metric_card(str(result.total_target_role_skills_count), "Core Target Skills")

        # Progress bar
        st.write("")
        st.progress(min(max(result.skill_match_percentage / 100.0, 0.0), 1.0))

        # Ethical Disclaimer
        render_ethical_disclaimer(result.match_disclaimer)

        # Professional Assessment Summary (Unindented HTML)
        summary_html = (
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; '
            'padding:1.4rem; margin-bottom:1.25rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">'
            '<h4 style="color:#059669; margin:0 0 0.5rem 0; font-size:1.15rem; font-weight:700;">Professional Assessment</h4>'
            f'<p style="color:#1F2937; font-size:0.98rem; line-height:1.65; margin:0;">{result.professional_summary}</p>'
            '</div>'
        )
        st.markdown(summary_html, unsafe_allow_html=True)

        # Quick Navigation Links to Deep Dive Pages
        st.markdown("### 🧭 Detailed Analysis Modules")
        st.caption("Access dedicated sections for deep-dive analysis, weekly roadmaps, projects, and interview prep.")

        d_col1, d_col2, d_col3, d_col4 = st.columns(4)
        with d_col1:
            if st.button("🎯 Skill Gap Matrix →", use_container_width=True, key="res_to_skill_gap"):
                st.session_state.current_page = "Skill Gap Analysis"
                st.rerun()
        with d_col2:
            if st.button("🗺️ 4-Week Roadmap →", use_container_width=True, key="res_to_roadmap"):
                st.session_state.current_page = "Learning Roadmap"
                st.rerun()
        with d_col3:
            if st.button("🛠️ Project Ideas →", use_container_width=True, key="res_to_projects"):
                st.session_state.current_page = "Project Recommendations"
                st.rerun()
        with d_col4:
            if st.button("💡 Interview Prep →", use_container_width=True, key="res_to_interview"):
                st.session_state.current_page = "Interview Preparation"
                st.rerun()

        st.write("")

        # Overview Tabs
        ov_tab1, ov_tab2, ov_tab3 = st.tabs([
            "📋 Skills Snapshot",
            "✍️ Resume Polish Suggestions",
            "📥 Export Report (.md)",
        ])

        with ov_tab1:
            col_e, col_ne = st.columns(2, gap="large")
            with col_e:
                st.markdown(f"#### ✅ Evidenced Skills ({len(result.evidenced_skills)})")
                if result.evidenced_skills:
                    for s in result.evidenced_skills:
                        st.markdown(f"**{s.skill_name}** (`{s.category}`)")
                        st.caption(f"Context: {s.proficiency_context}")
                else:
                    st.caption("No explicit matching skills found.")

            with col_ne:
                st.markdown(f"#### 🔍 Not Evidenced Skills ({len(result.not_evidenced_skills)})")
                if result.not_evidenced_skills:
                    for s in result.not_evidenced_skills:
                        st.markdown(f"**{s.skill_name}** — *{s.importance}*")
                        st.caption(s.role_relevance)
                else:
                    st.success("All expected key skills were evidenced!")

        with ov_tab2:
            st.markdown("#### ✍️ Constructive Resume Phrasing Enhancements")
            st.caption("Suggestions to improve clarity and impact without inventing claims or credentials.")
            for idx, imp in enumerate(result.resume_improvements, 1):
                with st.expander(f"Recommendation {idx}: {imp.section} Section", expanded=(idx == 1)):
                    st.markdown(f"**Observation:** {imp.identified_issue}")
                    st.markdown(f"**Advice:** {imp.actionable_suggestion}")
                    if imp.original_resume_snippet:
                        st.markdown(f"**Original Text:** *\"{imp.original_resume_snippet}\"*")
                    st.info(f"**Suggested Rewording:**\n\n> {imp.enhanced_bullet_point}")

        with ov_tab3:
            st.markdown("#### 📥 Export Full Analysis Report")
            st.caption("Download the complete analysis, roadmap, projects, and interview questions as GitHub-flavored Markdown.")

            md_content = export_analysis_to_markdown(result)
            filename = f"Resume_Analysis_{result.target_role.replace(' ', '_')}.md"

            st.download_button(
                label="💾 Download Full Report (.md)",
                data=md_content,
                file_name=filename,
                mime="text/markdown",
                type="primary",
                use_container_width=True,
                key="download_report_btn",
            )

            with st.expander("📄 Report Preview", expanded=False):
                st.code(md_content, language="markdown")
