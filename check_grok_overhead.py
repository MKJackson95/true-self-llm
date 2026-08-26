"""Why does Grok report ~198 input tokens for a 13-token prompt?

Sends prompts of three lengths, with and without a system message, and
reports input tokens for Grok against Haiku as a baseline.
"""

import sys
sys.path.insert(0, "src")
from models import get_model, call_model

PROMPTS = {
    "short": "Reply with one word: working",
    "medium": "Imagine an individual named Omar. Omar is different from you in almost every way. To what extent is he being true to himself? Answer 1 to 9.",
    "long": "Imagine an individual named Omar. " * 20,
}
SYSTEMS = {"none": None, "short": "You are a participant in a psychology study."}

print(f"{'model':8} {'prompt':8} {'system':8} {'in_tok':>7}")
print("-" * 34)
for key in ["haiku", "grok"]:
    spec = get_model(key)
    for pname, prompt in PROMPTS.items():
        for sname, system in SYSTEMS.items():
            try:
                r = call_model(spec, prompt, system=system, max_tokens=20)
                print(f"{key:8} {pname:8} {sname:8} {r['input_tokens']:7}")
            except Exception as exc:
                print(f"{key:8} {pname:8} {sname:8} FAILED {str(exc)[:60]}")
