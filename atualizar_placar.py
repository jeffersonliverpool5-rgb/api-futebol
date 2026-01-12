name: Atualizador de Placar

on:
  schedule:
    - cron: '0 * * * *' # Isso faz o robô rodar sozinho a cada 1 hora
  workflow_dispatch: # Isso cria o botão para você rodar na hora que quiser

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Baixar o codigo do seu repositorio
        uses: actions/checkout@v4

      - name: Configurar o Python no servidor
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Instalar bibliotecas necessarias
        run: pip install requests

      - name: Executar o script que atualiza o texto
        run: python atualizar_placar.py

      - name: Salvar as mudancas no seu arquivo txt
        run: |
          git config --global user.name 'Bot do Timao'
          git config --global user.email 'bot@github.com'
          git add apifutebol.txt
          git commit -m "Placar atualizado automaticamente" || echo "Sem alteracoes para salvar"
          git push
