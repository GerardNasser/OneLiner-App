"""Pure text-flattening logic for One-Liner. No UI dependencies."""

import re

# Null byte, zero-width chars, BOM, bidi controls, soft hyphen
_INVISIBLE_RE = re.compile(
    "[\x00\u200B\u200C\u200D\uFEFF\u200E\u200F"
    "\u202A\u202B\u202C\u202D\u202E\u2066\u2067\u2068\u2069\u00AD]"
)

# Space, tab, NBSP, and the exotic Unicode space block
_SPACE_RUN_RE = re.compile("[ \t\u00A0\u2000-\u200A\u202F\u205F\u3000]+")

# word-\n<word> -- the PDF line-wrap hyphenation artifact. A hyphen that
# starts a line (bullet) or follows a space is left alone.
_HYPHEN_WRAP_RE = re.compile(r"(?<=\w)-[ \t]*\n[ \t]*(?=\w)")

# A blank line (possibly containing spaces/tabs) marks a paragraph break
_PARAGRAPH_BREAK_RE = re.compile("\n(?:[ \t\u00A0]*\n)+")


def _collapse(text: str) -> str:
    text = text.replace("\n", " ")
    return _SPACE_RUN_RE.sub(" ", text).strip()


def flatten_text(raw: str, *, join_hyphens: bool = False, keep_paragraphs: bool = False) -> str:
    """Collapse text to a single clean line.

    join_hyphens    -- rejoin words split across lines with a trailing hyphen
                       ("exam-\\nple" -> "example")
    keep_paragraphs -- preserve blank-line paragraph breaks as "\\n\\n",
                       flattening each paragraph to one line
    """
    if not raw:
        return ""

    raw = _INVISIBLE_RE.sub("", raw)

    # Normalise every line/paragraph break variant to \n (U+2029 is an
    # explicit paragraph separator, so it becomes a blank line)
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = raw.replace("\v", "\n").replace("\f", "\n")
    raw = raw.replace("\u2028", "\n").replace("\u2029", "\n\n")

    if join_hyphens:
        raw = _HYPHEN_WRAP_RE.sub("", raw)

    if keep_paragraphs:
        paragraphs = (_collapse(p) for p in _PARAGRAPH_BREAK_RE.split(raw))
        return "\n\n".join(p for p in paragraphs if p)

    return _collapse(raw)
