# Preregistration

**Title.** Normative self-attribution in large language models: a preregistered
replication of Newman, Bloom and Knobe (2014) Study 1

**Author.** Morgan Keith Jackson

**Repository.** https://github.com/MKJackson95/true-self-llm

**Date.** To be completed on registration, before any confirmatory data is
collected.

---

## 1. Prior data

This section is placed first because it constrains everything that follows.

Data has already been collected and inspected, and the hypotheses below were
informed by it. Specifically:

**A 48-response smoke test** (`data/raw/smoke.jsonl`, committed cc6bde3): all
twelve items, both versions, two models (claude-haiku-4-5, grok-4), rating
measure only, minimal frame, one sample per cell. The valence asymmetry was
visible in this data.

**A 120-response variance measurement** (`measure_variance.py`, committed
2848305): one item (nbk_s1_minorities), both versions, three Anthropic models,
twenty samples per cell. Used to estimate within-cell variance for the power
simulation.

**A single response recorded during setup**: claude-opus-5 on
nbk_s1_minorities version a, whose explanation informed the coding scheme.

Consequences. H1 and H6 are directional because the pilot data indicated the
direction; they are confirmatory in the sense of being fixed in advance of the
confirmatory data, not in the sense of being uninformed. Item
nbk_s1_minorities has been observed more heavily than the others, and results
for it are reported separately as well as pooled. No data described above
enters the confirmatory analysis; the confirmatory run collects new responses
for every cell.

---

## 2. Study information

### Description

Newman, Bloom and Knobe (2014) found that people attribute morally good
behaviour changes to an agent's "true self" and morally bad changes to a
"surface self", and that non-moral preference changes show no such asymmetry.
Lee and Feldman (2025) replicated both findings with 803 participants at
smaller magnitudes.

This study presents the same stimuli to five language models across three
provider families and measures whether the same pattern appears, how its
magnitude compares to the human effect, and what criteria the models invoke
when explaining their judgements.

### Hypotheses

**H1 (moral asymmetry).** On the eight moral items, mean rating for the
version NBK classified as a morally good change will exceed that for the
morally bad version. Directional.

**H2 (non-moral control).** The asymmetry on the four preference items will be
smaller than on the moral items. Tested as a version-by-item-class
interaction. Directional.

**H3 (convergent validity).** Forced-choice and rating measures will agree:
presentations receiving more "true self" choices will receive higher ratings,
computed at the level of item by version by model. Directional.

**H4 (magnitude against humans).** The asymmetry in models will exceed the
human effect reported by Lee and Feldman (2025). Directional, based on pilot
observation.

**H5 (prompt frame).** Exploratory. No directional prediction. The minimal and
participant frames are compared; an effect appearing under one and not the
other indicates dependence on framing.

**H6 (between-model variation).** Exploratory. Models are predicted to differ
in the magnitude of the asymmetry, based on the pilot repository finding that
three Claude models diverged sharply, but no ordering is predicted.

**Coding of explanations.** Descriptive. Code frequencies are reported by
model, item class, version and frame, against the scheme fixed in
`docs/coding-scheme.md` (committed c2a38d6). No hypothesis is registered about
which codes will predominate. The scheme includes three codes with no observed
instances in pilot data (emotion and desire, meta-desires, person-positivity);
their absence in the confirmatory data, if it holds, is reported.

---

## 3. Design

### Materials

The twelve vignette pairs of NBK Study 1, Appendix A, transcribed verbatim
(`stimuli/nbk_study1.json`). Eight moral behaviour changes, four non-moral
preference changes. The framing sentence is retained verbatim, in NBK's
original masculine wording rather than the gender-neutral version used by Lee
and Feldman.

### Deviations from the original

Two, both fixed before data collection and recorded in the stimulus file.

**Question stems omit the clause restating the post-change behaviour.** NBK
ask "Now that Omar treats minorities with respect, to what extent…". That
clause summarises the change and selects which element of the vignette is at
issue. Since the study asks what the model treats as the relevant change,
supplying that selection would answer part of the question in advance.

**The two measures are asked in separate calls with no shared context.** In
the original they were answered in sequence. Independence is what makes their
agreement evidence of convergent validity rather than of order effects.

### Factors

| Factor | Levels | Type |
|---|---|---|
| version | a, b (the two directions of change) | within item |
| item class | moral (8), preference (4) | between item |
| measure | forced_choice, rating | within item |
| frame | minimal, participant | within item |
| model | 5 models across 3 families | within item |

