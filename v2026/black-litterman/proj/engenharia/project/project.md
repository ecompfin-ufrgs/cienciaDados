# Projeto de software

Este documento descreve a arquitetura do projeto Black-Litterman. Ele parte dos [requisitos](../eng_requisitos/documentacao.md) e das [decisões da análise](../eng_requisitos/analise.md). Os identificadores `A-xx` e `FR-xx` apontam para esses documentos.

## 1. Visão geral

A arquitetura separa o que coleta dados do que atende o usuário:

- **Máquina local:** coleta dados, calcula os insumos do modelo e gera um snapshot.
- **Servidor:** o backend no PythonAnywhere lê o snapshot e calcula as carteiras. Ele não consulta fontes externas durante uma requisição.
- **Frontend:** consome a API do backend e pode ser trocado sem alterar o restante.

```text
        MÁQUINA LOCAL                              SERVIDOR E FRONTEND

  yfinance        BCB                                   Frontend
     |             |                                       | HTTP / JSON
     v             v                                       v
 +-------------------+                              +-------------+
 | bl/data           |  coleta e origem             | bl/api      |  planejado
 +-------------------+                              +-------------+
          |                                                |
          v                                                v
 +-------------------+                              +-------------+
 | bl/core           |  retornos e Σ                | bl/services |  planejado
 +-------------------+                              +-------------+
          |                                                |
          v                                                v
   snapshot.json ---------------- envio --------->  +-------------+
                                                    | bl/domain   |
                                                    +-------------+
```

O `bl/domain` é usado tanto pelo servidor quanto pelas rotinas locais.

## 2. Estrutura do repositório

A fase atual tem o esqueleto de `domain`, `data` e `core`, com assinaturas e docstrings. As demais pastas estão planejadas.

```text
v2026/black-litterman/
├── bl/
│   ├── __main__.py         comandos locais
│   ├── core.py             simple_returns, excess_returns, covariance
│   ├── domain/             objetos reais e funções do Black-Litterman
│   │   ├── asset.py        AssetClass, PriceSeries, Asset
│   │   ├── market.py       Market
│   │   ├── parameters.py   ModelParameters
│   │   ├── portfolio.py    Strategy, Portfolio
│   │   ├── views.py        View, AbsoluteView, RelativeView
│   │   └── model.py        prior, posterior, optimize, pick_matrix, omega
│   ├── data/               coleta de dados
│   │   ├── yahoo.py        fetch_prices, fetch_benchmark, fetch_market_caps
│   │   ├── bcb.py          fetch_cdi
│   │   ├── storage.py      save, load, exists
│   │   ├── provenance.py   Provenance
│   │   └── builders.py     build_asset, build_market
│   ├── study/              planejado: seleção, market cap histórico e snapshot
│   ├── backtest/           planejado: walk-forward e métricas
│   ├── services/           planejado: casos de uso do servidor
│   └── api/                planejado: rotas HTTP
├── frontend/               planejado
├── dados/                  dados locais, fora do Git
├── tests/                  testes automatizados (test_*.py)
└── proj/                   documentos de engenharia e gestão
```

A pasta `dados/` entra no `.gitignore` (A-16).

## 3. Camadas e dependências

| Camada | Onde roda | Responsabilidade | Pode importar |
|---|---|---|---|
| `domain` | Local e servidor | Objetos reais e funções do Black-Litterman | `bizdays`, `pandas`, `numpy`, `scipy` |
| `core` | Local | Cálculos estatísticos, sem rede ou arquivos | `pandas`, `numpy` |
| `data` | Local | Coleta, gravação local e montagem dos objetos | `domain` |
| `study`, `backtest` | Local | Planejado | `domain`, `core`, `data` |
| `services`, `api` | Servidor | Planejado | `domain` |
| `frontend` | A definir | Interface | Somente a API, por HTTP |

Regras principais:

