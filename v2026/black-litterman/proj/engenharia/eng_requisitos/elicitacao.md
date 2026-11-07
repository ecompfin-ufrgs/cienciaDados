# Elicitação de requisitos

As decisões que resolveram contradições e dúvidas estão em [analise.md](analise.md).

## Requisitos do Sistema
Para o modelo BL funcionar, são necessárias algumas entradas.

1. Um modelo de equilíbrio de mercado. Os pesos de market cap definem a carteira de mercado, e o prior é calculado por otimização reversa, de forma consistente com o CAPM. Esse é o ponto de partida do programa, para verificar o que o mercado está sinalizando.
2. Opinião do investidor: o investidor dará a sua opinião sobre as taxas de retorno em relação ao modelo de equilíbrio do ponto 1.
3. Grau de confiança: está relacionado ao item 2. Na primeira versão, a incerteza das views segue a abordagem de He-Litterman. A confiança informada pelo usuário fica para uma versão futura.
4. Universo de ativos: como um dos produtos finais do projeto é uma carteira de ações brasileiras, será feito um processo documentado de seleção dos ativos, usando o critério de liquidez. A carteira do estudo terá os 10 ativos mais líquidos. No app, o usuário poderá editar a seleção dentro de um catálogo com os 30 ativos mais líquidos.
5. Dados históricos: a construção da carteira e o backtest podem usar fontes mais confiáveis que não são coletadas diretamente pelo software, como a Bloomberg, caso isso seja possível. Mesmo assim, deve existir um módulo de coleta de dados históricos de fonte gratuita. As duas formas devem entregar os dados no mesmo formato.

## Requisitos do Usuário
1. O usuário deverá ter algum conhecimento básico de mercado financeiro e de ações.
2. O usuário deverá conseguir expressar suas views como retornos em % ao ano acima do CDI.

## Requisitos funcionais
É o conjunto de funcionalidades que devem ser implementadas para resolver o problema do cliente.

### seleção de ativos
| ID | Requisito |
|---|---|
| RF-SEL-01 | Ler os arquivos COTAHIST baixados **manualmente** do site da B3, sem coleta automatizada. |
| RF-SEL-02 | Filtrar os registros de ações e units do mercado à vista em lote padrão, conforme o [documento de fluxo de dados](../project/fluxo_dados_backtest_bl.md). |
| RF-SEL-03 | Calcular, em cada data de rebalanceamento, o ranking de liquidez com os 252 pregões **estritamente anteriores**, excluindo papéis com presença inferior a 80%. |
| RF-SEL-04 | Manter uma classe por empresa e exigir histórico suficiente para estimar Σ. |
| RF-SEL-05 | Selecionar os **10 ativos mais líquidos** para a carteira do estudo. |
| RF-SEL-06 | Gerar o **catálogo de tickers** do app com os **30 ativos mais líquidos** do ranking mais recente, sem publicar preços ou volumes. |

### coleta de dados
| ID | Requisito |
|---|---|
| RF-COL-01 | Baixar série histórica de preços de fechamento **ajustado** (proventos e desdobramentos) de fonte gratuita, inicialmente `yfinance`, para cada ticker do universo, em janela e frequência parametrizáveis. |
| RF-COL-02 | Normalizar tickers B3 acrescentando o sufixo `.SA` e **validar a existência** do ticker antes de prosseguir; ticker inválido gera erro nomeado, não derruba a sessão. |
| RF-COL-03 | Coletar a série do **ativo livre de risco (CDI)** na API do BCB (SGS), série **12** (CDI % ao dia) — com a série **4389** (CDI a.a., base 252) como referência para anualização. |
| RF-COL-04 | Coletar o **valor de mercado (market cap) atual** de cada ativo para construir o vetor de pesos do prior no app. |
| RF-COL-05 | Coletar **volume financeiro diário** (preço × quantidade) para o diagnóstico de liquidez. |
| RF-COL-06 | Executar uma **rotina diária** fora do servidor, em dias úteis, que gere um **snapshot** com Σ, market caps, δ e fechamentos D-1 dos ativos do catálogo. |
| RF-COL-07 | Se a rotina falhar, manter o último snapshot válido e informar a data dos dados ao usuário. |
| RF-COL-08 | Registrar **proveniência** de cada dado (fonte, endpoint, data de extração) e expor isso no relatório final. |
| RF-COL-09 | Obter **free float** para ajustar o market cap (relevante na B3, onde empresas com float baixo distorcem o peso de equilíbrio). |
| RF-COL-10 | Obter a **carteira teórica do Ibovespa/IBrX** da B3 como alternativa de vetor de equilíbrio. |
| RF-COL-11 | Coletar a **quantidade histórica de ações** na CVM: FRE desde 2010 e composição do capital do ITR desde 2020, usando a data de entrega (`DT_RECEB`). |
| RF-COL-12 | Aceitar **dados externos** em arquivos com formato fixo, para que o backtest não dependa da fonte. |

