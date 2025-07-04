import re

# Sample keyword bank (can be expanded)
INTENT_KEYWORDS = {
    "overheating": ["overheat", "hot", "temperature", "fan", "heat"],
    "wifi_issue": ["wifi", "internet", "network", "router", "no connection"]
}

def keyword_detect(user_input, workflows):
    """
    Detects which issue tree (intent) the input matches based on keywords.
    """
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in user_input:
                return intent
    return None

def simple_llm_fallback(user_input):
    """
    Basic fallback logic when decision tree fails.
    """
    if "slow" in user_input:
        return "Try closing background apps and restarting. Also check for viruses."
    if "blue screen" in user_input:
        return "Check for driver updates or recent hardware changes."
    if "keyboard" in user_input:
        return "Try unplugging and reconnecting it. Test on another device."
    
    # Generic fallback
    return "Sorry, I couldn't identify the issue clearly. Can you describe it differently?"
