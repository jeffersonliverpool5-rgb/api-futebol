import requests
from bs4 import BeautifulSoup

def buscar_noticia():
    try:
        # Acessa o site do Meu Timão
        url = "https://www.meutimao.com.br/noticias-do-corinthians/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        resposta = requests.get(url, headers=headers)
        
        # Lê a página e busca o título da primeira notícia (geralmente em um h2)
        site = BeautifulSoup(resposta.text, 'html.parser')
        noticia = site.find('h2') 
        
        if noticia:
            return f"ÚLTIMA DO TIMÃO: {noticia.text.strip()}"
        else:
            return "Corinthians: Nenhuma notícia nova encontrada agora."
    except Exception as e:
        return f"Erro ao acessar o site: {e}"

if __name__ == "__main__":
    # Pega a informação do site
    texto_para_salvar = buscar_noticia()
    
    # Abre o arquivo apifutebol.txt, apaga o que tem e escreve o novo
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(texto_para_salvar)
    
    print("Sucesso: Arquivo apifutebol.txt atualizado!")
