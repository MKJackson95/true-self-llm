# Normative Self-Attribution in LLMs

An experimental test of whether large language models reproduce the normative
structure of the human concept of the "true self" described by Knobe and his
collaborators.

**Nothing has been run yet.** This README describes what the study will do. It
was written before the confirmatory data exists, and the commit history shows
when. Results will be added when they exist, whatever they turn out to be.

## The question

When an agent's psychological states or behaviours conflict, which does a
model treat as revealing who the agent really is? The Knobe–Newman account
predicts that people attribute to the true self whichever state they regard as
morally good, rather than using any of the criteria philosophers have
proposed. Do models do the same, and if not, on what basis do they decide?

Three goals follow. Establish whether the effect exists in models at all.
Determine which criterion they actually use. Measure how far models converge
with the human pattern and with each other.

## Two arms

### Replication

The stimuli, scales and measures of Newman, Bloom and Knobe (2014), run
verbatim: all twelve Study 1 vignette pairs including the four non-moral
preference items, all eight Study 2 items, both Study 3 vignettes. Their
9-point rating and their forced-choice measures unaltered — including the
framing sentence telling the reader the agent differs from them in almost
every way, an instruction written to suppress projection in a human reader and
given here to systems with no self to project.

Running the published items on the published scales makes the comparison
against published means direct rather than approximate.

Study 3's items carry the belief/feeling crossing: an agent whose reflective
belief pulls one way and whose feeling pulls the other. NBK found feelings
rated as more revealing of the true self than beliefs, but only marginally,
and across two vignettes on a single topic. Their whole result on this
question rests on one content domain.

### Extension

The extension does two things the original design cannot.

**It separates moral valence from departure-from-norm.** In every one of NBK's
moral pairs, the direction the agent moves in and the direction that departs
from the surrounding norm coincide. Omar's culture oppresses minorities and he
comes to respect them; Frank's workplace tolerates dishonesty and he becomes
ethical. Change and departure always travel together, so no result from those
items can tell the two apart. The extension crosses them: each item describes
an agent whose behaviour either departs from or conforms to the norm described
in their surroundings, crossed with the direction of the change. Norm-relation
is a structural property of the text — whether the agent's behaviour matches
what is described as usual around them — and requires no evaluation to state.

**It crosses belief against feeling across many domains** rather than one,
which is what Objective 6 needs and what the original could not supply.

Moral valence is not stipulated. A separate probe, carrying no true-self
framing, asks each model how it evaluates each behaviour. The analysis then
asks whether attribution tracks the model's own evaluation, the norm-relation,
the state type, or something else.

This matters because of a response recorded during setup. Asked about the Omar
item, Claude Opus 5 rated it 8 of 9 and explained that Omar had to overcome
both personal habit and social pressure, so the belief was genuinely his own
rather than absorbed from his surroundings, and that his earlier conduct
looked like residue of an oppressive environment rather than an expression of
who he essentially is. The reasoning is about independence from one's
surroundings, not about moral goodness. NBK's items cannot separate those. The
extension can.

## Prompting

Whether any convergence is a product of framing rather than of the concept is
a factor, not an assumption. Every item runs under two system-prompt frames: a
minimal instruction to answer the question, and a participant framing of the
kind used in psychological studies. An effect that appears under one and not
the other is an artefact of the instruction.

## What the models say

Ratings measure how strongly the true self is attributed. Explanations measure
on what grounds — and the grounds are what Goal 2 asks about. Some accounts
predict identical ratings for opposite reasons and are separable only in the
text.

Every response is collected with its explanation and coded against a scheme
fixed before the confirmatory run. The codes come from the source papers:
reflective endorsement (Aristotle, Frankfurt); emotion and desire (the
novelists' view NBK set against it); moral valence (their own account);
meta-desires, which NDK test separately and find come apart from true-self
attribution; psychological essentialism; person-positivity bias; and
attribution of general attitudes as distinct from a deeper self. An eighth
code covers anti-conditioning — the idea that the true self is what is not
merely socially inherited. That one is present in NBK's materials, where the
surface self is defined as what a person learned from society or others, but
never treated by them as a rival criterion, because their items cannot
separate it from moral valence.

## Design decisions

Counterbalancing of anchor direction and clause order applies to the extension
arm only. Applying it to the replication items would stop them being verbatim
and weaken the comparison against published data. The replication therefore
inherits the original's limitations, including the single scale direction, and
the extension is what tests whether those limitations were carrying the
result.

Repeated samples from one model are not independent participants. Analysis
uses cumulative-link mixed models with random intercepts for item and model as
a fixed effect, and reports effect sizes rather than raw means except where
the verbatim items make means comparable.

Sample size will be set by simulation before the confirmatory run.

## Models

| Family | Models |
|---|---|
| Anthropic | claude-haiku-4-5, claude-sonnet-5, claude-opus-5 |
| OpenAI | gpt-5.6-sol |
| xAI | grok-4 |

The Anthropic family is run across all three tiers, the other two at flagship
tier only. This makes the design asymmetric, and deliberately so: the pilot
found the three Claude models diverging sharply from one another on the
true-self items, with one showing a large asymmetry and another none at all.
Whether that within-family divergence survives a better-controlled design is a
question the pilot raised and this study can answer. The comparison across
families is between flagships, and any claim about a family as a whole rests
on a single model for OpenAI and xAI.

Note that `gpt-5.6` is an alias that resolves to Sol and may be repointed; the
pinned identifier is used here.

Claude Opus 5 returns a thinking block before its answer. On twelve trials of
a vignette it did so every time, so this is not occasional. Responses are
therefore assembled by filtering content blocks by type rather than taking the
first block, and whether thinking occurred is recorded for every call. Whether
a response preceded by extended reasoning is the same task as an immediate
judgement is an open question, so it is recorded rather than suppressed.

## Scope

The true self is the starting point rather than the whole subject. The same
method — present the case, record the attribution and the reasoning, separate
the criteria that the original design confounds — extends to the other
concepts where moral asymmetries have been found: intentional action,
responsibility, blame, valuing, happiness, weakness of will, freedom and
causation. Whether models reproduce the normative structure of folk
psychological concepts generally is the larger question this study opens.

## Prior work

An exploratory pilot across three Claude models motivated this design:
[knobe-pilot](https://github.com/MKJackson95/knobe-pilot). It was not
preregistered and its response format produced near-zero variance in most
cells. Both problems are addressed here.

## References

Knobe, J. (2005). Ordinary ethical reasoning and the ideal of 'being
yourself'. *Philosophical Psychology*, 18(3), 327–340.

Newman, G. E., Bloom, P., & Knobe, J. (2014). Value judgments and the true
self. *Personality and Social Psychology Bulletin*, 40(2), 203–216.

Newman, G. E., De Freitas, J., & Knobe, J. Beliefs about the true self explain
asymmetries based on moral judgment. *Cognitive Science*.

## Licence

Code under MIT. Stimuli and data under CC BY 4.0.
