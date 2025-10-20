# EKKO – Offline & Online AI Chatbot for Students

**EKKO** is a personal AI chatbot designed for students. It can answer study-related questions, do small calculations, provide reminders, and function completely offline once the model is downloaded. It can also run online through a web interface for easy deployment using platforms like Vercel.

---

## Features

- Fully functional **offline AI chatbot** using GPT-2 / DialoGPT small model
- GUI interface using **Tkinter** for desktop users
- Optional **web interface** deployable on **Vercel**
- Local **knowledge base** for common student queries
- Handles **simple calculations**
- **Offline and online modes**
- Lightweight and free to use

---

## Project Structure

EKKO/
│
├── README.md
├── requirements.txt
├── .gitignore
├── models/ # GPT-2 model for offline use
├── knowledge_base/
│ └── faqs.json # Local fallback answers
├── src/
│ ├── chatbot.py # Chatbot logic
│ ├── gui.py # Tkinter GUI
│ └── utils.py # Utility functions (knowledge base, reminders)
└── assets/ # Optional images/icons for GUI


---

## Tech Stack

| Component                  | Library / Tool                  | Notes |
|-----------------------------|--------------------------------|-------|
| Programming Language        | Python 3.11+                   | Core language |
| Offline AI Model            | GPT-2 / DialoGPT (Hugging Face) | Small pre-trained model |
| GUI                         | Tkinter                        | Lightweight desktop interface |
| Optional Web Interface      | Flask / Streamlit              | Can run on Vercel for online access |
| Knowledge Base              | JSON / TXT                     | Local fallback responses |
| Version Control             | Git + GitHub                   | Team collaboration |

---

## Installation & Setup (Offline Desktop Version)

1. Clone the repository:  

```bash
git clone https://github.com/yourusername/EKKO.git
cd EKKO


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Download GPT-2 small model offline into models/ folder:

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "gpt2"
AutoTokenizer.from_pretrained(model_name, cache_dir="./models")
AutoModelForCausalLM.from_pretrained(model_name, cache_dir="./models")


Run the desktop GUI:

python src/gui.py

Optional: Online Deployment (Vercel)

Wrap the chatbot in a Flask or Streamlit app (app.py) for web access:

# Example minimal Streamlit wrapper
import streamlit as st
from src.chatbot import EkkoChatbot

chatbot = EkkoChatbot()

st.title("EKKO - Offline AI Chatbot")
user_input = st.text_input("Ask EKKO something:")

if user_input:
    response = chatbot.get_response(user_input)
    st.text_area("EKKO says:", value=response, height=200)


Create requirements.txt including all dependencies.

Push the project to GitHub.

Connect the GitHub repo to Vercel:

Go to Vercel → New Project → Import GitHub repo

Set Python build command (pip install -r requirements.txt)

Set start command (streamlit run app.py or Flask equivalent)

Deploy

After deployment, EKKO will be accessible online. The first load may require internet, but the offline model works without internet afterward.

How to Use EKKO

Desktop (Offline): Run gui.py, type questions, get answers.

Web (Online): Deploy with Streamlit/Flask, accessible via browser.

Chatbot responds to study questions, performs calculations, and fallback queries from the local knowledge base.

Development & Collaboration

Branching strategy:

main → stable version

feature/chatbot → model logic

feature/gui → GUI development

feature/web → Streamlit/Flask deployment

Commits: Use descriptive messages:

feat(chatbot): add offline GPT-2 response generation

fix(gui): fix scroll issue in chat area

Adding new knowledge: Add Q&A to knowledge_base/faqs.json.