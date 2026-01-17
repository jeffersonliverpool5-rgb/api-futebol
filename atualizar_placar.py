import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

def executar():
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')
    
    try:
        url = "https://www.lance.com.br/futebol-americano"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Pega as manchetes
        titulos = [t.get_text().strip() for t in soup.find_all(['h2', 'h3']) if len(t.get_text().strip()) > 30]
        
        if not titulos:
            texto = f"{agora} - Buscando noticias..."
        else:
            # Carrossel: usa indice.txt para mudar a noticia
            if not os.path.exists("indice.txt"):
                with open("indice.txt", "w") as f: f.write("0")
            with open("indice.txt", "r") as f:
                idx = int(f.read().strip())
            
            if idx >= len(titulos) or idx >= 10: idx = 0
            
            texto = f"{agora} - NFL: {titulos[idx]}"
            
            with open("indice.txt", "w") as f:
                f.write(str(idx + 1))
    except:
        texto = f"{agora} - Erro ao acessar site."

    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(texto)

if __name__ == "__main__":
    executar()
