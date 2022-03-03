class dadosPortarias:

  def obterLista(diretorioPortarias):

    try:

      listaDeArquivos = {
        'arquivosAceitos': [],
        'arquivosIgnorados': []
      }

      import os

      for nomeArquivo in os.listdir(diretorioPortarias):
        if (nomeArquivo.count("~") == 0 and nomeArquivo.count(".rtf") > 0):  
          listaDeArquivos['arquivosAceitos'].append(nomeArquivo)
        else:
          listaDeArquivos['arquivosIgnorados'].append(nomeArquivo)

      return listaDeArquivos

    except Exception as e:
      
      return repr(e)