"""CDI pela API SGS do Banco Central (série 12)."""

from __future__ import annotations

from datetime import date

import pandas as pd

from bl.data.provenance import Provenance


def fetch_cdi(start: date, end: date) -> tuple[pd.Series, Provenance]:
    """CDI diário: índice = datas, valores = taxa em decimal ao dia.

    O BCB publica em % ao dia, com vírgula decimal e data dd/mm/aaaa.
    """
    pass
