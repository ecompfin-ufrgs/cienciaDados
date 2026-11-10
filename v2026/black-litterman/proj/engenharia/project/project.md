# Projeto de software

Este documento descreve a arquitetura do projeto Black-Litterman. Ele parte dos [requisitos](../eng_requisitos/documentacao.md) e das [decisões da análise](../eng_requisitos/analise.md). Os identificadores `A-xx` e `FR-xx` apontam para esses documentos.

## 1. Visão geral

A arquitetura separa o que coleta dados do que atende o usuário:

- **Máquina local:** coleta dados, roda o estudo de backtest e gera um snapshot com os insumos do modelo.
- **Servidor:** o backend no PythonAnywhere lê o snapshot e calcula as carteiras. Ele não consulta fontes externas durante uma requisição.
- **Frontend:** consome a API do backend e pode ser trocado sem alterar o restante.

```text
        MÁQUINA LOCAL                            SERVIDOR E FRONTEND

 COTAHIST  CVM  yfinance  brapi  BCB                  Frontend
     |      |      |        |     |              (Streamlit, inicial)
     v      v      v        v     v                      |
 +-------------------------------+                       | HTTP / JSON
 | bl/data e bl/study            |                       v
 +-------------------------------+                +-------------+
       |                  |                       | bl/api      |
       v                  v                       +-------------+
 +-------------+    snapshot.json --- envio --+          |
 | bl/backtest |                              |          v
 +-------------+                              +--> +-------------+
       |                                           | bl/services |
       v                                           +-------------+
   publicados/ ------- catálogo e resultados ---------> |
                                                         v
                                                  +-------------+
                                                  | bl/domain   |
                                                  +-------------+
```

`bl/core` prepara os dados na máquina local. `bl/domain` é usado tanto pelo servidor quanto pelo backtest.

## 2. Estrutura do repositório

```text
v2026/black-litterman/
├── bl/                     pacote Python do backend e do estudo
│   ├── __main__.py         comandos locais, como a geração do snapshot
│   ├── config.py           parâmetros default
│   ├── exceptions.py       erros nomeados
│   ├── schemas.py          estruturas trocadas entre as camadas
│   ├── domain/             modelo de domínio, orientado a objetos
│   │   ├── asset.py        Asset e Universe
│   │   ├── market.py       MarketInputs
│   │   ├── views.py        View, AbsoluteView, RelativeView e ViewSet
│   │   ├── model.py        BlackLittermanModel, Prior e Posterior
│   │   ├── constraints.py  Constraints
│   │   ├── optimizer.py    PortfolioOptimizer
│   │   └── portfolio.py    Portfolio e métricas ex-ante
│   ├── core/               funções numéricas de preparação
│   │   ├── cleaning.py     calendário e dados faltantes
│   │   ├── returns.py      retornos e excesso sobre o CDI
│   │   └── covariance.py   Σ e verificação PSD
│   ├── data/               coleta local nas fontes
│   │   ├── prices.py       preços ajustados e Ibovespa: yfinance
│   │   ├── quotes.py       market cap e fechamento D-1: brapi
│   │   ├── riskfree.py     CDI do BCB
│   │   ├── tickers.py      normalização e validação
│   │   ├── calendar.py     dias úteis da ANBIMA
│   │   └── provenance.py   fonte e data dos dados
│   ├── study/              rotinas locais
│   │   ├── cotahist.py     leitura e filtros do COTAHIST
│   │   ├── liquidity.py    ranking, universo e catálogo
│   │   ├── mapping.py      de-para de CNPJ, ticker e ISIN
│   │   ├── shares.py       quantidade de ações da CVM
│   │   ├── market_cap.py   market cap histórico
│   │   ├── quality.py      controle de qualidade
│   │   ├── dataset.py      gravação no formato fixo
│   │   └── snapshot.py     geração e envio do snapshot
│   ├── backtest/           motor do backtest
│   │   ├── engine.py       walk-forward
│   │   ├── costs.py        custos de transação
│   │   ├── benchmarks.py   Ibovespa, CDI, 1/N e market cap
│   │   └── metrics.py      métricas do backtest
│   ├── services/           casos de uso do servidor
│   │   ├── snapshot.py     leitura do snapshot e arquivos publicados
│   │   ├── portfolio.py    calcula a carteira
│   │   └── tracking.py     acompanhamento D-1 (opcional)
│   └── api/                camada HTTP
│       ├── app.py          criação da aplicação Flask
│       ├── routes.py       endpoints
│       └── serializers.py  conversão entre JSON e objetos
├── frontend/               interface, com dependências próprias
│   └── streamlit_app.py
├── publicados/             arquivos sem dados brutos
│   ├── catalog.json        catálogo de tickers
│   └── study_results.json  métricas e curvas agregadas
├── dados/                  dados locais, fora do Git
│   ├── brutos/
│   ├── processados/
│   └── snapshot/
├── tests/                  testes automatizados (test_*.py)
├── docs/                   guias do usuário e da API
├── proj/                   documentos de engenharia e gestão
├── requirements-server.txt dependências do servidor
└── requirements-local.txt  dependências das rotinas locais
```

