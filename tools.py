"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


def _size_tokens(size_str: str) -> list[str]:
    """Split a size string into whole tokens: "S/M" -> ["s", "m"],
    "XL (oversized)" -> ["xl", "oversized"], "US 8.5" -> ["us", "8.5"].

    Splitting instead of treating the string as one blob is what keeps a
    query for "S" from matching "US 9" and "L" from matching "XL" — both are
    true under a plain substring test, and both are wrong.
    """
    return [t for t in re.split(r"[\s/()]+", size_str.lower()) if t]


def _size_matches(query_size: str, listing_size: str) -> bool:
    """A size matches when it equals one whole token of the listing's size,
    case-insensitively. "M" matches "S/M" (a token), not "US 9" or "XL"."""
    return query_size.strip().lower() in _size_tokens(listing_size)


def _keyword_score(listing: dict, query_words: list[str]) -> int:
    """Count how many of the query's words appear as whole words somewhere
    in the listing's searchable text (title, description, category, tags,
    brand, colors)."""
    haystack = " ".join(
        [
            listing.get("title") or "",
            listing.get("description") or "",
            listing.get("category") or "",
            " ".join(listing.get("style_tags") or []),
            listing.get("brand") or "",
            " ".join(listing.get("colors") or []),
        ]
    ).lower()
    haystack_words = set(re.findall(r"[a-z0-9]+", haystack))
    return sum(1 for word in query_words if word in haystack_words)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Matched case-insensitively as a whole token — see "Size
                     matching" below.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    Size matching: a query matches when it equals one whole token of the
    listing's size string, split on whitespace/slashes/parens and compared
    case-insensitively. "M" matches "S/M" (a whole token); "S" does not match
    "US 9" and "L" does not match "XL", because neither is a whole token —
    see `_size_matches` / `_size_tokens`.

    Test it from a terminal:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()

    if max_price is not None:
        listings = [item for item in listings if item["price"] <= max_price]

    if size is not None:
        listings = [item for item in listings if _size_matches(size, item["size"])]

    query_words = re.findall(r"[a-z0-9]+", description.lower())
    scored = [(item, _keyword_score(item, query_words)) for item in listings]
    scored = [(item, score) for item, score in scored if score > 0]
    scored.sort(key=lambda pair: pair[1], reverse=True)

    return [item for item, _ in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, returns general styling advice for the item
        instead of naming specific pieces — see the two prompts below.

    Test it from a terminal:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    item_line = (
        f"{new_item['title']} — {new_item.get('description', '')} "
        f"(category: {new_item['category']}, colors: {', '.join(new_item.get('colors', []))})"
    )

    items = wardrobe.get("items") or []

    if not items:
        # No wardrobe on file yet — give general advice instead of failing.
        prompt = (
            f"Someone is considering buying this thrifted item:\n\n{item_line}\n\n"
            f"They don't have a wardrobe on file yet. In 2-3 sentences, give "
            f"general styling advice: what kinds of pieces would pair well "
            f"with this item?"
        )
        return generate(prompt)

    wardrobe_lines = "\n".join(
        f"- {piece['name']} ({piece['category']}, colors: {', '.join(piece.get('colors', []))})"
        for piece in items
    )
    prompt = (
        f"Someone is considering buying this thrifted item:\n\n{item_line}\n\n"
        f"Here is their existing wardrobe:\n{wardrobe_lines}\n\n"
        f"Suggest one or two specific outfits that pair the new item with "
        f"pieces they already own. Name the wardrobe pieces by name."
    )
    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    Test it from a terminal:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return "No outfit to caption yet — nothing to post about this item."

    prompt = (
        f"Write a short social-media caption (2-4 sentences) someone would "
        f"actually post about this thrifted find, not a product description:\n\n"
        f"Item: {new_item['title']}\n"
        f"Price: ${new_item['price']}\n"
        f"Platform: {new_item['platform']}\n"
        f"Outfit idea: {outfit}\n\n"
        f"Mention the item, its price, and the platform once each. Be "
        f"specific about the vibe."
    )
    return generate(prompt)
