"""Assemble the prompts sent to the models.

Every call carries a vignette and one question. Nothing else. No restatement
of what changed, no instruction on how to reason, no example. What the model
treats as the relevant change, and on what basis, is left to the model.

Two design points are encoded here and both depart from Newman, Bloom and
Knobe (2014).

The question stems drop the clause restating the post-change behaviour. That
clause summarises the change and selects which element of the vignette is
being asked about; supplying it would answer part of the research question in
advance.

The two measures are asked in separate calls with no shared context. In the
original they were answered in sequence, so the forced choice conditioned the
rating that followed. Running them independently is what makes their
agreement evidence of convergent validity rather than of consistency.

The design crosses, within each item:

    version   which direction the agent changes in (a | b)
    measure   forced_choice | rating
    frame     minimal | participant
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass, asdict
from pathlib import Path

VERSIONS = ("a", "b")
MEASURES = ("forced_choice", "rating")
FRAMES = ("minimal", "participant")

# The participant frame is the only place any framing enters the study. The
# minimal frame carries no system prompt at all, so the contrast between them
# measures exactly what the framing does.
FRAME_SYSTEM = {
    "minimal": None,
    "participant": (
        "You are a participant in a psychology study. You will read a short "
        "scenario and answer one question about it. There are no right or "
        "wrong answers; give your own judgement."
    ),
}


@dataclass(frozen=True)
class Presentation:
    """One prompt, with everything needed to identify it in the data."""

    item_id: str
    item_class: str          # moral | preference
    domain: str
    name: str
    version: str             # a | b
    measure: str             # forced_choice | rating
    frame: str               # minimal | participant
    system: str | None
    prompt: str


def load_stimuli(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _rating_question(measures: dict) -> str:
    r = measures["rating"]
    return (
        f"{r['stem']}\n\n"
        f"Answer on a {r['scale']}-point scale where 1 is "
        f"\"{r['low_anchor']}\" and {r['scale']} is \"{r['high_anchor']}\".\n\n"
        "Give the number, then explain your answer in one or two sentences."
    )


def _forced_choice_question(measures: dict, name: str) -> str:
    fc = measures["forced_choice"]
    options = "\n".join(f"({chr(97 + i)}) {opt}" for i, opt in enumerate(fc["options"]))
    return (
        f"{fc['stem'].format(name=name)}\n\n"
        f"{options}\n\n"
        "Give the letter of your choice, then explain your answer in one or "
        "two sentences."
    )


def build_presentations(
    stimuli: dict,
    versions=VERSIONS,
    measures=MEASURES,
    frames=FRAMES,
) -> list[Presentation]:
    """Every prompt the study sends, one Presentation each."""
    out: list[Presentation] = []
    framing = stimuli["framing"]
    measure_spec = stimuli["measures"]

    for item_class, key in [("moral", "moral_items"), ("preference", "preference_items")]:
        for item in stimuli[key]:
            for version, measure, frame in itertools.product(versions, measures, frames):
                vignette = item[f"version_{version}"]
                if measure == "rating":
                    question = _rating_question(measure_spec)
                else:
                    question = _forced_choice_question(measure_spec, item["name"])

                prompt = "\n\n".join([
                    framing.format(name=item["name"]),
                    vignette,
                    question,
                ])

                out.append(
                    Presentation(
                        item_id=item["item_id"],
                        item_class=item_class,
                        domain=item["domain"],
                        name=item["name"],
                        version=version,
                        measure=measure,
                        frame=frame,
                        system=FRAME_SYSTEM[frame],
                        prompt=prompt,
                    )
                )
    return out


def presentation_dict(p: Presentation) -> dict:
    return asdict(p)


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "stimuli/nbk_study1.json"
    stimuli = load_stimuli(path)
    presentations = build_presentations(stimuli)

    print(f"{len(presentations)} presentations from {path}")
    print(f"  {len(stimuli['moral_items'])} moral + "
          f"{len(stimuli['preference_items'])} preference items")
    print(f"  x {len(VERSIONS)} versions x {len(MEASURES)} measures "
          f"x {len(FRAMES)} frames")

    for measure in MEASURES:
        example = next(p for p in presentations
                       if p.measure == measure and p.frame == "participant"
                       and p.item_id == "nbk_s1_minorities" and p.version == "a")
        print("\n" + "=" * 70)
        print(f"{measure.upper()}  ({example.item_id}, version {example.version}, "
              f"{example.frame} frame)")
        print("=" * 70)
        if example.system:
            print(f"[system] {example.system}\n")
        print(example.prompt)
