import requests
from bs4 import BeautifulSoup

def buscar_noticia():
    try:
        url = "https://www.meutimao.com.br/noticias-do-corinthians/"
        # Este cabeçalho finge que somos um navegador Chrome no Windows
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        resposta = requests.get(url, headers=headers, timeout=10)
        
        if resposta.status_code == 200:
            site = BeautifulSoup(resposta.text, 'html.parser')
            # Tentando pegar o título da notícia principal
            noticia = site.find('h2')
            if noticia:
                return f"ÚLTIMA DO TIMÃO: {noticia.text.strip()}"
        
        return "Erro: O site bloqueou o acesso ou mudou o formato."
        
    except Exception as e:
        return f"Erro na busca: {e}"

if __name__ == "__main__":
    texto_final = buscar_noticia()
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(texto_final)
    print("Processo finalizado.")
