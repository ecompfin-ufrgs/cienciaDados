"""Views do investidor, em retorno anual acima do CDI."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class View(ABC):
    """Opinião sobre o retorno de ativos. Refere-se aos ativos pelo ticker."""

    expected_return: float  # decimal: 0.05 = 5% a.a. acima do CDI

    @abstractmethod
    def pick_row(self, assets: list[str]) -> np.ndarray:
        """Linha da matriz P na ordem de assets."""

    @abstractmethod
    def validate(self, assets: list[str]) -> None:
        """Levanta ValueError se algum ativo da view não estiver em assets."""


@dataclass(frozen=True)
class AbsoluteView(View):
    """Ex.: 'PETR4 renderá 5% a.a. acima do CDI'."""

    asset: str

    def pick_row(self, assets: list[str]) -> np.ndarray:
        """1 na posição do ativo, 0 nas demais."""
        pass

    def validate(self, assets: list[str]) -> None:
        pass


@dataclass(frozen=True)
class RelativeView(View):
    """Ex.: 'VALE3 superará ITUB4 em 2% a.a.'."""

    long_asset: str
    short_asset: str

    def pick_row(self, assets: list[str]) -> np.ndarray:
        """1 no ativo comprado, -1 no vendido, 0 nos demais."""
        pass

    def validate(self, assets: list[str]) -> None:
        """Também exige long_asset diferente de short_asset."""
        pass