### tratamento e estimação
| ID | Requisito |
|---|---|
| RF-TRA-01 | Alinhar todas as séries no **calendário de dias úteis da ANBIMA**. Dias com CDI e sem preço seguem a regra de dados faltantes. |
| RF-TRA-02 | Tratar dados faltantes por método aceito: *forward-fill* limitado a **N dias úteis** (default N = 5) para feriados/não-negociação; excluir do universo ativo com cobertura abaixo de um limiar — com aviso explícito ao usuário. |
| RF-TRA-03 | Construir a série de **retornos simples** `R = P_t/P_{t-1} − 1`. |
| RF-TRA-04 | Converter o CDI para a **mesma frequência** dos retornos dos ativos e construir a série de **excesso de retorno** `r_ex = r − r_f`. |
| RF-TRA-05 | Estimar a **matriz de covariância Σ** dos excessos de retorno pelo estimador amostral, com **anualização explícita**: ×252 para dados diários no app e ×52 para dados semanais no estudo. |
| RF-TRA-06 | Garantir que Σ seja **simétrica e positiva semidefinida**: verificar autovalores e aplicar correção para a matriz PSD mais próxima quando necessário; reportar o número de condição. |
| RF-TRA-07 | Oferecer estimador **encolhido de Ledoit-Wolf** como teste de robustez. |
| RF-TRA-08 | Oferecer estimador **EWMA** (RiskMetrics, λ = 0,94) como alternativa. |
| RF-TRA-09 | Calcular o **diagnóstico de liquidez** — volume financeiro diário mediano (ADTV) numa janela e % de pregões com negócio — e **sinalizar** (não excluir automaticamente) ativos abaixo do limiar. |
| RF-TRA-10 | Detectar e sinalizar *outliers* de retorno (ex.: retorno absoluto acima de 5σ) que sejam artefato de dado (split não ajustado), sem removê-los silenciosamente. |

### modelo BL
#### Prior de equilibrio
| ID | Requisito |
|---|---|
| RF-MOD-01 | Construir o vetor de pesos de mercado `w_mkt` por market cap **renormalizado dentro do universo** (`w_i = MC_i / Σ MC_j`). |
| RF-MOD-02 | Calcular os **retornos de equilíbrio implícitos** por otimização reversa, de forma consistente com o CAPM: $\Pi = \delta \, \Sigma \, w_{mkt}$. |
| RF-MOD-03 | Permitir o coeficiente de **aversão ao risco δ** de duas formas: (a) informado pelo usuário; (b) estimado por $\delta = (E[r_m] - r_f)/\sigma_m^2$ a partir do benchmark de mercado. Exibir o valor efetivamente usado. |
| RF-MOD-04 | Permitir vetor de equilíbrio alternativo (equal-weight ou carteira teórica do índice) quando o market cap for indisponível/não-confiável, **sinalizando a substituição** no relatório. |

#### visões (views)
| ID | Requisito |
|---|---|
| RF-MOD-05 | Permitir **view absoluta**: "o ativo *i* renderá q% ao ano em excesso ao CDI". Gera linha em `P` com `1` na coluna de *i*. |
| RF-MOD-06 | Permitir **view relativa**: "o ativo *i* supera o ativo *j* em q% ao ano". Gera linha em `P` com `+1` em *i* e `−1` em *j*. |
| RF-MOD-07 | Montar automaticamente a matriz `P` (k×N) e o vetor `Q` (k×1) a partir das views registradas, com **validação**: linha de view relativa deve somar 0; linha de view absoluta deve somar 1; sem views duplicadas ou linearmente dependentes. |
| RF-MOD-08 | Construir a matriz de incerteza das views **Ω** pelo método de He-Litterman: $\Omega = \mathrm{diag}(P\,\tau\Sigma\,P^{\top})$ — incerteza proporcional à variância do prior. |
| RF-MOD-09 | **Versão futura:** permitir ao usuário definir **confiança por view** (0–100%) e traduzi-la em Ω. |
| RF-MOD-10 | Expor o parâmetro **τ** com default documentado (τ = 0,05) e análise de sensibilidade disponível ao usuário. |
| RF-MOD-11 | Permitir view relativa **de cesta contra cesta** (grupos de ativos com pesos), não só par a par. |
| RF-MOD-12 | Exibir, antes de calcular, o **"choque implícito"** `Q − PΠ` — quanto a view diverge do que o mercado já precifica. É o que torna o modelo interpretável para o usuário. |

