"""Ativo e seus objetos auxiliares."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum

import pandas as pd


class AssetClass(Enum):
    """Tipos de ativo. Na primeira versão, só STOCK é usada."""

    STOCK = "stock"
    ETF = "etf"
    BOND = "bond"
    CURRENCY = "currency"
    CRYPTO = "crypto"


@dataclass(frozen=True)
class PriceSeries:
    """Histórico de preços de um ativo.

    Regras: datas ordenadas e sem repetição; preços maiores que zero.
    """

    series: pd.Series  # índice: DatetimeIndex; valores: preço
    currency: str      # "BRL"
    adjusted: bool     # ajustado por proventos?

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Levanta ValueError se as regras não forem atendidas."""
        pass

    def price_at(self, d: date) -> float:
        """Preço na data."""
        pass

    def slice(self, start: date, end: date) -> PriceSeries:
        """Nova série com o período [start, end]; a original não muda."""
        pass


@dataclass(frozen=True)
class Asset:
    """Ativo negociado em um mercado. A identidade é o ticker.

    Igualdade e hash usam só o ticker, o que permite usar o Asset como chave.
    """

    ticker: str                                                # "PETR4"
    asset_class: AssetClass = field(compare=False)
    market: str = field(compare=False)                         # "B3"
    prices: PriceSeries = field(compare=False, repr=False)
    issuer: str | None = field(default=None, compare=False)    # "Petrobras"

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Ticker no formato da B3 (4 letras + 1 ou 2 dígitos)."""
        pass

    def price_at(self, d: date) -> float:
        """Preço na data."""
        pass

    def compute_returns(self, kind: str = "simple") -> pd.Series:
        """Retornos 'simple' ou 'log'; exige preços ajustados."""
        pass
