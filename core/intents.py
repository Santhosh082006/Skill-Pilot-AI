"""
SkillPilot AI - Intent & Topic Classifier
"""

from typing import Dict, Any

def detect_intent(prompt: str) -> str:
    """Classify user query intent based on key structural patterns."""
    p = prompt.lower()
    intents = {
        "trip_planner": ["plan", "trip", "travel", "itinerary", "vacation", "tour", "visit", "days"],
        "comparison": ["compare", " vs ", "difference between", "better than", "which is best"],
        "explanation": ["what is", "why does", "how to", "explain", "meaning of", "define"],
        "roadmap": ["roadmap", "career path", "how to become", "learn path", "study plan", "curriculum"],
        "coding_help": ["python", "java", "c++", "bug", "error", "traceback", "fix code", "algorithm", "complexity", "dsa", "leetcode"],
        "resume": ["resume", "cv", "ats", "work experience", "bullet points", "job description"],
        "interview": ["interview", "mock", "question for role", "behavioral", "technical round"],
        "business": ["business model", "startup", "profit", "revenue", "competitor", "market analysis"]
    }
    for intent, keywords in intents.items():
        if any(word in p for word in keywords):
            return intent
    return "general"

def detect_topic(prompt: str) -> str:
    """Detect subject topic domain."""
    p = prompt.lower()
    if any(x in p for x in ["business", "profit", "company", "startup", "market"]):
        return "business"
    elif any(x in p for x in ["trip", "travel", "flight", "place", "hotel", "city"]):
        return "travel"
    elif any(x in p for x in ["college", "university", "degree", "course", "placement"]):
        return "education"
    elif any(x in p for x in ["code", "python", "javascript", "java", "bug", "sql", "error"]):
        return "coding"
    elif any(x in p for x in ["resume", "interview", "job", "career", "salary"]):
        return "career"
    return "general"

def extract_entity(prompt: str) -> str:
    """Extract primary subject entity if short."""
    words = prompt.strip().split()
    if len(words) <= 4:
        return prompt.strip()
    return ""
