# 🚀 SkillPilot AI

> **Enterprise AI Learning & Career Navigation Platform**

SkillPilot AI is an intelligent, multi-modal career mentor and technical assistant built with Python, Streamlit, and local Ollama LLMs. It empowers learners, developers, and job seekers with personalized career guidance, code optimization, ATS resume reviewing, interactive mock interviews, and visual learning roadmaps.

---

## ✨ Features

- 🎯 **Multi-Mode Career Navigation**:
  - **General Assistant**: Actionable advice for technical and general queries.
  - **Career Guidance**: Structured industry career architecture & skill matrices.
  - **Coding & DSA Coach**: Code debugging, line-by-line breakdowns, and $O(N)$ time/space complexity analysis.
  - **Interactive Mock Interviewer**: Sequential technical/behavioral interview rounds with instant 1-10 scoring & performance feedback.
  - **Resume & ATS Reviewer**: Instant ATS score calculation, missing keyword analysis, and bullet point rewrites.
  - **Skill Roadmap Generator**: Step-by-step milestone roadmaps with interactive progress tracking.

- 🎙️ 🖼️ **Multimodal Inputs (Voice, Photos & Files)**:
  - **Photos & Files Attachment**: Upload code snippets (`.py`, `.js`, `.cpp`, `.java`), PDFs (`.pdf`), text files (`.txt`, `.json`, `.csv`), and screenshots (`.png`, `.jpg`).
  - **Voice Speech-to-Text**: Real-time browser microphone voice recording with instant speech recognition.
  - **Voice Text-to-Speech**: HTML5 browser SpeechSynthesis and audio playback.

- ⚙️ **Clean & Minimal UI**:
  - Modern glassmorphism dark/light theme accents, clean sidebar mode selector, and crash-proof session management.

---

## 🏗️ Architecture

```
Carrer-pilot/
├── app.py                     # Main Dashboard UI & navigation entry point
├── requirements.txt           # Dependencies (Streamlit, Ollama, PyPDF2, SpeechRecognition, etc.)
├── core/                      # Core System Infrastructure
│   ├── config.py              # Theme CSS, modes, and configuration
│   ├── llm.py                 # Ollama integration, auto-discovery & streaming
│   ├── intents.py             # Smart query intent & topic classification
│   ├── prompts.py             # System prompt templates & AI personas
│   ├── gates.py               # Input validation & output sanitizer
│   ├── history.py             # Session state & chat transcript export
│   └── media.py               # Multimodal processing (Images, PDFs, Voice STT/TTS)
└── features/                  # Specialized Tool Modules
    ├── resume_analyzer.py     # ATS score & resume reviewer
    ├── interview_prep.py      # Interactive mock interviewer & scorecard
    ├── roadmap_generator.py   # Visual roadmap & milestone tracker
    └── code_assistant.py      # DSA coach, complexity analyzer & test generator
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python 3.10+**
- **Ollama**: [Download & install Ollama](https://ollama.com/)

Pull your preferred model (e.g. Mistral or LLaMA 3):
```bash
ollama pull mistral
```

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Santhosh082006/CareerPilot-AI.git
cd CareerPilot-AI
pip install -r requirements.txt
```

### 3. Run Application
Launch the Streamlit dashboard:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🐳 Docker Deployment

To build and run SkillPilot AI in a Docker container:

```bash
docker build -t skillpilot-ai .
docker run -p 8501:8501 skillpilot-ai
```

---

## 👤 Author
Santhosh

---

## 📜 License
MIT License - feel free to use and customize for your career & learning projects!
