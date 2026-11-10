# Documentação de requisitos

Documentar requisitos é a atividade de produzir um documento que resume e organiza os artefatos das fases de elicitação e análise. O objetivo é explicar com precisão os requisitos dos usuários e do sistema, sem dubiedades nem contradições.

O documento final está em LaTeX, na pasta [docs](docs/main.tex):

1. [Introdução](docs/cap1.tex): objetivo, escopo, público e definições.
2. [Definição do sistema](docs/cap2.tex): componentes, entradas, processamento e saídas.
3. [Especificação de requisitos](docs/cap3.tex): requisitos funcionais, não funcionais e itens fora do escopo inicial.

## Resumo do sistema

O projeto calcula pesos de carteiras de ações brasileiras com o modelo Black-Litterman e tem dois produtos.

| Produto | Função | Dados |
|---|---|---|
| Webapp | Calcula a carteira de hoje a partir de um catálogo com os 30 ativos mais líquidos, permitindo views | Snapshot gerado por uma rotina diária fora do servidor |
| Estudo de backtest | Avalia o método com os 10 ativos mais líquidos em cada data, sem views no resultado principal | Retornos: preços ajustados do yfinance. Seleção: COTAHIST. Market cap: quantidade de ações da CVM. Taxa livre de risco: CDI |

O backend roda no PythonAnywhere, lê o snapshot e expõe uma API. O frontend é separado e começa em Streamlit, podendo mudar.

## Artefatos relacionados

- [Elicitação](elicitacao.md): lista completa de necessidades levantadas.
- [Análise](analise.md): contradições, decisões e pontos em aberto.
- [Fluxo de dados do backtest](../project/fluxo_dados_backtest_bl.md): seleção de ativos, coleta e regras do estudo.

## Pendências

- **Rotina diária:** confirmar o envio do snapshot ao PythonAnywhere.
- **A-16:** conversar com o professor sobre o uso da Bloomberg.
