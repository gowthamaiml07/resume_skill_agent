"""
views_skill_gap.py
==================
Dedicated Skill Gap Analysis view: Comprehensive competency matrix, evidenced vs un-evidenced skills,
category filters, and evidence context.
Uses clean, unindented HTML for reliable rendering.
"""

from __future__ import annotations
import streamlit as st
from components.header import render_header
from components.cards import render_empty_state, render_ethical_disclaimer, render_metric_card


def render_skill_gap_view():
    """Renders the dedicated Skill Gap Analysis view."""
    if "analysis_result" not in st.session_state or not st.session_state["analysis_result"]:
        render_header(
            title="Skill Gap Matrix & Alignment",
            description="Deep dive into evidenced skills and key competencies required for your target role.",
            breadcrumb="Competencies • Skill Gap",
            status_text="No Active Analysis",
            status_type="neutral",
        )
        render_empty_state(
            title="No Active Skill Analysis Found",
            message="Please upload your PDF resume and run an analysis to view your customized skill gap breakdown.",
            action_label="Go to Resume Analysis",
            target_page="Resume Analysis",
        )
        return

    result = st.session_state["analysis_result"]

    render_header(
        title=f"Skill Gap Matrix • {result.target_role}",
        description="Detailed comparison of demonstrated competencies versus industry standards for your target position.",
        breadcrumb=f"Competencies • {result.target_role}",
        status_text=f"Match Score: {result.skill_match_percentage:.1f}%",
        status_type="emerald",
    )

    # Top Metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card(f"{result.skill_match_percentage:.1f}%", "Skill Overlap Score")
    with c2:
        render_metric_card(str(result.evidenced_skills_count), "Demonstrated Skills")
    with c3:
        render_metric_card(str(len(result.not_evidenced_skills)), "Skills to Bridge")

    st.write("")
    render_ethical_disclaimer(
        "Skills listed as 'Not Evidenced' mean explicit proof was not detected in the uploaded resume text. This is an objective audit of resume documentation, not a personal limitation."
    )

    # Two Main Columns: Evidenced vs Not Evidenced
    col_ev, col_not_ev = st.columns(2, gap="large")

    with col_ev:
        header_ev_html = (
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:0.75rem;">'
            '<div style="width:12px; height:12px; border-radius:50%; background-color:#16A34A; flex-shrink:0;"></div>'
            f'<h3 style="margin:0; font-size:1.25rem; font-weight:700; color:#111827;">Evidenced in Resume ({len(result.evidenced_skills)})</h3>'
            '</div>'
        )
        st.markdown(header_ev_html, unsafe_allow_html=True)
        st.caption("Skills backed by project, academic, or professional evidence in your resume text.")

        if result.evidenced_skills:
            categories = list(set(s.category for s in result.evidenced_skills))
            selected_cat = st.selectbox("Filter by Category", options=["All Categories"] + sorted(categories), key="filter_ev_cat")

            filtered_ev = (
                result.evidenced_skills
                if selected_cat == "All Categories"
                else [s for s in result.evidenced_skills if s.category == selected_cat]
            )

            for skill in filtered_ev:
                with st.expander(f"🟢 **{skill.skill_name}** — `{skill.category}`"):
                    st.markdown(f"**Resume Evidence:**\n\n> {skill.resume_evidence}")
                    st.markdown(f"**Context / Utilization:** *{skill.proficiency_context}*")
        else:
            st.info("No specific technical skills were explicitly identified in the parsed resume.")

    with col_not_ev:
        header_not_ev_html = (
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:0.75rem;">'
            '<div style="width:12px; height:12px; border-radius:50%; background-color:#D97706; flex-shrink:0;"></div>'
            f'<h3 style="margin:0; font-size:1.25rem; font-weight:700; color:#111827;">Skills to Bridge ({len(result.not_evidenced_skills)})</h3>'
            '</div>'
        )
        st.markdown(header_not_ev_html, unsafe_allow_html=True)
        st.caption("Standard competencies expected for this target role that were not found in the resume.")

        if result.not_evidenced_skills:
            priorities = ["All Priorities", "High Priority (Core)", "Medium Priority (Standard)", "Nice to Have (Bonus)"]
            selected_prio = st.selectbox("Filter by Priority", options=priorities, key="filter_not_ev_prio")

            filtered_not_ev = (
                result.not_evidenced_skills
                if selected_prio == "All Priorities"
                else [s for s in result.not_evidenced_skills if s.importance == selected_prio]
            )

            for skill in filtered_not_ev:
                is_high = "High" in skill.importance
                prio_bg = "#FEF2F2" if is_high else "#FFFBEB"
                prio_color = "#991B1B" if is_high else "#92400E"
                prio_border = "#FECACA" if is_high else "#FDE68A"

                with st.expander(f"🟡 **{skill.skill_name}** ({skill.importance})"):
                    prio_html = (
                        f'<span style="display:inline-block; background-color:{prio_bg}; color:{prio_color}; '
                        f'border:1px solid {prio_border}; font-size:0.78rem; font-weight:700; padding:2px 8px; '
                        f'border-radius:4px; text-transform:uppercase; margin-bottom:0.5rem;">{skill.importance}</span>'
                    )
                    st.markdown(prio_html, unsafe_allow_html=True)
                    st.markdown(f"**Role Relevance for {result.target_role}:**\n\n{skill.role_relevance}")
                    st.markdown(f"**Status:** *{skill.status_note}*")
        else:
            st.success("🎉 Outstanding! All core skills expected for this role were evidenced in your resume.")

    st.write("")
    st.markdown("---")

    # Action navigation
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🗺️ Open 4-Week Learning Roadmap to Bridge Gaps →", type="primary", use_container_width=True, key="gap_to_roadmap"):
            st.session_state.current_page = "Learning Roadmap"
            st.rerun()
    with col_nav2:
        if st.button("🛠️ View Practical Portfolio Projects →", type="secondary", use_container_width=True, key="gap_to_projects"):
            st.session_state.current_page = "Project Recommendations"
            st.rerun()
