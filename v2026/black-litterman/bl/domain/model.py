"""Funções do modelo Black-Litterman.

O modelo não é um objeto: é um processo sem estado que usa os objetos do domínio.
Fluxo: prior -> posterior -> optimize.

Tipos:
    sigma     pd.DataFrame n x n, índice e colunas = tickers (anualizada)
    pi, mu    pd.Series com n valores, índice = tickers
    P         np.ndarray k x n  (k views, n ativos)
    Q         np.ndarray k
    omega     np.ndarray k x k, diagonal
"""

from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from bl.domain.market import Market
from bl.domain.parameters import ModelParameters
from bl.domain.portfolio import Portfolio
from bl.domain.views import View


def prior(market: Market, sigma: pd.DataFrame, params: ModelParameters) -> pd.Series:
    """Retornos de equilíbrio Π = δ Σ w_mkt, com w_mkt dos market caps."""
    pass


def posterior(
    pi: pd.Series,
    views: list[View],
    sigma: pd.DataFrame,
    params: ModelParameters,
) -> pd.Series:
    """Retornos combinados μ_BL. Sem views, devolve Π."""
    pass


def optimize(
    mu: pd.Series,
    sigma: pd.DataFrame,
    params: ModelParameters,
    reference_date: date,
    name: str,
) -> Portfolio:
    """Maximiza w'μ − (δ/2) w'Σw com soma 1, w >= 0 e w <= max_weight.

    Levanta ValueError se não houver solução.
    """
    pass


def pick_matrix(views: list[View], assets: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """Monta P e Q; levanta ValueError se houver views duplicadas ou dependentes."""
    pass


def omega(P: np.ndarray, sigma: pd.DataFrame, tau: float) -> np.ndarray:
    """Incerteza das views pelo método de He-Litterman: diag(P τΣ P')."""
    pass
