"""
SkillPilot AI - Main Streamlit Dashboard Entry Point
Multimodal (Text + Voice + Image + Files) ChatGPT-Style Navigation Assistant v2.0
"""


import streamlit as st
try:
    from streamlit_mic_recorder import speech_to_text
    MIC_RECORDER_AVAILABLE = True
except ImportError:
    MIC_RECORDER_AVAILABLE = False


import importlib
import core.config
import core.llm
import core.history
import core.gates
import core.intents
import core.prompts
import core.media

for _mod in [core.config, core.llm, core.history, core.gates, core.intents, core.prompts, core.media]:
    try:
        importlib.reload(_mod)
    except Exception:
        pass


from core.config import (
    APP_TITLE, APP_SUBTITLE, APP_ICON, AVAILABLE_MODES, CUSTOM_CSS
)
from core.llm import get_installed_models, stream_chat_completion
from core.history import (
    init_session_state, clear_chat_history, export_chat_as_markdown, export_chat_as_json
)
from core.gates import input_gate, output_gate
from core.intents import detect_intent, detect_topic, extract_entity
from core.prompts import build_system_prompt
from core.media import (
    extract_text_from_image, extract_text_from_document, generate_tts_audio_bytes, play_voice_output
)



# Import Feature Modules
from features.resume_analyzer import render_resume_analyzer
from features.interview_prep import render_interview_prep
from features.roadmap_generator import render_roadmap_generator
from features.code_assistant import render_code_assistant

