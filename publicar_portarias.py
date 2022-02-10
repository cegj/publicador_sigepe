print('----------------------------------')
print('----------------------------------')
print('PUBLICADOR DE PORTARIAS NO SIGEPE')
print('----------------------------------')
print('----------------------------------')
print()
print('*****Por Carlos E. Gaspar Jr.*****')
print('******** github.com/cegj/ ********')
print()

## Configurar webdriver e definir funções

#Lê o arquivo de configurações config.json

print()
print('------------------------------------')
print()
print('Realizando configurações iniciais...')

import json

with open('config.json', 'r', encoding="utf-8") as config_json:
    config_json = json.load(config_json)
    
#Configura o webdriver

import selenium

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

import datetime 

from datetime import timedelta

import getpass

import time

#Define os tempos de espera

halfwait = WebDriverWait(navegador, 10)
wait = WebDriverWait(navegador, 20)
longwait = WebDriverWait(navegador, 40)

print('Webdriver configurado e navegador aberto')

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

##Formatar o texto da portaria para publicação (remover cabeçalho, quebras de linha etc)

def formatar_portaria_para_publicar(textoPortaria):

  if (config_json['delimitadores']['cabecalho'][1] == "var_ano_assinatura"):
    anoAssinatura = (dataAssinatura.split('/'))
    anoAssinatura = anoAssinatura[2]
    fimCabecalho = anoAssinatura
  else:
    fimCabecalho = config_json['delimitadores']['cabecalho'][1]  

  textoPortaria = textoPortaria.replace("\n", "") # Apagar quebras de linha

  textoPortariaSemCabecalho = textoPortaria.split(str(fimCabecalho), 1) #Remover cabeçalho (usa ano como limite)
  
  textoPortariaSemCabecalho = textoPortariaSemCabecalho[1] #Descarta o cabeçalho, fica só com o que vem depois do ano

  textoPortariaSemCabecalho = textoPortariaSemCabecalho.split(config_json['delimitadores']['preliminar_portaria'][1], 1) #Separa o texto em dois, antes e depois do dois-pontos do cabeçalho

  textoPreliminarPortaria = textoPortariaSemCabecalho[0] + config_json['delimitadores']['cabecalho'][1] #Define parte de cima do texto da portaria

  textoNormativoPortaria = textoPortariaSemCabecalho[1] #Define parte de baixo do texto da portaria

  textoPortaria = [textoPreliminarPortaria, textoNormativoPortaria] ##Parte preliminar, índice 0, parte normativa, índice 1

  return textoPortaria

#Receber a data no formato AAAA-MM-DD e converte para DD/MM/AAAA
def ajusta_data(data): 
  dataArray = str(data).split('-')
  dataAjustada = dataArray[2] + '/' + dataArray[1] + '/' + dataArray[0]
  data = str(dataAjustada)
  return data

##Verificar se a data será de hoje, amanhã ou data explícita informada no config.json

def verifica_data(tipoData): #Parâmetros: 'data_assinatura' ou 'data_publicacao'
  today = datetime.date.today() #Hoje no formato AAAA-MM-DD
  tomorrow = today + timedelta(1) #Amanhã no formato AAAA-MM-DD
  if (config_json['valores'][tipoData] == 'hoje'):
    return ajusta_data(today)
  elif (config_json['valores'][tipoData] == 'amanha'):
    if (tomorrow.weekday() == 5): #5 = sábado
      return ajusta_data(tomorrow + timedelta(2))
    elif (tomorrow.weekday() == 6): #6 = domingo
      return ajusta_data(tomorrow + timedelta(1))
    else:
      return ajusta_data(tomorrow)
  else:
    return config_json['valores'][tipoData]

##Verifica se elemento está presente na página

def verifica_elemento(termo_busca):
    try:
        termo_busca
        return True
    except:
        return False

print()
print('------------------------------------')
print()

## Obter lista de arquivos para publicar

