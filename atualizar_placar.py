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
        
        # Pega as manchetes do site
        manchetes = [t.get_text().strip() for t in soup.find_all(['h2', 'h3']) if len(t.get_text().strip()) > 30]
        
        if not manchetes:
            final = f"{agora} - Buscando noticias da NFL..."
        else:
            # Lógica para mudar a notícia a cada 3 horas
            indice_file = "indice.txt"
            idx = 0
            if os.path.exists(indice_file):
                with open(indice_file, "r") as f:
                    try: idx = int(f.read().strip())
                    except: idx = 0
            
            if idx >= len(manchetes) or idx >= 10: idx = 0
            
            final = f"{agora} - NFL: {manchetes[idx]}"
            
            with open(indice_file, "w") as f:
                f.write(str(idx + 1))
    except:
        final = f"{agora} - Erro ao carregar site do Lance."

    # ESCREVE NO ARQUIVO DA FOTO
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(final)

if __name__ == "__main__":
    executar()
