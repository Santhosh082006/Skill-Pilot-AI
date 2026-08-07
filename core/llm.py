import os
import json
import requests
import streamlit as st
import ollama
from typing import List, Dict, Generator, Any

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

def configure_ollama_client():
    """Configure Ollama client with host from secrets or environment if available."""
    try:
        if hasattr(st, "secrets") and "OLLAMA_HOST" in st.secrets:
            os.environ["OLLAMA_HOST"] = st.secrets["OLLAMA_HOST"]
    except Exception:
        pass

def get_installed_models() -> List[str]:
    """Retrieve list of locally or remotely installed Ollama models."""
    configure_ollama_client()
    try:
        models_response = ollama.list()
        models_list = models_response.get('models', []) if isinstance(models_response, dict) else getattr(models_response, 'models', [])
        
        extracted = []
        for m in models_list:
            if isinstance(m, dict):
                name = m.get('name') or m.get('model')
            else:
                name = getattr(m, 'name', None) or getattr(m, 'model', None)
            if name:
                clean_name = name.split(':')[0]
                if clean_name not in extracted:
                    extracted.append(clean_name)
                    
        return extracted if extracted else ["mistral"]
    except Exception:
        return ["mistral"]

def stream_groq_completion(messages: List[Dict[str, str]], api_key: str, temperature: float = 0.3) -> Generator[str, None, None]:
    """Stream response from Groq API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": temperature,
        "stream": True
    }
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, stream=True, timeout=30)
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith("data: ") and "[DONE]" not in line_str:
                    try:
                        data = json.loads(line_str[6:])
                        chunk = data["choices"][0]["delta"].get("content", "")
                        if chunk:
                            yield chunk
                    except Exception:
                        pass
    except Exception as e:
        yield f"\n\n❌ **Groq API Error:** {str(e)}"

def stream_gemini_completion(messages: List[Dict[str, str]], api_key: str, temperature: float = 0.3) -> Generator[str, None, None]:
    """Generate response from Google Gemini API using new google-genai SDK."""
    if not GEMINI_AVAILABLE:
        yield "\n\n❌ **Google GenAI SDK is missing.**\n👉 Please ensure `google-genai` is installed."
        return

    try:
        client = genai.Client(api_key=api_key.strip())
        
        contents = ""
        for msg in messages:
            if msg["role"] != "system":
                contents += f"{msg['role'].capitalize()}: {msg['content']}\n\n"
                
        if not contents.strip():
            contents = "Hello"
            
        # Discover models
        available_models = []
        try:
            for m in client.models.list():
                available_models.append(m.name)
        except Exception:
            pass
            
        # Try to pick 3.x models first, then 2.x, then 1.5
        prefs = ["gemini-3.5-flash", "gemini-3.0-flash", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
        model_name = "gemini-2.5-flash"
        
        if available_models:
            for p in prefs:
                if any(p in m for m in available_models):
                    model_name = next(m for m in available_models if p in m)
                    break
            if model_name not in available_models:
                model_name = available_models[0]
                
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents
            )
            if response.text:
                yield response.text
        except Exception as api_err:
            # If the chosen model fails, try the next available ones
            success = False
            for backup_model in available_models[:5]: 
                if backup_model == model_name: continue
                try:
                    res = client.models.generate_content(model=backup_model, contents=contents)
                    if res.text:
                        yield res.text
                        success = True
                        break
                except Exception:
                    continue
            if not success:
                raise api_err
            
    except Exception as e:
        yield f"\n\n❌ **Gemini SDK Error:** {str(e)}\n\n💡 **Tip:** Your API key might not have access to standard models yet. Check Google AI Studio!"





def stream_chat_completion(
    messages: List[Dict[str, str]],
    model: str = "mistral",
    temperature: float = 0.3
) -> Generator[str, None, None]:
    """
    Yields chunks of text from Gemini Cloud API, Groq API, or Ollama.
    """
    configure_ollama_client()

    # 1. Check if Gemini API Key is available in st.secrets or environment
    gemini_key = os.environ.get("GEMINI_API_KEY")
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            gemini_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if gemini_key:
        yield from stream_gemini_completion(messages, gemini_key, temperature)
        return

    # 2. Check if Groq API Key is available in st.secrets or environment
    groq_key = os.environ.get("GROQ_API_KEY")
    try:
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            groq_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    if groq_key:
        yield from stream_groq_completion(messages, groq_key, temperature)
        return

    # 3. Primary: Local / Remote Ollama
    try:
        response = ollama.chat(
            model=model,
            messages=messages,
            stream=True,
            options={"temperature": temperature}
        )
        for chunk in response:
            if isinstance(chunk, dict) and "message" in chunk and "content" in chunk["message"]:
                yield chunk["message"]["content"]
            elif hasattr(chunk, 'message') and hasattr(chunk.message, 'content'):
                yield chunk.message.content
    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            yield f"\n\n❌ **Model '{model}' not found in Ollama.**\n👉 Please run in terminal: `ollama pull {model}`"
        elif "connection refused" in error_msg.lower() or "connect" in error_msg.lower():
            yield (
                "\n\n❌ **Cannot connect to local Ollama service.**\n\n"
                "### 🌐 How to enable LLM on your Cloud App:\n"
                "1. **Local Usage**: Run `ollama serve` and `streamlit run app.py` on your computer.\n"
                "2. **Streamlit Cloud (Free Gemini API)**: Get a free API Key at [aistudio.google.com](https://aistudio.google.com/) and add `GEMINI_API_KEY = \"AIzaSy...\"` in your Streamlit Cloud Secrets!"
            )
        else:
            yield f"\n\n❌ **LLM Execution Error:** {error_msg}"



