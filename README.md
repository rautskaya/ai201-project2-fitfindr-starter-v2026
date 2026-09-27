# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

### `search_listings`

- **What it does:** Searches the mock listings for items matching a text description, and optionally filters by size and a maximum price.
- **Inputs:** `description` (str) — keywords describing what the user wants. `size` (str or None) — a size to filter by, case-insensitive. `max_price` (float or None) — the highest price allowed, inclusive.
- **Returns:** A list of matching listing dicts, best match first. Each dict has `id`, `title`, `description`, `category`, `style_tags` (list), `size`, `condition`, `price` (float), `colors` (list), `brand` (str or None), `platform`.
- **When it has nothing:** Returns an empty list — never `None`.

### `suggest_outfit`

- **What it does:** Suggests one or two outfits that pair a new thrifted item with pieces from the user's existing wardrobe.
- **Inputs:** `new_item` (dict) — a listing dict for the item being considered. `wardrobe` (dict) — a dict with an `items` key holding a list of wardrobe item dicts; this list may be empty.
- **Returns:** A non-empty string describing the suggested outfit(s), naming specific wardrobe pieces by name when the wardrobe isn't empty.
- **When it has nothing:** If the wardrobe is empty, returns a string with general styling advice for the item instead.

### `create_fit_card`

- **What it does:** Writes a short, social-media-style caption a user could actually post about the thrifted find and its outfit.
- **Inputs:** `outfit` (str) — the outfit suggestion text from `suggest_outfit`. `new_item` (dict) — the listing dict for the item.
- **Returns:** A string, two to four sentences long, that mentions the item, its price, and its platform once each.
- **When it has nothing:** If `outfit` is empty or whitespace-only, returns a descriptive message string explaining there's no outfit to caption.

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` saying what the user could change, and stop — do not call `suggest_outfit`. Otherwise, take the first result as `session["selected_item"]` and continue on to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::_parse_query` — not the model. It pulls a max price from an `"under $N"` pattern and a size from a `"size X"` pattern, then uses whatever text is left as the description. Chosen for the same reason `search_listings` doesn't call the model: parsing "under $30, size M" is mechanical and doesn't need an API call.

**What moves through the session:** `parsed` (from the query) → `search_results` (from `search_listings`) → `selected_item` (first of `search_results`) → `outfit_suggestion` (from `suggest_outfit`, reading `selected_item` and `wardrobe` back out of the session) → `fit_card` (from `create_fit_card`, reading `outfit_suggestion` and `selected_item` back out of the session). If `search_results` is empty, `error` is set instead and everything after it stays `None`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two specific outfits you can create using the Y2K butterfly baby tee and pieces from your existing wardrobe:

**Outfit 1: Casual Y2K Streetwear**
*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Black cropped zip hoodie (worn unzipped or casually draped)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* The fitted, cropped silhouette of the baby tee balances out the volume of the baggy dark-wash jeans, leaning fully into the 2000s aesthetic. Throwing on the black cropped zip hoodie and chunky white sneakers keeps the vibe effortless and tied together.

**Outfit 2: Contrast Casual (Prep meets Y2K)**
*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt + Black crossbody bag
*   **Shoes:** Black combat boots
*   *Why it works:* This pairs the ultra-feminine, pastel butterfly print of the baby tee with the structured, utilitarian look of the wide-leg khaki trousers. Tucking in the baby tee and wearing the brown leather belt adds definition at the waist, while the black combat boots add a bit of edge to ground the outfit.

  Fit card: Still pinching myself over scoring this dreamy butterfly baby tee on Depop for just $18! It's giving ultimate 2000s mall-rat energy, and I'm already planning to style it with baggy low-rise denim and chunky sneakers for that effortless Y2K streetwear vibe. ✨🦋
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two specific outfit ideas using the vintage Levi's 501 jeans and pieces from your existing wardrobe:

### Outfit 1: Casual & Effortless (Daytime / Running Errands)
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Bottoms:** Vintage Levi's 501 Jeans (new item)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The white tank tucked into the medium-wash 501s creates a classic, high-contrast base. Throwing the black denim jacket over the shoulders adds a cool, layered texture that ties in the black crossbody bag, while the chunky white sneakers keep the overall vibe sporty, fresh, and comfortable.

### Outfit 2: Edgy & Relaxed (Cool-Weather / Hangouts)
*   **Top:** Oversized grey crewneck sweatshirt
*   **Bottoms:** Vintage Levi's 501 Jeans (new item)
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:** Tucking the front of the oversized grey crewneck into the 501s balances the slouchy top with the straight-leg fit of the jeans. Pairing them with black combat boots and a black crossbody bag gives off an effortless grunge aesthetic, while the brown leather belt adds a subtle, grounding contrast to the black-and-grey color palette.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Finally found the holy grail of 90s slouch and scored these vintage Levi's 501 jeans on Depop for just $38. They've got that perfectly broken-in medium wash that looks effortless with just a crisp white tee and beat-up sneakers. Absolute 10/10 zero-effort vintage aesthetic.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
