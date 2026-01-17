import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

def executar():
    # Configuração de Hora para Brasília
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')
    
    try:
        url = "https://www.lance.com.br/futebol-americano"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        resposta = requests.get(url, headers=headers, timeout=15)
        site = BeautifulSoup(resposta.text, 'html.parser')
        
        # Procura as manchetes (filtramos títulos com mais de 30 caracteres para evitar lixo)
        manchetes = [m.get_text().strip() for m in site.find_all(['h2', 'h3']) if len(m.get_text().strip()) > 30]
        
        if not manchetes:
            conteudo = f"{agora} - Buscando novas noticias..."
        else:
            # Lógica do carrossel: lê o índice atual para saber qual notícia mostrar
            indice_file = "indice.txt"
            idx = 0
            if os.path.exists(indice_file):
                with open(indice_file, "r") as f:
                    try:
                        idx = int(f.read().strip())
                    except:
                        idx = 0
            
            # Se chegar ao fim da lista (limitado às 10 primeiras), volta ao início
            if idx >= len(manchetes) or idx >= 10:
                idx = 0
            
            # Define a notícia da vez
            noticia_escolhida = manchetes[idx]
            conteudo = f"{agora} - {noticia_escolhida}"
            
            # Salva o próximo índice para a próxima execução (daqui a 3h)
            with open(indice_file, "w") as f:
                f.write(str(idx + 1))
        
    except Exception as e:
        conteudo = f"{agora} - Erro na conexao."

    # Salva o arquivo final que o seu display OLED vai ler
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Postado no arquivo: {conteudo}")

if __name__ == "__main__":
    executar()
