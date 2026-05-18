import pytest

from scripts.migrate_wiki_frontmatter import migrate_text, parse_frontmatter


def test_author_to_authors():
    text = "---\nauthor: Alice\n---\nBody\n"
    new_text, changed = migrate_text(text)
    assert changed
    data, _ = parse_frontmatter(new_text)
    assert data.get("authors") == ["Alice"]


def test_tags_split():
    text = "---\ntags: foo, bar\n---\n"
    new_text, changed = migrate_text(text)
    assert changed
    data, _ = parse_frontmatter(new_text)
    assert data.get("tags") == ["foo", "bar"]


def test_idempotent():
    text = "---\nauthor: Alice\ntags: foo, bar\n---\nBody\n"
    first_text, ch1 = migrate_text(text)
    second_text, ch2 = migrate_text(first_text)
    assert ch1
    assert not ch2
    assert first_text == second_text


def test_date_normalization():
    text = "---\ncreated: 2026/05/18\n---\n"
    new_text, changed = migrate_text(text)
    assert changed
    data, _ = parse_frontmatter(new_text)
    assert data.get("date") == "2026-05-18"


def test_boolean_normalization():
    text = "---\ndraft: yes\n---\n"
    new_text, changed = migrate_text(text)
    assert changed
    data, _ = parse_frontmatter(new_text)
    assert data.get("draft") is True
