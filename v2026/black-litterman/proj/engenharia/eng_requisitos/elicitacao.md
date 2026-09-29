# Elicitação de requisitos 

## Requisitos do Sistema:
Para o modelo BL funcionar, são necessário algumas entradas.
1. Um modelo de Equilibrio de Mercado. Aqui seá utililado o modelo CAPM.Esse é o ponto de partida do programa, para verificar o que o mercado está sinalizando.
2. Opinião do Investidor: Aqui o investidor dará a sua opinião sobre as taxas de retorno em relação ao modelo de equilibrio do ponto 1.
3. Esta relacionado ao item 2. Aqui ele informar o seu grau de confiança em relação as suas opiniões

## Requisitos do Usuário
1. O usuário deverá ter algum conhecimento básico de mercado financeiro e de ações



   

## Requisitos funcionais
É o conjunto de funcionalidades que devem ser implementadas para resolver o problema do cliente. 
### coleta de dados
| ID | Requisito |
|---|---|
| RF-COL-01 | Baixar série histórica de preços de fechamento **ajustado** (proventos e desdobramentos) via `yfinance`, para cada ticker do universo, em janela e frequência parametrizáveis. 
| RF-COL-02 | Normalizar tickers B3 acrescentando o sufixo `.SA` e **validar a existência** do ticker antes de prosseguir; ticker inválido gera erro nomeado, não derruba a sessão. 
| RF-COL-03 | Coletar a série do **ativo livre de risco (CDI)** na API do BCB (SGS), série **12** (CDI % ao dia) — com a série **4389** (CDI a.a., base 252) como referência para anualização. 
| RF-COL-04 | Coletar **valor de mercado (market cap)** de cada ativo para construir o vetor de pesos do prior. 
| RF-COL-05 | Coletar **volume financeiro diário** (preço × quantidade) para o diagnóstico de liquidez. 
| RF-COL-06 | **Camada de cache local** (parquet/SQLite) com carimbo de data-hora e TTL, evitando redownload e protegendo contra *rate limit* do yfinance e do SGS. 
| RF-COL-07 | Tratar falha de rede/API com *retry* com *backoff*, mensagem clara ao usuário e *fallback* para o cache, informando a data do dado usado. 
| RF-COL-08 | Registrar **proveniência** de cada dado (fonte, endpoint, data de extração) e expor isso no relatório final. 
| RF-COL-09 | Obter **free float** para ajustar o market cap (relevante na B3, onde empresas com float baixo distorcem o peso de equilíbrio). 
| RF-COL-10 | Obter a **carteira teórica do Ibovespa/IBrX** da B3 como alternativa de vetor de equilíbrio. 

### tratamento e estimação
| ID | Requisito | 
|---|---|
| RF-TRA-01 | Alinhar todas as séries em um **calendário comum** (interseção de pregões), documentando a regra adotada. 
| RF-TRA-02 | Tratar dados faltantes por método aceito: *forward-fill* limitado a **N dias úteis** (default N = 5) para feriados/não-negociação; excluir do universo ativo com cobertura abaixo de um limiar — com aviso explícito ao usuário. 
| RF-TRA-03 | Construir a série de **retornos simples** `R = P_t/P_{t-1} − 1` . 
| RF-TRA-04 | Converter o CDI para a **mesma frequência** dos retornos dos ativos e construir a série de **excesso de retorno** `r_ex = r − r_f`. 
| RF-TRA-05 | Estimar a **matriz de covariância Σ** dos excessos de retorno pelo estimador amostral, com **anualização explícita** (×252 para dados diários). 
| RF-TRA-06 | Garantir que Σ seja **simétrica e positiva semidefinida**: verificar autovalores e aplicar correção para a matriz PSD mais próxima quando necessário; reportar o número de condição. 
| RF-TRA-07 | Oferecer estimador **encolhido de Ledoit-Wolf** como alternativa ao Σ amostral, e torná-lo o *default* quando `T < 10·N` (janela curta relativamente ao nº de ativos). 
| RF-TRA-08 | Oferecer estimador **EWMA** (RiskMetrics, λ = 0,94) como alternativa. 
| RF-TRA-09 | Calcular o **diagnóstico de liquidez** — volume financeiro diário mediano (ADTV) numa janela e % de pregões com negócio — e **sinalizar** (não excluir automaticamente) ativos abaixo do limiar. 
| RF-TRA-10 | Detectar e sinalizar *outliers* de retorno (ex.: retorno absoluto acima de 5σ) que sejam artefato de dado (split não ajustado), sem removê-los silenciosamente. 

### modelo BL
#### Prior de equilibrio
| ID | Requisito |
|---|---|
| RF-MOD-01 | Construir o vetor de pesos de mercado `w_mkt` por market cap **renormalizado dentro do universo** (`w_i = MC_i / Σ MC_j`).
| RF-MOD-02 | Calcular os **retornos de equilíbrio implícitos** por otimização reversa: $\Pi = \delta \, \Sigma \, w_{mkt}$, pode ser via CAPM
| RF-MOD-03 | Permitir o coeficiente de **aversão ao risco δ** de duas formas: (a) informado pelo usuário; (b) estimado por $\delta = (E[r_m] - r_f)/\sigma_m^2$ a partir do benchmark de mercado. Exibir o valor efetivamente usado. 
| RF-MOD-04 | Permitir vetor de equilíbrio alternativo (equal-weight ou carteira teórica do índice) quando o market cap for indisponível/não-confiável, **sinalizando a substituição** no relatório. 

