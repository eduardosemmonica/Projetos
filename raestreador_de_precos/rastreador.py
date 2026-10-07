import requests
from bs4 import BeautifulSoup
import time

url_do_site = input("Digite a URL do seu produto: ")


produto = input("Digite o nome do produto: ")

while True:

    tempo_de_espera = int(input("Digite o tempo de espera entre as verificações (em segundos): "))

    if tempo_de_espera > 0:
        break

    else:
        print("O tempo de espera deve ser maior que zero. Tente novamente.")

        
while True:
    resposta = requests.get(url_do_site)
    soup = BeautifulSoup(resposta.text, "html.parser")

    livros = soup.find_all("article")
    encontrou = False

    for livro in livros:
        titulo = livro.find("a").find("img")["alt"]
        preco = float(livro.find("p", {"class": "price_color"}).text.replace("Â£", ""))

        if produto.lower() in titulo.lower():
            encontrou = True
            print(titulo, preco)

            try:
                arquivo = open("preco.txt", "r")
                preco_antigo = float(arquivo.read())
                arquivo.close()

                if preco < preco_antigo:
                    print("O preço do produto caiu! Novo preço:", preco)

                elif preco > preco_antigo:
                    print("O preço do produto subiu! Novo preço:", preco)

                else:
                    print("O preço do produto permaneceu o mesmo.")

            except:
                print("Primeiro preço registrado:", preco)

            arquivo = open("preco.txt", "w")
            arquivo.write(str(preco))
            arquivo.close()

    if not encontrou:
        print("Produto não encontrado.")

    time.sleep(tempo_de_espera)

    sair = input("Deseja sair? (s/n): ").lower()

    if sair == "s":
        break