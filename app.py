"""
app.py
======
AI Resume Analyzer & Skill Development Agent.
Modern, clean white-and-emerald-green dashboard for resume parsing, competency benchmarking,
4-week learning roadmaps, portfolio project blueprints, and interview preparation.
"""

from __future__ import annotations

import os
import streamlit as st
from dotenv import load_dotenv

from components.theme import inject_theme
from components.navigation import render_sidebar_navigation
from components.views_home import render_home_view
from components.views_analysis import render_analysis_view
from components.views_skill_gap import render_skill_gap_view
from components.views_roadmap import render_roadmap_view
from components.views_projects import render_projects_view
from components.views_interview import render_interview_view
from components.views_settings import render_settings_view

from config import (
    get_groq_api_key,
    get_groq_model,
    get_openai_api_key,
    get_openai_model,
    DEFAULT_GROQ_MODEL,
)

# Load environment variables
load_dotenv()

# ==============================================================================
# Streamlit Application Configuration
# ==============================================================================

st.set_page_config(
    page_title="AI Resume & Skill Agent • Emerald Studio",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session State Defaults
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

if "pdf_metadata" not in st.session_state:
    st.session_state.pdf_metadata = {}

if "target_role_input" not in st.session_state:
    st.session_state.target_role_input = "Python Developer"

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "roadmap_progress" not in st.session_state:
    st.session_state.roadmap_progress = {}

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.2

if "provider_mode" not in st.session_state:
    if get_groq_api_key():
        st.session_state.provider_mode = "⚡ Groq (Fast & Free Cloud)"
        st.session_state.selected_model = get_groq_model()
    elif get_openai_api_key():
        st.session_state.provider_mode = "🟢 OpenAI API"
        st.session_state.selected_model = get_openai_model()
    else:
        st.session_state.provider_mode = "⚡ Groq (Fast & Free Cloud)"
        st.session_state.selected_model = DEFAULT_GROQ_MODEL

# Inject Design System (White & Emerald Theme)
inject_theme()

# Render Sidebar Navigation
active_page = render_sidebar_navigation()

# ==============================================================================
# View Router
# ==============================================================================

if active_page == "Home":
    render_home_view()
elif active_page == "Resume Analysis":
    render_analysis_view()
elif active_page == "Skill Gap Analysis":
    render_skill_gap_view()
elif active_page == "Learning Roadmap":
    render_roadmap_view()
elif active_page == "Project Recommendations":
    render_projects_view()
elif active_page == "Interview Preparation":
    render_interview_view()
elif active_page == "Settings & About":
    render_settings_view()
else:
    render_home_view()
