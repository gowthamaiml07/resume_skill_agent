"""
config.py
=========
Centralized secure configuration manager for Groq and OpenAI API keys.
Loads keys automatically according to priority:
  1. Streamlit Secrets: st.secrets["GROQ_API_KEY"]
  2. Environment Variables: os.getenv("GROQ_API_KEY")

Ensures secrets are never hardcoded, logged, or printed.
"""

from __future__ import annotations

import os
from typing import Optional, List, Tuple
from dotenv import load_dotenv

# Load local .env file if available
load_dotenv()

# Supported Groq Models
SUPPORTED_GROQ_MODELS: List[str] = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
]
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"

# Supported OpenAI Models
SUPPORTED_OPENAI_MODELS: List[str] = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

PLACEHOLDER_PREFIXES = [
    "gsk_replace",
    "your_groq",
    "sk-proj-your",
    "replace_with",
]


def is_placeholder(key: Optional[str]) -> bool:
    """Checks if a key string is empty or a template placeholder."""
    if not key or not isinstance(key, str):
        return True
    k = key.strip().lower()
    if len(k) < 10:
        return True
    return any(p in k for p in PLACEHOLDER_PREFIXES)


def get_groq_api_key() -> Optional[str]:
    """
    Securely loads the Groq API key using the following priority:
      1. Streamlit Secrets (st.secrets["GROQ_API_KEY"])
      2. Environment Variable (os.getenv("GROQ_API_KEY"))

    Returns:
        The valid API key string or None if unconfigured/placeholder.
    """
    # 1. Try Streamlit Secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            secret_val = st.secrets["GROQ_API_KEY"]
            if secret_val and not is_placeholder(secret_val):
                return str(secret_val).strip()
    except Exception:
        pass

    # 2. Try Environment Variable
    env_val = os.getenv("GROQ_API_KEY")
    if env_val and not is_placeholder(env_val):
        return env_val.strip()

    return None


def get_groq_model() -> str:
    """
    Retrieves the configured Groq model name from:
      1. Streamlit Secrets (st.secrets["GROQ_MODEL"])
      2. Environment Variable (os.getenv("GROQ_MODEL"))
      3. Default fallback: 'llama-3.3-70b-versatile'
    """
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GROQ_MODEL" in st.secrets:
            model = str(st.secrets["GROQ_MODEL"]).strip()
            if model in SUPPORTED_GROQ_MODELS:
                return model
    except Exception:
        pass

    env_model = os.getenv("GROQ_MODEL")
    if env_model and env_model.strip() in SUPPORTED_GROQ_MODELS:
        return env_model.strip()

    return DEFAULT_GROQ_MODEL


def get_openai_api_key() -> Optional[str]:
    """
    Securely loads the OpenAI API key from:
      1. Streamlit Secrets (st.secrets["OPENAI_API_KEY"])
      2. Environment Variable (os.getenv("OPENAI_API_KEY"))
    """
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
            secret_val = st.secrets["OPENAI_API_KEY"]
            if secret_val and not is_placeholder(secret_val):
                return str(secret_val).strip()
    except Exception:
        pass

    env_val = os.getenv("OPENAI_API_KEY")
    if env_val and not is_placeholder(env_val):
        return env_val.strip()

    return None


def get_openai_model() -> str:
    """Retrieves configured OpenAI model name."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "OPENAI_MODEL" in st.secrets:
            model = str(st.secrets["OPENAI_MODEL"]).strip()
            if model in SUPPORTED_OPENAI_MODELS:
                return model
    except Exception:
        pass

    env_model = os.getenv("OPENAI_MODEL")
    if env_model and env_model.strip() in SUPPORTED_OPENAI_MODELS:
        return env_model.strip()

    return DEFAULT_OPENAI_MODEL


def get_active_provider_status() -> Tuple[str, bool, str]:
    """
    Determines the active provider configuration status.
    Returns:
        (provider_name, is_configured, setup_hint)
    """
    groq_key = get_groq_api_key()
    if groq_key:
        return ("Groq Cloud", True, "Automatically loaded from local configuration.")

    openai_key = get_openai_api_key()
    if openai_key:
        return ("OpenAI API", True, "Automatically loaded from local configuration.")

    return (
        "Offline / Demo Mode",
        False,
        "No API key detected. Using local keyword analyzer. Add your key in .streamlit/secrets.toml or .env to enable Groq AI."
    )