listaDeArquivos = []

diretorioPortarias = config_json['config']['diretorio_portarias']

print('O diretório de portarias é: ', diretorioPortarias)
print('Para alterá-lo, edite config.json')

import os
for nomeArquivo in os.listdir(diretorioPortarias):
    if (nomeArquivo.count("~$") == 0):  
         listaDeArquivos.append(nomeArquivo)

print()
print('Lista de arquivos no diretório:')
for arquivo in listaDeArquivos:
  if ".rtf" in arquivo:
    print(arquivo)
  else:
    print('****** ATENÇÃO: Formato incorreto, converta para RTF antes de continuar: ' + arquivo)
print()
print('Quantidade de arquivos válidos no diretório: ', len(listaDeArquivos), 'arquivos')
print()

print()
print('------------------------------------')
print()

input('**Aperte ENTER para prosseguir**')

print()
print('------------------------------------')
print()
## Fazer login no SIGEPE

navegador.get("https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf");

print('Acessando a página de login do SIGEPE...')

usuario = input('CPF do usuário (somente números): ')

senha = getpass.getpass('Senha do SIGEPE: ')

campoUsuario = navegador.find_element(By.XPATH, '//*[@id="cpfUsuario"]');

campoUsuario.click();

campoUsuario.send_keys(usuario);

campoSenha = navegador.find_element(By.XPATH, '//*[@id="password"]');

campoSenha.click();

campoSenha.send_keys(senha);

botaoAcessar = navegador.find_element(By.XPATH, '//*[@id="botaoCredenciais"]');

botaoAcessar.click();

print('Fazendo login no Sigepe...')

try:
    erroLogin = halfwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="msg_alerta"]')));
    print('ERRO: ', erroLogin.text)
    print('Reinicie e tente novamente')
    navegador.quit()
except:
    nomePaginaPublicacao = halfwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="barra-infos"]/div[3]/div')));
    print('Página acessada: ', nomePaginaPublicacao.text)
    print()

print()
print('------------------------------------')
print()

## Preencher formulários com dados dos arquivos e publicar

listaPortariasPublicadas = []
listaPortariasNaoPublicadas = []
listaPortariasSemResultado = []

##Verifica e exibe para o usuário as informações de config.json

##Define data Assinatura

dataAssinatura = verifica_data('data_assinatura')

##Define data Publicação

dataPublicacao = verifica_data('data_publicacao')

##Define órgão, UORG, UPAG e autoridade

dadoIncorreto = False

if (config_json['valores']['edicao_bgp'] == "Normal" or config_json['valores']['edicao_bgp'] == "Extraordinária"):
    edicaoBGP = config_json['valores']['edicao_bgp']
else:
    edicaoBGP = '*** Tipo de edição',config_json['valores']['edicao_bgp'],'inválido. O valor deve ser "Normal" ou "Extraordinário"'
    dadoIncorreto = True

if (config_json['valores']['tipo_assinatura'] == "Manual") or (config_json['valores']['tipo_assinatura'] == "Digital"):
    tipoAssinatura = config_json['valores']['tipo_assinatura']
else:
    tipoAssinatura = '*** Tipo de assinatura',config_json['valores']['tipo_assinatura'],'inválido. O valor deve ser "Manual" ou "Digital"'
    dadoIncorreto = True

especie = config_json['valores']['especie']
tipoNumero = config_json['valores']['tipo_preenchimento']
orgao = config_json['valores']['orgao']
upag = config_json['valores']['upag']
uorg = config_json['valores']['uorg']
responsavelAssinatura = config_json['valores']['responsavel_assinatura']
cargoResponsavelAssinatura = config_json['valores']['cargo_responsavel']

