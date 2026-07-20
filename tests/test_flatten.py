import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flatten import flatten_text


# ── Basics ──

def test_empty_string():
    assert flatten_text("") == ""

def test_none_like_whitespace_only():
    assert flatten_text("  \n\t \n ") == ""

def test_single_line_unchanged():
    assert flatten_text("hello world") == "hello world"

def test_newlines_become_spaces():
    assert flatten_text("one\ntwo\nthree") == "one two three"

def test_crlf_and_cr():
    assert flatten_text("a\r\nb\rc") == "a b c"

def test_vertical_tab_and_formfeed():
    assert flatten_text("a\vb\fc") == "a b c"

def test_unicode_line_and_paragraph_separators():
    assert flatten_text("a b c") == "a b c"

def test_runs_of_whitespace_collapse():
    assert flatten_text("a   \t b\n\n\n c") == "a b c"

def test_leading_trailing_stripped():
    assert flatten_text("  hello  \n") == "hello"


# ── Invisible / exotic characters ──

def test_zero_width_and_bom_removed():
    assert flatten_text("he\u200Bllo\uFEFF wor\u200Dld") == "hello world"

def test_bidi_controls_removed():
    assert flatten_text("a\u202Eb\u2066c\u2069d") == "abcd"

def test_soft_hyphen_removed():
    assert flatten_text("ex\u00ADample") == "example"

def test_nbsp_and_fancy_spaces_collapse():
    assert flatten_text("a\u00A0b\u2003c\u3000d") == "a b c d"


# ── join_hyphens ──

def test_hyphen_join_off_by_default():
    assert flatten_text("exam-\nple") == "exam- ple"

def test_hyphen_join_basic():
    assert flatten_text("exam-\nple", join_hyphens=True) == "example"

def test_hyphen_join_crlf():
    assert flatten_text("exam-\r\nple", join_hyphens=True) == "example"

def test_hyphen_join_trailing_spaces():
    assert flatten_text("exam- \n  ple", join_hyphens=True) == "example"

def test_hyphen_join_leaves_dash_lists_alone():
    # a hyphen starting a line (bullet) must not be joined
    assert flatten_text("item one\n- item two", join_hyphens=True) == "item one - item two"

def test_hyphen_join_leaves_spaced_dash_alone():
    assert flatten_text("range 1 -\n5", join_hyphens=True) == "range 1 - 5"


# ── keep_paragraphs ──

def test_paragraphs_flattened_by_default():
    assert flatten_text("para one\nwrapped\n\npara two") == "para one wrapped para two"

def test_paragraphs_kept():
    assert (
        flatten_text("para one\nwrapped\n\npara two\nalso wrapped", keep_paragraphs=True)
        == "para one wrapped\n\npara two also wrapped"
    )

def test_multiple_blank_lines_collapse_to_one_break():
    assert flatten_text("a\n\n\n\nb", keep_paragraphs=True) == "a\n\nb"

def test_blank_line_with_spaces_still_a_break():
    assert flatten_text("a\n  \t\nb", keep_paragraphs=True) == "a\n\nb"

def test_unicode_paragraph_separator_kept():
    assert flatten_text("a b", keep_paragraphs=True) == "a\n\nb"


# ── Combined ──

def test_hyphen_join_with_paragraphs():
    raw = "first para-\ngraph wrapped\n\nsecond para"
    assert (
        flatten_text(raw, join_hyphens=True, keep_paragraphs=True)
        == "first paragraph wrapped\n\nsecond para"
    )