# Page Configuration
st.set_page_config(
    page_title=f"{APP_TITLE} - Intelligent Career Assistant",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS Styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize Session State
init_session_state()

if "attached_file_context" not in st.session_state:
    st.session_state.attached_file_context = ""

if "attached_file_name" not in st.session_state:
    st.session_state.attached_file_name = ""

if "transcribed_voice_text" not in st.session_state:
    st.session_state.transcribed_voice_text = ""

# Header Banner
st.markdown(
    f"""
    <div class="header-banner">
        <h1>{APP_ICON} {APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar Configuration Controls (Only Mode Selector)
with st.sidebar:
    st.title("🎯 Select Mode")
    
    if "mode" not in st.session_state or st.session_state.mode not in AVAILABLE_MODES:
        st.session_state.mode = AVAILABLE_MODES[0]

    current_mode = st.radio("Choose Mode", AVAILABLE_MODES, key="mode")

# Default background settings
installed_models = get_installed_models()
selected_model = installed_models[0] if installed_models else "mistral"
temperature = 0.3
strict_gate = False


# Render Feature Views depending on active mode
if current_mode == "Resume Analyzer":
    render_resume_analyzer(model=selected_model)

elif current_mode == "Interactive Interview":
    render_interview_prep(model=selected_model)

elif current_mode == "Skill Roadmap Generator":
    render_roadmap_generator(model=selected_model)

elif current_mode == "Coding & DSA Coach":
    render_code_assistant(model=selected_model)

else:
    # General Assistant & Career Guidance Chat View
    st.markdown(f'<div class="mode-badge">Current Mode: {current_mode}</div>', unsafe_allow_html=True)
    
    # Render Conversation Messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "audio" in msg and msg["audio"]:
                st.audio(msg["audio"], format="audio/mp3")

    # Active Attachments Banner (above input bar if files/voice attached)
    if st.session_state.transcribed_voice_text or st.session_state.attached_file_context:
        att_col1, att_col2 = st.columns([8.5, 1.5])
        with att_col1:
            att_desc = []
            if st.session_state.transcribed_voice_text:
                att_desc.append(f"🗣️ Voice Query: \"{st.session_state.transcribed_voice_text}\"")
            if st.session_state.attached_file_name:
                att_desc.append(f"📎 Attached File: {st.session_state.attached_file_name}")
            st.info(" | ".join(att_desc))
        with att_col2:
            if st.button("❌ Clear"):
                st.session_state.transcribed_voice_text = ""
                st.session_state.attached_file_context = ""
                st.session_state.attached_file_name = ""
                st.rerun()

    # Action Toolbar Row (Placed right above search input bar)
    col_plus, col_mic, col_space = st.columns([1.8, 1.8, 6.4])

    with col_plus:
        with st.popover("➕ Photos & Files", help="Attach photos, code files & documents", use_container_width=True):
            st.markdown("#### 📎 Attach Photos & Files")
            uploaded_file = st.file_uploader(
                "Upload photos, code files, PDFs, or documents",
                type=["png", "jpg", "jpeg", "pdf", "txt", "py", "js", "json", "md", "csv", "cpp", "java"],
                key="inline_file_uploader"
            )
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                f_label, f_text = extract_text_from_document(uploaded_file.name, file_bytes)
                st.session_state.attached_file_name = uploaded_file.name
                st.session_state.attached_file_context = f"\n\n--- ATTACHED FILE ({uploaded_file.name}) ---\n{f_text}"
                st.success(f"✅ {f_label} attached!")

    with col_mic:
        with st.popover("🎙️ Voice Input", help="Voice Input (Speech-to-Text)", use_container_width=True):
            st.markdown("#### 🎙️ Voice Input")
            
            # Browser Speech-to-Text Button
            if MIC_RECORDER_AVAILABLE:
                st.caption("Option 1: Browser Instant Speech-to-Text")
                voice_result = speech_to_text(
                    language='en',
                    start_prompt="🎙️ Start Recording Voice",
                    stop_prompt="⏹️ Stop Recording & Transcribe",
                    just_once=True,
                    use_container_width=True,
                    key='inline_mic_stt'
                )
                if voice_result:
                    st.session_state.transcribed_voice_text = voice_result
                    st.success(f"🗣️ Transcribed: \"{voice_result}\"")
                    st.rerun()

                st.divider()


            # Audio Input Widget Fallback
            st.caption("Option 2: Audio File Recorder")
            rec_audio = st.audio_input("Record audio", key="inline_mic_audio")
            if rec_audio is not None:
                audio_bytes = rec_audio.read()
                with st.spinner("Transcribing recorded audio..."):
                    success, transcribed_text = transcribe_audio_bytes(audio_bytes)
                    if success:
                        st.session_state.transcribed_voice_text = transcribed_text
                        st.success(f"🗣️ Transcribed: \"{transcribed_text}\"")
                        st.rerun()
                    else:
                        st.warning(transcribed_text)

    # Main Chat / Search Input Box (Anchored at the bottom of the screen)
    text_prompt = st.chat_input(f"Ask your {current_mode} question or paste code...")



    # Determine final prompt combining text, voice transcript, and file context
    prompt = text_prompt or st.session_state.transcribed_voice_text
    if st.session_state.attached_file_context and prompt:
        prompt = f"{prompt}\n{st.session_state.attached_file_context}"

    if prompt:
        status, gate_message = input_gate(prompt, strict_mode=strict_gate)
        
        if status == "reject":
            st.error(gate_message)
            st.stop()
        elif status == "warn":
            st.warning(gate_message)

        # Clear active attachments after sending
        st.session_state.transcribed_voice_text = ""
        st.session_state.attached_file_context = ""
        st.session_state.attached_file_name = ""

        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Handle instant greeting
        if prompt.lower().strip() in ["hi", "hello", "hey", "hii", "greetings"]:
            greeting_resp = "Hey 👋 Welcome to SkillPilot AI! How can I assist with your coding or career goals today?"
            with st.chat_message("assistant"):
                st.markdown(greeting_resp)
            st.session_state.messages.append({"role": "assistant", "content": greeting_resp})
            st.stop()

        intent = detect_intent(prompt)
        topic = detect_topic(prompt)

        if topic != st.session_state.last_topic:
            st.session_state.last_entity = None
            st.session_state.last_topic = topic

        entity = extract_entity(prompt)
        if entity:
            st.session_state.last_entity = entity
        entity = st.session_state.last_entity

        system_prompt = build_system_prompt(current_mode, intent, entity)
        
        messages = [{"role": "system", "content": system_prompt}]
        for msg in st.session_state.messages:
            messages.append({"role": msg["role"], "content": msg["content"]})

        with st.chat_message("assistant"):
            with st.spinner("SkillPilot AI is processing..."):
                placeholder = st.empty()
                output = ""
                for chunk in stream_chat_completion(messages, model=selected_model, temperature=temperature):
                    output += chunk
                    placeholder.markdown(output)

                cleaned_output = output_gate(output, current_mode)
                placeholder.markdown(cleaned_output)

                # Optional Text-to-Speech Output
                audio_bytes = None
                if st.session_state.get("enable_tts", False):
                    play_voice_output(cleaned_output)
                    audio_bytes = generate_tts_audio_bytes(cleaned_output)

        st.session_state.messages.append({"role": "assistant", "content": cleaned_output, "audio": audio_bytes})