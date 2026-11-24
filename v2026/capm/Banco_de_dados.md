# Documento de Requisitos
### Autor: Rachel Silveira Adolpho
### Data: 24-11-2026
### Versão: 0.0.1

## Introdução e visão geral do sistema

Este é um documento de resuisitos para armazenar os dados de uma agenda de telefones 
e endereços de uma pessoa


## Dados

Deverão ser armazenados dados de nomes dos contatos da pessoa, 
bem como de seus respectivos endereços, email e telefones tal como
descritos a seguir:

**contato** - prenome, nome do meio, sobrenome
**endereço** - logradouro, nome do logradouro, número, complemento, CEP, municipalidade,
estado/província** (pode ficar em branco), pais
**email** - tem que conter o caracter @
**telefone** - código numérico de país, código numérico de área, número de telefone

Note que uma pessoa pode ter mais de um endeço, telefone e email,
bem como pode compartilhar estes dados com outra pessoa, posto que pode ter pessoas
que moram juntas ou compartilham o telefone. O objetico da agenda telefônica é facilitar o controle
dos contatos da pessoa.

## Operações com os dados

As operções a seguir podem ser realizadas com todos os dados:

- Inclusão
- Consulta
- Update
- Remoção
