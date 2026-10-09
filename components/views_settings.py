"""
views_settings.py
=================
Settings & About View: Provider configuration, model parameters, system capabilities,
privacy architecture, and ethical AI policy.
Uses clean, unindented HTML for reliable rendering.
"""

from __future__ import annotations
import streamlit as st
from config import (
    get_groq_api_key,
    get_groq_model,
    get_openai_api_key,
    get_openai_model,
    SUPPORTED_GROQ_MODELS,
    SUPPORTED_OPENAI_MODELS,
    DEFAULT_GROQ_MODEL,
    DEFAULT_OPENAI_MODEL,
    is_placeholder,
)
from components.header import render_header
from components.cards import render_ethical_disclaimer


def render_settings_view():
    """Renders the Settings & About page."""
    provider_mode = st.session_state.get("provider_mode", "⚡ Groq (Fast & Free Cloud)")

    render_header(
        title="Settings & System Architecture",
        description="Configure your AI inference provider, model hyperparameters, and review privacy architecture.",
        breadcrumb="Preferences • Settings",
        status_text=f"Active: {provider_mode.split()[1] if len(provider_mode.split()) > 1 else provider_mode}",
        status_type="emerald",
    )

    col_config, col_about = st.columns([1.2, 1], gap="large")

    with col_config:
        st.markdown("### ⚙️ AI Engine Configuration")

        # Provider Selector
        modes = [
            "⚡ Groq (Fast & Free Cloud)",
            "🟢 OpenAI API",
            "🧪 Offline / Demo Mode",
        ]
        
        current_idx = modes.index(provider_mode) if provider_mode in modes else 0

        selected_mode = st.radio(
            "Select Inference Provider",
            options=modes,
            index=current_idx,
            help="Select your preferred AI execution environment.",
            key="settings_provider_mode_radio",
        )
        st.session_state.provider_mode = selected_mode

        if selected_mode == "⚡ Groq (Fast & Free Cloud)":
            auto_groq_key = get_groq_api_key()
            configured_model = get_groq_model()

            if auto_groq_key:
                status_box = (
                    '<div style="background-color:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; '
                    'padding:0.75rem 1rem; margin-bottom:1rem; color:#065F46; font-size:0.92rem; font-weight:600;">'
                    '🔒 <b>Groq API Key Active:</b> Automatically loaded from local configuration (<code>.streamlit/secrets.toml</code> or <code>.env</code>).'
                    '</div>'
                )
                st.markdown(status_box, unsafe_allow_html=True)
            else:
                status_box = (
                    '<div style="background-color:#FFFBEB; border:1px solid #FDE68A; border-radius:8px; '
                    'padding:0.75rem 1rem; margin-bottom:1rem; color:#92400E; font-size:0.92rem; font-weight:600;">'
                    '⚠️ <b>Groq Key Not Configured:</b> Add your free key to <code>.streamlit/secrets.toml</code> or paste it below.'
                    '</div>'
                )
                st.markdown(status_box, unsafe_allow_html=True)

            session_override = st.text_input(
                "Groq API Key (Override or Enter Key)",
                type="password",
                value=st.session_state.get("groq_api_key_override", ""),
                placeholder="gsk_... (Leave blank to use automatically loaded key)",
                help="Get your free key at https://console.groq.com/keys",
                key="settings_groq_key_input",
            )
            st.session_state.groq_api_key_override = session_override

            cur_model = st.session_state.get("selected_model", configured_model)
            if cur_model not in SUPPORTED_GROQ_MODELS:
                cur_model = DEFAULT_GROQ_MODEL
            m_idx = SUPPORTED_GROQ_MODELS.index(cur_model) if cur_model in SUPPORTED_GROQ_MODELS else 0

            chosen_model = st.selectbox("Groq Model", options=SUPPORTED_GROQ_MODELS, index=m_idx, key="settings_groq_model_select")
            st.session_state.selected_model = chosen_model

        elif selected_mode == "🟢 OpenAI API":
            auto_openai_key = get_openai_api_key()
            configured_model = get_openai_model()

            if auto_openai_key:
                status_box = (
                    '<div style="background-color:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; '
                    'padding:0.75rem 1rem; margin-bottom:1rem; color:#065F46; font-size:0.92rem; font-weight:600;">'
                    '🔒 <b>OpenAI API Key Active:</b> Automatically loaded from local configuration (<code>.streamlit/secrets.toml</code> or <code>.env</code>).'
                    '</div>'
                )
                st.markdown(status_box, unsafe_allow_html=True)
            else:
                status_box = (
                    '<div style="background-color:#FFFBEB; border:1px solid #FDE68A; border-radius:8px; '
                    'padding:0.75rem 1rem; margin-bottom:1rem; color:#92400E; font-size:0.92rem; font-weight:600;">'
                    '⚠️ <b>OpenAI Key Not Configured:</b> Add your key to <code>.streamlit/secrets.toml</code> or paste it below.'
                    '</div>'
                )
                st.markdown(status_box, unsafe_allow_html=True)

            session_override = st.text_input(
                "OpenAI API Key (Override or Enter Key)",
                type="password",
                value=st.session_state.get("openai_api_key_override", ""),
                placeholder="sk-proj-... (Leave blank to use automatically loaded key)",
                help="Your OpenAI API key from platform.openai.com",
                key="settings_openai_key_input",
            )
            st.session_state.openai_api_key_override = session_override

            cur_model = st.session_state.get("selected_model", configured_model)
            if cur_model not in SUPPORTED_OPENAI_MODELS:
                cur_model = DEFAULT_OPENAI_MODEL
            m_idx = SUPPORTED_OPENAI_MODELS.index(cur_model) if cur_model in SUPPORTED_OPENAI_MODELS else 0

            chosen_model = st.selectbox("OpenAI Model", options=SUPPORTED_OPENAI_MODELS, index=m_idx, key="settings_openai_model_select")
            st.session_state.selected_model = chosen_model

        else:
            st.success("💡 **Offline / Demo Mode Active.** Analyzes real keywords locally without external API tokens.")
            st.session_state.selected_model = "local-keyword-analyzer"

        # Temperature
        cur_temp = float(st.session_state.get("temperature", 0.2))
        chosen_temp = st.slider(
            "Analytical Temperature",
            min_value=0.0,
            max_value=0.7,
            value=cur_temp,
            step=0.05,
            help="Low temperature (0.1 - 0.2) guarantees strict factual grounding.",
            key="settings_temperature_slider",
        )
        st.session_state.temperature = chosen_temp

        st.write("")
        if st.button("🔄 Reset All Session Data", type="secondary", use_container_width=True, key="settings_reset_all_btn"):
            st.session_state.clear()
            st.session_state.current_page = "Home"
            st.rerun()

    with col_about:
        st.markdown("### 🛡️ Privacy & Technical Architecture")

        arch_box = (
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:1.25rem; margin-bottom:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">'
            '<h4 style="color:#059669; margin:0 0 0.4rem 0; font-size:1.08rem; font-weight:700;">Automatic Local Configuration</h4>'
            '<p style="color:#374151; font-size:0.92rem; line-height:1.55; margin:0;">'
            'API keys are automatically loaded in priority order:<br>'
            '1. <code>.streamlit/secrets.toml</code><br>'
            '2. <code>.env</code> environment file<br>'
            'Keys are held strictly in memory and never exposed in the UI or committed to Git.'
            '</p>'
            '</div>'
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:1.25rem; margin-bottom:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">'
            '<h4 style="color:#059669; margin:0 0 0.4rem 0; font-size:1.08rem; font-weight:700;">In-Memory Processing</h4>'
            '<p style="color:#374151; font-size:0.92rem; line-height:1.55; margin:0;">'
            'PDF resumes are parsed strictly in memory using <code>PyMuPDF</code>. No files or resumes are ever written to disk or stored permanently.'
            '</p>'
            '</div>'
            '<div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:1.25rem; margin-bottom:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">'
            '<h4 style="color:#059669; margin:0 0 0.4rem 0; font-size:1.08rem; font-weight:700;">Anti-Hallucination Guardrails</h4>'
            '<p style="color:#374151; font-size:0.92rem; line-height:1.55; margin:0;">'
            'System prompts enforce strict honesty: missing qualifications are categorized as <i>\'Not Evidenced\'</i> rather than assuming candidate inability, and advice never fabricates metrics.'
            '</p>'
            '</div>'
        )
        st.markdown(arch_box, unsafe_allow_html=True)

    st.write("")
    render_ethical_disclaimer(
        "Skill match score is an educational alignment indicator between resume text and industry standards, not a hiring guarantee or ATS rejection verdict."
    )
