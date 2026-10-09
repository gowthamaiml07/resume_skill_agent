"""
views_home.py
=============
Home Dashboard View: Hero banner, core value proposition, 5 feature cards, and active session status.
Uses clean, unindented HTML markup with high text contrast.
"""

from __future__ import annotations
import streamlit as st
from components.header import render_header
from components.cards import render_ethical_disclaimer, render_metric_card


def render_home_view():
    """Renders the Home Dashboard page."""
    has_analysis = bool(st.session_state.get("analysis_result"))
    status_text = "Analysis Ready" if has_analysis else "Ready for Upload"
    status_type = "emerald" if has_analysis else "neutral"

    render_header(
        title="AI Career & Skill Development Studio",
        description="Accelerate your professional trajectory with ethical AI-powered resume intelligence.",
        breadcrumb="Home • Overview",
        status_text=status_text,
        status_type=status_type,
    )

    # Hero Banner
    hero_html = (
        '<div style="background:linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%); '
        'border:1px solid #A7F3D0; border-radius:16px; padding:2rem 2.25rem; margin-bottom:1.75rem; '
        'box-shadow:0 2px 8px rgba(5, 150, 105, 0.07);">'
        '<div style="max-width:780px;">'
        '<div style="display:inline-block; background-color:#D1FAE5; color:#065F46; font-size:0.82rem; '
        'font-weight:700; padding:4px 12px; border-radius:9999px; margin-bottom:0.85rem; border:1px solid #A7F3D0;">'
        '✨ INTELLIGENT CAREER ACCELERATOR'
        '</div>'
        '<h2 style="font-size:2.2rem; font-weight:800; color:#111827; margin:0 0 0.75rem 0; line-height:1.2;">'
        'Build Your Career with AI'
        '</h2>'
        '<p style="font-size:1.05rem; color:#374151; line-height:1.65; margin:0 0 1.25rem 0;">'
        'Analyze your resume, discover skill gaps, and create a personalized learning plan for your target role. '
        'Receive honest, evidence-based feedback without exaggerated claims or fabricated qualifications.'
        '</p>'
        '</div>'
        '</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # Main Action Row
    col_cta1, col_cta2, col_cta3 = st.columns([1.5, 1.5, 1])
    with col_cta1:
        if st.button("🚀 Analyze My Resume", type="primary", use_container_width=True, key="home_hero_analyze_btn"):
            st.session_state.current_page = "Resume Analysis"
            st.rerun()
    with col_cta2:
        if has_analysis:
            if st.button("🗺️ View Active 4-Week Roadmap", type="secondary", use_container_width=True, key="home_hero_roadmap_btn"):
                st.session_state.current_page = "Learning Roadmap"
                st.rerun()
        else:
            if st.button("⚙️ Configure API / Demo Mode", type="secondary", use_container_width=True, key="home_hero_settings_btn"):
                st.session_state.current_page = "Settings & About"
                st.rerun()

    st.write("")

    # Active Analysis Overview if available
    if has_analysis:
        result = st.session_state["analysis_result"]
        st.markdown("### 📊 Current Analysis Snapshot")
        snap_col1, snap_col2, snap_col3, snap_col4 = st.columns(4)
        with snap_col1:
            render_metric_card(f"{result.skill_match_percentage:.1f}%", "Skill Match Score")
        with snap_col2:
            render_metric_card(str(result.evidenced_skills_count), "Skills Evidenced")
        with snap_col3:
            render_metric_card(str(len(result.not_evidenced_skills)), "Skills to Bridge")
        with snap_col4:
            render_metric_card(str(result.total_target_role_skills_count), "Role Benchmarks")

        st.info(f"**Target Role:** {result.target_role} • **Summary:** {result.professional_summary}")
        st.write("")

    # 5 Feature Cards Grid
    st.markdown("### 🌟 Platform Capabilities")
    st.caption("Comprehensive tools tailored for technical and professional career development.")

    row1_c1, row1_c2, row1_c3 = st.columns(3)

    with row1_c1:
        card1_html = (
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:1.4rem; '
            'box-shadow:0 1px 3px rgba(0,0,0,0.03); margin-bottom:0.75rem;">'
            '<div style="width:42px; height:42px; border-radius:10px; background-color:#ECFDF5; color:#059669; '
            'display:flex; align-items:center; justify-content:center; margin-bottom:0.85rem; border:1px solid #A7F3D0;">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
            '<polyline points="14 2 14 8 20 8"></polyline>'
            '</svg>'
            '</div>'
            '<div style="font-size:1.15rem; font-weight:700; color:#111827; margin-bottom:0.4rem;">1. Resume Analysis</div>'
            '<div style="font-size:0.92rem; color:#4B5563; line-height:1.5; min-height:55px;">Upload your digital PDF resume to extract competencies and evaluate alignment against target job roles.</div>'
            '</div>'
        )
        st.markdown(card1_html, unsafe_allow_html=True)
        if st.button("Open Resume Analysis →", key="feat_btn_1", use_container_width=True):
            st.session_state.current_page = "Resume Analysis"
            st.rerun()

    with row1_c2:
        card2_html = (
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:1.4rem; '
            'box-shadow:0 1px 3px rgba(0,0,0,0.03); margin-bottom:0.75rem;">'
            '<div style="width:42px; height:42px; border-radius:10px; background-color:#ECFDF5; color:#059669; '
            'display:flex; align-items:center; justify-content:center; margin-bottom:0.85rem; border:1px solid #A7F3D0;">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="10"></circle>'
            '<circle cx="12" cy="12" r="6"></circle>'
            '<circle cx="12" cy="12" r="2"></circle>'
            '</svg>'
            '</div>'
            '<div style="font-size:1.15rem; font-weight:700; color:#111827; margin-bottom:0.4rem;">2. Skill Gap Analysis</div>'
            '<div style="font-size:0.92rem; color:#4B5563; line-height:1.5; min-height:55px;">Discover evidenced competencies and identify key skills expected for the role that are not yet showcased.</div>'
            '</div>'
        )
        st.markdown(card2_html, unsafe_allow_html=True)
        if st.button("Open Skill Gap Matrix →", key="feat_btn_2", use_container_width=True):
            st.session_state.current_page = "Skill Gap Analysis"
            st.rerun()

    with row1_c3:
        card3_html = (
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:1.4rem; '
            'box-shadow:0 1px 3px rgba(0,0,0,0.03); margin-bottom:0.75rem;">'
            '<div style="width:42px; height:42px; border-radius:10px; background-color:#ECFDF5; color:#059669; '
            'display:flex; align-items:center; justify-content:center; margin-bottom:0.85rem; border:1px solid #A7F3D0;">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>'
            '<line x1="8" y1="2" x2="8" y2="18"></line>'
            '</svg>'
            '</div>'
            '<div style="font-size:1.15rem; font-weight:700; color:#111827; margin-bottom:0.4rem;">3. Four-Week Roadmap</div>'
            '<div style="font-size:0.92rem; color:#4B5563; line-height:1.5; min-height:55px;">A structured step-by-step curriculum featuring weekly goals, action items, hands-on tasks, and resources.</div>'
            '</div>'
        )
        st.markdown(card3_html, unsafe_allow_html=True)
        if st.button("Open Learning Roadmap →", key="feat_btn_3", use_container_width=True):
            st.session_state.current_page = "Learning Roadmap"
            st.rerun()

    st.write("")

    row2_c1, row2_c2 = st.columns(2)

    with row2_c1:
        card4_html = (
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:1.4rem; '
            'box-shadow:0 1px 3px rgba(0,0,0,0.03); margin-bottom:0.75rem;">'
            '<div style="width:42px; height:42px; border-radius:10px; background-color:#ECFDF5; color:#059669; '
            'display:flex; align-items:center; justify-content:center; margin-bottom:0.85rem; border:1px solid #A7F3D0;">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<polyline points="16 18 22 12 16 6"></polyline>'
            '<polyline points="8 6 2 12 8 18"></polyline>'
            '</svg>'
            '</div>'
            '<div style="font-size:1.15rem; font-weight:700; color:#111827; margin-bottom:0.4rem;">4. Recommended Projects</div>'
            '<div style="font-size:0.92rem; color:#4B5563; line-height:1.5; min-height:50px;">Explore practical, portfolio-grade project specifications designed to build, verify, and showcase un-evidenced skills.</div>'
            '</div>'
        )
        st.markdown(card4_html, unsafe_allow_html=True)
        if st.button("Open Project Ideas →", key="feat_btn_4", use_container_width=True):
            st.session_state.current_page = "Project Recommendations"
            st.rerun()

    with row2_c2:
        card5_html = (
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:1.4rem; '
            'box-shadow:0 1px 3px rgba(0,0,0,0.03); margin-bottom:0.75rem;">'
            '<div style="width:42px; height:42px; border-radius:10px; background-color:#ECFDF5; color:#059669; '
            'display:flex; align-items:center; justify-content:center; margin-bottom:0.85rem; border:1px solid #A7F3D0;">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>'
            '</svg>'
            '</div>'
            '<div style="font-size:1.15rem; font-weight:700; color:#111827; margin-bottom:0.4rem;">5. Interview Preparation</div>'
            '<div style="font-size:0.92rem; color:#4B5563; line-height:1.5; min-height:50px;">Prepare with tailored technical, architecture, and STAR-method behavioral questions crafted for your target role.</div>'
            '</div>'
        )
        st.markdown(card5_html, unsafe_allow_html=True)
        if st.button("Open Interview Prep →", key="feat_btn_5", use_container_width=True):
            st.session_state.current_page = "Interview Preparation"
            st.rerun()

    st.write("")
    render_ethical_disclaimer(
        "This platform processes resumes in-memory with strict ethical guidelines. Skills absent from the resume are categorized as 'Not Evidenced' rather than assuming candidate incapacity."
    )
