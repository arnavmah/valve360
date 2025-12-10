"""
Global Styles Module - Default Streamlit
Provides unified styling across the entire application
"""

import streamlit as st
from typing import Literal

# No custom theme config needed for default styling

def get_theme() -> dict:
    """Get current theme based on Streamlit's theme setting"""
    # Return empty dict or minimal config if needed, but for default we don't need much
    return {}


def get_global_css(theme: dict = None) -> str:
    """
    Generate global CSS styles based on theme
    Returns empty string to use default Streamlit styles
    """
    return ""


def apply_global_styles(theme: dict = None):
    """
    Apply global styles to the Streamlit app
    No-op for default styling
    """
    pass


def toggle_theme():
    """Toggle between light and dark mode"""
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    st.rerun()


def init_theme(default: Literal["light", "dark"] = "dark"):
    """
    Initialize theme in session state
    Args:
        default: Default theme to use ('light' or 'dark')
    """
    if "theme" not in st.session_state:
        st.session_state.theme = default


def render_theme_toggle(position: str = "sidebar"):
    """
    Render a theme toggle button
    Args:
        position: Where to render the toggle ('sidebar' or 'main')
    """
    # Optional: Keep the toggle if user wants to switch between light/dark mode preference
    # even with default styles
    if position == "sidebar":
        col = st.sidebar.columns([3, 1])
    else:
        col = st.columns([3, 1])
    
    current_theme = st.session_state.get("theme", "dark")
    theme_label = "🌙 Dark Mode" if current_theme == "light" else "☀️ Light Mode"
    
    with col[1]:
        if st.button(theme_label, key=f"theme_toggle_{position}"):
            toggle_theme()
