"""
views_projects.py
=================
Recommended Projects View: Portfolio-grade project specifications designed to build
and showcase un-evidenced competencies for hiring managers.
Uses clean, unindented HTML for reliable rendering.
"""

from __future__ import annotations
import streamlit as st
from components.header import render_header
from components.cards import render_empty_state, render_skill_badges_html


def render_projects_view():
    """Renders the Recommended Projects view."""
    if "analysis_result" not in st.session_state or not st.session_state["analysis_result"]:
        render_header(
            title="Portfolio Project Recommendations",
            description="Practical, real-world project specifications designed to build and prove target skills.",
            breadcrumb="Portfolio • Project Ideas",
            status_text="No Active Analysis",
            status_type="neutral",
        )
        render_empty_state(
            title="No Active Project Ideas Found",
            message="Analyze your resume against your target role to generate tailored portfolio project specifications.",
            action_label="Analyze Resume to Generate Projects",
            target_page="Resume Analysis",
        )
        return

    result = st.session_state["analysis_result"]

    render_header(
        title=f"Portfolio Project Blueprints • {result.target_role}",
        description="End-to-end practical project ideas designed to build and demonstrate missing competencies on GitHub and portfolio.",
        breadcrumb=f"Portfolio • {result.target_role}",
        status_text=f"{len(result.recommended_projects)} Projects Available",
        status_type="emerald",
    )

    st.markdown("### 🛠️ Targeted Portfolio Specifications")
    st.caption("Each project is specifically tailored to bridge un-evidenced competencies identified in your resume.")

    for idx, proj in enumerate(result.recommended_projects, 1):
        badges_html = render_skill_badges_html(proj.target_skills_developed, badge_type="matched")

        deliverables_html = "".join([
            '<div style="display:flex; align-items:flex-start; gap:8px; margin-bottom:0.45rem;">'
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0; margin-top:2px;">'
            '<polyline points="20 6 9 17 4 12"></polyline>'
            '</svg>'
            f'<span style="color:#1F2937; font-size:0.95rem; line-height:1.5;">{d}</span>'
            '</div>'
            for d in proj.key_deliverables
        ])

        card_html = (
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:1.5rem; '
            'margin-bottom:1.5rem; box-shadow:0 1px 4px rgba(0,0,0,0.03);">'
            '<div style="display:flex; align-items:center; gap:10px; margin-bottom:0.75rem;">'
            f'<span style="background-color:#ECFDF5; color:#047857; font-weight:800; font-size:0.84rem; padding:3px 10px; border-radius:6px; border:1px solid #A7F3D0;">PROJECT 0{idx}</span>'
            f'<h3 style="font-size:1.28rem; font-weight:700; color:#111827; margin:0;">{proj.project_title}</h3>'
            '</div>'
            f'<p style="color:#374151; font-size:0.98rem; line-height:1.65; margin-bottom:1rem;">{proj.overview}</p>'
            '<div style="margin-bottom:1rem;">'
            '<strong style="font-size:0.86rem; color:#111827; text-transform:uppercase; letter-spacing:0.04em;">Target Skills Built:</strong>'
            f'<div style="margin-top:0.4rem;">{badges_html}</div>'
            '</div>'
            '<div style="margin-bottom:1rem;">'
            '<strong style="font-size:0.86rem; color:#111827; text-transform:uppercase; letter-spacing:0.04em;">Core Deliverables to Implement:</strong>'
            f'<div style="margin-top:0.45rem;">{deliverables_html}</div>'
            '</div>'
            '<div style="background-color:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; padding:0.85rem 1.1rem; color:#065F46; font-size:0.92rem; margin-top:1rem;">'
            '<div style="display:flex; align-items:flex-start; gap:8px;">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#047857" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0; margin-top:1px;">'
            '<circle cx="12" cy="12" r="10"></circle>'
            '<line x1="12" y1="16" x2="12" y2="12"></line>'
            '<line x1="12" y1="8" x2="12.01" y2="8"></line>'
            '</svg>'
            '<div>'
            '<strong style="color:#047857;">Recruiter & Interviewer Impact:</strong> '
            f'<span style="color:#065F46;">{proj.portfolio_impact}</span>'
            '</div>'
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
        st.write("")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗺️ Back to 4-Week Learning Roadmap", type="secondary", use_container_width=True, key="proj_to_road"):
            st.session_state.current_page = "Learning Roadmap"
            st.rerun()
    with col2:
        if st.button("💡 Practice Role Interview Questions →", type="primary", use_container_width=True, key="proj_to_int"):
            st.session_state.current_page = "Interview Preparation"
            st.rerun()
