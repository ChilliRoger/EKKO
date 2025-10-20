import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from chatbot import OfflineChatbot
from utils import save_chat_history, load_chat_history, safe_eval


class ChatGUI:
    """
    Tkinter-based GUI for the Offline AI Chatbot.
    Handles user interaction, message display, and chatbot integration.
    """

    def __init__(self, root: tk.Tk, bot: OfflineChatbot, history_path: str = "chat_history.json"):
        self.root = root
        self.bot = bot
        self.history_path = history_path
        self.history = load_chat_history(history_path)

        self._build_ui()
        self._load_history()

    def _build_ui(self):
        """Builds and styles the main GUI components."""
        self.root.title("Offline AI Chatbot")
        self.root.geometry("650x520")
        self.root.configure(bg="#f4f4f4")

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED, bg="#ffffff", font=("Segoe UI", 10)
        )
        self.chat_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Define text tags for color-coded messages
        self.chat_display.tag_config("user", foreground="#0078d7")  # blue
        self.chat_display.tag_config("bot", foreground="#107c10")   # green

        # Input frame
        frame = tk.Frame(self.root, bg="#f4f4f4")
        frame.pack(fill=tk.X, padx=10, pady=6)

        self.input_var = tk.StringVar()
        self.entry = tk.Entry(frame, textvariable=self.input_var, font=("Segoe UI", 11))
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 6))
        self.entry.bind("<Return>", lambda e: self._on_send())

        send_button = tk.Button(
            frame, text="Send", command=self._on_send,
            bg="#0078d7", fg="white", font=("Segoe UI", 10, "bold"),
            relief="flat", padx=10, pady=3, cursor="hand2"
        )
        send_button.pack(side=tk.LEFT)

    def _append(self, role: str, text: str):
        """Appends messages to the chat display and stores them in history."""
        self.chat_display.configure(state=tk.NORMAL)
        tag = "user" if role.lower() == "you" else "bot"
        self.chat_display.insert(tk.END, f"{role}: {text}\n", tag)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

        # Save to memory
        self.history.append({"role": role, "text": text})

    def _load_history(self):
        """Loads and displays previous chat history (if available)."""
        for msg in self.history:
            tag = "user" if msg["role"].lower() == "you" else "bot"
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"{msg['role']}: {msg['text']}\n", tag)
            self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def _on_send(self):
        """Triggered when user presses Enter or clicks Send."""
        text = self.input_var.get().strip()
        if not text:
            return

        self._append("You", text)
        self.input_var.set("")

        # Handle small calculations
        if text.startswith("=") or text.lower().startswith("calc:"):
            expr = text.lstrip("=calc:").strip()
            try:
                result = safe_eval(expr)
                self._append("Bot", f"Result: {result}")
            except Exception as e:
                self._append("Bot", f"Error: {e}")
            return

        # Run chatbot reply in background thread
        threading.Thread(target=self._bot_reply, args=(text,), daemon=True).start()

    def _bot_reply(self, text: str):
        """Fetches chatbot reply (runs in background thread)."""
        try:
            reply = self.bot.generate_response(text)
        except Exception as e:
            reply = f"Error generating response: {e}"
        self.root.after(0, lambda: self._append("Bot", reply))


if __name__ == "__main__":
    try:
        bot = OfflineChatbot(model_name_or_path="microsoft/DialoGPT-small", kb_path="kb.json")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load chatbot model: {e}")
        exit()

    root = tk.Tk()
    app = ChatGUI(root, bot)

    def on_close():
        """Save chat history when window closes."""
        save_chat_history(app.history_path, app.history)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
