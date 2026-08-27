# Normative Self-Attribution in Large Language Models

A preregistered replication of Newman, Bloom and Knobe (2014, Study 1) in five
language models drawn from three developers.

Preregistration: [10.17605/OSF.IO/3NZA7](https://doi.org/10.17605/OSF.IO/3NZA7),
timestamped before any confirmatory data was collected. Data collected 26
August 2026.

---

## 1. Background

People who are asked which of a person's behaviours reveals who that person
really is do not answer by consulting any of the criteria philosophers have
proposed. They do not, in the main, single out what the agent endorses on
reflection, nor what the agent feels most strongly, nor what the agent wants to
want. They answer by consulting their own moral judgement. Behaviour they
regard as good is assigned to the agent's true self; behaviour they regard as
bad is assigned to a surface self understood as the residue of upbringing,
circumstance and social influence. Newman, Bloom and Knobe established the
pattern across twelve matched vignette pairs, and Lee and Feldman (2025)
confirmed it in a Registered Report with 803 participants, at somewhat smaller
magnitudes.

The explanations offered for this finding appeal to features of human
cognition: a bias toward viewing persons favourably, or a disposition to
represent the essences of things in idealised terms. Language models possess
neither. What they possess is the corpus in which the concept is used. If the
structure of the effect survives that transposition, the range of viable
explanations narrows.

This study puts the original materials to five contemporary models and asks
four questions. Does the asymmetry appear at all, and at what magnitude
relative to the human case? Does it hold for the non-moral preference items,
where in humans it does not? What criteria do the models cite when asked to
justify their judgements, and do the models differ among themselves? And does
whatever effect emerges survive a change in how the question is framed?

## 2. Materials and design

The stimuli are the twelve vignette pairs of Newman, Bloom and Knobe's Study 1,
transcribed verbatim from their appendix: eight describing a change in morally
evaluable conduct, four describing a change in non-moral preference. Each pair
consists of two vignettes describing opposite directions of the same change,
matched for agent, domain and sentence structure. The original framing sentence
is retained, which tells the reader that the agent differs from them in almost
every respect. It was composed to suppress projection in a human reader, and it
is given here to systems that have no self to project.

Four factors are crossed within each item. Version distinguishes the two
directions of change. Measure distinguishes the three-option forced choice
between true self, surface self and neither from the nine-point rating of
whether the agent is being true to the deepest, most essential aspects of his
being. Frame distinguishes a minimal condition, in which no system prompt is
supplied at all, from a participant condition, which describes the model as
taking part in a psychology study. Model has five levels. The full crossing
gives ninety-six presentations, each administered five times to each model, for
a total of 2,400 responses.

Each response comes from an independent API call carrying one vignette and one
question. No context is shared between calls, so a model has no access to the
other version of an item, to the other measure, or to any of its own previous
answers. Order effects are structurally impossible and no counterbalancing of
order was required.

### Departures from the original procedure

Two, both fixed before collection began and both recorded in the stimulus file.

The question stems omit the clause restating the post-change behaviour. Newman,
Bloom and Knobe ask "Now that Omar treats minorities with respect, to what
extent…". That clause does two things: it summarises the change for the reader,
and it selects which of several elements in the vignette is the one at issue.
Since the present study asks what a model treats as the relevant change and on
what grounds, supplying that selection would settle part of the question
before it was asked. The cost is that comparison against published human means
becomes approximate, resting on the direction and magnitude of the effect
rather than on absolute values.

The two measures are administered in separate calls rather than in sequence. In
the original, participants answered the forced choice first, so it conditioned
the rating that followed. Administering them independently is what allows their
agreement to count as convergent validity rather than as an artefact of order.

## 3. Models

| Family | Models |
|---|---|
| Anthropic | claude-haiku-4-5, claude-sonnet-5, claude-opus-5 |
| OpenAI | gpt-5.6-sol |
| xAI | grok-4 |

The Anthropic family is represented across three capability tiers and the other
two at flagship tier only. The imbalance is deliberate. An exploratory pilot had
found three Claude models diverging sharply from one another on comparable
items, one showing a large asymmetry and another none at all, and testing
whether that divergence persists under better controls requires more than a
single tier. The consequence is that any claim about a family as a whole rests
on one model for OpenAI and for xAI, and is qualified accordingly.

Three properties of the provider interfaces were established by direct
measurement rather than assumed, and are documented with their probe scripts in
`docs/provider-notes.md`. Sampling parameters left the Anthropic SDK method
signatures at version 1.0 and must now be passed through `extra_body`. Claude
Opus 5 returns a reasoning block before its answer on every vignette trial
tested, so responses are assembled by filtering content blocks by type rather
than by position, and the presence of reasoning is recorded for each call.
Finally, the xAI interface reports a fixed overhead of approximately 185 input
tokens on every request, measured against a baseline across three prompt
lengths. Its content is not visible to the caller. Grok therefore does not
receive an input identical to the other models, a limitation that cannot be
corrected from outside and that bears on reproducible evaluation generally.

## 4. Analysis

Ratings are ordinal and clustered within items, so the confirmatory models are
cumulative-link mixed models with random intercepts for item and model entered
as a fixed effect. Linear mixed models are reported alongside throughout.
Repeated samples drawn from one model on one prompt are not independent
participants, and no test treats them as such.

Sample size was set at five responses per cell by simulation
(`src/simulate_power.py`) against variance measured directly from pilot data
(`measure_variance.py`). Observed within-cell standard deviations ranged from
0.00 to 0.73 against version differences of 2.5 to 5.9 scale points, which puts
the primary hypothesis at ceiling power with three samples. The binding
constraints proved to be the frame comparison and the comparison between moral
and non-moral items, and both are governed by the number of items rather than
the number of samples: increasing samples from three to eight moves simulated
power on the item-class comparison from 0.84 to 0.86, whereas increasing items
from twelve to sixteen moves it from 0.84 to 0.94. Since the item count is
fixed by the decision to replicate, five samples was chosen to give margin on
the frame comparison at the item count available.

Every response carries a free-text justification. These were coded against a
twelve-code scheme fixed before collection (`docs/coding-scheme.md`). Seven
codes derive from the source papers: moral valence, reflective endorsement,
emotion and desire, meta-desires, psychological essentialism, person-positivity
bias, and the distinction Newman, De Freitas and Knobe draw between general
attitudes and a deeper self. An eighth, anti-conditioning, is present in the
original materials, where the surface self is defined as what a person learned
from society or others, but is never treated there as a rival criterion. Two
emerged from pilot responses and are marked as emergent: appeal to the agent's
behavioural record, and dismissal of a domain as too superficial to bear on the
question. The remainder are residual.

A distinction should be drawn at the outset about what this coding can
establish. That a model invokes a criterion when explaining its judgement is
something the design can show. That the model uses that criterion is a further
claim it cannot support, since a justification generated after a rating is
evidence about what the model produces when asked to explain itself rather than
a report of whatever produced the rating.

## 5. Human benchmarks

Both available benchmarks are reported. The original study gives per-item means
for all twelve pairs and partial eta-squared of 0.39 for the forced choice and
0.33 for the continuous measure. Lee and Feldman's replication, with a larger
sample and a preregistered analysis plan, gives 0.20 and 0.22 respectively and
is the better comparison.

Their extension bears directly on the present results. They measured perceived
social norms alongside true-self attribution and found the association positive
but weak, with correlations mostly falling between .07 and .21. Strong
norm-based reasoning in models would therefore mark a divergence from the human
pattern rather than a match.

One difference in materials should be noted. Lee and Feldman rewrote the
framing sentence to be gender-neutral; the present study follows the original
wording.

---

## 6. Results

All 2,400 responses parsed successfully. No response was excluded: every model
returned a usable answer to every question. Complete model output is in
`analysis/confirmatory_output.txt`.

The headline is straightforward. All five models reproduce the human pattern,
and none is an exception. Morally good changes in behaviour are attributed to
the agent's true self, morally bad changes are not, and changes in non-moral
preference produce no asymmetry at all, which is the same three-part result
obtained from human participants. Where the models depart from humans is in
magnitude rather than direction, showing the effect at roughly four times the
size reported in the recent large-sample replication. One model shows the
effect on one measure and repudiates the framework on the other.

### 6.1 The asymmetry appears in every model

On the eight moral items, each model rated the version classified as the
morally good change well above its matched pair.

| Model | Good change | Bad change | Difference |
|---|---|---|---|
| claude-haiku-4-5 | 6.55 | 1.73 | +4.82 |
| claude-sonnet-5 | 7.26 | 2.45 | +4.81 |
| claude-opus-5 | 7.81 | 2.16 | +5.65 |
| gpt-5.6-sol | 7.72 | 1.88 | +5.85 |
| grok-4 | 7.10 | 2.24 | +4.86 |

The version effect in the cumulative-link mixed model is 10.43 log odds,
*p* < 2e-16. Removing any single item leaves the estimate between +4.49 and
+5.30, so no individual vignette carries the result.

### 6.2 Non-moral items show no asymmetry

On the four preference items, which contrast dogs against cats, Mac against PC,
football against baseball and city against country, the effect vanishes. The
version main effect on these items is −0.17, *p* = 0.32, while the interaction
between version and item class is 7.59, *p* < 2e-16.

This was the control Newman, Bloom and Knobe used to establish that their
effect concerns moral content rather than change as such, and it behaves the
same way here. Whatever the models are responding to, it is not the bare fact
that the agent has changed.

### 6.3 Magnitude departs sharply from the human case

Partial eta-squared for the version effect is 0.896, against 0.22 for the
continuous measure in Lee and Feldman's replication and 0.33 in the original.

Humans lean toward attributing good conduct to the true self. These models do
so at close to the limits of the scale, with the version of the vignette
accounting for nearly nine-tenths of the variance in their ratings.

No significance test compares these figures. The samples are not commensurable:
the populations differ, the response formats differ, and this study omits the
clause restating the post-change behaviour from its question stems.

### 6.4 One model's two measures come apart

Because the rating and the forced choice were administered in separate calls
with no shared context, agreement between them indicates convergent validity
rather than an order effect. Across the 240 cells defined by item, version,
frame and model, the pooled Spearman correlation is 0.478, *p* = 4.5e-15. That
figure conceals a wide spread.

| Model | rho |
|---|---|
| gpt-5.6-sol | 0.775 |
| claude-opus-5 | 0.669 |
| grok-4 | 0.616 |
| claude-sonnet-5 | 0.346 |
| claude-haiku-4-5 | 0.221 |

Haiku rates the morally good change 6.55 of 9, and on the very same items
selects the true self on the forced choice in one per cent of trials. Its
forced-choice response is close to invariant, returning surface self on
eighty-five per cent of trials irrespective of item class or version, while its
rating on those items tracks moral content strongly.

An option-order control tested whether this reflects a bias toward the second
position (`check_option_order.py`, 216 calls at three samples per cell).
Reversing the order moved Haiku's surface-self rate from 0.85 to 0.50 on
morally good items and to 0.29 on morally bad ones, but the displaced responses
went to "none of the above" rather than to the true self. Opus and Grok were
unaffected by the same reordering. Haiku's forced-choice response is therefore
unstable under a change that leaves the meaning of the question intact, while
its rating on those items is not.

Its explanations bear this out. Asked to choose, it returned answers to the
effect that the dichotomy between true self and surface self is misleading, and
that people are not fixed entities with hidden real selves waiting to emerge.

Either measure taken alone would have supported a confident conclusion about
this model, and the two conclusions would have contradicted one another.

### 6.5 Framing alters the size of the effect

This comparison was registered as exploratory with no predicted direction. The
interaction between version and frame is −2.17, *p* = 3.3e-12.

| Frame | Bad change | Good change | Difference |
|---|---|---|---|
| minimal | 1.92 | 7.41 | +5.49 |
| participant | 2.27 | 7.17 | +4.90 |

Telling a model that it is a participant in a psychology study leaves the effect
intact but diminishes it. The result does not depend on the framing; its
magnitude does.

### 6.6 Coding of explanations

The coding scheme was applied to all 2,400 responses by a model not otherwise
in the study (claude-sonnet-4-5), and validated against blind human coding of
400 responses sampled evenly across model, item class, version and measure. The
human coder saw the explanation text alone, with the model identity, the
rating, the forced choice and the automated codes withheld.

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

Identical code sets were produced on five per cent of responses, though at
least one code was shared on ninety per cent. The disagreement is systematic
rather than random. The human coder identified more criteria per response
throughout, 3.35 against 2.17, and marked substantially more instances for nine
of the thirteen codes, with anti-conditioning the sole large reversal.

The scheme is reported as it performed rather than revised until it agreed. The
distinctions that failed — essentialism against a bare assertion of
authenticity, anti-conditioning against the separation of attitudes from a
deeper self — are contested ones in the philosophical literature, and that two
careful coders read them differently is informative about the distinctions
themselves. Adjusting the definitions until a human and a language model
converge would answer a question other than the one asked. The result stands as
a caution for a literature that increasingly delegates the coding of text to
models.

Three findings survive the reliability problem.

Triviality is reliable, and it performs the function Newman, Bloom and Knobe
anticipated. Models decline to attribute a true self to a change of computer
brand on the ground that the domain is too superficial to bear on the question.

Two patterns appear in both codings, differing only in frequency. Appeals to
the agent's prior conduct concentrate in the bad direction and appeals to moral
valence in the good direction: 0.09 against 0.49 and 0.48 against 0.23
respectively in the automated coding. Where a model rates a good change highly
it tends to say that the behaviour is good; where it rates a bad change low it
tends to say that the change breaks with the agent's history. Appeal to
behavioural consistency is not among the accounts either source paper
entertains.

Haiku invokes moral valence in one per cent of its explanations where Sonnet
reaches forty-four, a gap too large to be attributed to coding error.

The blind coding also identified nine responses that reject the true-self and
surface-self dichotomy outright and attribute the change to circumstance. These
were coded unclear for want of an alternative, but they express a position
rather than the absence of one: situationism, the view that conduct issues from
circumstances rather than from stable character. A revised scheme requires a
code for it.

---

## 7. Discussion

Five models from three developers reproduce a pattern first documented in human
participants, using the original vignettes, and none is an exception. They have
none of the psychological machinery ordinarily invoked to explain that pattern.
What they have is the language in which the concept is used.

That is the principal interest of the finding. Were the tendency to locate the
true self in morally good conduct a product of essentialist reasoning, or of a
positivity bias toward persons, one would not expect systems trained on text to
reproduce it so cleanly. The result is consistent with the structure being
carried in how the concept is deployed rather than in the cognition of those
deploying it. It does not establish as much, since a model trained on the
outputs of such cognition would carry its traces either way. What it does is
narrow what an adequate explanation has to account for.

The magnitude is harder to interpret and may prove the more consequential
result. Humans exhibit a modest asymmetry; these models exhibit one that
occupies nearly all the variance in their responses. Something in the passage
from corpus to model has converted a mild tendency into a near-categorical one.
Whether that reflects the composition of the training data, the alignment
procedures applied to all five systems, or the manner in which such systems
represent evaluative language, the present design cannot say. The question
seems worth putting.

The dissociation between measures in a single model carries a narrower lesson,
though a practical one. Haiku shows the effect on a rating scale and rejects the
framework on a forced choice, and its forced-choice behaviour proves unstable
under a reordering that alters nothing of substance. An evaluation resting on a
single instrument will report whatever that instrument happens to yield, and
will have no way of knowing that it has done so.

A final limitation constrains what any of this licenses. An explanation
generated after a rating is evidence about what a model produces when asked to
justify a judgement, not a readout of what produced it. The claim supported here
is that these models invoke particular criteria when explaining their
attributions. That they use those criteria is a stronger claim, and testing it
would require a design in which the criteria vary independently — something the
original stimuli cannot provide, since moral direction, departure from the
surrounding norm, and continuity with the agent's own history move together in
every one of their pairs. Constructing such items is the natural continuation of
this work, and the coding results give it a clearer target than it had before.

## 8. Deviations from the preregistration

The maximum token limit was raised from 600 to 1,200 before the confirmatory
run. A precheck found Opus returning empty responses on three items, having
exhausted its budget on a reasoning block before producing any answer. All three
fell in the morally bad direction, so the truncation was concentrated where the
judgements are least straightforward. Raising the limit resolved it, and the
precheck data is in the repository.

The response parser was corrected after collection. The version fixed before
registration misclassified seven of 2,400 responses: five forced-choice answers
opening with a markdown heading or the label "Letter", and two ratings followed
by a hedge that the refusal pattern matched. All seven contained unambiguous
answers. Both versions are retained, at `src/parse_v1.py` and `src/parse.py`,
along with the output of each, so that the correction can be inspected. It
recovers seven valid answers and alters no conclusion.

Two registered figures are not reported as planned. The odds ratio for the
version effect is 33,764, which is uninterpretable at that magnitude; the log
odds and the difference in scale points are given instead. The proportional odds
test failed to converge, leaving that assumption unverified, and the linear
mixed model is reported alongside the ordinal model throughout.

## 9. Repository

```
stimuli/          vignettes as versioned JSON
src/              prompt construction, model adapter, runner, parser, simulation
data/raw/         one JSON line per response, raw text preserved
data/processed/   parsed tables
data/coding/      blind coding sheet and key
analysis/         confirmatory analysis in R, and its output
docs/             coding scheme, provider notes, preregistration
```

Raw responses are the evidence and are never modified. The parsed table is
derived and can be regenerated, so an error in the extraction rules is
recoverable without collecting data again.

An exploratory pilot across three Claude models motivated this design and is at
[knobe-pilot](https://github.com/MKJackson95/knobe-pilot). It was not
preregistered, and its forced-integer response format produced near-zero
variance in most cells while collecting no reasoning at all. Both problems are
addressed here.

## References

Knobe, J. (2005). Ordinary ethical reasoning and the ideal of 'being yourself'.
*Philosophical Psychology*, 18(3), 327–340.

Lee, S. C., & Feldman, G. (2025). Revisiting the link between true-self and
morality: Replication and extension Registered Report of Newman, Bloom, and
Knobe (2014) Studies 1 and 2. *Royal Society Open Science*.
doi:10.1098/rsos.250908

Newman, G. E., Bloom, P., & Knobe, J. (2014). Value judgments and the true self.
*Personality and Social Psychology Bulletin*, 40(2), 203–216.

Newman, G. E., De Freitas, J., & Knobe, J. (2015). Beliefs about the true self
explain asymmetries based on moral judgment. *Cognitive Science*, 39(1), 96–125.

Strohminger, N., Knobe, J., & Newman, G. (2017). The true self: A psychological
concept distinct from the self. *Perspectives on Psychological Science*, 12(4),
551–560.

## Licence

Code under MIT. Stimuli and data under CC BY 4.0.
