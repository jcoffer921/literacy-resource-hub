"""Runtime configuration for the assistant module, loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _float_from_env(name: str) -> float | None:
    value = os.getenv(name)
    if value is None or value == "":
        return None
    return float(value)


@dataclass
class Settings:
    # Thresholds are intentionally left unset until tuned against real queries.
    STRONG_MATCH_THRESHOLD: float | None = None
    MIN_MATCH_THRESHOLD: float | None = None


settings = Settings(
    STRONG_MATCH_THRESHOLD=_float_from_env("STRONG_MATCH_THRESHOLD"),
    MIN_MATCH_THRESHOLD=_float_from_env("MIN_MATCH_THRESHOLD"),
)
