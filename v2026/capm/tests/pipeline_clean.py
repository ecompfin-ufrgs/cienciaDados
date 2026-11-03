
def clean_types(vetor):
  testar_tipo = np.frompyfunc(lambda x: isinstance(x, (int, float, np.int64, np.float64)), 1, 1)
  mascara = testar_tipo(vetor).astype(bool)
  vetor_filtrado = vetor[mascara]
  return vetor_filtrado

def clean_na(data: list) -> list:
    pass

def clean_repeat(data: list) -> list:
    pass