A pasta `dados/` entra no `.gitignore`, de acordo com a decisão A-16.

## 3. Camadas e dependências

| Camada | Onde roda | Responsabilidade | Pode importar |
|---|---|---|---|
| `domain` | Local e servidor | Regras e conceitos do Black-Litterman, em classes | `config`, `exceptions` |
| `core` | Local | Preparação numérica, sem rede ou arquivos | `config`, `schemas`, `exceptions` |
| `data` | Local | Coleta nas fontes | `config`, `schemas`, `exceptions` |
| `study` | Local | Base histórica, catálogo e snapshot | `core`, `data`, `config`, `schemas`, `exceptions` |
| `backtest` | Local | Simulação sobre a base no formato fixo | `domain`, `core`, `config`, `schemas`, `exceptions` |
| `services` | Servidor | Casos de uso do app | `domain`, `config`, `schemas`, `exceptions` |
| `api` | Servidor | HTTP e JSON | `services`, `schemas`, `exceptions` |
| `frontend` | A definir | Interface | Somente a API, por HTTP |

Regras principais:

1. `domain` e `core` não fazem I/O e não importam `data`, `services`, `api`, `study` nem `backtest`.
2. `services` e `api` não importam `data` nem `study`. O servidor só lê o snapshot e os arquivos publicados.
3. `backtest` não acessa nenhuma fonte de dados. Ele recebe uma base no formato fixo (seção 6).
4. O frontend não importa `bl`. Trocar o Streamlit não altera o backend (A-11).

### 3.1 Paradigmas

O domínio da aplicação usa programação orientada a objetos. As demais camadas seguem programação modular, com funções organizadas por responsabilidade (A-19).

| Camada | Paradigma | Motivo |
|---|---|---|
| `domain` | Orientado a objetos | Reúne conceitos, validações e comportamento do modelo |
| `core`, `data` | Modular | Transformações e coletas simples |
| `services`, `api` | Modular | Coordenam chamadas e convertem dados |
| `study`, `backtest` | Modular | Executam etapas sequenciais usando o domínio quando necessário |
| `frontend` | Definido pela ferramenta | Pode mudar sem afetar o backend |

### 3.2 Modelo de domínio

```text
Universe ---------- contém ----------> Asset

View  <|---- AbsoluteView
      <|---- RelativeView

ViewSet ----------- contém ----------> View

BlackLittermanModel --- usa ---------> MarketInputs
BlackLittermanModel --- produz ------> Prior, Posterior

PortfolioOptimizer ---- usa ---------> Posterior, Constraints
PortfolioOptimizer ---- produz ------> Portfolio
```

| Classe | Responsabilidade |
|---|---|
| `Asset` | Representa um ativo e seu ticker normalizado |
| `Universe` | Mantém a lista ordenada de ativos, sem duplicados, e define a ordem das matrizes |
| `MarketInputs` | Reúne Σ, `w_mkt`, δ e o universo, validando dimensões e coerência |
| `View` | Classe abstrata para uma opinião sobre retornos |
| `AbsoluteView` | Gera uma linha de `P` com `1` no ativo |
| `RelativeView` | Gera uma linha de `P` com `+1` e `-1` nos ativos |
| `ViewSet` | Monta `P` e `Q` e rejeita views duplicadas ou dependentes |
| `BlackLittermanModel` | Calcula o prior, Ω e o posterior |
| `Prior`, `Posterior` | Guardam os resultados do modelo |
| `Constraints` | Guarda o limite por ativo e verifica se o problema é viável |
| `PortfolioOptimizer` | Calcula os pesos ótimos |
| `Portfolio` | Guarda os pesos, compara com `w_mkt` e calcula as métricas ex-ante |

Um esboço do uso esperado:

```python
class View(ABC):
    @abstractmethod
    def pick_row(self, universe: Universe) -> np.ndarray: ...


model = BlackLittermanModel(inputs, tau=0.05)
posterior = model.posterior(views)
portfolio = PortfolioOptimizer(constraints).optimize(posterior)
```

