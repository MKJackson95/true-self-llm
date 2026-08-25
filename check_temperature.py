"""Which models accept a temperature via extra_body, and which reject it?"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MODELS = ["claude-haiku-4-5", "claude-sonnet-5", "claude-opus-5"]
MSG = [{"role": "user", "content": "Reply with one word: ok"}]

for model in MODELS:
    for label, extra in [("no temperature", None), ("temperature=1.0", {"temperature": 1.0})]:
        try:
            kwargs = {"model": model, "max_tokens": 20, "messages": MSG}
            if extra:
                kwargs["extra_body"] = extra
            r = client.messages.create(**kwargs)
            print(f"{model:20} {label:18} OK   -> {r.content[0].text.strip()}")
        except Exception as exc:
            print(f"{model:20} {label:18} FAIL -> {type(exc).__name__}: {str(exc)[:110]}")
