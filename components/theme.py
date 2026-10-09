"""
theme.py
========
Defines the Emerald & White Design System tokens, typography, and injects custom CSS for Streamlit.
Optimized for high readability, contrast accessibility, and responsive wrapping.
"""

from __future__ import annotations
import streamlit as st

# Color Palette Constants
COLOR_PRIMARY_EMERALD = "#059669"
COLOR_DARK_EMERALD = "#047857"
COLOR_LIGHT_EMERALD = "#D1FAE5"
COLOR_EMERALD_TINT = "#ECFDF5"
COLOR_EMERALD_BORDER = "#A7F3D0"
COLOR_BG_MAIN = "#F9FAFB"
COLOR_BG_CARD = "#FFFFFF"
COLOR_BG_SECTION = "#F8FAFC"
COLOR_TEXT_PRIMARY = "#111827"
COLOR_TEXT_SECONDARY = "#374151"
COLOR_TEXT_MUTED = "#4B5563"
COLOR_BORDER = "#E5E7EB"
COLOR_BORDER_LIGHT = "#F3F4F6"
COLOR_SUCCESS = "#16A34A"
COLOR_WARNING = "#D97706"
COLOR_WARNING_BG = "#FEF3C7"
COLOR_WARNING_BORDER = "#FDE68A"
COLOR_ERROR = "#DC2626"
COLOR_ERROR_BG = "#FEE2E2"

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global Root Variables */
    :root {
        --primary-emerald: #059669;
        --dark-emerald: #047857;
        --light-emerald: #D1FAE5;
        --tint-emerald: #ECFDF5;
        --border-emerald: #A7F3D0;
        --bg-main: #F9FAFB;
        --bg-card: #FFFFFF;
        --bg-section: #F8FAFC;
        --text-primary: #111827;
        --text-secondary: #374151;
        --text-muted: #4B5563;
        --border: #E5E7EB;
        --border-light: #F3F4F6;
        --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Base Font & Body */
    html, body, [class*="css"], .stApp {
        font-family: var(--font-family) !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    /* Paragraphs and general text readability */
    p, span, label, li {
        color: #1F2937 !important;
        font-size: 0.96rem !important;
        line-height: 1.6 !important;
    }

    /* Captions with readable contrast */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #4B5563 !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
    }

    /* Top decoration bar */
    header[data-testid="stHeader"] {
        background: transparent !important;
        border-bottom: 1px solid rgba(229, 231, 235, 0.6) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
        box-shadow: 1px 0 3px rgba(0,0,0,0.02) !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }

    /* Navigation Button Styles */
    .stButton button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.18s ease-in-out !important;
        border: 1px solid var(--border) !important;
        padding: 0.55rem 1rem !important;
    }

    /* Primary buttons */
    .stButton button[kind="primary"],
    div.stButton > button:first-child[kind="primary"] {
        background-color: #059669 !important;
        color: #FFFFFF !important;
        border-color: #059669 !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(5, 150, 105, 0.25) !important;
    }

    .stButton button[kind="primary"]:hover,
    div.stButton > button:first-child[kind="primary"]:hover {
        background-color: #047857 !important;
        border-color: #047857 !important;
        box-shadow: 0 4px 8px rgba(4, 120, 87, 0.3) !important;
        transform: translateY(-1px);
    }

    /* Secondary / standard buttons */
    .stButton button[kind="secondary"],
    div.stButton > button:first-child[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border-color: #D1D5DB !important;
    }

    .stButton button[kind="secondary"]:hover,
    div.stButton > button:first-child[kind="secondary"]:hover {
        background-color: #F0FDF4 !important;
        border-color: #059669 !important;
        color: #047857 !important;
    }

    /* Badges */
    .badge-matched {
        display: inline-block;
        background-color: #ECFDF5;
        color: #065F46;
        font-size: 0.86rem;
        font-weight: 600;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        margin: 0.2rem;
        border: 1px solid #A7F3D0;
    }

    .badge-missing {
        display: inline-block;
        background-color: #FFFBEB;
        color: #92400E;
        font-size: 0.86rem;
        font-weight: 600;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        margin: 0.2rem;
        border: 1px solid #FDE68A;
    }

    .badge-priority-high {
        background-color: #FEF2F2;
        color: #991B1B;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        border: 1px solid #FECACA;
        text-transform: uppercase;
    }

    .badge-priority-med {
        background-color: #FFFBEB;
        color: #92400E;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        border: 1px solid #FDE68A;
        text-transform: uppercase;
    }

    /* File Uploader styling */
    [data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #059669 !important;
    }

    [data-testid="stFileUploader"] section {
        border: 2px dashed #A7F3D0 !important;
        border-radius: 8px !important;
        background-color: #F0FDF4 !important;
        padding: 1.5rem 1rem !important;
    }

    /* Streamlit Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #059669 !important;
    }

    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.65rem 1.2rem !important;
        border-radius: 6px 6px 0 0 !important;
        font-weight: 700 !important;
        color: #4B5563 !important;
        font-size: 0.95rem !important;
        background-color: transparent !important;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        color: #047857 !important;
        border-bottom: 3px solid #059669 !important;
        background-color: #ECFDF5 !important;
    }

    /* Streamlit Expanders */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        margin-bottom: 0.85rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    }

    div[data-testid="stExpander"] > details > summary {
        font-weight: 700 !important;
        color: #111827 !important;
        padding: 0.85rem 1.1rem !important;
        font-size: 0.98rem !important;
    }

    div[data-testid="stExpander"] > details > summary:hover {
        color: #059669 !important;
    }

    /* Streamlit Text Inputs & Textareas */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 8px !important;
        border: 1px solid #D1D5DB !important;
        font-size: 0.96rem !important;
        color: #111827 !important;
        background-color: #FFFFFF !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #059669 !important;
        box-shadow: 0 0 0 2px rgba(5, 150, 105, 0.2) !important;
    }

    /* Checkbox labels */
    .stCheckbox label span {
        color: #1F2937 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }

    /* Hide standard Streamlit footer */
    footer {visibility: hidden !important;}

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .metric-num {
            font-size: 1.8rem !important;
        }
    }
</style>
"""

def inject_theme():
    """Injects the unified Emerald & White custom CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
