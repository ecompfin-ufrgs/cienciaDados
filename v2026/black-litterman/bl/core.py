"""Cálculos estatísticos sobre os dados coletados.

Funções puras: recebem tabelas e devolvem tabelas, sem ler arquivos nem acessar a rede.
Formato largo: índice = datas, colunas = tickers.
"""

from __future__ import annotations

import pandas as pd


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Retorno simples p_t / p_{t-1} − 1 de cada ativo; a primeira data sai."""
    pass


def excess_returns(returns: pd.DataFrame, risk_free: pd.Series) -> pd.DataFrame:
    """Retorno de cada ativo menos o CDI da mesma data.

    risk_free: índice = datas, valores = taxa no mesmo período dos retornos.
    """
    pass


def covariance(returns: pd.DataFrame, periods_per_year: int = 252) -> pd.DataFrame:
    """Matriz de covariância amostral anualizada (Σ), n x n, índice e colunas = tickers.

    periods_per_year: 252 para dados diários, 52 para semanais.
    """
    pass
