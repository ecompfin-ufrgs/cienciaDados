import time

def tela_entrada():
    while True:
        print('Bem vindo ao modelo BLM \n')
        print('você pode calcular as seguintes grandezas: alfa de Jensen e beta \n')
        grandeza= input('Digite "a" para alfa , e "b" para a beta \n')

        if grandeza== 'a':
            print( '\nvocê quer calcular o alfa')
            break
        elif grandeza == 'b':
            print('\nVocê quie calculaar o beta')
            break
        elif grandeza.upper()== 'X':
            print('\nVocê pediu para encerrar. Muito obrigado por usar a nosa aplicação \n')
            break
        else :
            time.sleep(5)# NÃO FUNCIONOU POR ENQUANTO
            print( 'Voce não digitou uma alternativa válida. Tente novamente')
            
        
            
           