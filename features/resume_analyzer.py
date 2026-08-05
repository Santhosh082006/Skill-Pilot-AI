"""
SkillPilot AI - Feature: Resume & Profile Analyzer
"""

import streamlit as st
from core.llm import stream_chat_completion
from core.prompts import build_system_prompt
from core.media import play_voice_output

def render_resume_analyzer(model: str = "mistral"):
    st.subheader("📄 AI Resume & ATS Reviewer")
    st.caption("Paste your resume and target job description to receive instant ATS score & optimization suggestions.")

    col1, col2 = st.columns(2)
    with col1:
        resume_text = st.text_area("📋 Paste Resume Text", height=200, placeholder="Paste your resume content here...")
    with col2:
        job_desc = st.text_area("🎯 Target Job Description", height=200, placeholder="Paste target job description or role requirements...")

    if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
        if not resume_text.strip():
            st.warning("Please paste your resume text first!")
            return

        prompt = (
            f"Please analyze this resume against the target job description:\n\n"
            f"--- RESUME ---\n{resume_text}\n\n"
            f"--- TARGET JOB DESCRIPTION ---\n{job_desc if job_desc.strip() else 'General Software Engineer / Tech Role'}"
        )
        
        system_prompt = build_system_prompt("Resume Analyzer", "resume")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        with st.spinner("Analyzing Resume & Calculating ATS Score..."):
            placeholder = st.empty()
            output = ""
            for chunk in stream_chat_completion(messages, model=model):
                output += chunk
                placeholder.markdown(output)

            # Auto Voice Output if enabled
            if st.session_state.get("enable_tts", False):
                play_voice_output(output)

        st.session_state.messages.append({"role": "user", "content": "Analyzed Resume"})
        st.session_state.messages.append({"role": "assistant", "content": output})
