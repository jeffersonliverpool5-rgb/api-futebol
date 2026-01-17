import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

def buscar_resumo(url_materia):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url_materia, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # O Lance costuma usar a classe 'content-text' ou apenas tags <p>
        paragrafos = soup.find_all('p')
        for p in paragrafos:
            texto = p.text.strip()
            if len(texto) > 50: # Pega o primeiro parágrafo relevante
                return texto[:90] + "..." 
        return ""
    except:
        return ""

def executar():
    url_base = "https://www.lance.com.br"
    url_nfl = "https://www.lance.com.br/futebol-americano"
    headers = {'User-Agent': 'Mozilla/5.0'}
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')

    try:
        resposta = requests.get(url_nfl, headers=headers, timeout=15)
        site = BeautifulSoup(resposta.text, 'html.parser')
        
        # Coleta todas as notícias da página principal
        links = site.find_all('a', href=True)
        noticias = []
        for l in links:
            titulo = l.find(['h2', 'h3'])
            if titulo and len(titulo.text.strip()) > 30:
                href = l['href']
                url_completa = href if href.startswith('http') else url_base + href
                noticias.append({'t': titulo.text.strip(), 'u': url_completa})

        if not noticias:
            print("Nenhuma notícia encontrada.")
            return

        # Lógica de rotação (lê qual foi a última notícia exibida)
        indice_file = "indice.txt"
        idx = 0
        if os.path.exists(indice_file):
            with open(indice_file, "r") as f:
                idx = int(f.read().strip())
        
        # Reinicia se chegar no fim da lista (limitado às 10 últimas)
        if idx >= len(noticias[:10]):
            idx = 0
        
        escolhida = noticias[idx]
        resumo = buscar_resumo(escolhida['u'])
        
        # Monta a linha única para o OLED
        # Formato: [HORA] TITULO | RESUMO
        conteudo_final = f"{agora} - {escolhida['t']} | {resumo}"
        
        # Salva para o OLED ler
        with open("apifutebol.txt", "w", encoding="utf-8") as f:
            f.write(conteudo_final)
            
        # Salva o próximo índice
        with open(indice_file, "w") as f:
            f.write(str(idx + 1))

        print(f"Atualizado: {conteudo_final}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    executar()
