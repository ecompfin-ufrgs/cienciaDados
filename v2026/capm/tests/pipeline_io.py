
def pipeline_input(matriz):
  primeira_coluna = matriz[:,0]
  return primeira_coluna

def pipeline_output(data):
    with open('dados.csv', 'w') as dados:
        dados.write('Valores\n')
        for i in range(len(data)):
            dados.write(f'{data[i]}\n')

