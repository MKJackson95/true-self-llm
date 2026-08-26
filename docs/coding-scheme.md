# Coding scheme: criteria invoked in model explanations

Fixed before any confirmatory data is collected. Anchor examples are taken
from the 48-response smoke test (`data/raw/smoke.jsonl`), truncated where
long, and are reproduced verbatim.

## What this measures

The rating measures how strongly the true self is attributed. It cannot
measure on what grounds. Several of the accounts below predict identical
ratings for opposite reasons — essentialism and self-creation both give a high
rating to Omar's change, one because the good was always latent, the other
because he made himself that way. Only the explanation distinguishes them.

## Coding rules

**Multi-label.** A response may invoke more than one criterion and frequently
does. Code every criterion present. Do not force a single choice.

**Code what is said, not what is implied.** A response that rates a moral
improvement highly is not thereby coded MORAL-VALENCE. It is coded
MORAL-VALENCE only if the explanation appeals to the goodness of the
behaviour. Attributing a criterion on the basis of the rating alone would make
the coding circular.

**Code the reasoning offered, not its correctness.** A criterion applied
inconsistently across items is still that criterion, and the inconsistency is
recorded separately.

**Unclear cases go to UNCLEAR.** Do not resolve ambiguity by preference. The
rate of UNCLEAR is a result.

## Codes from the source literature

### MORAL-VALENCE
*The true self holds whatever is morally good.* Newman, Bloom and Knobe's own
account. Coded when the explanation appeals to the moral quality of the
behaviour as the reason for the attribution.

> People intuitively regard the "true self" as morally good, so Bill's
> cessation of harmful behavior… — grok, employees, version a

> The change from neglectful to caring father is widely viewed as moral
> improvement that reveals an… — grok, father, version a

### REFLECTIVE
*The true self is what survives reflection.* Aristotle, Frankfurt. Coded for
appeals to deliberation, considered judgement, moral reasoning, or the agent's
endorsed beliefs as against their impulses.

> Amir is being true to his deepest self because he's following his capacity
> for moral reasoning and… — haiku, terrorism, version a

### EMOTIONAL
*The true self is what shows when deliberation is set aside.* The view NBK
attribute to novelists and poets. Coded for appeals to urges, cravings,
impulses or feelings as more revealing than considered belief.

No instance in the smoke test. Its absence is itself worth reporting.

### META-DESIRE
*The true self is constituted by what the agent wants to want.* Frankfurt's
second-order desires, which NDK test separately and find come apart from
true-self attribution. Coded for appeals to whether the agent endorses or
wishes to be rid of their own motivation.

No instance in the smoke test.

### ESSENTIALISM
*There is a fixed underlying nature, and behaviour either expresses it or does
not.* Coded for appeals to an essence, core, or deep nature treated as
independent of and prior to conduct.

> Luke's behavioral change suggests his essential nature was never simply
> "jerk boyfriend"… — haiku, boyfriend, version a

> His earlier conduct looks more like the residue of an oppressive environment
> than an expression of who he essentially is. — opus, minorities, version a
> (recorded during setup)

### PERSON-POSITIVITY
*People are viewed favourably by default, independent of any claim about
essences.* NDK offer this as the rival explanation to essentialism. Coded for
appeals to a general disposition to think well of people.

No instance in the smoke test.

### ATTITUDE-NOT-SELF
*General attitudes and the deep self are different things.* NDK argue an agent
can be credited with bad attitudes while a good deeper self is still posited.
Coded where a response explicitly separates the two levels.

### ANTI-CONDITIONING
*The true self is what is not merely socially inherited.* Present in NBK's
materials — the surface self is defined as what a person learned from society
or others — but never treated by them as a rival criterion, because their
items cannot separate it from moral valence. Coded for appeals to resisting
social pressure, acting against one's environment, or holding a view
independently of one's surroundings.

> Tom is now consistently choosing ethical conduct despite ongoing pressure
> from his corrupt station… — grok, police, version a

> Amir's shift away from supporting terrorism, despite cultural pressure to
> endorse it, suggests he… — grok, terrorism, version a

## Codes that emerged from the pilot data

These are not among the accounts the source papers name. Both appear
repeatedly in the smoke test and are recorded as emergent rather than
theory-derived.

### CONSISTENCY
*The true self is what matches the agent's established behavioural record.*
The most frequent criterion in the smoke test. Coded for appeals to the
agent's prior pattern, track record, or history as evidence about their real
character.

> Bill's changed behavior suggests he's acting against his former inclinations
> rather than expressing… — haiku, employees, version a

> Since Luke's past behavior consistently showed respect and affection, his
> current shift to mistreating… — grok, boyfriend, version b

> Al's earlier pattern of engaged, affectionate parenting indicates that his
> core identity centers o[n]… — grok, father, version b

**Why it matters.** CONSISTENCY and MORAL-VALENCE make the same prediction on
every one of NBK's items, because in each pair the agent's past in the bad
direction is both good and consistent. The two cannot be separated by their
design. Where CONSISTENCY appears on a good-direction item — as it does above
for Bill — it predicts a *low* rating for a morally good change, which is the
opposite of the Knobe–Newman prediction.

Distinguish from ESSENTIALISM: essentialism posits a nature underlying
behaviour, consistency infers character from the behavioural record itself. A
response may invoke both.

Distinguish from ANTI-CONDITIONING: anti-conditioning is about independence
from one's surroundings, consistency is about continuity with one's own past.
These can conflict — an agent departing from a norm they had internalised is
anti-conditioning-high and consistency-low.

### TRIVIALITY
*The domain is too superficial to bear on the true self at all.* Coded where
the response declines to attribute on the grounds that the behaviour is not
the kind of thing that reveals character. NBK predicted this for the
preference items and it appears there.

> Switching from PCs to Macs is a superficial consumer preference with no
> plausible connection to an[y]… — grok, computers, version a

> Pet preferences are superficial tastes, not core traits like values or
> personality… — grok, pets, version a

## Codes for responses that fit no account

### AUTHENTICITY-BARE
The response asserts that the behaviour is or is not genuinely the agent's
own, without giving a criterion for that judgement.

> Alex is being true to his deepest self by following his genuine preferences
> as they've evolved… — haiku, pets, version a

### GROWTH
*The self is made through change rather than revealed by it.* Coded for
appeals to development, evolution or becoming, where change is treated as
constitutive rather than as evidence of something prior.

> Sam's changed environmental preferences reflect a capacity for genuine
> adaptation and growth rathe[r]… — grok, living, version a

### UNCLEAR
No criterion identifiable, or the response is too brief to code.

## Reliability

A random sample of at least 20% of responses, stratified by model and item
class, is double-coded. Agreement is reported as Krippendorff's alpha, which
handles multi-label data and missing codes. Disagreements are resolved by
discussion and the resolution recorded; the reported alpha is the figure
before resolution.

## Analysis

Code frequencies are reported by model, item class, version and frame. The
primary questions:

Which criteria does each model invoke, and do models differ?

Does the criterion invoked predict the rating given, within model and item?

Do CONSISTENCY and MORAL-VALENCE dissociate on any item — and if the extension
arm is run, does separating norm-relation from direction of change dissociate
them systematically?

Is any criterion applied inconsistently, in the sense of supporting opposite
ratings on structurally similar items? One instance is already recorded: grok
rated the sport item 2 in one direction and 8 in the other while giving
materially the same reason, that changing a preferred sport is superficial and
unrelated to core values.
