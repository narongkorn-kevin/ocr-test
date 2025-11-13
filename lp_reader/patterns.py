from __future__ import annotations
import re


THAI_LETTERS = r"[ก-ฮ]"
ENG_LETTERS = r"[A-Z]"
DIGITS = r"[0-9]"

PATTERNS = [
    re.compile(rf"^{THAI_LETTERS}{{1,2}}\s?-?{DIGITS}{{1,4}}$"),
    re.compile(rf"^{ENG_LETTERS}{{1,3}}\s?-?{DIGITS}{{1,4}}$"),
    re.compile(rf"^{THAI_LETTERS}{{1,2}}{DIGITS}{{1,4}}$"),
    re.compile(rf"^{ENG_LETTERS}{{1,3}}{DIGITS}{{1,4}}$"),
    # Thai green commercial plates often start with a leading digit, then 2 Thai letters, then 3-4 digits
    re.compile(rf"^{DIGITS}{THAI_LETTERS}{{1,2}}\s?-?{DIGITS}{{1,4}}$"),
    re.compile(rf"^{DIGITS}{THAI_LETTERS}{{1,2}}{DIGITS}{{1,4}}$"),
]


CONFUSABLE_MAP = {
    "O": "0",
    "I": "1",
    "l": "1",
    "B": "8",
    "S": "5",
    "Z": "2",
}

# Common Thai look-alikes on license plates (heuristic).
# We only apply these when it helps satisfy a known plate pattern.
THAI_CONFUSABLE_MAP = {
    "ผ": "ฒ",
    "ฌ": "ฒ",
    "ศ": "ส",
    "ษ": "ส",
    "ฬ": "ล",
}


def normalize_plate_text(text: str) -> str:
    t = text.strip()
    t = t.replace(" ", "")
    t = t.replace("—", "-").replace("_", "-")
    t = t.upper()
    t = "".join(CONFUSABLE_MAP.get(c, c) for c in t)
    return t


def _apply_thai_confusables(t: str) -> str:
    return "".join(THAI_CONFUSABLE_MAP.get(c, c) for c in t)


def normalize_to_plausible(text: str) -> str:
    """Normalize and, if needed, apply Thai confusable fixes to reach a plausible pattern."""
    base = normalize_plate_text(text)
    if any(p.match(base) for p in PATTERNS):
        return base
    fixed = _apply_thai_confusables(base)
    if any(p.match(fixed) for p in PATTERNS):
        return fixed
    return base


def is_plausible_plate(text: str) -> bool:
    t = normalize_to_plausible(text)
    return any(p.match(t) for p in PATTERNS)


def score_plate(text: str, confidence: float) -> float:
    t = normalize_to_plausible(text)
    length_bonus = min(len(t), 8) / 8.0
    return confidence * 0.8 + length_bonus * 0.2
