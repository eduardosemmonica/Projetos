import random

CARACTERES_PADRAO = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+"


def gerar_senha(variavel_senha="", quantidade_de_caracteres=0):
    if variavel_senha == "":
        escolha_usuario = input(
            "Digite 1 para usar os caracteres padrão ou 2 para escrever os seus: "
        ).strip()

        if escolha_usuario == "1":
            variavel_senha = CARACTERES_PADRAO
        elif escolha_usuario == "2":
            variavel_senha = input("Digite os caracteres que deseja usar: ").strip()
            while variavel_senha == "":
                print("Digite pelo menos um caractere.")
                variavel_senha = input("Digite os caracteres que deseja usar: ").strip()
        else:
            print("Escolha inválida. Digite 1 ou 2.")
            return gerar_senha("", quantidade_de_caracteres)

    while quantidade_de_caracteres <= 0:
        try:
            quantidade_de_caracteres = int(
                input("Digite a quantidade de caracteres que deseja na senha: ")
            )
            if quantidade_de_caracteres <= 0:
                print("A quantidade de caracteres deve ser maior que zero.")
        except ValueError:
            print("Digite um número válido.")

    senha = ""
    for _ in range(quantidade_de_caracteres):
        senha += random.choice(variavel_senha)

    return senha


if __name__ == "__main__":
    senha_gerada = gerar_senha()
    print(senha_gerada)