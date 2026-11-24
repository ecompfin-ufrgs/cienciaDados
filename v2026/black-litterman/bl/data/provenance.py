"""Origem de cada dado coletado, informada ao cliente."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class Provenance:
    """De onde e quando um dado foi obtido."""

    source: str               # "yfinance" ou "bcb"
    collected_at: datetime
    period_start: date | None  # None em dados só de hoje (market cap)
    period_end: date | None

    def to_dict(self) -> dict:
        """Formato serializável, usado no snapshot e na API."""
        pass
