
# Manipulação de Dados

O objetivo é criar uma timeline de compras a partir dos eventos disponíveis neste endpoint: https://storage.googleapis.com/dito-questions/events.json. Onde evento representa um comportamento de uma pessoa, seja no mundo online ou offline. Quando uma pessoa faz uma compra, um evento comprou é gerado contendo o total de receita gerada e o nome da loja. Para cada produto dessa compra é gerado um evento comprou-produto, contendo o nome e preço do
produto.

A implementação foi realizada em python devida às boas ferramentas de manipulação que a linguagem fornece.

## Para rodar

### Pré-requisitos

 - Python 3.7+

### Preparação do ambiente

Essas instruções instruirão como obter uma cópia do projeto e executá-lo na sua máquina local para fins de desenvolvimento e teste.

 - Clonar o repositório
 
 - Criar o ambiente virtual
 ```
virtualenv venv
```
Caso virtualenv não esteja instalado, será necessário, primeiramente, instalá-lo
 ```
pip install virtualenv
```

 - Ativar o ambiente virtual
 ```
venv\Scripts\activate (para Windows)
```

 - Instalar as dependências
  ```
pip install -r requirements.txt
```

### Rodando

Pode-se passar a url com os dados de entrada como parâmetro:

```
python event_manipulation.py https://storage.googleapis.com/dito-questions/events.json
```

Ou rodar com a url padrão, que é https://storage.googleapis.com/dito-questions/events.json:

```
python event_manipulation.py
```

## Running the tests

```
pytest
```
