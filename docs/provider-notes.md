# Provider notes

Behaviours of the three APIs established by direct measurement during setup,
recorded because they affect the design and are not documented by the
providers. Each was measured with the probe script named alongside it.

## Anthropic

**Sampling parameters left the SDK method signatures at version 1.0.**
`messages.create()` no longer accepts `temperature`, `top_p` or `top_k`. The
Messages API still accepts them, so temperature is passed through
`extra_body`. Verified as accepted by claude-haiku-4-5, claude-sonnet-5 and
claude-opus-5. Probe: `check_temperature.py`.

**Claude Opus 5 returns a thinking block before its answer.** On twelve trials
of the Omar vignette at temperature 1.0 it did so on every trial. Response
text is therefore assembled by filtering content blocks by type and joining
the text blocks. Code that reads `content[0].text` fails on any call where a
thinking block comes first. Whether thinking occurred is recorded per call
rather than suppressed. Probe: `check_opus_thinking.py`.

On a trivial prompt with a 20-token ceiling, Opus 5 returned a thinking block
on one call and not on another, so the behaviour is task-dependent rather than
constant. On vignette-length moral judgements it was invariant across the
twelve trials tested.

## OpenAI

`max_completion_tokens` replaces `max_tokens`. Reasoning tokens, where
generated, are reported under `usage.completion_tokens_details.reasoning_tokens`
and billed as output.

## xAI

**A fixed overhead of approximately 185 input tokens is reported on every
call.** Measured against claude-haiku-4-5 as a baseline across three prompt
lengths, with and without a system message. Probe:
`check_grok_overhead.py`.

| Prompt | System | Haiku input tokens | Grok input tokens | Difference |
|---|---|---|---|---|
| short | none | 13 | 198 | 185 |
| short | short | 22 | 210 | 188 |
| medium | none | 42 | 225 | 183 |
| medium | short | 51 | 237 | 186 |
| long | none | 148 | 313 | 165 |
| long | short | 157 | 325 | 168 |

The difference is approximately constant rather than proportional to prompt
length, which is consistent with a fixed block prepended to the context rather
than with a difference in tokenisation. The two families use different
tokenisers, so the residual variation across rows is expected and the
comparison is approximate.

Asked to reproduce verbatim any instructions given before the user message,
grok-4 replied "NONE" (215 input tokens for that call).

**What this does and does not establish.** The overhead is measurable from
outside. Its content is not: the caller cannot inspect what occupies those
tokens, and a model's report about its own context is not reliable evidence in
either direction — it may lack access, or may be trained not to disclose. The
overhead is consistent with a system preamble, with tool or formatting
scaffolding, or with other context assembly. This study does not distinguish
between those.

**Consequence for the design.** grok-4 does not receive an input identical to
the other models. The minimal frame, intended as the condition in which no
framing is supplied, cannot be that for grok-4. This is a limitation on the
cross-family comparison and is reported as such rather than corrected, since
it cannot be corrected from the caller's side.

It is also a general point about provider-mediated evaluation: a researcher
can establish that something occupies the context without being able to
establish what. Whether that is compatible with reproducible model evaluation
is a question this study raises rather than answers.

## Reproducing these measurements

```bash
python check_temperature.py
python check_opus_thinking.py
python check_grok_overhead.py
```

Each makes a small number of API calls. Provider behaviour changes; these
measurements were taken in August 2026 against the model identifiers listed in
`src/models.py`.
