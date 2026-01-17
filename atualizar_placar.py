import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

def buscar_texto_interno(url_materia):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url_materia, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Procura o primeiro parágrafo longo dentro da matéria
        paragrafos = soup.find_all('p')
        for p in paragrafos:
            texto = p.get_text().strip()
            if len(texto) > 50:
                return texto[:100] + "..." # Pega os primeiros 100 caracteres do artigo
        return ""
    except:
        return ""

def executar():
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')
    
    try:
        url_base = "https://www.lance.com.br"
        url_nfl = "https://www.lance.com.br/futebol-americano"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        res = requests.get(url_nfl, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Busca links que contêm títulos (h2 ou h3)
        links_noticias = []
        for a in soup.find_all('a', href=True):
            titulo = a.find(['h2', 'h3'])
            if titulo and len(titulo.get_text().strip()) > 30:
                url_materia = a['href']
                if not url_materia.startswith('http'):
                    url_materia = url_base + url_materia
                links_noticias.append({'titulo': titulo.get_text().strip(), 'url': url_materia})

        if not links_noticias:
            final = f"{agora} - Sem notícias novas."
        else:
            # Lógica de Carrossel (Garante que mude a cada execução)
            indice_file = "indice.txt"
            idx = 0
            if os.path.exists(indice_file):
                with open(indice_file, "r") as f:
                    try: idx = int(f.read().strip())
                    except: idx = 0
            
            # Se chegar ao fim da lista, volta ao começo
            if idx >= len(links_noticias) or idx >= 8: idx = 0
            
            noticia_atual = links_noticias[idx]
            # ENTRA NO ARTIGO PARA PEGAR O TEXTO
            resumo_interno = buscar_texto_interno(noticia_atual['url'])
            
            # Monta a linha para o seu OLED
            final = f"{agora} - {noticia_atual['titulo']} | {resumo_interno}"
            
            # Salva o próximo índice para o próximo disparo ser uma notícia diferente
            with open(indice_file, "w") as f:
                f.write(str(idx + 1))
    except:
        final = f"{agora} - Erro ao processar notícias."

    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(final)

if __name__ == "__main__":
    executar()
