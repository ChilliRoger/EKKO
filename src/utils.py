import json
import os

def load_knowledge_base(file_path="knowledge_base/faqs.json"):
    """
    Load FAQs or fallback Q&A from a JSON file.
    """
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        kb = json.load(f)
    return kb

def search_knowledge_base(query, kb):
    """
    Search for an exact match in the knowledge base.
    Returns the answer if found, else None.
    """
    return kb.get(query, None)
