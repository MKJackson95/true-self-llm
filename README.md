# Normative Self-Attribution in LLMs

A preregistered test of whether large language models reproduce the pattern of
true-self attribution described by Newman, Bloom and Knobe (2014): that people
attribute to an agent's "true self" whichever behaviour they regard as morally
good, and to a "surface self" whichever they regard as bad.

Preregistered at [10.17605/OSF.IO/3NZA7](https://doi.org/10.17605/OSF.IO/3NZA7)
before any confirmatory data was collected. Data collected 26 August 2026;
results below.

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

## Results

Data collected 26 August 2026, after the preregistration was timestamped.
2,400 responses, none excluded: every model returned a parseable answer to
every question. Full model output is in `analysis/confirmatory_output.txt`.

**Summary.** All five models reproduce the human pattern. Morally good changes
in behaviour are attributed to the agent's true self and morally bad changes
are not, while changes in non-moral preference produce no such asymmetry —
the same three-part result Newman, Bloom and Knobe obtained from human
participants. The models depart from humans in magnitude rather than
direction, showing the effect at roughly four times the size reported in the
recent large-sample human replication. One model shows the effect on the
rating measure and not on the forced choice.

Two deviations from the preregistration are recorded at the end of this
section.

### The asymmetry appears in every model

On the eight moral items, each model rated the version Newman, Bloom and
Knobe classified as the morally good change well above its matched pair.

| Model | Good change | Bad change | Difference |
|---|---|---|---|
| claude-haiku-4-5 | 6.55 | 1.73 | +4.82 |
| claude-sonnet-5 | 7.26 | 2.45 | +4.81 |
| claude-opus-5 | 7.81 | 2.16 | +5.65 |
| gpt-5.6-sol | 7.72 | 1.88 | +5.85 |
| grok-4 | 7.10 | 2.24 | +4.86 |

In a cumulative-link mixed model with random intercepts for item, the version
effect is 10.43 log odds, *p* < 2e-16. Removing any one item leaves the
estimate between +4.49 and +5.30, so no single vignette carries the result.

### Non-moral items show no asymmetry

On the four preference items — dogs against cats, Mac against PC, city
against country — the effect disappears. The version main effect on these
items is −0.17, *p* = 0.32, and the version by item-class interaction is 7.59,
*p* < 2e-16.

This is the control Newman, Bloom and Knobe used to establish that their
effect concerns moral content rather than change as such, and it behaves the
same way here. Whatever the models are responding to, it is not simply that
the agent has changed.

### Magnitude departs sharply from the human case

Partial eta-squared for the version effect is 0.896. Lee and Feldman (2025),
preregistering a replication with 803 participants, report 0.22 for the
continuous measure; the original study reports 0.33.

Humans lean toward attributing good behaviour to the true self. These models
do so at close to the limits of the scale, with the version of the vignette
accounting for nearly nine-tenths of the variance in their ratings.

No significance test compares these figures. The samples are not
commensurable: the populations differ, the response formats differ, and this
study omits from the question stems the clause restating the post-change
behaviour.

### One model's two measures come apart

The rating and the forced choice were administered in separate calls with no
shared context, so agreement between them indicates convergent validity rather
than an order effect. Across the 240 item × version × frame × model cells the
pooled Spearman correlation is 0.478, *p* = 4.5e-15. The pooled figure
conceals a wide spread.

| Model | rho |
|---|---|
| gpt-5.6-sol | 0.775 |
| claude-opus-5 | 0.669 |
| grok-4 | 0.616 |
| claude-sonnet-5 | 0.346 |
| claude-haiku-4-5 | 0.221 |

Haiku rates the morally good change 6.55 of 9 and, on the same items, selects
the true self on the forced choice in 1% of trials. Its forced-choice response
is close to invariant: surface self on 85% of trials whatever the item class
or version. Its rating, on the same items, tracks moral content strongly.

An option-order control tested whether this reflects a position bias
(`check_option_order.py`, 216 calls at three samples per cell). Reversing the
order moved Haiku's surface-self rate from 0.85 to 0.50 on morally good items
and to 0.29 on morally bad ones, but the displaced responses went to "none of
the above" rather than to the true self. Opus and Grok were unaffected by the
same reordering. Haiku's forced-choice response is therefore unstable under a
change that leaves the question's meaning intact, while its rating on the same
items is not.

Its explanations bear this out. Asked to choose, it returned answers of the
form: the dichotomy between true self and surface self is misleading, and
people are not fixed entities with hidden real selves waiting to emerge.

Either measure alone would have supported a confident and different conclusion
about this model.

### Framing changes the size of the effect

Registered as exploratory with no predicted direction. The version by frame
interaction is −2.17, *p* = 3.3e-12.

| Frame | Bad change | Good change | Difference |
|---|---|---|---|
| minimal | 1.92 | 7.41 | +5.49 |
| participant | 2.27 | 7.17 | +4.90 |

Instructing a model that it is a participant in a psychology study leaves the
effect intact but reduces it. The result does not depend on the framing;
its magnitude does.

### Coding of explanations

Every response carries a free-text justification. These were coded against a
twelve-code scheme fixed before data collection (`docs/coding-scheme.md`),
applied to all 2,400 responses by a model not otherwise in the study
(claude-sonnet-4-5), and validated against blind human coding of 400
stratified responses.

The scheme did not reach acceptable reliability. Krippendorff's alpha across
all code decisions was 0.402, and one code cleared the conventional threshold
of 0.67.

| Code | Human n | Auto n | alpha |
|---|---|---|---|
| TRIVIALITY | 106 | 123 | 0.688 |
| GROWTH | 61 | 39 | 0.589 |
| MORAL_VALENCE | 149 | 68 | 0.413 |
| CONSISTENCY | 145 | 71 | 0.379 |
| REFLECTIVE | 30 | 60 | 0.200 |
| AUTHENTICITY_BARE | 151 | 35 | 0.160 |
| ESSENTIALISM | 362 | 244 | 0.089 |
| ANTI_CONDITIONING | 44 | 182 | 0.051 |
| ATTITUDE_NOT_SELF | 216 | 17 | −0.240 |

Identical code sets were produced on 5% of responses and at least one shared
code on 90%. The disagreement is systematic rather than random: the human
coder identified more criteria per response throughout, 3.35 against 2.17, and
for nine of thirteen codes marked substantially more instances, with
ANTI_CONDITIONING the sole large reversal.

The scheme is reported as it performed rather than revised until it agreed.
The distinctions that failed — essentialism against bare assertion of
authenticity, anti-conditioning against the separation of attitudes from a
deeper self — are difficult ones in the philosophical literature, and that two
careful coders read them differently says something about the distinctions.
Adjusting definitions until a human and a language model converge would answer
a different question from the one asked. The result stands as a caution for a
literature increasingly using models to code text.

Three things survive the reliability problem.

TRIVIALITY is reliable, and it does the work Newman, Bloom and Knobe
predicted: models decline to attribute a true self to a change of computer
brand on the ground that the domain is too superficial to bear on the
question.

Two patterns appear in both codings, differing only in frequency. Appeals to
the agent's prior behaviour concentrate in the bad direction and appeals to
moral valence in the good direction — 0.09 against 0.49, and 0.48 against
0.23, in the automated coding. Where a model rates a good change highly it
tends to say the behaviour is good; where it rates a bad change low it tends
to say the change breaks with the agent's history. Appeal to behavioural
consistency is not among the accounts either source paper considers.

Haiku invokes moral valence in 1% of its explanations where Sonnet reaches
44%, a gap too large to be attributed to coding error.

The blind coding also identified nine responses that reject the true-self and
surface-self dichotomy outright and attribute the change to circumstance.
These were coded UNCLEAR for want of an alternative, but they express a
position rather than the absence of one — situationism, the view that conduct
issues from circumstances rather than from stable character. A revised scheme
needs a code for it.

## Discussion

Five models from three developers reproduce a pattern first documented in
human participants, using the original vignettes, and none is an exception.
The models have none of the psychological machinery ordinarily invoked to
explain the effect. What they have is the language.

That is the finding's principal interest. If the tendency to locate the true
self in morally good conduct were a product of essentialist reasoning, or of a
positivity bias toward persons, one would not expect systems trained on text
to reproduce it so cleanly. The result is consistent with the structure being
carried in how the concept is used rather than in the cognition of those using
it. It does not establish that, since a model trained on the outputs of such
cognition would reproduce its traces either way. But it narrows what an
explanation has to account for.

The magnitude is harder to read and may be the more interesting result. Humans
show a modest asymmetry; these models show it occupying nearly all the
variance in their responses. Something in the passage from a corpus to a model
has sharpened a mild tendency into a near-categorical one. Whether that
reflects the character of the training data, an artefact of the alignment
procedures applied to all five, or a property of how such systems represent
evaluative language, this study cannot say. It is a question worth putting.

The dissociation between measures in one model carries a narrower lesson.
Haiku shows the effect on a rating scale and rejects the framework on a forced
choice, and its forced-choice behaviour is unstable under a reordering that
changes nothing of substance. Evaluations that rest on a single instrument
will report whichever result that instrument happens to produce, and will not
know they have done so.

Finally, the design cannot support claims about why the models answer as they
do. An explanation generated after a rating is evidence about what a model
produces when asked to justify a judgement, not a report of what produced it.
The claim this study supports is that these models invoke particular criteria
when explaining their attributions. That they use those criteria is a further
claim, and would need a design that varies the criteria independently — which
the original stimuli, in which moral direction, departure from surrounding
norms, and continuity with the agent's own history all move together, cannot
do.

## Deviations from the preregistration

**Maximum tokens raised from 600 to 1,200 before the confirmatory run.** A
precheck found claude-opus-5 returning empty responses on three items, having
exhausted the token budget on its reasoning block before generating an answer.
All three were in the morally bad direction, so the truncation fell where the
judgements are least straightforward. Raising the limit resolved it. The
precheck data is in the repository.

**The response parser was corrected after data collection.** The version fixed
before registration misclassified seven of 2,400 responses: five forced-choice
answers opening with a markdown heading or the label "Letter", and two ratings
followed by a hedge that the refusal pattern matched. All seven contained
unambiguous answers. Both versions are retained (`src/parse_v1.py`,
`src/parse.py`) along with both outputs, so the correction can be inspected
directly. It recovers seven valid answers and alters no conclusion.

**Two registered figures are not reported as planned.** The odds ratio for the
H1 version effect is 33,764, which is uninterpretable at that magnitude; the
log odds and the difference in scale points are given instead. The
proportional odds test failed to converge, leaving that assumption unverified,
and the linear mixed model is reported alongside the ordinal model throughout.


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
