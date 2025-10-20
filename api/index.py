import os
from flask import Flask, request, jsonify

# Ensure src is importable when running on Vercel
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.chatbot import EkkoChatbot


app = Flask(__name__)

# Lazy singleton to avoid cold-start cost on every request
_bot_instance = None


def get_bot() -> EkkoChatbot:
    global _bot_instance
    if _bot_instance is None:
        # Disable model for web deployment to avoid large downloads
        os.environ["EKKO_DISABLE_MODEL"] = "1"
        model_name = os.getenv("EKKO_MODEL", "gpt2")
        cache_dir = os.getenv("EKKO_MODELS_DIR", os.path.join(os.getcwd(), "models"))
        _bot_instance = EkkoChatbot(model_name=model_name, cache_dir=cache_dir, enable_model=False)
    return _bot_instance


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "message is required"}), 400
    bot = get_bot()
    reply = bot.get_response(message)
    return jsonify({"reply": reply})


# Vercel Python looks for an `app` WSGI variable