`View` é o principal uso de polimorfismo: `ViewSet` monta `P` sem precisar saber o tipo de cada view. Objetos que representam resultados são imutáveis, para que um cálculo não altere outro.

`schemas.py` continua existindo para transportar dados entre camadas, como `FetchResult`, `Provenance` e `Snapshot`. As regras do modelo ficam em `domain`.

## 4. Fontes de dados e snapshot

| Dado | Fonte | Onde entra |
|---|---|---|
| Seleção por liquidez | COTAHIST, baixado manualmente | `study` |
| Retornos e Σ | Preços ajustados do yfinance | `data`, `study` |
| Market cap histórico | Preço bruto do COTAHIST e quantidade de ações da CVM | `study` |
| Market cap atual | Candidata: brapi | `data` |
| Fechamento D-1 | Candidata: brapi | `data` |
| CDI | Série 12 do SGS | `data` |
| Calendário | Dias úteis da ANBIMA | `data` |

### Snapshot

O snapshot é o único insumo de mercado do servidor (A-14). Ele é um arquivo JSON pequeno, gerado pela rotina local.

| Campo | Conteúdo |
|---|---|
| `as_of` | Data do último fechamento usado |
| `tickers` | Os 30 ativos do catálogo, na ordem das matrizes |
| `covariance` | Σ anualizada, com janela de 3 anos |
| `market_caps` | Market cap de cada ativo |
| `delta` | δ estimado com o Ibovespa |
| `last_close` | Fechamento D-1 de cada ativo |
| `provenance` | Fontes e datas de extração |

Quando o usuário escolhe ativos, o servidor recorta a parte correspondente de Σ e renormaliza os market caps para formar `w_mkt`.

## 5. Fluxos principais

### 5.1 Rotina diária

A rotina roda fora do servidor, em dias úteis:

1. `study/snapshot.py` coleta os dados dos 30 ativos, do Ibovespa e do CDI.
2. `core` trata os dados e estima Σ.
3. A rotina valida o resultado: todos os ativos presentes, Σ positiva semidefinida e market caps disponíveis.
4. O snapshot é enviado ao PythonAnywhere, pela API de arquivos ou manualmente.

Se a rotina falhar, nada é enviado. O servidor continua com o último snapshot válido, e o app mostra a data dos dados (FR-COL-08).

### 5.2 Carteira de hoje

1. O frontend pede o catálogo e abre com os 10 ativos mais líquidos.
2. O usuário ajusta os ativos, os parâmetros e as views.
3. O frontend envia os dados para `POST /api/v1/portfolio`.
4. `services/snapshot.py` lê o snapshot e recorta os ativos escolhidos.
5. `services/portfolio.py` cria `MarketInputs`, `ViewSet` e `BlackLittermanModel`, e `PortfolioOptimizer` devolve um `Portfolio`.
6. A API devolve pesos, métricas, parâmetros usados e a data dos dados.

### 5.3 Preparação do estudo

1. A equipe baixa manualmente os arquivos do COTAHIST.
2. `study/cotahist.py` aplica os filtros.
3. `study/liquidity.py` gera o ranking, o universo de cada data e o catálogo atual.
4. `data/prices.py` coleta os preços ajustados.
5. `study/shares.py` e `study/market_cap.py` calculam o market cap em cada rebalanceamento.
6. `study/quality.py` verifica a base, e `study/dataset.py` grava o formato fixo.

### 5.4 Backtest

Em cada rebalanceamento `t`, `backtest/engine.py`:

1. lê o universo definido com dados anteriores a `t`;
2. estima Σ com a janela encerrada em `t-1`;
3. calcula os pesos com as classes de `domain`, sem views;
4. mantém os pesos até o rebalanceamento seguinte;
5. aplica custos de transação e a regra de deslistagem.

O motor recebe uma base já pronta. Assim, a mesma lógica serve para a versão pública e para uma eventual base da Bloomberg.

### 5.5 Acompanhamento D-1 (opcional)

`services/tracking.py` lê `last_close` do snapshot e calcula o valor da carteira. A resposta sempre informa a data dos dados (A-18).

## 6. Formato da base do backtest

O motor lê estes arquivos em `dados/processados/`. Eles usam Parquet, ou CSV para dados externos.

| Arquivo | Colunas | Conteúdo |
|---|---|---|
| `returns` | `date`, `ticker`, `return` | Retornos semanais ajustados |
| `risk_free` | `date`, `return` | CDI capitalizado na mesma frequência |
| `universe` | `rebalance_date`, `rank`, `ticker` | Ativos de cada rebalanceamento |
| `market_cap` | `rebalance_date`, `ticker`, `market_cap` | Market cap em `t-1` |
| `benchmark` | `date`, `name`, `return` | Ibovespa e demais séries de comparação |
| `events` | `date`, `ticker`, `event` | Deslistagens e tratamentos aplicados |
| `manifest` | Fontes, datas de extração e parâmetros | Rastreabilidade da base |