1. `domain` e `core` não fazem I/O e não importam `data`.
2. `data` importa `domain` para montar os objetos; o contrário não acontece.
3. `services` e `api` não importam `data`. O servidor só lê o snapshot.
4. O frontend não importa `bl` (A-11).

Erros de valor inválido usam `ValueError`, do próprio Python. Os códigos de erro da API serão definidos com ela.

### 3.1 Paradigmas

| Camada | Paradigma | Motivo |
|---|---|---|
| `domain` (objetos) | Orientado a objetos | Reúne dados e regras dos objetos reais (A-19, A-20) |
| `domain` (modelo) | Funções | O Black-Litterman não tem estado nem identidade (A-20) |
| `core`, `data` | Modular | Transformações e coletas simples |

## 4. Modelo de domínio

Todos os objetos são `@dataclass(frozen=True)`: imutáveis e validados ao serem criados.

```text
Market ──contém──▶ bizdays.Calendar
   └── universe ──contém──▶ Asset ──contém──▶ PriceSeries
                                └── usa ──▶ AssetClass

Portfolio ──refere-se pelo ticker──▶ Asset
Portfolio ──usa──▶ Strategy, ModelParameters
View      ──refere-se pelo ticker──▶ Asset
```

### 4.1 Objetos

| Objeto | Tipo | Atributos | Métodos |
|---|---|---|---|
| `AssetClass` | Enum | `STOCK`, `ETF`, `BOND`, `CURRENCY`, `CRYPTO` | — |
| `PriceSeries` | Objeto de valor | `series: pd.Series`, `currency: str`, `adjusted: bool` | `price_at`, `slice` |
| `Asset` | Identificado pelo ticker | `ticker`, `asset_class`, `market`, `prices`, `issuer` | `price_at`, `compute_returns` |
| `Market` | Objeto | `code`, `location`, `currency`, `timezone`, `trading_hours`, `calendar`, `universe`, `market_caps`, `risk_free`, `benchmark` | `find_asset`, `list_assets`, `market_portfolio` |
| `Strategy` | Enum | `MARKET`, `BLACK_LITTERMAN`, `EQUAL_WEIGHT` | — |
| `Portfolio` | Entidade, identificada pelo `id` | `id`, `name`, `weights`, `reference_date`, `strategy`, `parameters` | `validate`, `expected_return`, `volatility`, `compare` |
| `View` | Classe abstrata | `expected_return` (decimal ao ano, acima do CDI) | `pick_row`, `validate` |
| `AbsoluteView` | Subclasse de `View` | `asset` | — |
| `RelativeView` | Subclasse de `View` | `long_asset`, `short_asset` | — |
| `ModelParameters` | Objeto de valor | `tau = 0.05`, `delta = 2.5`, `max_weight = 0.20` | `validate` |

Escolhas de estrutura:

- **`Asset`:** igualdade e hash usam só o ticker. Por isso ele pode ser chave de dicionário. O ISIN fica fora da primeira versão.
- **`Market.universe`:** é um mapa ticker → `Asset`, para busca direta e sem repetição.
- **`Market.calendar`:** é o calendário B3 da `bizdays`, usado diretamente (A-21).
- **`Portfolio`:** é a única entidade. Duas carteiras com os mesmos pesos continuam sendo carteiras diferentes.

### 4.2 Funções do modelo

O Black-Litterman é um processo sem estado que usa os objetos (A-20).

| Função | Entrada | Saída |
|---|---|---|
| `prior(market, sigma, params)` | `Market`, Σ e `ModelParameters` | Π |
| `posterior(pi, views, sigma, params)` | Π, lista de `View`, Σ e `ModelParameters` | `μ_BL` |
| `optimize(mu, sigma, params, reference_date, name)` | `μ_BL`, Σ e `ModelParameters` | `Portfolio` |
| `pick_matrix(views, assets)` | Views e ordem dos ativos | P e Q |
| `omega(P, sigma, tau)` | P, Σ e τ | Ω, por He-Litterman |

