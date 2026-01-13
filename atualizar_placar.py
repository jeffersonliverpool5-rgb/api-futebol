import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def buscar_noticia():
    try:
        # Site da Gazeta Esportiva (Seção Corinthians)
        url = "https://www.gazetaesportiva.com/times/corinthians/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        resposta = requests.get(url, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            site = BeautifulSoup(resposta.text, 'html.parser')
            # Busca todos os títulos (h3)
            manchetes = site.find_all('h3')
            
            if manchetes:
                # Pega a primeira notícia da lista
                texto_noticia = manchetes[0].text.strip()
                
                # Pega o horário de Brasília para o seu OLED
                fuso = pytz.timezone('America/Sao_Paulo')
                agora = datetime.now(fuso).strftime('%d/%m %H:%M')
                
                return f"{agora}\n{texto_noticia}"
        
        return "Erro: Nao foi possivel ler o site."
        
    except Exception as e:
        return f"Erro na busca: {e}"

if __name__ == "__main__":
    conteudo = buscar_noticia()
    # Salva no arquivo que o seu ESP32 lê
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Atualizado: {conteudo}")
