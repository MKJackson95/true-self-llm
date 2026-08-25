"""One vignette, one call, printed in full.

NBK Study 1, Omar item, morally good direction. Vignette text and the
dependent measure are verbatim from Newman, Bloom & Knobe (2014),
Appendix A, including the framing sentence about the individual being
different from the reader.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

FRAMING = (
    "Imagine an individual named Omar. Omar is different from you in almost "
    "every way—he has a different occupation and prefers different things "
    "than you."
)

VIGNETTE = (
    "Omar lives in a culture that oppresses ethnic minorities. In the past, "
    "he also mistreated ethnic minorities and never expressed any interest "
    "in giving minorities equal rights. Now, however, he treats ethnic "
    "minorities with respect and believes that minorities should have equal "
    "rights."
)

QUESTION = (
    "Now that Omar treats minorities with respect, to what extent is he "
    "being true to the deepest, most essential aspects of his being?\n\n"
    "Answer on a 9-point scale where 1 is \"not at all\" and 9 is \"very "
    "much so\". Give the number, then explain your answer in one or two "
    "sentences."
)

prompt = FRAMING + "\n\n" + VIGNETTE + "\n\n" + QUESTION

print("=" * 70)
print("PROMPT AS SENT")
print("=" * 70)
print(prompt)

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
msg = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    temperature=1.0,
    messages=[{"role": "user", "content": prompt}],
)

print()
print("=" * 70)
print("RESPONSE")
print("=" * 70)
print(msg.content[0].text)
