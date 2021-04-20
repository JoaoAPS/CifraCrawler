# Cifra Crawler

Um web crawler simples que salva todas as cifras de um artista presentes no [Cifra Club](https://www.cifraclub.com.br/) como arquivos .txt.

Implementado usando [Scrapy](https://scrapy.org/).


## Instalação

1. Clone o repositório e entre nele
2. Instale o pacote [pipenv](https://pypi.org/project/pipenv/): `pip install pipenv`
3. Instale as dependências: `pipenv install`


## Uso

Na pasta do projeto rode

``` python
pipenv run scrapy crawl cifras -a artist="<artista>"
```

Substituindo `<artista>` pelo nome do artista desejado.
Tente usar a forma slug presente no Cifra Club.

Uma pasta deve aparecer em `output/<artista>` contendo as cifras.