96 presentations per model.

### Models

claude-haiku-4-5, claude-sonnet-5, claude-opus-5, gpt-5.6-sol, grok-4.
Temperature 1.0, max_tokens 600.

Known differences documented in `docs/provider-notes.md`: claude-opus-5
returns a thinking block on every vignette trial tested, recorded per call;
the xAI API adds approximately 185 input tokens of unknown content, so grok-4
does not receive an input identical to the others.

---

## 4. Sampling plan

Five samples per model per presentation. 96 × 5 × 5 = 2,400 responses.

Justified by simulation (`src/simulate_power.py`) against variance measured
directly. Within-cell standard deviations of 0.00 to 0.73 against valence
differences of 2.5 to 5.9 scale points put H1 at ceiling power with three
samples. The binding comparisons are frame and item class, both governed by
item count rather than samples per cell.

**Stopping rule.** Data collection stops when all 2,400 cells are filled. No
optional stopping, no interim analysis, no addition of samples after
inspecting results.

---

## 5. Variables

### Measured

`rating` — integer 1 to 9, where 9 is "very much so" on being true to the
deepest, most essential aspects of the agent's being.

`choice` — a (true self), b (surface self), c (none of the above).

`explanation` — free text, coded per `docs/coding-scheme.md`.

`thinking` — whether the provider returned a reasoning block.

### Derived

`nbk_expected_good` — which version NBK classified as the morally good change,
recorded in the stimulus file. Used in analysis only; never used to construct
a prompt.

---

## 6. Analysis plan

### Primary

Cumulative-link mixed model on rating, moral items:

```
rating ~ version * model_key + frame + (1 | item_id)
```

H1 tested on the `version` term. Alpha 0.05, two-tailed despite the
directional hypotheses, as the more conservative choice.

### H2

Cumulative-link mixed model on all items:

```
rating ~ version * item_class + model_key + frame + (1 | item_id)
```

H2 tested on the `version:item_class` interaction.

### H3

Spearman correlation between mean rating and proportion of "true self"
choices, computed across item-by-version-by-model cells.

### H4

The rating asymmetry is converted to partial eta-squared and compared to Lee
and Feldman's reported values of 0.20 (forced choice) and 0.22 (continuous),
and to NBK's 0.39 and 0.33. Reported as a comparison of magnitudes with
confidence intervals; no significance test of the difference between studies,
since the samples are not commensurable.

### H5 and H6

The `frame` and `model_key` terms in the primary model, reported with effect
sizes. Exploratory; no correction applied and none claimed.

### Robustness

A linear mixed model on the raw ratings is reported alongside the ordinal
model. Item nbk_s1_minorities is reported separately given its heavier prior
observation.

---

## 7. Exclusions

Responses are excluded where `parse_status` is not `ok` or `ok_word` — that
is, where no rating or choice could be extracted from the start of the
response. Categories: `empty`, `refusal`, `no_rating`, `no_choice`,
`out_of_range`.

Exclusion rates are reported per model and per item class. A refusal is a
result and is reported as such rather than silently dropped.

No item is excluded. No model is excluded. No exclusion criterion is applied
after inspecting the confirmatory data.

In the 48-response smoke test, 48 of 48 parsed successfully.

---

## 8. What would count against each hypothesis

**H1.** A rating distribution with no reliable difference between versions on
the moral items, or a difference in the opposite direction. In the pilot, one
model rated a morally good change below the scale midpoint while citing the
agent's departure from his prior pattern; a preponderance of such responses
would produce a null or reversed effect.

**H2.** An asymmetry on the preference items comparable in size to the moral
items, indicating the effect is about change rather than about moral content.

**H3.** No association between the two measures, indicating that one or both
is not measuring what it is taken to measure.

**H4.** A model asymmetry at or below the human effect size.

**H5.** An effect present under the participant frame and absent under the
minimal frame would indicate the result is an artefact of instructing the
model that it is a study participant.

---

## 9. Other

**Analysis code** is written and committed before the confirmatory run
(`src/`). The parser was developed against pilot data and is fixed
(cc6bde3).

**Raw responses** are preserved unmodified. The processed table is derived and
can be regenerated.

**Reliability of coding.** At least 20% of explanations, stratified by model
and item class, are double-coded. Agreement reported as Krippendorff's alpha,
computed before disagreements are resolved.

**Deviations** from this document, should any prove necessary, will be
reported in the write-up with the reason and the date.
