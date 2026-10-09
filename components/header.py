"""
header.py
=========
Renders uniform, accessible page headers with breadcrumbs, title, description, and dynamic status indicators.
Uses clean, unindented HTML to prevent Markdown parser code-block misinterpretation.
"""

from __future__ import annotations
from typing import Optional
import streamlit as st


def render_header(
    title: str,
    description: str,
    breadcrumb: str = "Dashboard",
    status_text: Optional[str] = None,
    status_type: str = "emerald",
):
    """
    Renders a unified top header for application views.

    Args:
        title: Main heading for the page.
        description: Brief contextual description.
        breadcrumb: Breadcrumb label or route hierarchy.
        status_text: Optional status text (e.g. 'Active Analysis', 'Ready for Upload').
        status_type: 'emerald', 'warning', or 'neutral'.
    """
    if status_text:
        is_emerald = (status_type == "emerald")
        pill_bg = "#ECFDF5" if is_emerald else "#F3F4F6"
        pill_border = "#A7F3D0" if is_emerald else "#E5E7EB"
        pill_text = "#047857" if is_emerald else "#374151"
        dot_color = "#059669" if is_emerald else "#6B7280"

        status_html = (
            f'<div style="display:inline-flex; align-items:center; gap:7px; background-color:{pill_bg}; '
            f'border:1px solid {pill_border}; color:{pill_text}; padding:5px 14px; border-radius:9999px; '
            f'font-size:0.84rem; font-weight:600; white-space:nowrap;">'
            f'<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background-color:{dot_color}; flex-shrink:0;"></span>'
            f'{status_text}</div>'
        )
    else:
        status_html = ""

    header_html = (
        '<div style="display:flex; justify-content:space-between; align-items:flex-start; '
        'padding:1rem 0 1.25rem 0; margin-bottom:1.5rem; border-bottom:1px solid #E5E7EB; flex-wrap:wrap; gap:12px;">'
        '<div style="flex:1; min-width:260px;">'
        '<div style="font-size:0.84rem; font-weight:700; color:#059669; text-transform:uppercase; '
        'letter-spacing:0.05em; margin-bottom:4px; display:flex; align-items:center; gap:6px;">'
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>'
        '<polyline points="9 22 9 12 15 12 15 22"></polyline>'
        '</svg>'
        f'{breadcrumb}</div>'
        f'<h1 style="font-size:1.9rem; font-weight:800; color:#111827; margin:0 0 6px 0; line-height:1.25;">{title}</h1>'
        f'<p style="font-size:0.98rem; color:#4B5563; margin:0; line-height:1.55;">{description}</p>'
        '</div>'
        f'<div style="display:flex; align-items:center; margin-top:4px;">{status_html}</div>'
        '</div>'
    )

    st.markdown(header_html, unsafe_allow_html=True)
