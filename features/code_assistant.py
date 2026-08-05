"""
SkillPilot AI - Feature: Coding & DSA Coach
"""

import streamlit as st
from core.llm import stream_chat_completion
from core.prompts import build_system_prompt
from core.media import play_voice_output

def render_code_assistant(model: str = "mistral"):
    st.subheader("💻 DSA & Code Assistant")
    st.caption("Debug code, optimize time/space complexity, generate unit tests, and master data structures.")

    language = st.selectbox("🌐 Select Language", ["Python", "C++", "Java", "JavaScript", "Go", "SQL"], index=0)
    task_type = st.radio("🛠️ Select Task", ["Debug / Fix Code", "Optimize Complexity", "Explain Code Line-by-Line", "Generate Test Cases"], horizontal=True)

    code_input = st.text_area("✍️ Paste Code or Problem Statement", height=220, placeholder="Paste code snippet or problem details here...")

    if st.button("⚡ Run Code Assistant", type="primary", use_container_width=True):
        if not code_input.strip():
            st.warning("Please paste code or problem details first!")
            return

        prompt = (
            f"Language: {language}\n"
            f"Task: {task_type}\n\n"
            f"--- CODE / PROBLEM STATEMENT ---\n{code_input}"
        )

        system_prompt = build_system_prompt("Coding & DSA Coach", "coding_help")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        with st.spinner("Analyzing code & computing complexity..."):
            placeholder = st.empty()
            output = ""
            for chunk in stream_chat_completion(messages, model=model):
                output += chunk
                placeholder.markdown(output)

            # Auto Voice Output if enabled
            if st.session_state.get("enable_tts", False):
                play_voice_output(output)

        st.session_state.messages.append({"role": "user", "content": f"[{task_type} - {language}]\n{code_input[:100]}..."})
        st.session_state.messages.append({"role": "assistant", "content": output})
