import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

def executar():
    # Configuração de Hora
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')
    
    try:
        url = "https://www.lance.com.br/futebol-americano"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        resposta = requests.get(url, headers=headers, timeout=15)
        site = BeautifulSoup(resposta.text, 'html.parser')
        
        # Busca todas as manchetes
        manchetes = [m.get_text().strip() for m in site.find_all(['h2', 'h3']) if len(m.get_text().strip()) > 30]
        
        if not manchetes:
            conteudo = f"{agora} - Buscando noticias..."
        else:
            # Lógica para alternar as notícias (Carrossel)
            indice_file = "indice.txt"
            idx = 0
            if os.path.exists(indice_file):
                with open(indice_file, "r") as f:
                    try: idx = int(f.read().strip())
                    except: idx = 0
            
            # Se chegar ao fim das 10 primeiras, volta ao zero
            if idx >= len(manchetes) or idx >= 10:
                idx = 0
            
            conteudo = f"{agora} - {manchetes[idx]}"
            
            # Salva o próximo índice
            with open(indice_file, "w") as f:
                f.write(str(idx + 1))
        
    except Exception as e:
        conteudo = f"{agora} - Erro: {str(e)[:20]}"

    # Salva o arquivo para o OLED
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Salvo: {conteudo}")

if __name__ == "__main__":
    executar()
