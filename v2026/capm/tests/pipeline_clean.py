
def clean_types(vetor):
    testar_tipo = np.frompyfunc(lambda x: isinstance(x, (int, float, np.int64, np.float64)), 1, 1)
    mascara = testar_tipo(vetor).astype(bool)
    vetor_filtrado = vetor[mascara]
    return vetor_filtrado

def clean_na(data):
    """
    Esta função remove dados no formato numpy.nan, enquanto dados no formato None são automaticamente removidos pela
    função anterior.
    """
    testar_na = np.frompyfunc(lambda x: np.isnan(x), 1, 1)
    mascara = ~testar_na(data).astype(bool)
    vetor_filtrado = data[mascara]
    return vetor_filtrado

def clean_repeat(data: list) -> list:
    pass

