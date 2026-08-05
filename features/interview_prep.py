"""
SkillPilot AI - Feature: Interactive Mock Interviewer
"""

import streamlit as st
from core.llm import stream_chat_completion
from core.prompts import build_system_prompt
from core.media import play_voice_output

def render_interview_prep(model: str = "mistral"):
    st.subheader("🎙️ Interactive AI Mock Interviewer")
    st.caption("Simulate real-time technical and behavioral interview rounds with instant performance feedback.")

    role = st.text_input("🎯 Target Role", value="Software Engineer", placeholder="e.g. Full Stack Developer, Data Scientist, System Architect")
    difficulty = st.selectbox("⚡ Difficulty Level", ["Entry Level", "Mid Level", "Senior / Lead"], index=1)

    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
        st.session_state.interview_turn = 0

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 Start New Interview Round", use_container_width=True):
            st.session_state.interview_started = True
            st.session_state.interview_turn = 1
            st.session_state.interview_history = []
            
            prompt = f"Start a technical interview for a {difficulty} {role} position. Ask Question 1."
            system_prompt = build_system_prompt("Interactive Interview", "interview")
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            with st.spinner("Preparing interview question..."):
                output = ""
                placeholder = st.empty()
                for chunk in stream_chat_completion(messages, model=model):
                    output += chunk
                    placeholder.markdown(output)

                if st.session_state.get("enable_tts", False):
                    play_voice_output(output)

            st.session_state.interview_history.append({"role": "assistant", "content": output})

    with col_btn2:
        if st.button("🏁 End Interview & Summarize", use_container_width=True):
            st.session_state.interview_started = False
            st.info("Interview session completed! Review your conversation history below.")

    if st.session_state.interview_started:
        st.divider()
        st.markdown(f"**Turn #{st.session_state.interview_turn}**")
        
        # Display interview transcript
        for item in st.session_state.interview_history:
            role_label = "👤 Candidates Answer" if item["role"] == "user" else "🤖 Interviewer Question / Feedback"
            with st.chat_message(item["role"]):
                st.markdown(item["content"])

        user_answer = st.text_area("✍️ Your Answer", key=f"ans_{st.session_state.interview_turn}", placeholder="Type your answer here...")
        
        if st.button("📤 Submit Answer", type="primary"):
            if not user_answer.strip():
                st.warning("Please type an answer before submitting.")
                return

            st.session_state.interview_history.append({"role": "user", "content": user_answer})
            
            messages = [
                {"role": "system", "content": build_system_prompt("Interactive Interview", "interview")}
            ]
            for item in st.session_state.interview_history:
                messages.append({"role": item["role"], "content": item["content"]})
                
            messages.append({"role": "user", "content": "Evaluate my response above with a Score (1-10), give feedback, and then ask Question #" + str(st.session_state.interview_turn + 1)})

            with st.spinner("Interviewer is evaluating your response..."):
                output = ""
                placeholder = st.empty()
                for chunk in stream_chat_completion(messages, model=model):
                    output += chunk
                    placeholder.markdown(output)

                if st.session_state.get("enable_tts", False):
                    play_voice_output(output)

            st.session_state.interview_history.append({"role": "assistant", "content": output})
            st.session_state.interview_turn += 1
            st.rerun()
