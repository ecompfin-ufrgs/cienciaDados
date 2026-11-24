"""Preços históricos, Ibovespa e market cap pelo yfinance."""

from __future__ import annotations

from datetime import date

import pandas as pd

from bl.data.provenance import Provenance


def fetch_prices(tickers: list[str], start: date, end: date) -> tuple[pd.DataFrame, Provenance]:
    """Fechamento ajustado por proventos.

    Recebe tickers sem o sufixo .SA. Devolve formato largo:
    índice = datas, colunas = tickers, valores = preço em BRL.
    """
    pass


def fetch_benchmark(start: date, end: date, symbol: str = "^BVSP") -> tuple[pd.Series, Provenance]:
    """Série do Ibovespa: índice = datas, valores = pontos."""
    pass


def fetch_market_caps(tickers: list[str]) -> tuple[pd.Series, Provenance]:
    """Market cap atual de cada ativo: índice = tickers, valores = R$.

    Só o valor de hoje (Ticker.info["marketCap"]), uma requisição por ativo.
    Não serve para o backtest; o histórico virá depois da CVM.
    """
    pass
