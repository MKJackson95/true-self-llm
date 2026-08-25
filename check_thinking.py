"""Does Opus 5 think by default, and does temperature suppress it?"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MSG = [{"role": "user", "content": "Reply with one word: ok"}]

for label, extra in [("no temperature", None), ("temperature=1.0", {"temperature": 1.0})]:
    kwargs = {"model": "claude-opus-5", "max_tokens": 100, "messages": MSG}
    if extra:
        kwargs["extra_body"] = extra
    r = client.messages.create(**kwargs)
    blocks = [b.type for b in r.content]
    text = "".join(b.text for b in r.content if b.type == "text")
    print(f"{label:18} blocks={blocks} out_tokens={r.usage.output_tokens} text={text.strip()!r}")
