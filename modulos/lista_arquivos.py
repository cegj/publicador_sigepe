import sys
from modulos.config import config_json

## Obter lista de arquivos para publicar

listaDeArquivos = []

try:

  diretorioPortarias = config_json['config']['diretorio_arquivos']

  import os
  for nomeArquivo in os.listdir(diretorioPortarias):
    if (nomeArquivo.count("~") == 0):  
      listaDeArquivos.append(nomeArquivo)

except KeyError:
  print('A chave diretorio_arquivos não foi encontrada em config.json. Verifique e tente novamente.')
  input('Aperte ENTER para encerrar a aplicação...')
  sys.exit()