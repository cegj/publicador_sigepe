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
print()
print('----------------------------------')
print()
print('Realizando configurações iniciais...')

from modulos.config import *

print('Configurações iniciais concluídas')

print()
print('----------------------------------')
print()

from modulos.lista_arquivos import diretorioPortarias, listaDeArquivos

print('O diretório de portarias é: ', diretorioPortarias)
print('Para alterá-lo, edite config.json')
print()
print('Lista de arquivos no diretório:')
for arquivo in listaDeArquivos:
  if ".rtf" in arquivo:
    print(arquivo)
  else:
    print('ATENÇÃO: Formato incorreto, converta para RTF antes de continuar: ' + arquivo)
print()
print('Quantidade de arquivos válidos no diretório: ', len(listaDeArquivos), 'arquivos')
print()
input('**Aperte ENTER para prosseguir**')
print()
print('----------------------------------')
print()

## Fazer login no SIGEPE

from modulos.login_sigepe import fazer_login_sigepe

fazer_login_sigepe()

print()
print('----------------------------------')
print()

## Preencher formulários com dados dos arquivos e publicar

import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.publicador import preencher
from modulos.funcoes import formatar_portaria_para_publicar, obter_texto_portaria, obter_numero_portaria, formatar_portaria_para_publicar
 
listaPortariasPublicadas = []
listaPortariasNaoPublicadas = []
listaPortariasSemResultado = []

for nomeArquivo in listaDeArquivos:

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

  modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

  try:
    mensagemErro = halfwait.until(EC.visibility_of_element_located(
      (By.XPATH, '//*[@id="msgCadastrarAto"]/div[2]/ul/li/span[2]')))
    print(numPortaria, '- ERRO:', mensagemErro.text)
    listaPortariasNaoPublicadas.append(numPortaria)
  except:
    try:
      mensagemSucesso = navegador.find_element(
      By.XPATH, '//*[@id="idFormMsg:idMensagem"]/div/ul/li/span[2]')
      print(numPortaria, '- SUCESSO:', mensagemSucesso.text)
      listaPortariasPublicadas.append(numPortaria)
      time.sleep(0.3)
    except:
       mensagemErro = 'Resultado não identificado! Verifique se a portaria foi publicada.'
       print(numPortaria, '- ERRO:', mensagemErro.text)
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
  for portaria in quantidadePortariasSemResultado:
    print(portaria)
  print('IMPORTANTE: Verifique se as portarias sem resultado foram cadastradas para publicação no SIGEPE')
        
navegador.quit()
input('Aperte ENTER para encerrar a aplicação...')