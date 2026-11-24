"""Gravação e leitura local dos dados coletados, para não baixar de novo."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from bl.data.provenance import Provenance


def save(data: pd.DataFrame | pd.Series, name: str, provenance: Provenance) -> Path:
    """Grava em dados/<name>.parquet, com a origem ao lado em <name>.json."""
    pass


def load(name: str) -> tuple[pd.DataFrame | pd.Series, Provenance]:
    """Lê o dado e a origem gravados."""
    pass


def exists(name: str) -> bool:
    """Se o dado já foi gravado."""
    pass
