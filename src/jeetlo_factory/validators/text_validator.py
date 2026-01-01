"""
Text Validator
==============

Validates on-screen text in Manim reel code:
1. Headers should be in English
2. Key terms should be in English
3. Only certain phrases can be in Hindi (for emphasis)

This catches the mistake of putting Hindi text on screen when it should be English.
"""

import re
from typing import List, Tuple
from pathlib import Path


# Devanagari Unicode range
DEVANAGARI_PATTERN = re.compile(r'[\u0900-\u097F]+')

# Allowed Hindi phrases on screen (emotional/emphasis only)
ALLOWED_HINDI_PHRASES = [
    "याद रखिए",
    "याद रखो",
    "गलत",
    "सही",
    "क्यों",
    "कैसे",
    "देखिए",
    "देखो",
]


class TextValidator:
    """Validates on-screen text in reel code."""

    def __init__(self, code_content: str):
        self.content = code_content
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate all Text() calls in the code.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self._check_text_calls()
        return len(self.errors) == 0, self.errors, self.warnings

    def _check_text_calls(self):
        """Check all Text() calls for Hindi content."""
        # Find all Text() calls
        text_pattern = re.compile(
            r'Text\s*\(\s*["\'](.+?)["\']\s*[,)]',
            re.MULTILINE
        )

        matches = text_pattern.findall(self.content)

        for text in matches:
            hindi_matches = DEVANAGARI_PATTERN.findall(text)

            if hindi_matches:
                # Check if it's an allowed phrase
                is_allowed = any(
                    phrase in text for phrase in ALLOWED_HINDI_PHRASES
                )

                if not is_allowed:
                    self.errors.append(
                        f"TEXT LANGUAGE ERROR: On-screen text contains Hindi: '{text}'. "
                        f"Use English text on screen. Audio can be Hindi, but visuals should be English. "
                        f"Allowed Hindi: {', '.join(ALLOWED_HINDI_PHRASES[:5])}..."
                    )

    def _is_header_text(self, text: str) -> bool:
        """Check if text appears to be a header (all caps or specific patterns)."""
        return text.isupper() or text.endswith("!") or "TIP" in text


def validate_reel_code(reel_py_path: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a reel.py file for text language issues.

    This is called by CI to validate all reel code.
    """
    with open(reel_py_path, "r") as f:
        content = f.read()

    validator = TextValidator(content)
    return validator.validate()
