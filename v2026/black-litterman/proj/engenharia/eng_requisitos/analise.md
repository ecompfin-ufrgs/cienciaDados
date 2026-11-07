# Análise de requisitos

Retirada de contradições, duplicações e dubiedades da elicitação.

Cada item registra um problema encontrado, a decisão tomada e os requisitos afetados.

**Status**

- **Decidido:** definido pela equipe.
- **Proposta:** recomendação que ainda precisa de confirmação.
- **Em aberto:** depende de conversa com o professor.

## Resumo

| ID | Tema | Status |
|---|---|---|
| A-01 | Escolha dos ativos | Decidido |
| A-02 | Tipo de retorno | Decidido |
| A-03 | Views no backtest | Decidido |
| A-04 | Market cap histórico | Decidido |
| A-05 | Carteira de mercado | Decidido |
| A-06 | Fonte do CDI | Decidido |
| A-07 | Covariância na otimização | Decidido |
| A-08 | Unidade das views | Decidido |
| A-09 | Duplicação da covariância | Decidido |
| A-10 | Número de ativos | Decidido |
| A-11 | Hospedagem | Decidido |
| A-12 | Confiança das views | Decidido |
| A-13 | Backtest no app | Decidido |
| A-14 | Fonte de dados do app | Decidido |
| A-15 | Calendário | Decidido |
| A-16 | Publicação dos dados | Decidido; Bloomberg em aberto |
| A-17 | Estimador e frequência | Decidido |
| A-18 | Acompanhamento da carteira | Decidido |
| A-19 | Paradigma de programação | Decidido |

## Universo e dados

### A-01: Escolha dos ativos

- **Status:** Decidido.
- **Problema:** a proposta diz que o usuário define o universo, mas também cita um filtro de liquidez como método de seleção.
- **Decisão:** um processo documentado seleciona os ativos por liquidez com o COTAHIST. A carteira do estudo usa os 10 ativos mais líquidos em cada data de rebalanceamento. No app, o usuário escolhe ativos dentro de um catálogo com os 30 ativos mais líquidos do ranking mais recente.
- **Justificativa:** o COTAHIST inclui papéis deslistados, o que evita survivorship bias na seleção. O catálogo limita o app a ativos com dados disponíveis e reduz a validação de dados.
- **Requisitos afetados:** seleção de ativos, RF-UI-01 e FR-UI-01.

### A-04: Market cap histórico

- **Status:** Decidido.
- **Problema:** o prior precisa do market cap em cada data do backtest, mas o yfinance só informa o valor atual.
- **Decisão:** no estudo, calcular `MC = preço bruto ON × ações ON + preço bruto PN × ações PN`. Os preços vêm do COTAHIST. A quantidade de ações vem do FRE desde 2010 e da composição do capital do ITR desde 2020. No app, usar o market cap atual.
- **Regras:**
  - Usar a última versão entregue até `t-1`, de acordo com `DT_RECEB`.
  - Manter preço e quantidade de ações na mesma base, considerando desdobramentos e grupamentos.
  - Definir o tratamento de units e de classes sem preço.
  - Ligar CNPJ, ticker e ISIN em uma tabela de-para.
- **Consequência:** a versão com fontes públicas começa em janeiro de 2011 e não cobre a crise de 2008. A cobertura de todos os ativos ainda precisa ser verificada.
- **Requisitos afetados:** RF-COL-04, FR-COL-04, RF-MOD-01 e FR-BKT-01.

### A-06: Fonte do CDI

- **Status:** Decidido.
- **Problema:** a proposta cita o Banco Central ou a B3 como fonte.
- **Decisão:** usar a série 12 do SGS, do Banco Central.
- **Justificativa:** é uma API pública e documentada.
- **Requisitos afetados:** RF-COL-03 e FR-COL-03.

### A-14: Fonte de dados do app

- **Status:** Decidido.
- **Problema:** não há confirmação de que o yfinance funciona de forma estável no PythonAnywhere, e a arquitetura deve ser enxuta.
- **Decisão:** o servidor não coleta dados. Uma rotina fora do PythonAnywhere coleta os dados e gera um snapshot com Σ, market caps, δ e fechamentos D-1. O servidor só lê esse arquivo e recorta os ativos escolhidos.
- **Justificativa:** elimina coleta ao vivo, cache e dependência de fontes externas no servidor. Também reduz as dependências instaladas no PythonAnywhere.
- **Consequências:**
  - A janela de estimação do app fica fixa em 3 anos, porque Σ é calculada antes da requisição.
  - Os dados são atualizados pela rotina, e o app sempre mostra sua data.
  - Se a rotina falhar, o app continua com o último snapshot válido.
