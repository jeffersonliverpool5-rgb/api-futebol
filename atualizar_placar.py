import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import time

def buscar_conteudo_materia(url_materia):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url_materia, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Tenta encontrar o primeiro parágrafo da notícia
        paragrafo = soup.find('p')
        if paragrafo:
            texto = paragrafo.text.strip()
            return (texto[:100] + '...') if len(texto) > 100 else texto
        return "Conteúdo indisponível."
    except:
        return "Erro ao ler matéria."

def rodar_noticias():
    url_base = "https://www.lance.com.br"
    url_nfl = "https://www.lance.com.br/futebol-americano"
    headers = {'User-Agent': 'Mozilla/5.0'}
    fuso = pytz.timezone('America/Sao_Paulo')

    print("Iniciando carrossel de notícias... (Ctrl+C para parar)")

    while True:
        try:
            resposta = requests.get(url_nfl, headers=headers, timeout=15)
            site = BeautifulSoup(resposta.text, 'html.parser')
            
            # Busca os links das matérias
            cards = site.find_all('a', href=True)
            noticias_encontradas = []

            for card in cards:
                titulo = card.find(['h2', 'h3'])
                link = card['href']
                if titulo and len(titulo.text.strip()) > 30:
                    url_completa = link if link.startswith('http') else url_base + link
                    noticias_encontradas.append({
                        'titulo': titulo.text.strip(),
                        'url': url_completa
                    })

            # Agora percorre cada notícia encontrada
            for item in noticias_encontradas[:5]: # Pega as 5 últimas
                agora = datetime.now(fuso).strftime('%H:%M')
                resumo = buscar_conteudo_materia(item['url'])
                
                # Formata a linha única para o OLED
                conteudo_final = f"{agora} - {item['titulo']} | {resumo}"
                
                with open("apifutebol.txt", "w", encoding="utf-8") as f:
                    f.write(conteudo_final)
                
                print(f"Exibindo agora: {item['titulo']}")
                
                # Tempo de espera antes de mudar para a próxima notícia (ex: 20 segundos)
                time.sleep(20) 

        except Exception as e:
            print(f"Erro no loop: {e}")
            time.sleep(60) # Espera um minuto se der erro de conexão

if __name__ == "__main__":
    rodar_noticias()
