"""
navigation.py
=============
Sidebar navigation component with brand identity, working route switching, and session indicators.
Uses clean, unindented HTML for reliable rendering.
"""

from __future__ import annotations
import streamlit as st


NAV_ITEMS = [
    {
        "id": "Home",
        "label": "Home",
    },
    {
        "id": "Resume Analysis",
        "label": "Resume Analysis",
    },
    {
        "id": "Skill Gap Analysis",
        "label": "Skill Gap Analysis",
    },
    {
        "id": "Learning Roadmap",
        "label": "Learning Roadmap",
    },
    {
        "id": "Project Recommendations",
        "label": "Project Recommendations",
    },
    {
        "id": "Interview Preparation",
        "label": "Interview Preparation",
    },
    {
        "id": "Settings & About",
        "label": "Settings & About",
    },
]


def render_sidebar_navigation() -> str:
    """
    Renders the sidebar brand and working navigation menu.
    Returns the currently active page.
    """
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    with st.sidebar:
        # Brand Header (Unindented HTML)
        brand_html = (
            '<div style="display:flex; align-items:center; gap:12px; padding:0.5rem 0.25rem 1.25rem 0.25rem; '
            'margin-bottom:0.75rem; border-bottom:1px solid #E5E7EB;">'
            '<div style="width:38px; height:38px; background:linear-gradient(135deg, #059669 0%, #047857 100%); '
            'border-radius:10px; display:flex; align-items:center; justify-content:center; color:#FFFFFF; '
            'box-shadow:0 2px 4px rgba(5,150,105,0.25); flex-shrink:0;">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>'
            '<path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>'
            '</svg>'
            '</div>'
            '<div>'
            '<div style="font-size:1.1rem; font-weight:800; color:#111827; line-height:1.2;">Career Agent AI</div>'
            '<div style="font-size:0.78rem; color:#059669; font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">Resume & Skill Studio</div>'
            '</div>'
            '</div>'
        )
        st.markdown(brand_html, unsafe_allow_html=True)

        st.caption("NAVIGATION")

        current = st.session_state.current_page

        for item in NAV_ITEMS:
            page_id = item["id"]
            is_active = (current == page_id)
            btn_label = f"● {item['label']}" if is_active else f"   {item['label']}"
            btn_type = "primary" if is_active else "secondary"

            if st.button(
                btn_label,
                key=f"nav_btn_{page_id.replace(' ', '_')}",
                use_container_width=True,
                type=btn_type,
            ):
                st.session_state.current_page = page_id
                st.rerun()

        # Session Status Snapshot
        st.write("")
        st.caption("SESSION STATUS")
        has_analysis = bool(st.session_state.get("analysis_result"))

        if has_analysis:
            res = st.session_state["analysis_result"]
            status_card_html = (
                '<div style="background-color:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; '
                'padding:0.75rem 0.85rem; margin-top:0.25rem;">'
                '<div style="font-size:0.78rem; font-weight:700; color:#047857; text-transform:uppercase;">Active Analysis</div>'
                f'<div style="font-size:0.92rem; font-weight:700; color:#111827; margin-top:2px;">{res.target_role}</div>'
                f'<div style="font-size:0.84rem; color:#065F46; font-weight:600; margin-top:4px;">Match: {res.skill_match_percentage:.1f}% ({res.evidenced_skills_count}/{res.total_target_role_skills_count} Skills)</div>'
                '</div>'
            )
            st.markdown(status_card_html, unsafe_allow_html=True)
        else:
            empty_status_html = (
                '<div style="background-color:#F8FAFC; border:1px solid #E5E7EB; border-radius:8px; '
                'padding:0.75rem 0.85rem; margin-top:0.25rem;">'
                '<div style="font-size:0.78rem; font-weight:700; color:#4B5563; text-transform:uppercase;">No Resume Loaded</div>'
                '<div style="font-size:0.84rem; color:#6B7280; margin-top:2px;">Upload a PDF to begin</div>'
                '</div>'
            )
            st.markdown(empty_status_html, unsafe_allow_html=True)

        st.divider()

        # Quick Actions
        if st.button("🔄 Reset Application", use_container_width=True, key="sidebar_reset_btn"):
            st.session_state.clear()
            st.session_state.current_page = "Home"
            st.rerun()

        st.caption("v2.0 • Emerald Career Platform")

    return st.session_state.current_page
