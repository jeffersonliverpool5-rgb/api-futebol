import requests

def buscar_dados():
    # Texto que será enviado para o arquivo
    mensagem = "CORINTHIANS 3 X 0 VAI CORINTHIANS !!!\n"
    mensagem += "Atualizado automaticamente via GitHub Actions."
    return mensagem

if __name__ == "__main__":
    info = buscar_dados()
    with open("apifutebol.txt", "w") as f:
        f.write(info)
    print("Arquivo atualizado!")
