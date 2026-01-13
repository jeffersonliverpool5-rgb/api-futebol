import requests
from bs4 import BeautifulSoup

def buscar_noticia():
    try:
        # Trocamos para a Gazeta Esportiva (Seção Corinthians)
        url = "https://www.espn.com.br/futebol/time/_/id/874/corinthians"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        resposta = requests.get(url, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            site = BeautifulSoup(resposta.text, 'html.parser')
            # Na Gazeta, as notícias principais ficam em tags <h3> ou <a> dentro de títulos
            noticia = site.find('h3')
            
            if noticia:
                return f"NOTÍCIA DO TIMÃO (Gazeta): {noticia.text.strip()}"
        
        return "Erro: O servidor não conseguiu ler a notícia no momento."
        
    except Exception as e:
        return f"Erro na busca: {e}"

if __name__ == "__main__":
    texto_final = buscar_noticia()
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(texto_final)
    print("Processo finalizado com sucesso!")
