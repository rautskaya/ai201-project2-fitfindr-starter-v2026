"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # State check: does the item that reached suggest_outfit match
        # session["selected_item"]? Any matching query works — what's being
        # checked is the session, not the wording of the query.
        "name": "selected item reaches suggest_outfit",
        "query": "corduroy pants under $40",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Does the fit card mention the item's price? A different item from
        # scenario 1 so this isn't just re-testing the same search/prompt.
        "name": "fit card mentions price",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # A user with nothing saved. Criterion 5.
        "name": "empty wardrobe gets useful advice",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
