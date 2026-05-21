"""Helper functions for report generation.

These utilities handle transcript file reading, metadata extraction,
normalization, and simple checklist scoring.
"""

from datetime import datetime
from pathlib import Path

import re
from typing import Iterable

from technical_task_garage_race.report.constants import DATE_PREFIX_RE, PHONE_RE


def read_text(path: Path) -> str:
    """Read a transcript file as UTF-8 text.

    Args:
        path: Path to the transcript file.

    Returns:
        str: File contents with decode errors ignored.
    """
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_phone(path: Path, text: str) -> str:
    """Extract a phone number from the file name or transcript body.

    Args:
        path: Path to the transcript file.
        text: Transcript body.

    Returns:
        str: Phone number if one is found, otherwise an empty string.
    """
    parts = path.stem.split("_")
    if len(parts) >= 3 and PHONE_RE.fullmatch(parts[2]):
        return parts[2]

    match = PHONE_RE.search(path.stem)
    if match:
        return match.group(0)

    match = PHONE_RE.search(text)
    if match:
        return match.group(0)

    return ""


def extract_date(path: Path) -> str:
    """Extract the call date from the file name.

    Args:
        path: Path to the transcript file.

    Returns:
        str: ISO date string if the file name starts with a date,
        otherwise an empty string.
    """
    parts = path.stem.split("_")
    if parts and DATE_PREFIX_RE.fullmatch(parts[0]):
        return parts[0]

    match = DATE_PREFIX_RE.match(path.stem)
    if not match:
        return ""

    try:
        return datetime.strptime(match.group(1), "%Y-%m-%d").date().isoformat()
    except ValueError:
        return match.group(1)


def normalize_text(text: str) -> str:
    """Normalize text for keyword-based matching.

    Args:
        text: Raw transcript text.

    Returns:
        str: Lowercased text with whitespace collapsed.
    """
    return re.sub(r"\s+", " ", text.lower()).strip()


def score_yes_no(
    text: str, positive_keywords: Iterable[str], negative_keywords: Iterable[str] = ()
) -> int:
    """Score a transcript segment using simple keyword checks.

    Args:
        text: Text to analyze.
        positive_keywords: Keywords that indicate a successful check.
        negative_keywords: Keywords that override the positive score.

    Returns:
        int: ``1`` when the positive condition is met, otherwise ``0``.
    """
    normalized = normalize_text(text)
    if any(keyword in normalized for keyword in negative_keywords):
        return 0
    return 1 if any(keyword in normalized for keyword in positive_keywords) else 0
