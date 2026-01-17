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
        # Procura o primeiro parágrafo com conteúdo real
        paragrafos = soup.find_all('p')
        for p in paragrafos:
            texto = p.get_text().strip()
            if len(texto) > 50:
                # Retorna os primeiros 80 caracteres para caber no display
                return texto[:80] + "..." 
        return "Resumo indisponivel."
    except:
        return "Erro ao ler artigo."

def executar():
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')
    
    try:
        url_base = "https://www.lance.com.br"
        url_nfl = "https://www.lance.com.br/futebol-americano"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        res = requests.get(url_nfl, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Coleta links de noticias reais
        links_noticias = []
        for a in soup.find_all('a', href=True):
            titulo = a.find(['h2', 'h3'])
            if titulo and len(titulo.get_text().strip()) > 30:
                link = a['href']
                url_materia = link if link.startswith('http') else url_base + link
                links_noticias.append({'t': titulo.get_text().strip(), 'u': url_materia})

        if not links_noticias:
            final = f"{agora} - Buscando novas noticias..."
        else:
            # Controle de rotacao (Carrossel)
            indice_file = "indice.txt"
            idx = 0
            if os.path.exists(indice_file):
                with open(indice_file, "r") as f:
                    try: idx = int(f.read().strip())
                    except: idx = 0
            
            # Garante que mude para a proxima noticia
            if idx >= len(links_noticias) or idx >= 10: idx = 0
            
            escolhida = links_noticias[idx]
            # Busca o texto dentro da materia
            resumo = buscar_texto_interno(escolhida['u'])
            
            final = f"{agora} - {escolhida['t']} | {resumo}"
            
            # Salva o proximo indice para o proximo disparo
            with open(indice_file, "w") as f:
                f.write(str(idx + 1))
                
    except Exception as e:
        final = f"{agora} - Erro de conexao."

    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(final)
    print(f"Atualizado: {final}")

if __name__ == "__main__":
    executar()
