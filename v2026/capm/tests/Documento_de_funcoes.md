
# Documento de funcoes e métodos

## Módeulo init
1. pipeline_init(): [Esta função cria uma classe, é executada automaticamente no momento da criação de um objeto](Documento_de_algoritmo.md)

## Módulo pipeline_io
1. pipeline_input(): [Esta função faz a leitura dos dados de entrada via API](Documento_de_algoritmo.md)
2. pipeline_output(): [Esta função faz a gravação dos dados em um arquivo csv, após concluídas todas as funções do módulo pipeline_clean](Documento_de_algoritmo.md)

## Módulo pipeline_clean

1. clean_types(): [Esta função faz a limpeza inicial dos dados, removendo dados que não sejam do tipo numérico](Documento_de_algoritmo.md)
2. clean_na(): [Esta função remove os dados faltantes](Documento_de_algoritmo.md)
3. clean_repeat(): [Esta função remove dados repetidos](Documento_de_algoritmo.md)

## Módulo mvc_model

1. estimation(): [Esta função faz a estimação do modelo econométrico descrito no documento de requisitos](Documento_de_algoritmo.md)
2. price(): [Esta função calcula o preço teórico do ativo](Documento_de_algoritmo.md)
3. risk_return(): [Esta função calcula o risco e o retorno da carteira ótima](Documento_de_algoritmo.md)
