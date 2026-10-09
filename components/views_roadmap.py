"""
views_roadmap.py
================
Dedicated 4-Week Learning Roadmap view: Progressive timeline, weekly objectives,
actionable exercises, curated resources, and session-based task progress tracking.
Uses clean, unindented HTML for reliable rendering.
"""

from __future__ import annotations
import streamlit as st
from components.header import render_header
from components.cards import render_empty_state


def render_roadmap_view():
    """Renders the 4-Week Learning Roadmap view."""
    if "analysis_result" not in st.session_state or not st.session_state["analysis_result"]:
        render_header(
            title="Personalized 4-Week Learning Roadmap",
            description="Step-by-step curriculum designed to bridge missing competencies for your target role.",
            breadcrumb="Curriculum • Learning Roadmap",
            status_text="No Active Roadmap",
            status_type="neutral",
        )
        render_empty_state(
            title="No Active Learning Roadmap Found",
            message="Upload your resume and analyze your target career role to generate a personalized 4-week learning plan.",
            action_label="Generate My Roadmap",
            target_page="Resume Analysis",
        )
        return

    result = st.session_state["analysis_result"]

    render_header(
        title=f"4-Week Skill Bridge Plan • {result.target_role}",
        description="Structured, week-by-week curriculum prioritizing high-impact un-evidenced competencies.",
        breadcrumb=f"Curriculum • {result.target_role}",
        status_text="4-Week Plan Active",
        status_type="emerald",
    )

    # Initialize progress tracker in session state if needed
    if "roadmap_progress" not in st.session_state:
        st.session_state.roadmap_progress = {}

    total_tasks = sum(len(w.action_items) for w in result.four_week_roadmap)
    completed_tasks = sum(1 for v in st.session_state.roadmap_progress.values() if v)
    progress_pct = (completed_tasks / total_tasks * 100.0) if total_tasks > 0 else 0.0

    # Progress Header Card (Unindented HTML)
    prog_html = (
        '<div style="background:linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%); border:1px solid #A7F3D0; '
        'border-radius:12px; padding:1.25rem 1.4rem; margin-bottom:1.25rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">'
        '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">'
        '<span style="font-size:1.05rem; font-weight:700; color:#111827;">Roadmap Progress (Session Tracking)</span>'
        f'<span style="font-size:1.02rem; font-weight:800; color:#047857;">{completed_tasks} / {total_tasks} Tasks Completed ({progress_pct:.0f}%)</span>'
        '</div>'
        '</div>'
    )
    st.markdown(prog_html, unsafe_allow_html=True)
    st.progress(min(max(progress_pct / 100.0, 0.0), 1.0))
    st.caption("Note: Task completion checkboxes are stored for your current browser session.")

    st.write("")

    # Weekly Progression Cards
    for week in result.four_week_roadmap:
        w_num = week.week_number
        week_html = (
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-left:5px solid #059669; '
            'border-radius:10px; padding:1.25rem 1.4rem; margin-bottom:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">'
            '<div style="display:flex; align-items:center; gap:10px; margin-bottom:0.75rem; padding-bottom:0.5rem; border-bottom:1px solid #F3F4F6;">'
            f'<span style="background-color:#059669; color:#FFFFFF; font-weight:800; font-size:0.86rem; padding:3px 10px; border-radius:6px;">WEEK {w_num}</span>'
            f'<span style="font-size:1.2rem; font-weight:700; color:#047857;">{week.week_title}</span>'
            '</div>'
            '<div style="font-size:0.95rem; font-weight:600; color:#1F2937; background-color:#F8FAFC; padding:0.6rem 0.85rem; border-radius:6px; border:1px solid #E5E7EB;">'
            f'🎯 <b>Core Focus:</b> {week.core_focus}'
            '</div>'
            '</div>'
        )
        st.markdown(week_html, unsafe_allow_html=True)

        col_obj, col_act = st.columns(2, gap="large")

        with col_obj:
            st.markdown("#### 🎯 Learning Objectives")
            for obj in week.learning_objectives:
                st.markdown(f"- **{obj}**")

        with col_act:
            st.markdown("#### ⚡ Hands-On Action Items")
            for act_idx, act in enumerate(week.action_items):
                key_id = f"task_w{w_num}_{act_idx}"
                is_checked = st.checkbox(
                    act,
                    value=st.session_state.roadmap_progress.get(key_id, False),
                    key=key_id,
                )
                st.session_state.roadmap_progress[key_id] = is_checked

        with st.expander(f"📚 Recommended Topics & Resources for Week {w_num}"):
            for res in week.recommended_resources:
                st.markdown(f"- 📖 **{res}**")

        st.write("")
        st.markdown("---")

    # Bottom Actions
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button("🛠️ Check Recommended Practical Projects →", type="primary", use_container_width=True, key="road_to_proj"):
            st.session_state.current_page = "Project Recommendations"
            st.rerun()
    with b_col2:
        if st.button("💡 Practice Interview Preparation Questions →", type="secondary", use_container_width=True, key="road_to_int"):
            st.session_state.current_page = "Interview Preparation"
            st.rerun()
