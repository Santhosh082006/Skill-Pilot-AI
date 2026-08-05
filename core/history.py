"""
SkillPilot AI - Session State & History Manager
"""

import streamlit as st
import json
from typing import List, Dict

def init_session_state():
    """Ensure all required session state keys exist."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "last_topic" not in st.session_state:
        st.session_state.last_topic = None
        
    if "last_entity" not in st.session_state:
        st.session_state.last_entity = None
        
    if "mode" not in st.session_state:
        st.session_state.mode = "General Assistant"
        
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "mistral"

    if "interview_history" not in st.session_state:
        st.session_state.interview_history = []

    if "roadmap_progress" not in st.session_state:
        st.session_state.roadmap_progress = {}

    if "enable_tts" not in st.session_state:
        st.session_state.enable_tts = False


def clear_chat_history():
    """Clear chat history and reset context state."""
    st.session_state.messages = []
    st.session_state.last_topic = None
    st.session_state.last_entity = None
    st.session_state.interview_history = []

def export_chat_as_markdown() -> str:
    """Export current conversation as Markdown text."""
    if not st.session_state.messages:
        return "# SkillPilot AI Chat Transcript\n\n*No messages recorded.*"
        
    md = "# 🚀 SkillPilot AI - Chat Transcript\n\n"
    for msg in st.session_state.messages:
        role = "👤 User" if msg["role"] == "user" else "🤖 SkillPilot AI"
        md += f"### {role}\n{msg['content']}\n\n---\n\n"
    return md

def export_chat_as_json() -> str:
    """Export current conversation as JSON text."""
    return json.dumps(st.session_state.messages, indent=2)
