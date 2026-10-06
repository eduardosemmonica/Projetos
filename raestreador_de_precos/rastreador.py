import requests
from bs4 import BeautifulSoup

url_do_site = input("Digite a URL do seu produto: ")

resposta = requests.get(url_do_site)

soup = BeautifulSoup(resposta.text, "html.parser")

livros = soup.find_all("article")

produto = input("Digite o nome do produto: ")

encontrou = False

for livro in livros:
    titulo = livro.find("a").find("img")["alt"]
    preco = livro.find("p", {"class": "price_color"}).text

    if produto.lower() in titulo.lower():
        encontrou = True
        print(titulo, preco)

if not encontrou:
    print("Produto não encontrado.")