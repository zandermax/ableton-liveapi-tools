import pytest

from scripts.validate_wiki_parity import compare_texts


def make_md(fm: str, body: str) -> str:
    return f"---\n{fm}\n---\n{body}\n"


def test_identical():
    text = make_md("title: X\ndraft: yes", "Hello")
    ok, diff = compare_texts(text, text)
    assert ok


def test_frontmatter_difference():
    a = make_md("title: X\ndraft: yes", "Hello")
    b = make_md("title: Y\ndraft: yes", "Hello")
    ok, diff = compare_texts(a, b)
    assert not ok


def test_body_difference():
    a = make_md("title: X", "Hello")
    b = make_md("title: X", "Goodbye")
    ok, diff = compare_texts(a, b)
    assert not ok


def test_boolean_normalization_equivalent():
    a = make_md("title: X\ndraft: yes", "Hello")
    b = make_md("title: X\ndraft: true", "Hello")
    ok, diff = compare_texts(a, b)
    assert ok
