import requests
from bs4 import BeautifulSoup

def buscar_noticia():
    try:
        # Acessa o site do Meu Timão
        url = "https://www.meutimao.com.br/noticias-do-corinthians/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers)
        
        # Lê a página e pega o título da primeira notícia
        site = BeautifulSoup(resposta.text, 'html.parser')
        noticia = site.find('h2') 
        
        if noticia:
            return f"NOTÍCIA DO TIMÃO: {noticia.text.strip()}"
        else:
            return "Nenhuma notícia encontrada agora."
    except:
        return "Erro ao acessar o site do Meu Timão."

if __name__ == "__main__":
    texto = buscar_noticia()
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(texto)
