# Elicitação de requisitos

## Sumário
1. [Requisitos funcionais](#requisitos-funcionais)
2. [Requisitos não funcionais](#requisitos-nao-funcionais)
3. [Primeira iteração - 14/09/2026 - Franco Mendes](#primeira-iteracao)
4. [Segunda iteração - 14/09/2026 - Franco Mendes](#segunda-iteracao)



## Requisitos funcionais

É o conjunto de funcionalidades que devem ser implementadas para resolver o problema do cliente.

reqfun001 - calcular o beta do modelo CAPM

reqfun002 - Calcular o alfa do modelo CAPM

## Requisitos não funcionais

É o conjunto de restrições que o software precisa atender sejam eles desempenho, sistema operacional, protocolos de rede, etc.


## Primeira iteração - 14/09/2026 - Franco Mendes

Descrição: Foram feitas duas leituras do artigo (sem, e depois com ênfase nas notas de rodapé), e após foi ouvido um "resumo em audio" feito pela inteligência artificial Notebook LM, utilizando-se o prompt abaixo:

"Faça um resumo deste artigo, enfatizando exatamente quais cálculos precisam serem feitos para que o modelo apresentado no artigo seja usado na criação de um software, com o propósito de precificar as ações da bolsa brasileira. O propósito deste resumo é auxiliar na implementação prática do modelo do artigo, e não uma discussão teórica."

Requisitos funcionais elicitados:

1. Importar os dados de preços e outros rendimentos das ações da B3. Utilizar esses dados importados para construir médias de retorno para cada ativo e seus respectivos desvios padrão.
2. Utilizar os dados anteriores para calcular os retornos esperados e desvios padrão (risco) de "todos" os possíveis portfólios de ativos
3. Definir, a partir dos dados anteriores, a curva de investimentos eficientes.
4. Definir o "ativo sem risco" e sua taxa de retorno (SELIC?).
5. A partir de 3 e 4, calcular o portfólio ótimo, seu retorno e seu risco.
6. A partir de 2 e 5, calcular os betas dos ativos
7. A partir de 5 e 6, calcular os retornos esperados dos ativos individuais, e seus valores presente (preço final estimado para o ativo)?

OBS: Os requisitos 1 e 2 exigem a definição de um horizonte de tempo, bem como de alguma restrição no número de portólios possíveis (pois esse número é teoricamente infinito).

## Segunda iteração - 15/09/2026 - Franco Mendes

Descrição: Anotação feita a partir de uma requisição do professor Nelson feita em aula.

Requisitos não funcionais elicidados:

1. O programa como um todo não pode demorar mais de 5 segundos para concluir os cálculos