- **Rotina:** roda inicialmente na máquina local. O envio usa a API de arquivos do PythonAnywhere, se disponível na conta gratuita, ou é feito manualmente.
- **Requisitos afetados:** RF-COL-01, RF-COL-06, RF-COL-07, FR-COL-01, FR-COL-07, FR-COL-08, RF-UI-02, RNF-08 e RNF-09.

### A-15: Calendário

- **Status:** Decidido.
- **Problema:** as séries precisam de um calendário comum. A interseção de pregões eliminaria os dados faltantes antes de medir a cobertura.
- **Decisão:** usar o calendário de dias úteis da ANBIMA como base.
- **Observações:**
  - O calendário da ANBIMA não é igual ao de pregões da B3. Até 2021, por exemplo, a B3 fechava em feriados municipais de São Paulo.
  - Nesses dias há CDI, mas não há preço. Eles seguem a regra de dados faltantes.
  - No estudo semanal, se a quarta-feira não for dia útil, usar o dia útil anterior.
- **Requisitos afetados:** RF-TRA-01, RF-TRA-02, FR-TRA-01 e FR-TRA-02.

### A-16: Publicação dos dados

- **Status:** Decidido; uso da Bloomberg em aberto.
- **Problema:** o projeto será open source, mas as fontes têm regras diferentes de uso e redistribuição.
- **Decisão:** publicar código, metodologia, instruções de coleta e resultados agregados. Não publicar dados brutos da B3, do Yahoo ou da Bloomberg. Os dados da CVM podem ser publicados, com atribuição, sob a licença ODbL.
- **Em aberto:** o uso da Bloomberg será tratado com o professor.
- **Requisitos afetados:** RNF-13, RNF-15 e estrutura de pastas do repositório.

## Modelo

### A-02: Tipo de retorno

- **Status:** Decidido.
- **Problema:** a proposta pede log-retorno como padrão, enquanto o documento de especificação usa retorno simples.
- **Decisão:** usar retorno simples.
- **Justificativa:** o retorno simples agrega corretamente entre ativos de uma carteira e evita conversões entre log-retorno e média aritmética.
- **Requisitos afetados:** RF-TRA-03 e FR-TRA-03.

### A-05: Carteira de mercado

- **Status:** Decidido.
- **Problema:** um universo pequeno de ativos não é a carteira de mercado teórica do CAPM.
- **Decisão:** usar o market cap renormalizado dentro do universo para formar `w_mkt`, com prior `Π = δΣw_mkt`.
- **Justificativa:** é a abordagem usual na literatura. Os documentos devem declarar que o universo renormalizado é uma aproximação da carteira de mercado.
- **Requisitos afetados:** RF-MOD-01, RF-MOD-02, FR-MOD-01 e FR-MOD-02.

### A-07: Covariância na otimização

- **Status:** Decidido.
- **Problema:** a otimização pode usar Σ ou `Σ_BL = Σ + M`. Σ mede a variação dos retornos. M acrescenta a incerteza sobre os retornos esperados.
- **Decisão:** usar Σ na primeira versão e maximizar `w'μ_BL - (δ/2) w'Σw`, com pesos somando 1, sem venda a descoberto e com limite de 20% por ativo.
- **Justificativa:** sem restrições e sem views, os pesos voltam exatamente a `w_mkt`. Com `Σ_BL`, o resultado seria `w_mkt/(1 + τ)`. A escolha também mantém a primeira versão mais simples.
- **Consequência:** o teste T-02 vale para o caso sem restrições. Com limite de 20%, os pesos podem diferir de `w_mkt`. `Σ_BL` pode entrar depois como comparação.
- **Requisitos afetados:** RF-MOD-14, RF-MOD-17, RF-MOD-18, FR-MOD-10 e T-02.

### A-08: Unidade das views

- **Status:** Decidido.
- **Problema:** um valor como "8%" pode significar períodos e retornos diferentes.
- **Decisão:** informar as views em % ao ano, acima do CDI, e deixar essa unidade explícita na interface.
- **Requisitos afetados:** RF-MOD-05, RF-MOD-06, FR-MOD-04, FR-MOD-05 e FR-UI-02.

### A-09: Duplicação da covariância

- **Status:** Decidido.
- **Problema:** as funções de covariância do tratamento e a estimação de Σ para o prior descrevem o mesmo requisito.
- **Decisão:** consolidar em um único requisito de estimação de Σ, usado pelas demais etapas.
- **Requisitos afetados:** RF-TRA-05 e FR-TRA-05.

### A-10: Número de ativos

- **Status:** Decidido.
- **Problema:** com pesos somando 1 e limite de 20%, uma carteira precisa de pelo menos 5 ativos.
- **Decisão:** a carteira do estudo tem 10 ativos.
- **Decisão para o app:** abrir com os 10 ativos mais líquidos e permitir que o usuário edite a seleção dentro do catálogo, mantendo pelo menos 5 ativos.
- **Requisitos afetados:** RF-MOD-18, FR-MOD-10 e FR-UI-01.

