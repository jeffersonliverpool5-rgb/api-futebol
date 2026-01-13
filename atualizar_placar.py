import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def buscar_noticia():
    try:
        # Mudamos para o LANCE! (Seção Corinthians) - mais fácil de ler
        url = "https://www.lance.com.br/corinthians"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        resposta = requests.get(url, headers=headers, timeout=15)
        fuso = pytz.timezone('America/Sao_Paulo')
        agora = datetime.now(fuso).strftime('%d/%m %H:%M')

        if resposta.status_code == 200:
            site = BeautifulSoup(resposta.text, 'html.parser')
            
            # No Lance!, as notícias ficam em h2 ou h3 dentro de cartões
            noticia = site.find('h2')
            
            if noticia:
                return f"{agora}\n{noticia.text.strip()}"
        
        return f"{agora}\nErro: Site nao respondeu."
        
    except Exception as e:
        return f"{agora}\nErro na busca: {str(e)[:20]}"

if __name__ == "__main__":
    conteudo = buscar_noticia()
    # Grava o resultado (nunca deixará em branco agora)
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("Arquivo atualizado!")