Tipos usados nas funções (A-23):

| Dado | Tipo | Forma |
|---|---|---|
| Σ | `pd.DataFrame` | n × n, índice e colunas = tickers |
| Π, `μ_BL` | `pd.Series` | n valores, índice = tickers |
| P | `np.ndarray` | k × n |
| Q | `np.ndarray` | k |
| Ω | `np.ndarray` | k × k, diagonal |

As entradas e saídas têm rótulos. Dentro das funções, a conta é feita em `numpy`, na ordem de `sigma.index`.

Uso esperado:

```python
params = ModelParameters(tau=0.05, delta=2.5, max_weight=0.20)
pi = prior(market, sigma, params)
mu = posterior(pi, views, sigma, params)
portfolio = optimize(mu, sigma, params, reference_date=date(2026, 11, 17), name="BL top 10")
```

## 5. Coleta e cálculos

### 5.1 Fontes da fase inicial

Cada fonte é uma função que devolve o dado no formato do projeto e um `Provenance` (A-22). Não há fonte de reserva nem ordem de tentativas.

| Função | Fonte | Saída |
|---|---|---|
| `yahoo.fetch_prices(tickers, start, end)` | yfinance | `pd.DataFrame`: datas × tickers, fechamento ajustado |
| `yahoo.fetch_benchmark(start, end)` | yfinance | `pd.Series`: Ibovespa por data |
| `yahoo.fetch_market_caps(tickers)` | yfinance | `pd.Series`: market cap atual por ticker |
| `bcb.fetch_cdi(start, end)` | BCB, SGS 12 | `pd.Series`: CDI em decimal ao dia |

O `Provenance` guarda `source`, `collected_at`, `period_start` e `period_end`. O `storage` grava cada dado em Parquet, com a origem ao lado, para não baixar de novo. O `builders` monta os `Asset` e o `Market`.

COTAHIST, CVM e brapi ficam para as próximas fases.

### 5.2 Cálculos

| Função | Entrada | Saída |
|---|---|---|
| `simple_returns(prices)` | Preços, datas × tickers | Retornos simples |
| `excess_returns(returns, risk_free)` | Retornos e CDI | Retornos acima do CDI |
| `covariance(returns, periods_per_year=252)` | Retornos | Σ anualizada |

Fluxo: `fetch_prices` → `simple_returns` → `excess_returns` → `covariance` → `prior`.

### 5.3 Snapshot

O snapshot é o único insumo de mercado do servidor (A-14). Ele é gerado pela rotina local.

| Campo | Conteúdo |
|---|---|
| `generated_at` | Quando a rotina rodou |
| `data_as_of` | Último pregão nos dados |
| `tickers` | Ativos, na ordem das matrizes |
| `sigma` | Σ anualizada, janela de 3 anos |
| `market_caps` | Market cap de cada ativo |
| `delta` | δ usado |
| `provenance` | Fonte e data de coleta de cada dado |

Quando o usuário escolhe ativos, o servidor recorta Σ e renormaliza os market caps para formar `w_mkt`.

## 6. Planejado

As partes abaixo seguem as decisões da análise, mas ainda não têm assinaturas:

- **`study`:** seleção por liquidez com o COTAHIST, market cap histórico com a CVM, de-para de tickers e geração do snapshot.
- **`backtest`:** walk-forward sem views, custos de transação, benchmarks e métricas (A-03, A-13, A-17).
- **`services` e `api`:** recorte do snapshot, chamada de `prior → posterior → optimize` e rotas HTTP (A-11).
- **`frontend`:** interface sobre a API.
- **Acompanhamento:** marcação a mercado de uma carteira pronta, com a brapi (A-18).
- **Tratamento de dados:** alinhamento no calendário B3 e regra de dados faltantes (FR-TRA-01 e FR-TRA-02).

## 7. Dados publicados e dados locais

