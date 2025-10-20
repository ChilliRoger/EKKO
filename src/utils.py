import json
import re
import threading
import time
from difflib import SequenceMatcher
from datetime import datetime, timedelta


# ---------- Knowledge Base Functions ---------- #

def load_knowledge_base(path: str):
    """Load FAQ JSON file."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def search_knowledge_base(query: str, faqs: list, threshold: float = 0.6):
    """
    Search for the most similar question in FAQs.
    Returns the matched answer or None if no good match.
    """
    best_match, best_score = None, 0
    for faq in faqs:
        score = SequenceMatcher(None, query.lower(), faq["question"].lower()).ratio()
        if score > best_score:
            best_score, best_match = score, faq
    return best_match["answer"] if best_score >= threshold else None


# ---------- Calculator Utility ---------- #

def calculate_expression(expression: str):
    """
    Evaluate basic math expressions safely (no eval exploits).
    Accepts +, -, *, /, (), and decimals.
    """
    expr = expression.replace("x", "*").replace("X", "*")
    if not re.fullmatch(r"[0-9\.\+\-\*\/\(\)\s]+", expr):
        return "Invalid expression."
    try:
        result = eval(expr, {"__builtins__": {}})
        return round(result, 3)
    except Exception:
        return "Calculation error."


# ---------- Reminder Utility ---------- #

def _reminder_thread(delay_seconds: int, task: str):
    """Internal thread function to wait and display reminder."""
    time.sleep(delay_seconds)
    print(f"\n🔔 Reminder: {task}\n")


def set_reminder(time_str: str, task: str):
    """
    Schedule a reminder after N seconds/minutes/hours
    Examples:
        set_reminder("10s", "drink water")
        set_reminder("5m", "submit assignment")
    """
    match = re.match(r"(\d+)([smh])", time_str.strip().lower())
    if not match:
        return "Invalid time format. Use like '10s', '5m', or '2h'."

    value, unit = int(match.group(1)), match.group(2)
    delay = value * {"s": 1, "m": 60, "h": 3600}[unit]

    t = threading.Thread(target=_reminder_thread, args=(delay, task), daemon=True)
    t.start()
    return f"Reminder set for '{task}' in {value}{unit}."


# ---------- Combined Fallback Logic ---------- #

def fallback_response(query: str, faqs: list):
    """
    Combined fallback:
      - if query looks like a calculation → calculator
      - else → KB search
    """
    if re.search(r"[\d\+\-\*\/]", query):
        return f"Answer: {calculate_expression(query)}"

    kb_answer = search_knowledge_base(query, faqs)
    return kb_answer or "I'm sorry, I couldn't find that information right now."
