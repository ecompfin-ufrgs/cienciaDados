
# Documento de projetos de algoritmo

## Módulo Domain

### pipeline_init_():

A função é construtora da classe, é executada automaticamente no momento da criação de um objeto, inicializa os atributos do objeto com os valores fornecidos na instanciação.

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

### class ativo

Esta classe defini um objeto para o ativo selecionado, que receberá os seguintes atributos:

1. ticker: o código do ativo
2. ri: a lista com as rentabilidades do ativo em um determinado período
3. rm: a lista com as rentabilidades de mercado durante o mesmo período
4. rf: a lista com as rentabilidades do ativo livre de risco durante o mesmo período

### estimation(): 

Implementa algum método de estimação, para estimar a equação econométrica descrita no documento de requisitos. Retorna como saída uma lista, contendo dois valores, respectivamente o alfa e o beta do ativo.

### alfa():

Este método tem como objetivo apenas simplificar a seleção do coeficiente alfa do modelo. Desse modo, o algoritmo apenas invoca o método estimation() e seleciona o valor alfa, ou seja, o primeiro valor da lista que estimation() retorna como saída. Esse valor alfa é a saída do método alfa().

### beta():

Este método, assim como o anterior, tem como objetivo apenas simplificar a seleção do coeficiente beta do modelo. Desse modo, o algoritmo apenas invoca o método estimation() e seleciona o valor beta, ou seja, o segundo valor da lista que estimation() retorna como saída. Esse valor beta é a saída do método beta().

### price():

calcula o preço teórico do ativo, a partir dos valores de alfa e beta obtidos na estimação. O algoritmo consiste em aplicar o seguinte cálculo:

P = Pi*( (ri - rf) + rf) + Pi

onde:

P = Preço final estimado do ativo.
Pi = Preço inicial do ativo.
(ri - rf) = A resposta do ativo à variação da rentabilidade de mercado, obtido a partir do modelo de sharpe.
rf = A rentabilidade do ativo livre de risco.

Importante lembrar que os valores precisam estar ajustados aos prazos que se está trablahando. Por exemplo, se estamos considerando variação diária, mas temos apenas os dados de rentabilidade anual do ativo livre de risco, precisamos calcular o equivalente diário dessa taxa.

### risk_return():

Esta função recebe como entrada um valor alfa (NÃO é o mesmo alfa do método estimation() da classe ativo), que representa a parcela do capital que o usuário pretende investir em ativos livres de rísco, e retorna como saída uma lista contendo a rentabilidade esperada da carteira ótima de mercado e o rísco esperado da carteira ótima de mercado. Os valores serão computados segundo as fórmnulas abaixo (extraídas do artigo de Sharpe):

Rentabilidade esperada = alfa*(rentabilidade sem rísco) + (1 - alfa)*(rentabilidade de mercado)

Rísco esperado = (1 - alfa)*(Desvio padrão da rentabilidade de mercado)