| Conteúdo | Git | Servidor |
|---|---|---|
| Código e documentos | Sim | Sim |
| Snapshot | Não | Sim |
| Séries de preços do Yahoo | Não | Não |
| COTAHIST e dados da Bloomberg | Não | Não |
| Quantidade de ações da CVM | Pode entrar, com atribuição | Não |

## 8. Dependências

| Pacote | Uso |
|---|---|
| `pandas`, `numpy` | Dados e cálculos |
| `scipy` | Otimização |
| `bizdays` | Calendários B3 e ANBIMA |
| `yfinance` | Coleta de preços e market cap |
| `requests` | Coleta do CDI |
| `pyarrow` | Gravação em Parquet |

O servidor precisará só de `pandas`, `numpy`, `scipy` e `bizdays`.

## 9. Decisões de arquitetura

| Decisão | Motivo | Referência |
|---|---|---|
| API entre frontend e backend | Permite trocar o frontend | A-11 |
| Snapshot como única fonte do servidor | Elimina coleta ao vivo no servidor | A-14 |
| Objetos reais no domínio | Responde à estrutura de dados de cada conceito | A-20 |
| Black-Litterman em funções | Processo sem estado nem identidade | A-20 |
| `bizdays` usado diretamente | Evita uma classe que só repetiria a biblioteca | A-21 |
| Duas fontes na fase inicial | Mantém a coleta simples | A-22 |
| Rótulos nas entradas, `numpy` por dentro | Garante a ordem dos ativos | A-23 |
| Σ na otimização | Preserva o teste sem views | A-07 |

## 10. Rastreabilidade

| Requisito | Onde |
|---|---|
| FR-COL-01, FR-COL-02 | `data/yahoo.py` (`fetch_prices`) |
| FR-COL-03 | `data/bcb.py` |
| FR-COL-04 | `data/yahoo.py` (`fetch_market_caps`) |
| FR-COL-05 a 08 | Planejado: `study` |
| FR-TRA-01, FR-TRA-02 | Planejado |
| FR-TRA-03 | `core.simple_returns`, `Asset.compute_returns` |
| FR-TRA-04 | `core.excess_returns` |
| FR-TRA-05 | `core.covariance` |
| FR-MOD-01 | `Market.market_portfolio` |
| FR-MOD-02 | `model.prior` |
| FR-MOD-03 | `ModelParameters.delta`; estimação planejada |
| FR-MOD-04, FR-MOD-05 | `domain/views.py` |
| FR-MOD-06 | `model.pick_matrix` |
| FR-MOD-07 | `model.omega` |
| FR-MOD-08, FR-MOD-09 | `model.posterior` |
| FR-MOD-10, FR-MOD-13 | `model.optimize` |
| FR-MOD-11 | `Portfolio.compare` |
| FR-MOD-12 | `Portfolio.expected_return`, `Portfolio.volatility` |
| Origem dos dados (NFR) | `data/provenance.py`, `data/storage.py` |
| FR-SEL, FR-BKT, FR-API, FR-UI | Planejado |

## 11. Ordem de implementação

1. **Domínio:** implementar os objetos e as funções do modelo e testar com dados fictícios (T-01 a T-09).
2. **Coleta e cálculos:** implementar `data` e `core` e testar sem rede (T-11, T-12).
3. **Snapshot:** gerar o snapshot na máquina local.
4. **Backend:** implementar `services` e `api` e publicar no PythonAnywhere.
5. **Estudo e backtest:** COTAHIST, CVM e motor do backtest.
6. **Frontend.**

## 12. Pontos em aberto

- Framework da API: Flask (opção inicial) ou FastAPI, conforme o suporte do PythonAnywhere.
- Se `Asset.compute_returns` deve chamar `core.simple_returns`, para a fórmula ficar em um lugar só.
- Hospedagem do frontend.
- Uso da Bloomberg (A-16).
