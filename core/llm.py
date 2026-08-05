import os
import streamlit as st
import ollama
from typing import List, Dict, Generator, Any

def configure_ollama_client():
    """Configure Ollama client with host from secrets or environment if available."""
    host = os.environ.get("OLLAMA_HOST")
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

def stream_chat_completion(
    messages: List[Dict[str, str]],
    model: str = "mistral",
    temperature: float = 0.3
) -> Generator[str, None, None]:
    """
    Yields chunks of text from Ollama chat stream.
    """
    configure_ollama_client()
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
            yield "\n\n❌ **Cannot connect to Ollama service.**\n👉 For local usage: ensure `ollama serve` is running.\n👉 For Streamlit Cloud: set `OLLAMA_HOST` in Streamlit Secrets."
        else:
            yield f"\n\n❌ **LLM Execution Error:** {error_msg}"

