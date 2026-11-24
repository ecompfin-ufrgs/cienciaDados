"""Montagem dos objetos do domínio a partir dos dados coletados."""

from __future__ import annotations

from datetime import date

import pandas as pd

from bl.domain.asset import Asset
from bl.domain.market import Market


def build_asset(ticker: str, prices: pd.DataFrame, issuer: str | None = None) -> Asset:
    """Cria um Asset (STOCK, B3, BRL, adjusted=True) com a coluna do ticker na tabela de preços."""
    pass


def build_market(
    prices: pd.DataFrame,
    market_caps: pd.Series,
    risk_free: pd.Series,
    benchmark: pd.Series,
    reference_date: date,
) -> Market:
    """Cria o Market B3 com um Asset por coluna de prices e o calendário B3 do bizdays."""
    pass
