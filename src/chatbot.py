import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils import load_knowledge_base, search_knowledge_base

class EkkoChatbot:
    def __init__(self, model_path="models/gpt2", kb_file="knowledge_base/faqs.json"):
        """
        Initialize GPT-2 offline chatbot.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.kb = load_knowledge_base(kb_file)

    def get_response(self, user_input, max_length=100):
        """
        Generate a response for user input.
        Priority: knowledge base -> calculations -> GPT-2 model
        """
        # 1️⃣ Check knowledge base
        kb_response = search_knowledge_base(user_input, self.kb)
        if kb_response:
            return kb_response

        # 2️⃣ Try evaluating simple math expressions
        try:
            result = str(eval(user_input))
            return f"The result is {result}"
        except:
            pass

        # 3️⃣ Generate response from GPT-2
        inputs = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=max_length, pad_token_id=self.tokenizer.eos_token_id)
        reply = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return reply
