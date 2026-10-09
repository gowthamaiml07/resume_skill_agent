"""
cards.py
========
Reusable UI components: high-contrast metric cards, empty states, skill badges, and disclaimers.
Constructs unindented HTML to ensure reliable rendering in Streamlit.
"""

from __future__ import annotations
from typing import List, Optional
import streamlit as st


def render_metric_card(value: str, label: str, icon_svg: Optional[str] = None):
    """Renders a single high-contrast emerald metric card."""
    card_html = (
        '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-top:4px solid #059669; '
        'border-radius:12px; padding:1.25rem 1rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04); margin-bottom:0.75rem;">'
        f'<div style="font-size:2.25rem; font-weight:800; color:#059669; line-height:1.15; margin-bottom:4px;">{value}</div>'
        f'<div style="font-size:0.82rem; font-weight:700; color:#374151; text-transform:uppercase; letter-spacing:0.04em;">{label}</div>'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)


def render_empty_state(
    title: str,
    message: str,
    action_label: Optional[str] = "Analyze Resume Now",
    target_page: str = "Resume Analysis",
):
    """
    Renders an informative, modern empty state when analysis data is not yet available.
    """
    empty_html = (
        '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:14px; '
        'text-align:center; padding:3rem 2rem; max-width:680px; margin:2rem auto 1.5rem auto; box-shadow:0 1px 4px rgba(0,0,0,0.04);">'
        '<div style="width:64px; height:64px; background-color:#ECFDF5; border-radius:50%; '
        'display:flex; align-items:center; justify-content:center; margin:0 auto 1.25rem auto; border:1px solid #A7F3D0;">'
        '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
        '<polyline points="14 2 14 8 20 8"></polyline>'
        '<line x1="16" y1="13" x2="8" y2="13"></line>'
        '<line x1="16" y1="17" x2="8" y2="17"></line>'
        '<polyline points="10 9 9 9 8 9"></polyline>'
        '</svg>'
        '</div>'
        f'<h3 style="font-size:1.35rem; font-weight:700; color:#111827; margin:0 0 0.5rem 0;">{title}</h3>'
        f'<p style="color:#4B5563; font-size:0.96rem; line-height:1.6; margin:0 auto 1.5rem auto; max-width:500px;">{message}</p>'
        '</div>'
    )
    st.markdown(empty_html, unsafe_allow_html=True)

    if action_label:
        col_l, col_btn, col_r = st.columns([1, 1.3, 1])
        with col_btn:
            if st.button(f"🚀 {action_label}", type="primary", use_container_width=True, key=f"empty_cta_{target_page.replace(' ', '_')}"):
                st.session_state.current_page = target_page
                st.rerun()


def render_ethical_disclaimer(disclaimer_text: str):
    """Renders the standard transparency and ethical disclaimer box."""
    html = (
        '<div style="background-color:#F0FDF4; border:1px solid #A7F3D0; border-left:4px solid #059669; '
        'border-radius:8px; padding:1rem 1.25rem; color:#065F46; font-size:0.92rem; line-height:1.55; margin:1rem 0;">'
        '<div style="display:flex; align-items:flex-start; gap:10px;">'
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0; margin-top:2px;">'
        '<circle cx="12" cy="12" r="10"></circle>'
        '<line x1="12" y1="16" x2="12" y2="12"></line>'
        '<line x1="12" y1="8" x2="12.01" y2="8"></line>'
        '</svg>'
        '<div>'
        '<strong style="color:#047857; font-weight:700;">Ethical AI & Transparency Note:</strong> '
        f'<span style="color:#065F46;">{disclaimer_text}</span>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_skill_badges_html(skills: List[str], badge_type: str = "matched") -> str:
    """Helper that returns HTML string of styled skill badges."""
    is_match = (badge_type == "matched")
    bg = "#ECFDF5" if is_match else "#FFFBEB"
    color = "#065F46" if is_match else "#92400E"
    border = "#A7F3D0" if is_match else "#FDE68A"

    return "".join([
        f'<span style="display:inline-block; background-color:{bg}; color:{color}; '
        f'border:1px solid {border}; font-size:0.86rem; font-weight:600; padding:4px 10px; '
        f'border-radius:9999px; margin:3px 4px 3px 0;">{s}</span>'
        for s in skills
    ])
