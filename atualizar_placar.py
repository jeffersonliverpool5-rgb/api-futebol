import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import random

def buscar_noticia_variada():
    try:
        url = "https://www.lance.com.br/corinthians"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        resposta = requests.get(url, headers=headers, timeout=15)
        fuso = pytz.timezone('America/Sao_Paulo')
        agora = datetime.now(fuso).strftime('%H:%M')

        if resposta.status_code == 200:
            site = BeautifulSoup(resposta.text, 'html.parser')
            
            # Pega todos os títulos de notícias
            manchetes = site.find_all(['h3', 'h2'])
            
            # Filtra apenas notícias reais (textos longos e sem ser propaganda)
            lista_noticias = []
            for m in manchetes:
                texto = m.text.strip()
                if len(texto) > 35 and "Últimas notícias" not in texto:
                    lista_noticias.append(texto)
            
            if lista_noticias:
                # Escolhe uma notícia aleatória da lista das 10 primeiras
                # Assim, a cada 3 horas, a chance de mudar no seu OLED é gigante
                noticia_escolhida = random.choice(lista_noticias[:10])
                return f"{agora} - {noticia_escolhida}"
        
        return f"{agora} - Sem noticias novas."
        
    except Exception as e:
        return f"{agora} - Erro na busca."

if __name__ == "__main__":
    conteudo = buscar_noticia_variada()
    
    # Salva em uma única linha para facilitar a leitura no seu display OLED
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Postado no arquivo: {conteudo}")