#### visões (views)
| ID | Requisito |
|---|---|
| RF-MOD-05 | Permitir **view absoluta**: "o ativo *i* renderá q% ao ano em excesso ao CDI". Gera linha em `P` com `1` na coluna de *i*. |
| RF-MOD-06 | Permitir **view relativa**: "o ativo *i* supera o ativo *j* em q% ao ano". Gera linha em `P` com `+1` em *i* e `−1` em *j*. |
| RF-MOD-07 | Montar automaticamente a matriz `P` (k×N) e o vetor `Q` (k×1) a partir das views registradas, com **validação**: linha de view relativa deve somar 0; linha de view absoluta deve somar 1; sem views duplicadas ou linearmente dependentes. 
| RF-MOD-08 | Construir a matriz de incerteza das views **Ω**, no mínimo pelo método de He-Litterman: $\Omega = \mathrm{diag}(P\,\tau\Sigma\,P^{\top})$ — incerteza proporcional à variância do prior. 
| RF-MOD-09 | Permitir ao usuário definir **confiança por view** (0–100%) e traduzi-la em Ω (abordagem de Idzorek): confiança alta → Ω pequeno → a view domina o prior. |
| RF-MOD-10 | Expor o parâmetro **τ** com default documentado (τ = 0,05 ou τ = 1/T) e análise de sensibilidade disponível ao usuário. |
| RF-MOD-11 | Permitir view relativa **de cesta contra cesta** (grupos de ativos com pesos), não só par a par. |
| RF-MOD-12 | Exibir, antes de calcular, o **"choque implícito"** `Q − PΠ` — quanto a view diverge do que o mercado já precifica. É o que torna o modelo interpretável para o usuário. |

#### posterior
| ID | Requisito |
|---|---|
| RF-MOD-13 | Calcular o **retorno esperado posterior** pela forma numericamente estável (que evita inverter `τΣ`): $\mu_{BL} = \Pi + \tau\Sigma P^{\top}\left(P\,\tau\Sigma\,P^{\top} + \Omega\right)^{-1}(Q - P\Pi)$ |
| RF-MOD-14 | Calcular a **covariância posterior**: $M = \left[(\tau\Sigma)^{-1} + P^{\top}\Omega^{-1}P\right]^{-1}$ e $\Sigma_{BL} = \Sigma + M$; documentar se a otimização usa `Σ` ou `Σ_BL`. |
| RF-MOD-15 | **Não usar inversão explícita de matriz** (`np.linalg.inv`): resolver sistemas com `np.linalg.solve`/Cholesky. É requisito de precisão numérica, não de estilo. |
| RF-MOD-16 | Suportar o caso **k = 0 (sem views)**: o posterior deve degenerar exatamente no prior. |

| ID | Requisito |
|---|---|
| RF-MOD-17 | Calcular os **pesos ótimos** no caso irrestrito: $w^{*} = \frac{1}{\delta}\,\Sigma_{BL}^{-1}\,\mu_{BL}$. |
| RF-MOD-18 | Suportar **restrições**: soma dos pesos = 1; *long-only* (`w ≥ 0`) opcional; peso máximo por ativo (default 20%).
| RF-MOD-19 | Apresentar a **decomposição do resultado**: tabela comparando `w_mkt` (prior) × `w_BL` (posterior) × **Δ peso**, permitindo ao usuário ver o efeito isolado de cada view. |
| RF-MOD-20 | Reportar **métricas ex-ante** da carteira: retorno esperado, volatilidade, Sharpe esperado e contribuição de risco por ativo. |
| RF-MOD-21 | Tratar o caso de **otimização inviável** (restrições conflitantes) com mensagem explicativa, não com exceção crua. |

#### Backtest
| ID | Requisito |
|---|---|
| RF-BKT-01 | Executar backtest **walk-forward**: em cada data de rebalanceamento `t`, usar **exclusivamente** dados com data ≤ `t` para estimar Σ, Π e os pesos; aplicar os pesos ao período `(t, t+1]`. |
| RF-BKT-02 | Parametrizar **janela de estimação**  e **frequência de rebalanceamento** (mensal/trimestral). |
| RF-BKT-03 | Comparar contra benchmarks: **Ibovespa (`^BVSP`)**, **CDI**, **equal-weight (1/N)**, **carteira de market cap (o próprio prior)**. 
| RF-BKT-04 | Calcular métricas: retorno acumulado, CAGR, volatilidade anualizada, **Sharpe (excesso sobre CDI)**, **máximo drawdown**. 
| RF-BKT-05 | Incorporar **custos de transação** (bps por lado sobre o turnover) e emolumentos, parametrizáveis. Sem isso o BL — que gira mais que 1/N — aparece artificialmente melhor. 
| RF-BKT-06 | **Declarar explicitamente no relatório** o viés de sobrevivência: o universo foi escolhido *hoje*, logo condiciona o passado a empresas que sobreviveram.
| RF-BKT-07 | Gerar gráficos: curva de capital (base 100), drawdown *underwater* e evolução dos pesos ao longo do tempo. 
| RF-BKT-09 | Análise de sensibilidade de τ e δ sobre o resultado do backtest. 

## Requisitos não funcionais



É o conjunto de restrições que o software precisa atender sejam elas desempenho, sistema operacional, protocolo de rede et
