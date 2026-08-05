"""
SkillPilot AI - Input & Output Gates
Validates user input quality and cleans LLM outputs.
"""

import re
from typing import Tuple, Optional

def input_gate(prompt: str, strict_mode: bool = False) -> Tuple[str, Optional[str]]:
    """
    Validates input quality.
    If strict_mode is True and prompt is pure text with > 2 question marks (and no code),
    it prompts the user to focus their query. Otherwise it allows complex queries and code seamlessly.
    """
    if not prompt or not prompt.strip():
        return "reject", "Please enter a non-empty question or prompt."

    # Check if prompt looks like code snippet or structured text
    code_indicators = ["def ", "class ", "import ", "public class", "function", "{", "}", ";", "for(", "while(", "return "]
    has_code = any(ind in prompt for ind in code_indicators)

    if strict_mode and not has_code and prompt.count("?") > 2:
        return "warn", "💡 Tip: For best results, consider focusing on your primary question."

    return "ok", None

def output_gate(text: str, mode: str = "General") -> str:
    """
    Cleans raw LLM response by filtering meta-chatter and formatting cleanly.
    """
    if not text:
        return ""

    # Remove standard meta phrases
    text = re.sub(r"as an ai (language model)?|i am an ai model", "", text, flags=re.I)
    
    # Clean redundant weak words if needed
    weak_words = ["maybe", "probably", "in conclusion"]
    for w in weak_words:
        text = re.sub(rf"\b{w}\b", "", text, flags=re.I)

    # Clean double blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    return text.strip()
