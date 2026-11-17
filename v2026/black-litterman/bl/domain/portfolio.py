"""Carteira e estratégias de construção."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from uuid import uuid4

import pandas as pd

from bl.domain.parameters import ModelParameters


class Strategy(Enum):
    """Estratégias de construção de carteira."""

    MARKET = "market"
    BLACK_LITTERMAN = "black-litterman"
    EQUAL_WEIGHT = "equal-weight"


@dataclass(frozen=True, eq=False)
class Portfolio:
    """Ativos com seus pesos em uma data.

    É uma entidade: igualdade e hash usam só o id.
    Regras: pesos somam 1 (tolerância 1e-6), não negativos, sem tickers repetidos.
    """

    weights: pd.Series                        # índice: ticker; valores: peso
    reference_date: date
    name: str                                 # "BL top 10 - mai/2026"
    strategy: Strategy | None = None          # None = informada à mão
    parameters: ModelParameters | None = None
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self) -> None:
        self.validate()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Portfolio) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def validate(self) -> None:
        """Levanta ValueError se as regras não forem atendidas."""
        pass

    def expected_return(self, mu: pd.Series) -> float:
        """Retorno esperado w'μ; mu indexado por ticker."""
        pass

    def volatility(self, sigma: pd.DataFrame) -> float:
        """Volatilidade √(w'Σw); sigma indexado por ticker."""
        pass

    def compare(self, other: Portfolio) -> pd.DataFrame:
        """Pesos das duas carteiras lado a lado e a diferença."""
        pass