### A-12: Confiança das views

- **Status:** Decidido.
- **Problema:** a interface pede confiança, mas a fórmula de Ω não usa esse dado.
- **Decisão:** usar inicialmente a abordagem mais simples, de He-Litterman: `Ω = diag(PτΣP')`. A confiança informada pelo usuário fica para uma versão futura.
- **Consequência:** o item de confiança da elicitação, `cap2.tex` e FR-UI-02 precisam indicar que a confiança por view não faz parte da primeira versão.
- **Requisitos afetados:** RF-MOD-08, RF-MOD-09, FR-MOD-07 e FR-UI-02.

### A-17: Estimador e frequência

- **Status:** Decidido.
- **Problema:** a especificação usa dados diários e covariância amostral. O fluxo do estudo usa dados semanais e cita Ledoit-Wolf.
- **Decisão:** o estudo usa dados semanais, anualizados por 52, e rebalanceamento quadrimestral. O app usa dados diários, anualizados por 252. Os dois usam covariância amostral na primeira versão, e Ledoit-Wolf fica como teste de robustez.
- **Justificativa:** com 3 anos de dados semanais e 10 ativos, há cerca de 156 observações, acima da regra `T ≥ 10N`.
- **Requisitos afetados:** RF-TRA-05, RF-TRA-07, FR-TRA-05 e FR-BKT-02.

## Backtest e arquitetura

### A-03: Views no backtest

- **Status:** Decidido.
- **Problema:** uma view escrita hoje e aplicada ao passado gera look-ahead.
- **Decisão:** o backtest principal não usa views. Exercícios com views podem ser feitos depois, de forma separada e identificada. As carteiras de hoje aceitam views.
- **Requisitos afetados:** RF-BKT-01, RF-BKT-08 e FR-BKT-01.

### A-11: Hospedagem

- **Status:** Decidido.
- **Problema:** o Streamlit no PythonAnywhere é experimental e exige plano pago.
- **Decisão:** somente o backend roda no PythonAnywhere. O frontend é independente e consome uma API. O Streamlit é a opção inicial, mas pode mudar.
- **Consequência:** o frontend não importa os módulos de cálculo. A arquitetura precisa definir o formato das entradas e saídas da API.
- **Requisitos afetados:** RNF-01, RNF-02, RNF-14 e os requisitos não funcionais do `cap3.tex`.

### A-13: Backtest no app

- **Status:** Decidido.
- **Problema:** o ideal seria permitir uma simulação da carteira do usuário, mas isso exigiria guardar séries históricas no servidor. Como o catálogo usa os ativos líquidos de hoje, esse resultado também teria viés de seleção.
- **Decisão:** o backtest do estudo é feito e documentado, e o app mostra seus resultados. A simulação de uma carteira montada no catálogo fica fora da primeira versão.
- **Justificativa:** mantém a arquitetura enxuta, de acordo com a decisão A-14.
- **Consequência:** `backtest/engine.py` recebe dados em um formato fixo, sem depender da fonte. Isso permite retomar a simulação em uma versão futura.
- **Requisitos afetados:** RF-BKT-01 a RF-BKT-09, RF-UI-05, RF-UI-09, FR-BKT-01 a FR-BKT-05 e FR-UI-03.

### A-18: Acompanhamento da carteira

- **Status:** Decidido.
- **Problema:** a equipe quer acompanhar a carteira depois de pronta, mas o escopo inicial excluía dados em tempo real.
- **Decisão:** incluir, como recurso opcional, um acompanhamento diário com o fechamento do dia útil anterior (D-1). A rotina diária coleta e guarda esse dado no snapshot. O servidor só lê o resultado. A fonte candidata é a brapi.
- **Justificativa:** uma rotina evita coletar dados durante o acesso do usuário. Como a conta gratuita do PythonAnywhere usada no projeto não tem tarefas agendadas, a rotina roda fora do servidor.
- **Limites do plano gratuito da brapi:** 15.000 requisições por mês, 1 ativo por requisição, atraso de cerca de 30 minutos e histórico de até 3 meses. Uma atualização diária de 30 ativos usa cerca de 630 requisições por mês, mas a brapi gratuita não substitui os dados históricos.
- **Requisitos afetados:** RF-ACO-01, FR-UI-04 e RNF-08.

### A-19: Paradigma de programação

- **Status:** Decidido.
- **Problema:** a arquitetura precisava definir como organizar o código do modelo e das demais camadas.
- **Decisão:** o domínio da aplicação usa programação orientada a objetos. As demais camadas podem seguir programação modular.
- **Justificativa:** classes reúnem os conceitos e validações do modelo. Funções mantêm simples a coleta, a preparação e a execução.
- **Requisitos afetados:** RNF-02 e arquitetura do projeto.
