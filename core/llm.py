"""
SkillPilot AI - LLM Integration Wrapper
Handles communication with Ollama and available models.
"""

import ollama
from typing import List, Dict, Generator, Any

def get_installed_models() -> List[str]:
    """Retrieve list of locally installed Ollama models."""
    try:
        models_response = ollama.list()
        # Handle both dict-like and object structures returned by ollama-python
        models_list = models_response.get('models', []) if isinstance(models_response, dict) else getattr(models_response, 'models', [])
        
        extracted = []
        for m in models_list:
            if isinstance(m, dict):
                name = m.get('name') or m.get('model')
            else:
                name = getattr(m, 'name', None) or getattr(m, 'model', None)
            if name:
                # Remove tag if present, e.g., 'mistral:latest' -> 'mistral'
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
            yield "\n\n❌ **Cannot connect to Ollama service.**\n👉 Ensure Ollama is running (`ollama serve`)."
        else:
            yield f"\n\n❌ **LLM Execution Error:** {error_msg}"
