
# Documento de projetos de algoritmo

## Módulo Domain

### pipeline_init_():

Este procedimento delimita o domínio de aplicação com a criação de um objeto a partir de uma classe, neste caso serão utilizadas as classes: Ativo, Mercado e o Resultado do Modelo.

## Módulo pipeline_io

### pipeline_input():

A função não recebe nenhum argumento. A primeira linha executará uma leitura de dados via API, e armazenará a lista de dados numa variável. Em seguida, retorna esta variável como valor de saída.

### pipeline_output():

Este procedimento recebe como entrada os dados de saída da função clean_repeat(), do módulo pipeline_clean, ou seja, recebe como entrada os dados completamente pré-processados. Em seguida, executa um comando de gravação dos dados numa planilha csv, e não retorna nada como saída.

## Módulo pipeline_clean

### clean_types():

Esta função recebe como entrada a variável de saída da função pipeline_input(), do módulo pipeline_io. Em seguida, executa um loop sobre a lista de dados de entrada, verificando numa instrução if se cada elemento da lista é um dado do tipo numérico ou não. Caso o dado não seja numérico, será removido da lista. Ao final do loop, a lista resultante é definida como valor de retorno.

### clean_na():

Esta função recebe como entrada a variável de saída da função clean_types(), ou seja, recebe os dados limpos de erros de tipo. Em seguida, executa um loop sobre a lista de dados, verificando numa instrução if se cada elemento da lista é um valor faltante (na). Caso seja, o valor será removido da lista. Ao final, a lista resultante é definida como valor de retorno.

### clean_repeat():

Esta função recebe como entrada a variável de saida da função clean_na(), ou seja, recebe os dados limpos tanto de erros de tipo quanto de dados faltantes. Em seguida, executa um loop sobre a lista de dados de entrada, verificando numa instrução if se cada eemento da lista é um dados repetido de algum outro. Caso seja, será removido da lista. Ao final do loop, a lista resultante é definida como valor de retorno.

## Módulo mvc_model

### estimation():

Esta função recebe como entrada os retornos de um dos ativos (presentes na planilha csv resultante do pipeline), o retorno de mercado e o retorno livre de risco. Em seguida, implementa a estimação do modelo econométrico descrito no documento de requisitos. Após isso, armazena numa lista o alfa da estimação. Após isso, faz a mesma coisa com o beta. Por fim, define como valor de saída a lista contendo o alfa e o beta do ativo.

### price():

calcula o preço teórico do ativo

### risk_return():

calcula o risco e retorno da carteira ótima
