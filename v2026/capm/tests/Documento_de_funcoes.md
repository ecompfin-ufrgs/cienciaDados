
# Documento de funcoes e métodos

## Módulo pipeline_io

1. pipeline_input(): [Esta função faz a leitura dos dados de entrada via API](Documento_de_algoritmo.md)
2. pipeline_output(): [Esta função faz a gravação dos dados em um arquivo csv, após concluídas todas as funções do módulo pipeline_clean](Documento_de_algoritmo.md)

## Módulo pipeline_clean

1. clean_types(): [Esta função faz a limpeza inicial dos dados, removendo dados que não sejam do tipo numérico](Documento_de_algoritmo.md)
2. clean_na(): [Esta função remove os dados faltantes](Documento_de_algoritmo.md)
3. clean_repeat(): [Esta função remove dados repetidos](Documento_de_algoritmo.md)

## Módulo mvc_model

Classe Ativo: Esta classe define um objeto para o ativo específico cujos cálculos se deseja efetuar, e que receberá os atributos necessários para efetuar os cálculos descritos no documento de requisitos. Conterá os seguintes métodos:

1. estimation(): [Esta função faz a estimação do modelo econométrico descrito no documento de requisitos](Documento_de_algoritmo.md)
2. alfa(): [Este método invoca o método estimation e seleciona o valor do alfa](Documento_de_algoritmo.md)
3. beta(): [Este método invoca o método estimation e seleciona o valor do beta](Documento_de_algoritmo.md)
4. price(): [Este método utiliza os métodos anteriores para calcular o preço estimado do ativo](Documento_de_algoritmo.md)

Funções: Complementam o módulo as seguintes funções

1. risk_return(): [Esta função retorna o rísco e o retorno da carteira ótimo](Documento_de_algoritmo.md)
