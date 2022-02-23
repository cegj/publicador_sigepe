from modulos.config import config_json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.lista_arquivos import diretorioPortarias
import datetime 
from datetime import timedelta
from selenium.webdriver.support.ui import WebDriverWait
from modulos.config import navegador
import os
import shutil

#define valor das variaveis de data

today = datetime.date.today() #Hoje no formato ANSI AAAA-MM-DD
tomorrow = today + timedelta(1) #Amanhã no formato ANSI AAAA-MM-DD

#Define das funções utilizadas pela aplicação

##Obter o TEXTO DA PORTARIA a partir de arquivo RTF

def obter_texto_portaria(nomeArquivo):
  from striprtf.striprtf import rtf_to_text

  with open(str(diretorioPortarias) + str(nomeArquivo), encoding='cp1252') as arquivo:
    conteudo = arquivo.read()
    portaria = rtf_to_text(conteudo)
    arquivo.close()

  return portaria

##Obter o NÚMERO DA PORTARIA a partir do texto da portaria

def obter_numero_portaria(textoPortaria):

  A = textoPortaria.split(config_json['delimitadores']['numero_portaria'][0], 1)

  B = A[1].split(config_json['delimitadores']['numero_portaria'][1], 1)

  numPortaria = B[0]

  return numPortaria

##Obter SIAPE a partir do texto da portaria

def obter_siape(textoPortaria):
  textoPortariaSplit = textoPortaria.split(config_json['delimitadores']['siape'][0], 1)
  matriculaSiape = textoPortariaSplit[1].split(config_json['delimitadores']['siape'][1], 1)
  matriculaSiape = matriculaSiape[0]

  return matriculaSiape
    
##Obter tema e nível do assunto a partir do texto da portaria e config.json

def obter_tema(textoPortaria): 
    for key in config_json['temas_assuntos']:
        if (textoPortaria.count(key) > 0):         
            temaBgp = config_json['temas_assuntos'][key]['tema_bgp']
            nivelAssuntoBgp = config_json['temas_assuntos'][key]['nivel_assunto_bgp']
            temaArrowDown = config_json['temas_assuntos'][key]['arrow_down']
            temaAssunto = {'tema': temaBgp, 'nivel_assunto': nivelAssuntoBgp, 'arrow_down': temaArrowDown}

            return temaAssunto
            break

##Limpar quebras de linha

def limpar_quebras_linha(string):
    string = string.replace("\n", "") # Apagar quebras de linha
    return string

##Formatar o texto da portaria para publicação (remover cabeçalho, quebras de linha etc)

def formatar_portaria_para_publicar(textoPortaria):

  from modulos.publicador.valores_configurados import dataAssinatura

  if (config_json['delimitadores']['cabecalho'][1] == "var_ano_assinatura"):
    anoAssinatura = (dataAssinatura.split('/'))
    anoAssinatura = anoAssinatura[2]
    fimCabecalho = anoAssinatura
  else:
    fimCabecalho = config_json['delimitadores']['cabecalho'][1]  

  textoPortaria = limpar_quebras_linha(textoPortaria)

  textoPortariaSemCabecalho = textoPortaria.split(str(fimCabecalho), 1) #Remover cabeçalho (usa ano como limite)
  
  textoPortariaSemCabecalho = textoPortariaSemCabecalho[1] #Descarta o cabeçalho, fica só com o que vem depois do ano

  textoPortariaSemCabecalho = textoPortariaSemCabecalho.split(config_json['delimitadores']['preliminar_portaria'][1], 1) #Separa o texto em dois, antes e depois do dois-pontos do cabeçalho

  textoPreliminarPortaria = textoPortariaSemCabecalho[0] + config_json['delimitadores']['preliminar_portaria'][1] #Define parte de cima do texto da portaria

  textoNormativoPortaria = textoPortariaSemCabecalho[1] #Define parte de baixo do texto da portaria

  textoPortaria = [textoPreliminarPortaria, textoNormativoPortaria] ##Parte preliminar, índice 0, parte normativa, índice 1

  return textoPortaria

#Receber a data no formato AAAA-MM-DD e converte para DD/MM/AAAA
def ajusta_data(data, separador): 
  dataArray = str(data).split('-')
  dataAjustada = dataArray[2] + separador + dataArray[1] + separador + dataArray[0]
  data = str(dataAjustada)
  return data

##Verificar se a data será de hoje, amanhã ou data explícita informada no config.json

def verifica_data(tipoData): #Parâmetros: 'data_assinatura' ou 'data_publicacao'
  if (config_json['valores'][tipoData] == '[hoje]'):
    return ajusta_data(today, '/')
  elif (config_json['valores'][tipoData] == '[amanha]'):
    if (tomorrow.weekday() == 5): #5 = sábado
      return ajusta_data(tomorrow + timedelta(2), '/')
    elif (tomorrow.weekday() == 6): #6 = domingo
      return ajusta_data(tomorrow + timedelta(1), '/')
    else:
      return ajusta_data(tomorrow, '/')
  else:
    return config_json['valores'][tipoData]

##Verifica se elemento está presente na página

def verifica_elemento(termo_busca):
    try:
        termo_busca
        return True
    except:
        return False

def aguardar_loading():
    modalAguarde = WebDriverWait(navegador, 300).until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

def renomear_arquivo(nomeArquivoCompleto):
  nomeArquivoArray = nomeArquivoCompleto.split('.', 1)
  nomeArquivo = nomeArquivoArray[0]
  extensaoArquivo = str('.' + nomeArquivoArray[1])
  diretorio = config_json['config']['diretorio_arquivos']
  termoNomeArquivo = config_json['config']['adicionar_termo_nome_arquivo']
  novoNomeArquivoCompleto = str(nomeArquivo + " " + termoNomeArquivo + extensaoArquivo)

  file_oldname = os.path.join(diretorio, nomeArquivoCompleto)
  file_newname_newfile = os.path.join(diretorio, novoNomeArquivoCompleto)

  os.rename(file_oldname, file_newname_newfile)

  return novoNomeArquivoCompleto

def mover_arquivo(nomeArquivo):

  diretorioAtual = config_json['config']['diretorio_arquivos']
  diretorioDestino = config_json['config']['mover_arquivo_diretorio']

  if (diretorioDestino.find('[hoje, .]')):
    diretorioDestino.replace('[hoje, .]', ajusta_data(today, '.'))
  elif (diretorioDestino.find('[hoje, /]')):
    diretorioDestino.replace('[hoje, /]', ajusta_data(today, '/'))
  elif (diretorioDestino.find('[hoje, -]')):
    diretorioDestino.replace('[hoje, -]', ajusta_data(today, '-'))

  origem = str(diretorioAtual + nomeArquivo)
  destino = str(diretorioDestino + nomeArquivo)

  shutil.move(origem,destino)

  return diretorioDestino

  