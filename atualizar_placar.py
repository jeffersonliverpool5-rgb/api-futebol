import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

def executar():
    # Configuração de fuso horário e hora atual
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso).strftime('%H:%M')
    
    try:
        # URL da ESPN (ajuste para a seção desejada)
        url = "https://noticiasdatv.uol.com.br/canal/novelas-6"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status() # Garante que a requisição foi bem sucedida
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Busca manchetes em tags h2 e h3 com mais de 30 caracteres
        titulos = [t.get_text().strip() for t in soup.find_all(['h2', 'h3']) if len(t.get_text().strip()) > 30]
        
        if not titulos:
            texto = f"{agora} - BUSCANDO NOTICIAS..."
        else:
            # Controle de índice para o carrossel de notícias
            if not os.path.exists("indice.txt"):
                with open("indice.txt", "w") as f: 
                    f.write("0")
            
            with open("indice.txt", "r") as f:
                conteudo = f.read().strip()
                idx = int(conteudo) if conteudo.isdigit() else 0
            
            # Reseta o índice se ultrapassar a lista ou o limite de 10
            if idx >= len(titulos) or idx >= 10: 
                idx = 0
            
            # Formata o texto final e aplica .upper() para LETRAS DE FORMA
            # Você pode alterar 'CORINTHIANS' para o tema que preferir
            texto = f"{agora} - CORINTHIANS: {titulos[idx]}".upper()
            
            # Salva o próximo índice
            with open("indice.txt", "w") as f:
                f.write(str(idx + 1))
                
    except Exception as e:
        # Caso ocorra erro, salva a mensagem em maiúsculas
        texto = f"{agora} - ERRO AO ACESSAR SITE".upper()

    # Salva o resultado final no arquivo apifutebol.txt
    with open("apifutebol.txt", "w", encoding="utf-8") as f:
        f.write(texto)
        print(f"Texto gerado: {texto}")

if __name__ == "__main__":
    executar()
