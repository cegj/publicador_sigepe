from modulos.config import config_json

## Obter lista de arquivos para publicar

listaDeArquivos = []

diretorioPortarias = config_json['config']['diretorio_portarias']

import os
for nomeArquivo in os.listdir(diretorioPortarias):
  if (nomeArquivo.count("~$") == 0):  
    listaDeArquivos.append(nomeArquivo)