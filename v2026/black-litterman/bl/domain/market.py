"""Mercado onde os ativos são negociados."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, time
from typing import TYPE_CHECKING

import pandas as pd
from bizdays import Calendar

from bl.domain.asset import Asset

if TYPE_CHECKING:
    from bl.domain.portfolio import Portfolio


@dataclass(frozen=True)
class Market:
    """Mercado de negociação.

    Regras: todo ticker de market_caps existe no universe; market caps > 0.
    """

    code: str                          # "B3"
    location: str                      # "Brasil"
    currency: str                      # "BRL"
    timezone: str                      # "America/Sao_Paulo"
    trading_hours: tuple[time, time]   # (abertura, fechamento)
    calendar: Calendar                 # Calendar.load("B3")
    universe: Mapping[str, Asset]      # ticker -> Asset
    market_caps: pd.Series             # índice: ticker; valores: R$
    risk_free: pd.Series               # índice: datas; valores: taxa ao dia
    benchmark: pd.Series               # índice: datas; valores: Ibovespa

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Levanta ValueError se as regras não forem atendidas."""
        pass

    def find_asset(self, ticker: str) -> Asset:
        """Ativo pelo ticker; levanta ValueError se não existir."""
        pass

    def list_assets(self) -> list[Asset]:
        """Ativos do universo, em ordem de ticker."""
        pass

    def market_portfolio(self, reference_date: date) -> Portfolio:
        """Carteira de mercado: pesos proporcionais ao market cap."""
        pass
