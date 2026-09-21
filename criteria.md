# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**

`search_listings` matches by keyword overlap, not meaning — it scores zero if a query's words don't appear in the listing's title, description, or tags. Listing sizes also come in inconsistent formats ("W30 L30", "S/M", "XL (oversized)"), so a size filter can miss a real match too. Both are realistic ways one phrasing in five fails, so 4 of 5 fits a keyword-only search.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**

Criterion 1 depends on search quality, which is fuzzy and can miss. This one only depends on a plain `if not results: stop` check in the code — no wording, no matching, just a yes/no branch. That should hold every time.

---

## 3. The selected item matches what reaches suggest_outfit

The item's name in `session["selected_item"]` appears in the outfit suggestion text, in at least 4 of 5 tries.

**Why this target:**

Passing the item into `suggest_outfit`should never fail. But checking it this way relies on the model choosing to name the item in its answer — it might describe an item without repeating its exact name. 
---

## 4. The fit card always mentions the price

The fit card includes the item's price, in at at least 4 of 5 tries.

**Why this target:**

`create_fit_card`'s own spec says it should mention the price once.
---

## 5. A new customer with no wardrobe still gets useful advice

For a user with an empty wardrobe, `suggest_outfit` still returns real, usable styling advice for the new item in 5 of 5 tries.

**Why this target:**

Everyone starts as a new customer with nothing in their wardrobe entered yet. The agent should not only work well for users with an established wardrobe.
---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