## 7. API

A versão inicial usa JSON e o prefixo `/api/v1`.

| Método | Rota | Função | Requisito |
|---|---|---|---|
| `GET` | `/health` | Verifica o backend e a data do snapshot | Implantação |
| `GET` | `/catalog` | Lista o catálogo | FR-API-01 |
| `POST` | `/portfolio` | Calcula a carteira | FR-API-02 |
| `GET` | `/study` | Devolve os resultados do estudo | FR-API-03 |
| `POST` | `/tracking` | Devolve o acompanhamento D-1 (opcional) | FR-UI-04 |

### Exemplo de requisição

```json
{
  "tickers": ["PETR4", "VALE3", "ITUB4", "BBDC4", "ABEV3"],
  "views": [
    {"type": "absolute", "asset": "VALE3", "value": 0.08},
    {"type": "relative", "asset": "PETR4", "versus": "ITUB4", "value": 0.03}
  ],
  "parameters": {"tau": 0.05, "delta": null, "max_weight": 0.20}
}
```

Os valores das views são decimais anuais, acima do CDI. `delta` nulo indica o valor estimado no snapshot.

### Exemplo de resposta

```json
{
  "weights": [
    {"ticker": "PETR4", "market": 0.20, "black_litterman": 0.20, "difference": 0.00}
  ],
  "metrics": {"expected_return": 0.12, "volatility": 0.22, "sharpe": 0.55},
  "parameters_used": {"tau": 0.05, "delta": 2.4, "max_weight": 0.20},
  "data_date": "2026-11-05",
  "warnings": [],
  "provenance": [
    {"source": "yfinance", "extracted_at": "2026-11-06T18:00:00Z"}
  ]
}
```

Os valores acima são apenas ilustrativos.

### Erros

```json
{
  "error": {
    "code": "INFEASIBLE_OPTIMIZATION",
    "message": "Não foi possível calcular pesos com essas restrições.",
    "details": {}
  }
}
```

| Exceção | Código | HTTP |
|---|---|---|
| `InvalidTickerError` | `INVALID_TICKER` | 422 |
| `InvalidViewError` | `INVALID_VIEW` | 422 |
| `InsufficientDataError` | `INSUFFICIENT_DATA` | 422 |
| `InfeasibleOptimizationError` | `INFEASIBLE_OPTIMIZATION` | 422 |
| `SnapshotUnavailableError` | `SNAPSHOT_UNAVAILABLE` | 503 |

## 8. Dados publicados e dados locais

| Conteúdo | Git | Servidor |
|---|---|---|
| Código e documentos | Sim | Sim |
| Catálogo de tickers | Sim | Sim |
| Resultados agregados do estudo | Sim | Sim |
| Snapshot | Não | Sim |
| Quantidade de ações da CVM | Pode entrar, com atribuição | Não |
| COTAHIST e ranking com volumes | Não | Não |
| Séries de preços do Yahoo | Não | Não |
| Dados da Bloomberg | Não | Não |

O snapshot fica fora do Git até a equipe confirmar que os termos das fontes permitem publicá-lo.

## 9. Implantação

**Backend**

- Aplicação Flask, por WSGI, no PythonAnywhere.
- Conta gratuita, sem tarefas agendadas.
- Dependências mínimas: Flask, NumPy e SciPy. O servidor não precisa de yfinance nem de brapi.
- O snapshot fica em uma pasta do servidor, fora do repositório.

**Rotina local**

- Execução por comando, como `python -m bl snapshot`, em dias úteis.
- Pode ser agendada no Agendador de Tarefas do Windows. Se o computador estiver desligado, o app segue com o último snapshot.
- Tokens da brapi e do PythonAnywhere ficam em variáveis de ambiente, nunca no Git.

**Frontend**

- Separado do backend, com `requirements` próprio.
- Recebe o endereço da API por configuração.
- A hospedagem ainda será definida.

**Pontos a verificar**

- Espaço ocupado pelas dependências, porque a conta gratuita tem 512 MB.
- Envio pela API de arquivos do PythonAnywhere em conta gratuita. Se não funcionar, o envio é feito manualmente.
- Tempo de resposta do cálculo no servidor.

## 10. Decisões de arquitetura

