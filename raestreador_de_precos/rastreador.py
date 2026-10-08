
import requests
from bs4 import BeautifulSoup
import time
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

url_do_site = input("Digite a URL do seu produto: ")
produto = input("Digite o nome do produto: ")

while True:
    try:
        tempo_de_espera = int(
            input("Digite o intervalo entre verificações (em segundos): ")
        )

        if tempo_de_espera > 0:
            break

        print("O tempo deve ser maior que zero.")

    except ValueError:
        print("Digite um número inteiro válido.")

connection = None
cursor = None

try:
    connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT", "5432"))
)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id_produtos, nome, url, preco_atual, preco_anterior
        FROM produtos
        WHERE LOWER(nome) = LOWER(%s)
        AND url = %s
        ORDER BY id_produtos DESC
        LIMIT 1
    """, (produto, url_do_site))

    registro = cursor.fetchone()

    if registro:
        produto_id = registro[0]
        preco_antigo = registro[3]
        print("Preço atual registrado:", preco_antigo)
    else:
        produto_id = None
        preco_antigo = None
        print("Produto ainda não cadastrado no banco.")

    while True:
        resposta = requests.get(
            url_do_site,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")
        livros = soup.find_all("article")
        encontrou = False

        for livro in livros:
            imagem = livro.find("img")
            elemento_preco = livro.find("p", class_="price_color")

            if not imagem or not elemento_preco:
                continue

            titulo = imagem.get("alt", "").strip()

            if produto.lower() not in titulo.lower():
                continue

            encontrou = True

            texto_preco = (
                elemento_preco.get_text(strip=True)
                .replace("Â£", "")
                .replace("£", "")
                .replace(",", ".")
            )
            preco = float(texto_preco)

            print(f"\nProduto: {titulo}")
            print(f"Preço encontrado: {preco:.2f}")

            if produto_id is None:
                cursor.execute("""
                    INSERT INTO produtos
                    (nome, url, preco_atual, preco_anterior, intervalo)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_produtos
                """, (
                    titulo,
                    url_do_site,
                    preco,
                    preco,
                    tempo_de_espera
                ))

                produto_id = cursor.fetchone()[0]
                connection.commit()

                preco_antigo = preco
                print("Primeiro preço registrado no PostgreSQL.")

            else:
                if preco < preco_antigo:
                    print("O preço caiu!")
                elif preco > preco_antigo:
                    print("O preço subiu!")
                else:
                    print("O preço permaneceu igual.")

                cursor.execute("""
                    UPDATE produtos
                    SET preco_anterior = preco_atual,
                        preco_atual = %s,
                        intervalo = %s
                    WHERE id_produtos = %s
                """, (preco, tempo_de_espera, produto_id))

                connection.commit()
                preco_antigo = preco

            break

        if not encontrou:
            print("Produto não encontrado nesta página.")

        pergunta = input(
            f"Verificar novamente em {tempo_de_espera} segundos? (s/n): "
        ).strip().lower()

        if pergunta != "s":
            break

        time.sleep(tempo_de_espera)

except requests.RequestException as erro:
    print("Erro ao acessar o site:", erro)

except (ValueError, TypeError) as erro:
    print("Erro ao interpretar o preço:", erro)

except psycopg2.Error as erro:
    if connection:
        connection.rollback()
    print("Erro no PostgreSQL:", erro)

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None:
        connection.close()

print("Monitoramento encerrado.")