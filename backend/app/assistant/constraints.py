"""Coverage classification and citation validation for the assistant's answers."""

from __future__ import annotations

import logging
import re
from enum import Enum

from app.assistant.config import settings
from app.assistant.schemas import SourceChunk

logger = logging.getLogger(__name__)

CITATION_RE = re.compile(r"\[(S\d+)\]")


class Coverage(str, Enum):
    STRONG = "strong"
    WEAK = "weak"
    NONE = "none"


NO_MATCH_MESSAGE = (
    "I couldn't find anything on that in the Literacy Hub's resources. I'm "
    "focused on literacy instruction: reading, writing, phonics, comprehension, "
    "and related strategies. Try rephrasing, or ask about a literacy angle on "
    "your question."
)


def classify_coverage(chunks: list[SourceChunk]) -> Coverage:
    if settings.STRONG_MATCH_THRESHOLD is None or settings.MIN_MATCH_THRESHOLD is None:
        raise RuntimeError(
            "STRONG_MATCH_THRESHOLD and MIN_MATCH_THRESHOLD must be configured "
            "before coverage can be classified."
        )
    if not chunks:
        return Coverage.NONE
    top = max(chunk.score for chunk in chunks)
    if top >= settings.STRONG_MATCH_THRESHOLD:
        return Coverage.STRONG
    if top >= settings.MIN_MATCH_THRESHOLD:
        return Coverage.WEAK
    return Coverage.NONE


def extract_citations(answer: str) -> list[str]:
    """Return cited labels in order of first appearance, with duplicates removed."""
    seen: dict[str, None] = {}
    for label in CITATION_RE.findall(answer):
        seen.setdefault(label, None)
    return list(seen)


def validate_citations(answer: str, label_map: dict[str, SourceChunk]) -> tuple[str, set[str]]:
    """Strip any [Sx] labels not present in label_map, tidying leftover double spaces."""
    invalid: set[str] = set()

    def _replace(match: re.Match[str]) -> str:
        label = match.group(1)
        if label in label_map:
            return match.group(0)
        invalid.add(label)
        return ""

    cleaned = CITATION_RE.sub(_replace, answer)
    cleaned = re.sub(r" {2,}", " ", cleaned).strip()

    if invalid:
        logger.warning("Removed invalid citation labels: %s", sorted(invalid))

    return cleaned, invalid