#### posterior
| ID | Requisito |
|---|---|
| RF-MOD-13 | Calcular o **retorno esperado posterior** pela forma numericamente estável (que evita inverter `τΣ`): $\mu_{BL} = \Pi + \tau\Sigma P^{\top}\left(P\,\tau\Sigma\,P^{\top} + \Omega\right)^{-1}(Q - P\Pi)$ |
| RF-MOD-14 | **Versão futura:** calcular a **covariância posterior** `Σ_BL = Σ + M` para comparação. A primeira versão usa `Σ` na otimização. |
| RF-MOD-15 | **Não usar inversão explícita de matriz** (`np.linalg.inv`): resolver sistemas com `np.linalg.solve`/Cholesky. É requisito de precisão numérica, não de estilo. |
| RF-MOD-16 | Suportar o caso **k = 0 (sem views)**: o posterior deve degenerar exatamente no prior. |

#### pesos finais
| ID | Requisito |
|---|---|
| RF-MOD-17 | Calcular os **pesos ótimos** maximizando $w^{\top}\mu_{BL} - \frac{\delta}{2}\,w^{\top}\Sigma\,w$. No caso irrestrito e sem views, os pesos devem voltar a `w_mkt`. |
| RF-MOD-18 | Suportar **restrições**: soma dos pesos = 1; sem venda a descoberto (`w ≥ 0`); peso máximo por ativo (default 20%). |
| RF-MOD-19 | Apresentar a **decomposição do resultado**: tabela comparando `w_mkt` (prior) × `w_BL` (posterior) × **Δ peso**, permitindo ao usuário ver o efeito isolado de cada view. |
| RF-MOD-20 | Reportar **métricas ex-ante** da carteira: retorno esperado, volatilidade, Sharpe esperado e contribuição de risco por ativo. |
| RF-MOD-21 | Tratar o caso de **otimização inviável** (restrições conflitantes) com mensagem explicativa, não com exceção crua. |

### Backtest
| ID | Requisito |
|---|---|
| RF-BKT-01 | Executar backtest **walk-forward** sem views: em cada data de rebalanceamento `t`, usar **exclusivamente** dados disponíveis antes de `t` para selecionar ativos e estimar Σ, Π e os pesos; aplicar os pesos até o rebalanceamento seguinte. |
| RF-BKT-02 | Usar dados semanais (`W-WED`), **rebalanceamento quadrimestral** (primeiro pregão de janeiro, maio e setembro) e **janela de estimação** de 3 anos, com 5 anos como robustez. |
| RF-BKT-03 | Comparar contra benchmarks: **Ibovespa (`^BVSP`)**, **CDI**, **equal-weight (1/N)**, **carteira de market cap (o próprio prior)**. |
| RF-BKT-04 | Calcular métricas: retorno acumulado, CAGR, volatilidade anualizada, **Sharpe (excesso sobre CDI)**, **máximo drawdown**. |
| RF-BKT-05 | Incorporar **custos de transação** (bps por lado sobre o turnover) e emolumentos, parametrizáveis. Sem isso o BL — que gira mais que 1/N — aparece artificialmente melhor. |
| RF-BKT-06 | **Declarar explicitamente no relatório** o tratamento do viés de sobrevivência, incluindo o resultado com e sem os ativos deslistados reconstruídos. |
| RF-BKT-07 | Gerar gráficos: curva de capital (base 100), drawdown *underwater* e evolução dos pesos ao longo do tempo. |
| RF-BKT-08 | Permitir exercícios com views de forma separada e identificada, sem substituir o backtest principal. |
| RF-BKT-09 | Análise de sensibilidade de τ e δ sobre o resultado do backtest. |
| RF-BKT-10 | Se um ativo deixar de ser negociado, vender a posição pelo último preço e manter o valor no CDI até o rebalanceamento seguinte. |

### API
| ID | Requisito |
|---|---|
| RF-API-01 | Expor o catálogo de ativos. |
| RF-API-02 | Receber ativos, parâmetros e views e devolver os pesos, as métricas e os parâmetros usados. |
| RF-API-03 | Expor os resultados documentados do estudo de backtest. |
| RF-API-04 | Devolver erros em formato padronizado e com mensagem clara. |

