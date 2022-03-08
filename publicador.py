import sys
from modulos.Config import Config

print('----------------------------------')
print('----------------------------------')
print('PUBLICADOR DE PORTARIAS NO SIGEPE')
print('----------------------------------')
print('----------------------------------')
print()
print('*****Por Carlos E. Gaspar Jr.*****')
print('******** github.com/cegj/ ********')
print()
input('Aperte ENTER para iniciar...')

print('\n----------------------------------\n')

print('Realizando configurações iniciais...')

Config.navegador
Config.configJson

print('\nConfigurações iniciais concluídas')

print('\n----------------------------------\n')

from modulos.DadosPortarias import dadosPortarias

diretorioPortarias = configJson['config']['diretorio_arquivos']

print('O diretório de portarias é: ' + diretorioPortarias)
print('Para alterá-lo, edite config.json \n')

listaDeArquivos = dadosPortarias.obterLista(diretorioPortarias)

if (type(listaDeArquivos) is dict):

  arquivosAceitos = listaDeArquivos['arquivosAceitos']
  arquivosIgnorados = listaDeArquivos['arquivosIgnorados']

  if (len(arquivosAceitos) > 0):

    print('Lista de arquivos aceitos no diretório: \n')

    for arquivoAceito in arquivosAceitos:
      print(arquivoAceito)

    print('\n Quantidade de arquivos válidos no diretório: ', len(arquivosAceitos), 'arquivos \n')

  else:

    print('ERRO: Não houve arquivos aceitos no diretório. Verifique o formato dos arquivos.')

    input('Aperte ENTER para encerrar a aplicação...')

    sys.exit()

  if (len(arquivosIgnorados) > 0):
    print('Lista de arquivos ignorados no diretório: \n')

    for arquivoIgnorado in arquivosIgnorados:
      print(arquivoIgnorado)

    print('\n Quantidade de arquivos ignorados no diretório: ', len(arquivosIgnorados), 'arquivos \n')
    print('Os arquivos ignorados não serão publicados. Um arquivo pode ter sido ignorado por estar fora do formato .rtf ou por outros motivos que o deixem fora do padrão esperado. \n')
  
  input('**Aperte ENTER para prosseguir**')
  print()
  print('----------------------------------')
  print()

else:
  print('ERRO: Não foi possível importar a lista de arquivos. Retorno do sistema:' + listaDeArquivos)

## Fazer login no SIGEPE

from modulos.loginSigepe import Login

Login.fazerLogin()

## Preencher formulários com dados dos arquivos e publicar

import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.funcoes_publicacao import preencher
from modulos.funcoes import formatar_portaria_para_publicar, mover_arquivo, obter_texto_portaria, obter_numero_portaria, formatar_portaria_para_publicar, aguardar_loading, renomear_arquivo
 
listaPortariasPublicadas = []
listaPortariasNaoPublicadas = []
listaPortariasSemResultado = []

for nomeArquivo in listaDeArquivos:

  try:

    print()
    print('----------------------------------')

    print()

    textoPortaria = obter_texto_portaria(nomeArquivo)

    numPortaria = obter_numero_portaria(textoPortaria)

    textoPortariaFormatado = formatar_portaria_para_publicar(textoPortaria)

    preencher(textoPortaria, numPortaria, textoPortariaFormatado)

    # ENVIAR PARA PUBLICAÇÃO

    botaoGravarOrgao = wait.until(EC.element_to_be_clickable(
      (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnEnviarPublicacao"]/span')))

    botaoGravarOrgao.click()

    print(numPortaria, '- Enviando para publicação...')

    aguardar_loading()

  except:
    print("ERRO: Não foi possível publicar a portaria")

  finally:

    try:
      mensagemErro = navegador.find_element(
        By.XPATH, '//*[@id="msgCadastrarAto"]/div[2]/ul/li/span[2]')
      print(numPortaria, '- ERRO:', mensagemErro.text)
      listaPortariasNaoPublicadas.append(numPortaria + ' - ' + mensagemErro.text)
    except:
      try:
        mensagemSucesso = navegador.find_element(
          By.XPATH, '//*[@id="idFormMsg:idMensagem"]/div/ul/li/span[2]')
        print(numPortaria, '- SUCESSO:', mensagemSucesso.text)
        listaPortariasPublicadas.append(numPortaria)
        
        if (config_json['config']['adicionar_termo_nome_arquivo'] != ""):
          nomeArquivo = renomear_arquivo(nomeArquivo)
          print(numPortaria, '- Arquivo renomeado para:', nomeArquivo)

        if (config_json['config']['mover_arquivo_diretorio'] != ""):
          novoDiretorio = mover_arquivo(nomeArquivo)
          print(numPortaria, '- Arquivo movido para:', novoDiretorio)

      except:
        mensagemErro = 'Resultado não identificado! Verifique se a portaria foi publicada.'
        print(numPortaria, '- ERRO:', mensagemErro)
        listaPortariasSemResultado.append(numPortaria)
    
    navegador.get(
    "https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")

# RESULTADO DAS PUBLICAÇÕES

quantidadePortariasPublicadas = len(listaPortariasPublicadas)
quantidadePortariasNaoPublicadas = len(listaPortariasNaoPublicadas)
quantidadePortariasSemResultado = len(listaPortariasSemResultado)

print('----------------------------------')
print('----------------------------------')

print()
print("PUBLICAÇÕES CONCLUÍDAS!")

if (quantidadePortariasPublicadas > 0):
  print()
  print("Quantidade de portarias publicadas: " + str(quantidadePortariasPublicadas))
  for portaria in listaPortariasPublicadas:
    print(portaria)

if (quantidadePortariasNaoPublicadas > 0):
  print()
  print("Quantidade de portarias não publicadas: " + str(quantidadePortariasNaoPublicadas))
  for portaria in listaPortariasNaoPublicadas:
    print(portaria)

if (quantidadePortariasSemResultado > 0):
  print()
  print("Quantidade de portarias sem resultado identificado: " + str(quantidadePortariasNaoPublicadas))
  for portaria in listaPortariasSemResultado:
    print(portaria)
  print('IMPORTANTE: Verifique se as portarias sem resultado foram cadastradas para publicação no SIGEPE')
        
navegador.quit()
input('Aperte ENTER para encerrar a aplicação...')