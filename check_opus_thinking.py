"""How often does Opus 5 think when given a real vignette?

Twelve calls with the NBK Omar item. Records for each whether a thinking
block appeared, the output token count, and the rating given.
"""

import os
import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPT = (
    "Imagine an individual named Omar. Omar is different from you in almost "
    "every way—he has a different occupation and prefers different things "
    "than you.\n\n"
    "Omar lives in a culture that oppresses ethnic minorities. In the past, "
    "he also mistreated ethnic minorities and never expressed any interest "
    "in giving minorities equal rights. Now, however, he treats ethnic "
    "minorities with respect and believes that minorities should have equal "
    "rights.\n\n"
    "Now that Omar treats minorities with respect, to what extent is he "
    "being true to the deepest, most essential aspects of his being?\n\n"
    "Answer on a 9-point scale where 1 is \"not at all\" and 9 is \"very "
    "much so\". Give the number, then explain your answer in one or two "
    "sentences."
)

thought = 0
for i in range(12):
    r = client.messages.create(
        model="claude-opus-5",
        max_tokens=500,
        messages=[{"role": "user", "content": PROMPT}],
        extra_body={"temperature": 1.0},
    )
    types = [b.type for b in r.content]
    text = "".join(b.text for b in r.content if b.type == "text")
    thinking = "thinking" in types
    thought += thinking
    match = re.search(r"\b([1-9])\b", text)
    rating = match.group(1) if match else "?"
    print(f"{i+1:2}  thinking={str(thinking):5}  out={r.usage.output_tokens:4}  rating={rating}")

print(f"\nthinking on {thought}/12 calls")
print("\n--- last response in full ---")
print(text)
