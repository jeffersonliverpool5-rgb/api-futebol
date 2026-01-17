import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

def executar():
    url_nfl = "https://www.lance.com.br/futebol-americano"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')

    try:
        resposta = requests.get(url_nfl, headers=headers, timeout=15)
        site = BeautifulSoup(resposta.text, 'html.parser')
        
        # Pega os títulos das notícias (h2 ou h3)
        manchetes = site.find_all(['h2', 'h3'])
        
        lista_noticias = []
        for m in manchetes:
            texto = m.get_text().strip()
            # Filtra apenas textos que pareçam manchetes reais
            if len(texto) > 35 and "Últimas notícias" not in texto:
                lista_noticias.append(texto)

        if not lista_noticias:
            conteudo = f"{agora} - Sem noticias novas no momento."
        else:
            # Lógica para rotacionar a notícia a cada execução
            indice_file = "indice.txt"
            idx = 0
            if os.path.exists(indice_file):
                with open(indice_file, "r") as f:
                    try:
                        idx = int(f.read().strip())
                    except:
                        idx = 0
            
            # Se chegar no fim da lista (ou passar de 10), volta ao início
            if idx >= len(lista_noticias) or idx >= 10:
                idx = 0
            
            noticia_escolhida = lista_noticias[idx]
            conteudo = f"{agora} - {noticia_escolhida}"
            
            # Salva o próximo índice para a próxima rodada
            with open(indice_file, "w") as f:
                f.write(str(idx + 1))

        # Salva o arquivo que o seu OLED lê
        with open("apifutebol.txt", "w", encoding="utf-8") as f:
            f.write(conteudo)
            
        print(f"Postado: {conteudo}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    executar()