| Decisão | Motivo | Referência |
|---|---|---|
| API entre frontend e backend | Permite trocar o frontend | A-11 |
| Flask como opção inicial | É publicado por WSGI no PythonAnywhere, sem depender do suporte experimental a ASGI | A-11 |
| Snapshot como única fonte do servidor | Elimina coleta ao vivo, cache e dependência de fontes externas no servidor | A-14 |
| Estudo fora do servidor | Evita limites do servidor e mantém dados brutos locais | A-13, A-16 |
| Backtest com formato fixo | Separa o método da fonte dos dados | A-13 |
| Domínio orientado a objetos | Reúne conceitos e validações do modelo em classes | A-19 |
| Demais camadas modulares | Mantém simples as etapas de coleta, preparação e execução | A-19 |
| Domínio e núcleo sem I/O | Permite testar a matemática sem rede | RNF-02 |
| Σ na otimização | Mantém a primeira versão simples e preserva o teste sem views | A-07 |

## 11. Rastreabilidade

| Requisito | Módulos |
|---|---|
| FR-SEL-01 a 02 | `study/cotahist.py` |
| FR-SEL-03 a 06 | `study/liquidity.py`, `study/mapping.py` |
| FR-COL-01 | `data/prices.py` |
| FR-COL-02 | `data/tickers.py` |
| FR-COL-03 | `data/riskfree.py` |
| FR-COL-04 | `data/quotes.py` |
| FR-COL-05 | `study/shares.py` |
| FR-COL-06 | `study/dataset.py` |
| FR-COL-07 a 08 | `study/snapshot.py`, `services/snapshot.py` |
| FR-TRA-01 a 02 | `core/cleaning.py`, `data/calendar.py` |
| FR-TRA-03 a 04 | `core/returns.py` |
| FR-TRA-05 | `core/covariance.py` |
| FR-MOD-01 a 03 | `domain/market.py`, `domain/model.py` |
| FR-MOD-04 a 06 | `domain/views.py` |
| FR-MOD-07 a 09 | `domain/model.py` |
| FR-MOD-10, FR-MOD-13 | `domain/constraints.py`, `domain/optimizer.py` |
| FR-MOD-11 | `services/portfolio.py`, `frontend/` |
| FR-MOD-12 | `domain/portfolio.py` |
| FR-BKT-01 a 02 | `backtest/engine.py` |
| FR-BKT-03 | `backtest/benchmarks.py` |
| FR-BKT-04 a 05 | `backtest/metrics.py`, `frontend/` |
| FR-BKT-06 | `study/market_cap.py` |
| FR-BKT-07 | `backtest/engine.py` |
| FR-BKT-08 | `backtest/costs.py` |
| FR-BKT-09 | `backtest/engine.py`, com views informadas no exercício |
| FR-API-01 a 04 | `api/`, `services/` |
| FR-UI-01 a 04 | `frontend/` |

## 12. Testes

| Tipo | Alvo | Exemplo |
|---|---|---|
| Unitário | `domain` | Sem views, `μ_BL = Π` |
| Unitário | `core` | `r_ex + r_f = r` |
| Unitário | `backtest` | Pesos em `t` não mudam com dados futuros |
| Integração | `services` e `api` | Requisição com snapshot de teste devolve carteira válida |
| Contrato | `frontend` e `api` | Respostas seguem o formato documentado |
| Manual | Implantação | Envio do snapshot e tempo de resposta no PythonAnywhere |

Os testes automatizados não acessam a rede. Eles usam um snapshot de teste com dados fictícios. O detalhamento fica em `tests/tests.md`.

## 13. Ordem de implementação

1. **Base do projeto:** mover o esqueleto para `bl/`, ajustar os imports e criar dependências, `.gitignore` e `tests/`.
2. **Domínio:** implementar as classes de `domain` e testar com dados fictícios.
3. **Backend:** implementar `services` e `api`, publicar com um snapshot de teste e medir a resposta no PythonAnywhere.
4. **Estudo:** gerar ranking, catálogo, market cap e base histórica.
5. **Rotina:** implementar `data`, `core` e `study/snapshot.py`.
6. **Backtest:** implementar o motor e publicar os resultados.
7. **Frontend:** implementar a interface sobre a API.
8. **Opcional:** implementar o acompanhamento D-1.

As etapas 2 e 4 podem andar em paralelo, porque usam contratos definidos neste documento.

## 14. Pontos em aberto

- Onde a rotina roda depois da fase inicial, se o computador local não for suficiente.
- Hospedagem do frontend.
- Local dos arquivos atuais de `tests/`, que dependem da orientação do professor.
- Uso da Bloomberg (A-16).
