"""
views_interview.py
==================
Interview Preparation View: Categorized technical, architectural, and behavioral questions
with interviewer intent and strategic response formulation frameworks.
Uses clean, unindented HTML for reliable rendering.
"""

from __future__ import annotations
import streamlit as st
from components.header import render_header
from components.cards import render_empty_state


def render_interview_view():
    """Renders the Interview Preparation view."""
    if "analysis_result" not in st.session_state or not st.session_state["analysis_result"]:
        render_header(
            title="Role-Specific Interview Preparation",
            description="Tailored technical, behavioral, and architectural questions tailored to your profile.",
            breadcrumb="Preparation • Interview Readiness",
            status_text="No Active Analysis",
            status_type="neutral",
        )
        render_empty_state(
            title="No Active Interview Questions Found",
            message="Analyze your resume against your target role to generate realistic interview questions and answering strategies.",
            action_label="Run Resume Analysis to Prepare",
            target_page="Resume Analysis",
        )
        return

    result = st.session_state["analysis_result"]

    render_header(
        title=f"Interview Readiness Suite • {result.target_role}",
        description="Comprehensive technical deep-dives, architecture questions, and behavioral STAR prompts tailored to your profile.",
        breadcrumb=f"Preparation • {result.target_role}",
        status_text=f"{len(result.interview_questions)} Questions Ready",
        status_type="emerald",
    )

    # Categories filter
    all_categories = sorted(list(set(q.category for q in result.interview_questions)))
    selected_cat = st.selectbox(
        "Filter by Question Category",
        options=["All Question Types"] + all_categories,
        key="filter_interview_cat",
    )

    filtered_questions = (
        result.interview_questions
        if selected_cat == "All Question Types"
        else [q for q in result.interview_questions if q.category == selected_cat]
    )

    st.write("")

    for idx, q in enumerate(filtered_questions, 1):
        with st.expander(f"❓ **Question {idx}:** {q.question}", expanded=(idx == 1)):
            tag_html = (
                f'<span style="display:inline-block; background-color:#ECFDF5; color:#047857; '
                f'border:1px solid #A7F3D0; font-size:0.78rem; font-weight:700; padding:2px 8px; '
                f'border-radius:4px; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:0.6rem;">{q.category}</span>'
            )
            st.markdown(tag_html, unsafe_allow_html=True)
            
            st.markdown("#### 🎯 What the Interviewer is Evaluating")
            st.markdown(f"*{q.interviewer_intent}*")
            
            st.markdown("#### 💡 Recommended Answer Formulation Strategy")
            st.info(f"{q.suggested_approach}")

    st.write("")
    st.markdown("---")

    # STAR Framework Guide
    with st.expander("📖 Pro-Tip: Mastering the STAR Method for Technical & Behavioral Interviews"):
        st.markdown(
            """
            - **Situation (S):** Set the scene and provide necessary context of the challenge or business problem.
            - **Task (T):** Clearly explain your specific role, responsibilities, and constraints.
            - **Action (A):** Detail the exact engineering decisions, algorithms, tools, and methodologies you applied.
            - **Result (R):** Share quantifiable outcomes, lessons learned, and system performance improvements.
            """
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗺️ Return to Learning Roadmap", type="secondary", use_container_width=True, key="int_to_road"):
            st.session_state.current_page = "Learning Roadmap"
            st.rerun()
    with col2:
        if st.button("📄 View Full Analysis & Export Report →", type="primary", use_container_width=True, key="int_to_ana"):
            st.session_state.current_page = "Resume Analysis"
            st.rerun()
