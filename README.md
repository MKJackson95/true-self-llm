# Normative Self-Attribution in LLMs

A preregistered test of whether large language models reproduce the pattern of
true-self attribution described by Newman, Bloom and Knobe (2014): that people
attribute to an agent's "true self" whichever behaviour they regard as morally
good, and to a "surface self" whichever they regard as bad.

**No confirmatory data has been collected.** This README describes what the
study will do. It was written before the data exists and the commit history
shows when. Results will be added when they exist, whatever they show.

## Preregistration

Registered on OSF before any confirmatory data was collected:
[10.17605/OSF.IO/3NZA7](https://doi.org/10.17605/OSF.IO/3NZA7)

## Questions

Do models show the asymmetry, and how large is it relative to the human
effect?

Does it hold for non-moral preference changes, which in humans it does not?

What criteria do models invoke when explaining their judgements, and do models
differ?

Does any effect survive a change of prompt framing?

## Design

The stimuli are the twelve vignette pairs of NBK Study 1 — eight moral
behaviour changes and four non-moral preference changes — run verbatim,
including the framing sentence telling the reader the agent differs from them
in almost every way. That sentence was written to reduce projection in a human
reader; here it is given to systems with no self to project.

Two measures, crossed with two prompt frames, over both directions of change:

| Factor | Levels |
|---|---|
| version | the two directions of change in each pair |
| measure | forced choice (true self / surface self / neither); 9-point rating |
| frame | minimal (no system prompt); participant (psychology-study framing) |

Twelve items × 2 versions × 2 measures × 2 frames = 96 presentations, run at
five samples per model.

### Two deviations from the original

**The question stems drop the clause restating the post-change behaviour.**
NBK ask "Now that Omar treats minorities with respect, to what extent…". That
clause summarises the change and selects which element of the vignette is
being asked about. Since this study asks what the model treats as the relevant
change and on what basis, supplying that selection would answer part of the
question in advance. Comparison against published human means is therefore
approximate, resting on effect direction and magnitude rather than absolute
values.

**The two measures are asked in separate calls with no shared context.** In
the original they were answered in sequence, so the forced choice conditioned
the rating that followed. Running them independently is what makes their
agreement evidence of convergent validity rather than of consistency.

## Human benchmarks

Two, both reported.

Newman, Bloom and Knobe (2014), the original: per-item means for all twelve
pairs, and partial eta-squared of 0.39 for the forced choice and 0.33 for the
continuous measure in Study 1.

Lee and Feldman (2025), a Registered Report replication with 803 participants:
both effects replicated at smaller magnitudes, 0.20 and 0.22 respectively. The
larger sample and preregistration make this the better comparison. Their
extension is directly relevant here — they measured perceived social norms
alongside true-self attribution and found the association positive but weak,
with correlations mostly between .07 and .21. Any strong norm-based reasoning
in models is therefore a divergence from the human pattern rather than a
match.

Note that Lee and Feldman altered the framing sentence to be gender-neutral.
This study follows NBK's original wording.

## What the models say

The rating measures how strongly the true self is attributed. It cannot
measure on what grounds, and several accounts predict identical ratings for
opposite reasons. Every response is collected with its explanation and coded
against a scheme fixed before the confirmatory run: `docs/coding-scheme.md`.

Twelve codes. Seven are drawn from the source papers — moral valence,
reflective endorsement, emotion and desire, meta-desires, psychological
essentialism, person-positivity, and the distinction between general attitudes
and a deeper self. One, anti-conditioning, is present in NBK's materials but
never treated by them as a rival criterion. Two emerged from pilot responses
and are marked as such: appeals to the agent's behavioural record, and
dismissal of a domain as too superficial to bear on the true self. The
remainder are residual.

A claim this design supports: the models invoke criterion X when explaining
their judgements. A claim it does not: the models use criterion X. A generated
explanation is evidence about what a model produces when asked to justify a
judgement, not a readout of what produced the judgement.

## Sample size

Five samples per model per presentation, from simulation
(`src/simulate_power.py`) against variance measured directly
(`measure_variance.py`).

Within-cell standard deviations ranged from 0.00 to 0.73 against valence
differences of 2.5 to 5.9 scale points, so the primary effect is at ceiling
power with three samples. The binding constraints are the frame comparison and
the moral-against-non-moral comparison, and both are governed by item count
rather than by samples per cell: raising samples from three to eight moves
power on the item-class comparison from 0.84 to 0.86, where raising items from
twelve to sixteen moves it from 0.84 to 0.94. Five samples gives margin on the
frame comparison at the item count the replication fixes.

## Analysis

Ratings are ordinal and clustered within items. Cumulative-link mixed models
with random intercepts for item and model as a fixed effect. Repeated samples
from one model are not independent participants and nothing is reported as
though they were. Effect sizes rather than raw means when comparing against
human data.

## Models

| Family | Models |
|---|---|
| Anthropic | claude-haiku-4-5, claude-sonnet-5, claude-opus-5 |
| OpenAI | gpt-5.6-sol |
| xAI | grok-4 |

The Anthropic family is run across three tiers and the others at flagship tier
only. This asymmetry is deliberate: the pilot found the three Claude models
diverging sharply from one another, with one showing a large asymmetry and
another none. Any claim about a family as a whole rests on a single model for
OpenAI and xAI.

Three API behaviours were established by direct measurement and are documented
in `docs/provider-notes.md`: sampling parameters must be passed through
`extra_body` on the Anthropic SDK; Claude Opus 5 returns a thinking block
before its answer on every vignette trial tested, and whether thinking occurred
is recorded per call; and the xAI API reports a fixed overhead of roughly 185
input tokens whose content is not visible to the caller, so grok-4 does not
receive an input identical to the other models.

## Repository

```
stimuli/     vignettes as versioned JSON
src/         prompt construction, model adapter, runner, parser, simulation
data/raw/    one JSON line per response, raw text preserved
data/processed/  parsed CSV
docs/        coding scheme, provider notes
```

Raw responses are the evidence and are never modified. The parsed table is
derived; if the extraction rules prove wrong the data is re-parsed rather than
re-collected.

## Prior work

An exploratory pilot across three Claude models motivated this design:
[knobe-pilot](https://github.com/MKJackson95/knobe-pilot). It was not
preregistered and its forced-integer response format produced near-zero
variance in most cells and collected no reasoning. Both problems are addressed
here.

## Scope

This study is descriptive: present the vignettes, record what is attributed
and how it is explained. It does not manipulate the factors that NBK's items
hold together — moral direction, relation to the surrounding norm, and
continuity with the agent's own past all move together in every one of their
pairs. Separating them requires new stimuli and is the natural follow-up,
better motivated once the coding shows which criteria actually appear.

## References

Knobe, J. (2005). Ordinary ethical reasoning and the ideal of 'being
yourself'. *Philosophical Psychology*, 18(3), 327–340.

Lee, S. C., & Feldman, G. (2025). Revisiting the link between true-self and
morality: Replication and extension Registered Report of Newman, Bloom, and
Knobe (2014) Studies 1 and 2. *Royal Society Open Science*.
doi:10.1098/rsos.250908

Newman, G. E., Bloom, P., & Knobe, J. (2014). Value judgments and the true
self. *Personality and Social Psychology Bulletin*, 40(2), 203–216.

Newman, G. E., De Freitas, J., & Knobe, J. (2015). Beliefs about the true self
explain asymmetries based on moral judgment. *Cognitive Science*, 39(1),
96–125.

Strohminger, N., Knobe, J., & Newman, G. (2017). The true self: A
psychological concept distinct from the self. *Perspectives on Psychological
Science*, 12(4), 551–560.

## Licence

Code under MIT. Stimuli and data under CC BY 4.0.
