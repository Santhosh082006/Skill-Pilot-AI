"""
SkillPilot AI - Configuration & UI Theme Definitions
"""

APP_TITLE = "SkillPilot AI"
APP_SUBTITLE = "Enterprise Learning & Career Navigation Platform"
APP_ICON = "🚀"

AVAILABLE_MODES = [
    "General Assistant",
    "Career Guidance",
    "Coding & DSA Coach",
    "Interactive Interview",
    "Resume Analyzer",
    "Skill Roadmap Generator"
]

DEFAULT_MODEL = "mistral"
FALLBACK_MODELS = ["mistral", "llama3", "phi3", "codellama", "gemma", "qwen2"]

# Custom CSS theme for rich aesthetics
CUSTOM_CSS = """
<style>
    /* Global styles & typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);
        color: #ffffff;
        padding: 1.8rem 2.2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(67, 56, 202, 0.3);
        margin-bottom: 1.8rem;
    }

    .header-banner h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #ffffff;
    }

    .header-banner p {
        margin: 0.4rem 0 0 0;
        font-size: 1.05rem;
        color: #c7d2fe;
    }

    /* Glassmorphism Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }

    /* Mode Badge */
    .mode-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        background: #4f46e5;
        color: #ffffff;
        margin-bottom: 1rem;
    }

    /* Custom Chat Message Styling */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 0.8rem;
    }

    /* Sidebar Styling & High Contrast Text */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: #f1f5f9 !important;
    }

    section[data-testid="stSidebar"] .stRadio label p,
    section[data-testid="stSidebar"] .stCheckbox label p {
        color: #cbd5e1 !important;
        font-size: 0.95rem;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #0f172a !important;
    }

    section[data-testid="stSidebar"] .stSlider p {
        color: #f1f5f9 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #334155 !important;
    }
</style>

"""