print()
print('VALORES CONFIGURADOS:')
print()
print('Edição do BGP: ', edicaoBGP)
print('TIpo de assinatura:', tipoAssinatura)
print('Espécie:', especie)
print('Tipo de preenchimento do número: ', tipoNumero)
print('Data de assinatura (emissão): ', dataAssinatura)
print('Data de publicação: ', dataPublicacao)
print('Órgão: ', orgao)
print('UPAG: ', upag)
print('UORG: ', uorg)
print('Responsável pela assinatura: ', responsavelAssinatura)
print('Cargo do responsável pela assinatura: ', cargoResponsavelAssinatura)
print('Para alterá-los, edite config.json e reinicie a aplicação')
print()
if (dadoIncorreto == True):
    print('Há dados inválidos em config.json. Corrija e inicie novamente')
    navegador.quit()
    print('Sessão encerrada')
else:
    print('------------------------------------')
    input('****Aperte ENTER para para iniciar publicação das portarias****')

##Inicia o processo de preenchimento e publicação das portarias

for nomeArquivo in listaDeArquivos:

    print()
    print('------------------------------------')
    print()

    textoPortaria = obter_texto_portaria(nomeArquivo)

    numPortaria = obter_numero_portaria(textoPortaria)
    
    textoPortariaFormatado = formatar_portaria_para_publicar(textoPortaria)
    
    print(numPortaria, '- Iniciando cadastro da portaria...')
    
    print(textoPortariaFormatado[0])
    print(textoPortariaFormatado[1])
    
    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
    
    ##Tipo de assinatura (manual)
    
    tipoAssinaturaDigital = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:radTipoAssinatura"]/tbody/tr/td[2]/label')));
    tipoAssinaturaManual = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:radTipoAssinatura"]/tbody/tr/td[4]/label')));
    
    if (tipoAssinatura == "Manual"):
        tipoAssinaturaManual.click()
    elif (tipoAssinatura == "Digital"):
        tipoAssinaturaDigital.click();
    
    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
    
    print(numPortaria, '- Tipo assinatura selecionado:', tipoAssinatura)
    
    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

    ##Espécie (portaria)
    
    campoEspecie = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selEspecie_label"]')));
        
    campoEspecie.click();

    time.sleep(0.3)
        
    campoBuscarEspecie = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selEspecie_filter"]')));

    campoBuscarEspecie.send_keys(especie)

    time.sleep(1)

    campoBuscarEspecie.send_keys(Keys.ENTER)

    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
        
    print(numPortaria, '- Espécie selecionada: ', campoEspecie.text)
    
    ##Tipo de preenchimento do número
    
    campoTipoNumero = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTipoPreenchimento_label"]')));
        
    campoTipoNumero.click();
    
    time.sleep(0.3)
        
    campoBuscarTipoNumero = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTipoPreenchimento_filter"]')));

    campoBuscarTipoNumero.send_keys(tipoNumero)

    time.sleep(1)

    campoBuscarTipoNumero.send_keys(Keys.ENTER)

    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
            
    print(numPortaria, '- Tipo de preenchimento do número selecionado: ', campoTipoNumero.text)
        
    ##Tema
    
    if (obter_tema(textoPortariaFormatado[1])):
        temaAssunto = obter_tema(textoPortariaFormatado[1])
    else:
        print('!!!TEMA NÃO IDENTIFICADO!!!')
        
    campoTema = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_label"]')));
        
    campoTema.click();

    time.sleep(0.3)
        
    campoBuscarTema = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_filter"]')));        
        
    campoBuscarTema.send_keys(temaAssunto['tema'])

    time.sleep(1)
    
    if (temaAssunto['arrow_down'] > 0):
        cont = 1
        while cont <= temaAssunto['arrow_down']:
            campoBuscarTema.send_keys(Keys.ARROW_DOWN)
            cont = cont + 1        

    campoBuscarTema.send_keys(Keys.ENTER)

    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
    
    campoTemaPreenchido = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_label"]')));
    
    print(numPortaria, '- Tema selecionado: ', campoTemaPreenchido.text)
    
        
    ####################
        
    #campoTema = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_label"]'))); 
    
    #campoTema.click();

    #time.sleep(0.3)

    #opcaoCampoTema.click();

    #modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
    
    #campoTemaPreenchido = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_label"]')));

    #print(numPortaria, '- Tema selecionado: ', campoTemaPreenchido.text)

    ##Assunto
    
    time.sleep(0.3)
    
    botaoProcurarAssunto = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnSelecionarClassificacaoAssunto"]')));
    
    botaoProcurarAssunto.click();
        
    janelaSelecionarAssunto = wait.until(EC.element_to_be_clickable((By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:idDlgSelecionarAssunto')));

    time.sleep(0.3)
    
    navegador.execute_script("document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:treeClassificacao_selection').setAttribute('type', 'text');");

    time.sleep(0.3)
    
    campoNivelTemaOculto = wait.until(EC.element_to_be_clickable((By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:treeClassificacao_selection')));
        
    campoNivelTemaOculto.send_keys(temaAssunto['nivel_assunto'])
    
    time.sleep(0.3)
    
    botaoSelecionarAssunto = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnSelecionar"]/span')));
    
    botaoSelecionarAssunto.click();
    
    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
        
    campoAssuntoPreenchido = wait.until(EC.element_to_be_clickable((By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:txtClassificacao')));
    
    print(numPortaria, '- Assunto selecionado: ', campoAssuntoPreenchido.get_attribute("value"))
    
    time.sleep(0.3)
    
    #if (verifica_elemento("wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id='messagesBox']')))")):
    #    botaoFecharAlerta = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="msgCadastrarAto"]/div/a/span')));
    #    botaoFecharAlerta.click();    
    
    ##Número do ato
    
    campoNumeroAto = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNumeroAto"]')));
    
    campoNumeroAto.send_keys(str(numPortaria));
    
    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

    print(numPortaria, '- Número do ato preenchido')
    
    ##Data de assinatura
    
    if (tipoAssinatura == "Manual"):
    
        campoDataAssinatura = wait.until(EC.element_to_be_clickable((By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataAssinatura_input')));
    
        cont = 1
        while cont <= 8:
            campoDataAssinatura.send_keys(Keys.BACKSPACE)
            cont = cont + 1

        campoDataAssinatura.send_keys(dataAssinatura)
        
        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

        print(numPortaria, '- Data de assinatura preenchida: ', dataAssinatura)
    
    else:
        print(numPortaria, '- Tipo de assinatura é digital. Data de assinatura não é preenchida.') 
        
    ##Data de publicação
        
    campoDataPublicacao = wait.until(EC.element_to_be_clickable((By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataParaPublicacao_input')));

    campoDataPublicacao.click();
    
    cont = 1
    while cont <= 8:
        campoDataPublicacao.send_keys(Keys.BACKSPACE)
        cont = cont + 1
        
    campoDataPublicacao.send_keys(dataPublicacao)
    
    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

    print(numPortaria, '- Data da publicação preenchida: ', dataPublicacao)
    
    ##Texto da portaria (iframe)
        
    navegador.switch_to.frame(0);
        
    campoTextoPortaria = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'body')));
    
    campoTextoPortaria.click();
    
    time.sleep(0.3)

    campoTextoPortaria.send_keys(textoPortariaFormatado[1]);

    time.sleep(0.3)
            
    campoTextoPortaria.send_keys(Keys.ENTER);
    
    time.sleep(0.3)
        
    campoTextoPortaria.send_keys(textoPortariaFormatado[0]);
    
    time.sleep(0.3)
    
    navegador.switch_to.default_content()
    
    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

    print(numPortaria, '- Texto da portaria preenchido')

    ##Órgãos elaboradores

    print(numPortaria, '- Iniciando preenchimento do órgão/autoridade...')
            
    #####Há dois modelos de janela para selecionar uorg/upag/autoridade no SIGEPE
    
    try: ##Gatilho para modelo novo é o XPATH do botão para abrir janela, pois são diferentes
        botaoIncluirOrgaoElabAnt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt395"]/span')));

        print(numPortaria, '- [obs:] Cadastro pelo modelo antigo de janela')

        botaoIncluirOrgaoElabAnt.click()

        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

        campoUpag = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadePagadora_label"]'))); 
            
        campoUpag.click();

        time.sleep(0.3)
        
        campoBuscarUpag = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadePagadora_filter"]')));
    
        campoBuscarUpag.send_keys(upag)

        time.sleep(1)

        campoBuscarUpag.send_keys(Keys.ENTER)

        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
        
        print(numPortaria, '- UPAG preenchida: ', campoUpag.text)
        
        time.sleep(0.3)
                
        campoUorg = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadeOrganizacional_label"]')));
        
        campoUorg.click();

        time.sleep(0.3)
        
        campoBuscarUorg = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadeOrganizacional_filter"]')));        
        
        campoBuscarUorg.send_keys(uorg)

        time.sleep(1)

        campoBuscarUorg.send_keys(Keys.ENTER)

        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

        print(numPortaria, '- UORG preenchido: ', campoUorg.text)
        
        campoResponsavelAssinatura = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNomeResponsavel"]')));
            
        campoResponsavelAssinatura.send_keys(responsavelAssinatura);
                
        campoCargoResponsavelAssinatura = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptCargoResponsavel"]')));
        
        campoCargoResponsavelAssinatura.send_keys(cargoResponsavelAssinatura);
                
        botaoGravarOrgao = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt699"]/span')));
                
        botaoGravarOrgao.click();
        
        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
    
    except:
        botaoIncluirOrgaoElab = navegador.find_element(By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt396"]');

        print(numPortaria, '- [obs:] Cadastro pelo novo modelo de janela')

        botaoIncluirOrgaoElab.click()

        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

        janelaOrgaosElaboradores = wait.until(EC.element_to_be_clickable((By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:dlgIncluirOrgaoElaborador')));
        
        campoUpag = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt446_label"]')));
    
        campoUpag.click();

        time.sleep(0.3)
        
        campoBuscarUpag = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt446_filter"]')));

        campoBuscarUpag.send_keys(upag)

        time.sleep(1)

        campoBuscarUpag.send_keys(Keys.ENTER)

        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
        
        print(numPortaria, '- UPAG preenchida: ', campoUpag.text)
                
        campoUorg = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt453_label"]')));
      
        campoUorg.click();

        time.sleep(0.3)
        
        campoBuscarUorg = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt453_filter"]')));

        campoBuscarUorg.send_keys(uorg)

        time.sleep(1)

        campoBuscarUorg.send_keys(Keys.ENTER)
        
        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

        print(numPortaria, '- UORG preenchido: ', campoUorg.text)
        
        campoResponsavelAssinatura = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt463"]')));
        
        campoResponsavelAssinatura.send_keys(responsavelAssinatura)
        
        botaoPesquisarAutoridade = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt492"]/span')));
        
        botaoPesquisarAutoridade.click()

        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
        
        radiusSelecionarAutoridade = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt494:dataTableResultado_data"]/tr/td[1]/div/div/div[2]/span')));

        radiusSelecionarAutoridade.click()

        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

        botaoSelecionarAutoridade = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt538"]/span')));

        botaoSelecionarAutoridade.click()

        modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
        
    responsavelAssinaturaSelecionado = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:tblResponsaveis:0:j_idt416:txtContent"]')));

    CargoResponsavelAssinaturaSelecionado = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:tblResponsaveis:0:j_idt418:txtContent"]')));
        
    print(numPortaria, '- Responsável pela assinatura preenchido: ', responsavelAssinaturaSelecionado.text, " - ", CargoResponsavelAssinaturaSelecionado.text)
    
    ##Interessado

    siapeInteressado = obter_siape(textoPortaria)

    print(numPortaria, '- Interessado identificado: ', siapeInteressado)
    print('Iniciando busca e preenchimento do interessado...')
    
    botaoAbrirInteressados = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt1415"]/span')));
    
    botaoAbrirInteressados.click();

    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

    campoMatricula = wait.until(EC.element_to_be_clickable((By.ID,  'frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt434:j_idt466')));
        
    campoMatricula.click();

    time.sleep(0.2)

    campoMatricula.send_keys(str(siapeInteressado));

    botaoPesquisarInteressado = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt492"]/span')));
    
    botaoPesquisarInteressado.click();

    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

    checkboxSelecionarServidor = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt494:dataTableResultado:j_idt499"]/div/div/div[2]')));
    
    checkboxSelecionarServidor.click();

    ####Função .click() do Selenium não está funcionando nessos botões abaixo. Usando Javascript:

    time.sleep(0.3)
    
    navegador.execute_script("botaoIncluirServidor = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt494:j_idt517');");
    
    navegador.execute_script("botaoIncluirServidor.click();");

    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

    botaoSelecionarServidor = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt538"]/span')));
    
    navegador.execute_script("botaoSelecionarServidor = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt538');");
    
    navegador.execute_script("botaoSelecionarServidor.click();");
    
    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));

    nomeServidorCadastrado = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:tblInteressados:0:j_idt1427:txtContent"]')));
    
    print(numPortaria, '- Servidor interessado cadastrado: ', str(siapeInteressado), '-', nomeServidorCadastrado.text)
    
    ##ENVIAR PARA PUBLICAÇÃO
    
    botaoGravarOrgao = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnEnviarPublicacao"]/span')));
        
    botaoGravarOrgao.click();

    print(numPortaria, '- Enviando para publicação...')
    
    modalAguarde = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')));
        
    try:
        mensagemErro = halfwait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="msgCadastrarAto"]/div[2]/ul/li/span[2]')));
        print(numPortaria, '- ERRO:', mensagemErro.text)
        listaPortariasNaoPublicadas.append(numPortaria)
    except:
        try:
            mensagemSucesso = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="idFormMsg:idMensagem"]/div/ul/li/span[2]')));
            print(numPortaria, '- SUCESSO:', mensagemSucesso.text)
            listaPortariasPublicadas.append(numPortaria)
            time.sleep(0.3)
        except:
            mensagemErro = 'Resultado não identificado! Verifique se a portaria foi publicada.';
            print(numPortaria, '- ERRO:', mensagemErro.text)
            listaPortariasSemResultado.append(numPortaria)
    
    navegador.get("https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf");

quantidadePortariasPublicadas = len(listaPortariasPublicadas)
quantidadePortariasNaoPublicadas = len(listaPortariasNaoPublicadas)
quantidadePortariasSemResultado = len(listaPortariasSemResultado)


##RESUTADOS DAS PUBLICAÇÕES

print("------------------")
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


# # Outras opções

# In[ ]:


#Atualizar navegador

navegador.refresh()


# In[ ]:


#Ir para a página de cadastro para publicação

navegador.get("https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf");


# In[ ]:


import json

with open('/content/drive/MyDrive/Colab Notebooks/valores_padrao.json', 'r') as arquivo_json:
  arquivo_json = json.load(arquivo_json)

print(arquivo_json['valores_padrao']['responsavel_assinatura'])


# In[ ]:


#Fechar navegador

navegador.quit()


# In[ ]:


import json

with open('config.json', 'r', encoding="utf-8") as config_json:
    config_json = json.load(config_json)
    
print(config_json['temas_assuntos']) #0 = tema_bgp #1 = nivel_assunto_bgp #2 = arrow_down

print()

for key,value in config_json['temas_assuntos'].items():
    print (key)
    print (key[''])
        


# In[ ]:





# In[ ]:




