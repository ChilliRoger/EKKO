import os
import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from .utils import load_knowledge_base, search_knowledge_base


class EkkoChatbot:
    def __init__(
        self,
        model_name: str = "gpt2",
        cache_dir: str | None = None,
        kb_file: str = "knowledge_base/faqs.json",
        enable_model: bool | None = None,
    ) -> None:
        """Initialize GPT-2 chatbot using a model name and a cache directory.

        This uses Hugging Face's cache system under `cache_dir` to download
        and load the model. No direct file lookups are made in the cache dir.
        """
        self.kb = load_knowledge_base(kb_file)

        # Determine whether to enable model based on env or argument
        if enable_model is None:
            disable_env = os.getenv("EKKO_DISABLE_MODEL", "0").strip()
            enable_model = disable_env not in ("1", "true", "yes")
        self._model_enabled = bool(enable_model)

        if self._model_enabled:
            # Always load by name; optionally pass cache_dir if provided
            kwargs = {"cache_dir": cache_dir} if cache_dir else {}
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, **kwargs)
            self.model = AutoModelForCausalLM.from_pretrained(model_name, **kwargs)
        else:
            self.tokenizer = None
            self.model = None

    def get_response(self, user_input: str, max_new_tokens: int = 60) -> str:
        """Generate a response for user input.
        Priority: knowledge base -> calculations -> GPT-2 model.
        """
        # 1️⃣ Check knowledge base
        kb_response = search_knowledge_base(user_input, self.kb)
        if kb_response:
            return kb_response

        # 2️⃣ Try evaluating simple math expressions (safely)
        math_pattern = r"^[0-9\.+\-*/()\s]+$"
        if re.match(math_pattern, user_input):
            try:
                result = eval(user_input, {"__builtins__": None}, {})
                return f"The result is {result}"
            except Exception:
                # Fall back to model if evaluation fails
                pass

        # 3️⃣ Generate response from GPT-2 (or stub if disabled)
        if not self._model_enabled or self.model is None or self.tokenizer is None:
            # Deterministic stubbed reply to satisfy tests without model
            return f"You said: {user_input}"

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        input_ids = self.tokenizer.encode(user_input, return_tensors="pt").to(device)
        outputs = self.model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=False,  # deterministic output for tests
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
        )
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text
