import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

def buscar_resumo(url_materia):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url_materia, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Tenta pegar o primeiro parágrafo longo
        paragrafos = soup.find_all('p')
        for p in paragrafos:
            texto = p.get_text().strip()
            if len(texto) > 40:
                return texto[:80] + "..."
        return ""
    except:
        return ""

def executar():
    url_nfl = "https://www.lance.com.br/futebol-americano"
    headers = {'User-Agent': 'Mozilla/5.0'}
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')

    try:
        resposta = requests.get(url_nfl, headers=headers, timeout=15)
        site = BeautifulSoup(resposta.text, 'html.parser')
        
        # Pega todos os links que tenham títulos dentro
        tags_noticias = site.find_all('a')
        noticias = []
        
        for tag in tags_noticias:
            titulo = tag.find(['h2', 'h3'])
            link = tag.get('href')
            if titulo and link:
                texto_titulo = titulo.get_text().strip()
                if len(texto_titulo) > 25:
                    url_completa = link if link.startswith('http') else f"https://www.lance.com.br{link}"
                    noticias.append({'t': texto_titulo, 'u': url_completa})

        if not noticias:
            conteudo_final = f"{agora} - Nenhuma noticia encontrada no site."
        else:
            # Controle de índice
            if not os.path.exists("indice.txt"):
                with open("indice.txt", "w") as f: f.write("0")
            
            with open("indice.txt", "r") as f:
                idx = int(f.read().strip())
            
            if idx >= len(noticias) or idx > 10: idx = 0
            
            escolhida = noticias[idx]
            resumo = buscar_resumo(escolhida['u'])
            conteudo_final = f"{agora} - {escolhida['t']} | {resumo}"
            
            with open("indice.txt", "w") as f:
                f.write(str(idx + 1))

        with open("apifutebol.txt", "w", encoding="utf-8") as f:
            f.write(conteudo_final)
        print(f"Sucesso: {conteudo_final}")

    except Exception as e:
        with open("apifutebol.txt", "w", encoding="utf-8") as f:
            f.write(f"{agora} - Erro ao processar dados.")
        print(f"Erro: {e}")

if __name__ == "__main__":
    executar()
