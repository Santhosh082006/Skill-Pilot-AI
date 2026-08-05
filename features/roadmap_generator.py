"""
SkillPilot AI - Feature: Skill Roadmap & Trackable Milestones
"""

import streamlit as st
from core.llm import stream_chat_completion
from core.prompts import build_system_prompt
from core.media import play_voice_output

def render_roadmap_generator(model: str = "mistral"):
    st.subheader("🗺️ Custom Skill & Career Roadmap Generator")
    st.caption("Generate structured learning paths and check off milestones as you master skills.")

    col1, col2 = st.columns(2)
    with col1:
        target_goal = st.text_input("🎯 Target Career / Skill Goal", value="Full Stack Python Developer", placeholder="e.g. AI Engineer, DevOps Specialist")
    with col2:
        timeframe = st.selectbox("⏳ Desired Timeframe", ["1 Month (Fast Track)", "3 Months (Standard)", "6 Months (Comprehensive)"], index=1)

    if st.button("🚀 Generate Structured Roadmap", type="primary", use_container_width=True):
        prompt = f"Create a step-by-step career roadmap to become a {target_goal} within {timeframe}."
        system_prompt = build_system_prompt("Skill Roadmap Generator", "roadmap")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        with st.spinner("Building your custom learning path..."):
            placeholder = st.empty()
            output = ""
            for chunk in stream_chat_completion(messages, model=model):
                output += chunk
                placeholder.markdown(output)

            # Auto Voice Output if enabled
            if st.session_state.get("enable_tts", False):
                play_voice_output(output)

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": output})

    st.divider()
    st.subheader("📌 Skill Milestone Progress Checklist")
    
    # Pre-built interactive milestone tracker
    default_milestones = [
        "Phase 1: Programming Fundamentals & Data Structures",
        "Phase 2: Database Design (SQL & NoSQL)",
        "Phase 3: Core Frameworks & API Development",
        "Phase 4: Capstone Portfolio Projects",
        "Phase 5: Interview Prep & System Design"
    ]
    
    completed = 0
    for idx, milestone in enumerate(default_milestones):
        is_checked = st.checkbox(milestone, key=f"ms_{idx}", value=st.session_state.roadmap_progress.get(f"ms_{idx}", False))
        st.session_state.roadmap_progress[f"ms_{idx}"] = is_checked
        if is_checked:
            completed += 1

    progress = completed / len(default_milestones) if default_milestones else 0.0
    st.progress(progress)
    st.caption(f"Progress: {completed} / {len(default_milestones)} Milestones Completed ({int(progress * 100)}%)")
