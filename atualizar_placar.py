import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

def executar():
    # Define o fuso horário de Brasília
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')
    
    try:
        url = "https://www.lance.com.br/futebol-americano"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Filtra títulos que tenham mais de 35 letras (manchetes reais)
        noticias = [t.get_text().strip() for t in soup.find_all(['h2', 'h3']) if len(t.get_text().strip()) > 35]
        
        if not noticias:
            final = f"{agora} - Sem noticias novas no site."
        else:
            # Gerencia qual noticia exibir (0, 1, 2...)
            if not os.path.exists("indice.txt"):
                with open("indice.txt", "w") as f: f.write("0")
            
            with open("indice.txt", "r") as f:
                idx = int(f.read().strip())
            
            # Se chegar ao fim das 10 primeiras, volta ao começo
            if idx >= len(noticias) or idx >= 10: idx = 0
            
            final = f"{agora} - {noticias[idx]}"
            
            # Salva o próximo índice para a próxima execução
            with open("indice.txt", "w") as f:
                f.write(str(idx + 1))
    except:
        final = f"{agora} - Erro ao acessar o site."

    # Escreve a linha única no arquivo que o seu OLED consome
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(final)

if __name__ == "__main__":
    executar()
