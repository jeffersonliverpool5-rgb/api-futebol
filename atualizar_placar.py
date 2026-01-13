import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def buscar_noticia():
    try:
        url = "https://www.lance.com.br/corinthians"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        resposta = requests.get(url, headers=headers, timeout=15)
        fuso = pytz.timezone('America/Sao_Paulo')
        agora = datetime.now(fuso).strftime('%d/%m %H:%M')

        if resposta.status_code == 200:
            site = BeautifulSoup(resposta.text, 'html.parser')
            
            # Procuramos por títulos que geralmente são as notícias reais
            # Ele vai tentar encontrar manchetes em h3 ou h2 que sejam grandes
            manchetes = site.find_all(['h3', 'h2'])
            
            for m in manchetes:
                texto = m.text.strip()
                # Se o texto for pequeno ou for o aviso de "últimas notícias", ele pula
                if len(texto) > 30 and "Últimas notícias" not in texto:
                    return f"{agora}\n{texto}"
        
        return f"{agora}\nSem noticias novas no momento."
        
    except Exception as e:
        return f"{agora}\nErro: {str(e)[:20]}"

if __name__ == "__main__":
    conteudo = buscar_noticia()
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("Atualizado!")
