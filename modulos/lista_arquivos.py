import sys
from modulos.config import config_json

## Obter lista de arquivos para publicar

listaDeArquivos = []

try:

  diretorioPortarias = config_json['config']['diretorio_arquivos']
  diretorioDestino = config_json['config']['mover_arquivo_diretorio']

  import os
  for nomeArquivo in os.listdir(diretorioPortarias):
    if (nomeArquivo.count("~") == 0):  
      listaDeArquivos.append(nomeArquivo)

except KeyError:
  print('A chave diretorio_arquivos e/ou mover_arquivo_diretorio não foi encontrada em config.json. Verifique e tente novamente.')
  input('Aperte ENTER para encerrar a aplicação...')
  sys.exit()