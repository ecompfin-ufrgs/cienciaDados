class Ativo:

    def __init__(self, ticker, nome):
        self.ticker = ticker
        self.nome = nome
            pass
   
class Mercado:

    def __init__(self, indice, descricao):
        self.indice = indice
        self.descricao = descricao
            pass

class ResultadoCAPM:

    def __init__(self,
                 alfa,
                 beta,
                 retorno_esperado):

        self.alfa = alfa
        self.beta = beta
        self.retorno_esperado = retorno_esperado
            pass 
