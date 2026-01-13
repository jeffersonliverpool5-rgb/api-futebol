import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def buscar_noticia():
    try:
        # Focamos na página que lista as notícias cronologicamente
        url = "https://www.gazetaesportiva.com/times/corinthians/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        resposta = requests.get(url, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            site = BeautifulSoup(resposta.text, 'html.parser')
            
            # Procuramos os títulos dentro da classe de "últimas notícias" ou lista
            # Tentamos primeiro o padrão de links de notícias recentes
            manchetes = site.find_all('a', class_='noticia__link')
            
            if not manchetes:
                # Caso o site mude a classe, buscamos por todos os h3 (títulos)
                manchetes = site.find_all('h3')
            
            if manchetes:
                # Pegamos a que não seja repetida ou vazia
                texto_noticia = ""
                for m in manchetes:
                    t = m.text.strip()
                    if len(t) > 10: # Garante que não é um menu ou texto curto
                        texto_noticia = t
                        break
                
                # Horário de Brasília para conferir no OLED
                fuso = pytz.timezone('America/Sao_Paulo')
                agora = datetime.now(fuso).strftime('%d/%m %H:%M')
                
                return f"{agora}\n{texto_noticia}"
        
        return "Erro: Nao foi possivel acessar as noticias."
        
    except Exception as e:
        return f"Erro na busca: {e}"

if __name__ == "__main__":
    conteudo = buscar_noticia()
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Atualizado: {conteudo}")
