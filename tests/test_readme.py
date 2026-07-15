"""Tests for README.md content and formatting."""

import os
import re

import pytest

README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")


@pytest.fixture(scope="module")
def readme_text():
    with open(README_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def readme_lines(readme_text):
    return readme_text.splitlines()


def test_readme_file_exists():
    assert os.path.isfile(README_PATH)


def test_timer_countdown_code_block_has_no_trailing_blank_line(readme_lines):
    # The timer countdown example must be immediately followed by the
    # closing code fence, with no blank line in between.
    idx = readme_lines.index("00 h 05 m 30.000 s")
    assert readme_lines[idx + 1] == "```"


def test_stopwatch_code_block_has_no_trailing_blank_line(readme_lines):
    # Regression guard: ensure the analogous stopwatch example block was
    # not affected and still has no trailing blank line either.
    idx = readme_lines.index("00 h 00 m 00.000 s")
    assert readme_lines[idx + 1] == "```"


def test_no_code_block_ends_with_a_blank_line(readme_text):
    # General regression check: no fenced code block in the README should
    # contain a blank line immediately before its closing fence.
    fenced_blocks = re.findall(r"```.*?\n(.*?)```", readme_text, re.DOTALL)
    for block in fenced_blocks:
        block_lines = block.splitlines()
        if block_lines:
            assert block_lines[-1].strip() != "", (
                "Found a fenced code block with a trailing blank line"
            )


def test_readme_still_contains_expected_examples(readme_text):
    assert "00 h 05 m 30.000 s" in readme_text
    assert "00 h 00 m 00.000 s" in readme_text