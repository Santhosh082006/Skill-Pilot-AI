"""
SkillPilot AI - Multimodal Media & File Processing (Images, Documents, Voice)
"""

import io
import os
import base64
from typing import Tuple, Optional
from PIL import Image
import streamlit as st

# PDF Extraction
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

# Image OCR fallback handling
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
    _easyocr_reader = None
except ImportError:
    EASYOCR_AVAILABLE = False

# Text to Speech (gTTS) handling
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


def extract_text_from_image(image_bytes: bytes) -> Tuple[Optional[Image.Image], str]:
    """
    Safely extract text from image using Tesseract, EasyOCR, or PIL fallback.
    Guarantees no crash on missing system binaries.
    """
    global _easyocr_reader
    try:
        img = Image.open(io.BytesIO(image_bytes))
        extracted_text = ""
        
        # 1. Try pytesseract first
        if PYTESSERACT_AVAILABLE:
            try:
                extracted_text = pytesseract.image_to_string(img).strip()
            except Exception:
                extracted_text = ""

        # 2. Try EasyOCR if pytesseract returned empty or wasn't available
        if not extracted_text and EASYOCR_AVAILABLE:
            try:
                if _easyocr_reader is None:
                    _easyocr_reader = easyocr.Reader(['en'], gpu=False)
                results = _easyocr_reader.readtext(image_bytes)
                extracted_text = " ".join([res[1] for res in results]).strip()
            except Exception:
                extracted_text = ""

        # 3. Fallback: Base64 image summary metadata
        if not extracted_text:
            extracted_text = f"[Attached Image: {img.format} image, {img.size[0]}x{img.size[1]} px]"

        return img, extracted_text
    except Exception as e:
        return None, f"Error reading image: {str(e)}"


def extract_text_from_document(filename: str, file_bytes: bytes) -> Tuple[str, str]:
    """
    Extract text content from uploaded files (PDF, Code, TXT, JSON, MD, etc.).
    Returns (file_type_label, extracted_text).
    """
    ext = os.path.splitext(filename)[1].lower()
    
    # 1. PDF Files
    if ext == ".pdf":
        if PYPDF2_AVAILABLE:
            try:
                reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                return "PDF Document", text.strip() if text.strip() else "[PDF content could not be converted to plain text]"
            except Exception as e:
                return "PDF Document", f"[Error reading PDF: {str(e)}]"
        else:
            return "PDF Document", "[PyPDF2 not installed]"

    # 2. Plain Text / Code / Markdown / JSON / CSV Files
    text_extensions = [".txt", ".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".cs", ".json", ".md", ".csv", ".xml", ".yaml", ".yml", ".sql", ".sh"]
    if ext in text_extensions or ext == "":
        try:
            content = file_bytes.decode("utf-8", errors="replace")
            return f"Code / Document ({ext})", content.strip()
        except Exception as e:
            return "Text File", f"[Error decoding text file: {str(e)}]"

    # 3. Image Files
    if ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp"]:
        img, img_text = extract_text_from_image(file_bytes)
        return "Image File", img_text

    return "File", f"[Attached binary file: {filename}]"


def generate_tts_audio_bytes(text: str) -> Optional[bytes]:
    """
    Convert text to speech audio bytes using gTTS.
    """
    if not GTTS_AVAILABLE or not text.strip():
        return None

    try:
        clean_text = text[:800]
        tts = gTTS(text=clean_text, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None


def play_voice_output(text: str):
    """
    Auto-speaks AI response aloud using browser SpeechSynthesis API & audio player fallback.
    """
    if not text or not text.strip():
        return

    # Clean text for JS speech synthesis
    clean_js_text = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')[:500]
    
    # HTML5 SpeechSynthesis JS snippet
    tts_html = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{clean_js_text}");
            msg.rate = 1.0;
            msg.pitch = 1.0;
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """
    st.components.v1.html(tts_html, height=0)

    # Audio Player Backup
    audio_bytes = generate_tts_audio_bytes(text)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