### Interface do usuário
| ID | Requisito |
|---|---|
| RF-UI-01 | Abrir com os 10 ativos mais líquidos e permitir editar a seleção dentro do catálogo, mantendo pelo menos 5 ativos. |
| RF-UI-02 | Configurar os parâmetros do modelo (τ, δ e restrições) com defaults sensatos. O app deve rodar sem o usuário alterar nenhum parâmetro. |
| RF-UI-03 | **Editor de views**: selecionar o ativo, escolher o tipo (absoluta/relativa), informar a contraparte e o valor esperado; listar, editar e remover views. |
| RF-UI-04 | Exibir a carteira em **tabela e gráfico**, com `w_mkt` × `w_BL` × Δ lado a lado. |
| RF-UI-05 | Exibir os **resultados do estudo de backtest**, com curva de capital e tabela de métricas contra benchmarks. |
| RF-UI-06 | Exibir as **fórmulas em LaTeX** e os parâmetros efetivamente usados. |
| RF-UI-07 | Mostrar estado de carregamento, data dos dados e alertas de qualidade. |
| RF-UI-08 | Interface em **português (pt-BR)**, com explicação de cada parâmetro. |
| RF-UI-09 | **Versão futura:** permitir uma **simulação histórica** de carteira montada no catálogo, sem views e com aviso sobre viés de seleção. |

### Acompanhamento
| ID | Requisito |
|---|---|
| RF-ACO-01 | **Opcional:** acompanhar a carteira pronta com o fechamento D-1 guardado no snapshot, informando a data dos dados. |

### Saída e documentação
| ID | Requisito |
|---|---|
| RF-DOC-01 | Exportar a carteira final em **CSV** (ticker, peso, retorno esperado, Δ contra o prior). |
| RF-DOC-02 | Exportar o **manifesto da execução** em JSON: universo, janela, τ, δ, views, Ω, fontes e datas dos dados. |
| RF-DOC-03 | Manter `docs/user_guide.md`, `docs/tutorial.md` e `docs/api_reference.md` preenchidos e versionados junto ao código. |
| RF-DOC-04 | Toda função pública deve ter **docstring** e **type hints**. |
| RF-DOC-05 | Manter relatório metodológico com fórmulas, decisões de modelagem e link para o repositório. |
| RF-DOC-06 | Documentar como obter os dados que não podem ser publicados no repositório. |

## Requisitos não funcionais
É o conjunto de restrições que o software precisa atender, sejam elas desempenho, sistema operacional, protocolo de rede etc.

| ID | Categoria | Requisito |
|---|---|---|
| RNF-01 | Plataforma | Backend em Python ≥ 3.11, com API (Flask como opção inicial). Frontend separado, inicialmente em Streamlit, podendo mudar. |
| RNF-02 | Arquitetura | Separar coleta, domínio, preparação numérica, backtest, API e frontend. O domínio usa programação orientada a objetos, e as demais camadas podem ser modulares. Domínio e preparação numérica não fazem I/O, e o frontend não importa os módulos de cálculo. |
| RNF-03 | Reprodutibilidade | Mesmos insumos devem gerar os mesmos resultados, com dependências fixadas. |
| RNF-04 | Precisão numérica | Usar `float64`, sem inversão explícita de matriz, com verificação de PSD e alerta de mau condicionamento. |
| RNF-05 | Corretude | Reproduzir um exemplo publicado do modelo com tolerância ≤ 1e-4. |
| RNF-06 | Testabilidade | Usar testes automatizados com `pytest`, com cobertura mínima de 80% em `core/`. |
| RNF-07 | Desempenho | O cálculo da carteira deve terminar em menos de 2 s, a partir do snapshot. |
| RNF-08 | Dados no servidor | O servidor não consulta fontes externas durante uma requisição. Ele usa apenas o snapshot. |
| RNF-09 | Robustez | Falhas de API externa afetam apenas a rotina, sem derrubar o app. Erros devem gerar mensagem em português. |
| RNF-10 | Usabilidade | Um usuário sem conhecimento de BL deve chegar a uma carteira válida em até 3 interações. |
| RNF-11 | Transparência | Todo parâmetro usado no cálculo deve ficar visível. |
| RNF-12 | Manutenibilidade | Seguir PEP 8, com formatação padronizada e nomes coerentes com a notação matemática. |
| RNF-13 | Versionamento | Usar Git, com código, testes e documentos em pastas separadas. |
| RNF-14 | Implantação | Publicar o backend no PythonAnywhere, sem depender do frontend escolhido. |
| RNF-15 | Legal e ético | Exibir aviso de ferramenta acadêmica, sem recomendação de investimento, e respeitar os termos das fontes. |
| RNF-16 | Observabilidade | Registrar parâmetros, fontes, tempos e avisos de cada execução. |
| RNF-17 | Portabilidade | Funcionar em Windows, Linux e macOS, sem caminhos fixos. |
| RNF-18 | Dados | Não publicar dados brutos da B3, do Yahoo ou da Bloomberg no repositório. |
