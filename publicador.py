import shutil
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import getpass
import os
import json
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from datetime import timedelta
import datetime
print('Iniciando...')

# Definição das funções de utilidades

today = datetime.date.today()  # Hoje no formato ANSI AAAA-MM-DD
tomorrow = today + timedelta(1)  # Amanhã no formato ANSI AAAA-MM-DD
day = today.day
month = today.month
year = today.year


def ajustar_data(data, separador):
    dataArray = str(data).split('-')
    dataAjustada = dataArray[2] + separador + \
        dataArray[1] + separador + dataArray[0]
    return str(dataAjustada)


def limpar_quebras_de_linha(string):
    string = string.replace("\n", "")  # Apagar quebras de linha
    return string


def aguardar_loading():
    modalAguarde = WebDriverWait(navegador, 300).until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))


def limpar_terminal_exibir_cabecalho():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('----------------------------------')
    print('----------------------------------')
    print('PUBLICADOR DE PORTARIAS NO SIGEPE')
    print('----------------------------------')
    print('----------------------------------')
    print('******** github.com/cegj/ ********')
    print('----------------------------------')
    print()


def print_titulo(string):
    print('\033[1;36m' + string + '\033[0m\n')


def print_erro(string):
    print('\033[1;31m' + 'ERRO: ' + string + '\033[0m')


def print_sucesso(string):
    print('\033[1;32m' + 'SUCESSO: ' + string + '\033[0m')


def input_seguir(string):
    input('\033[1;33m' + string + '\033[0m')

def print_color(cor, string):
    if (cor == 'cinza'):
        cor = '\033[1;90m'

    print(cor + string + '\033[0m')




# Definição das funções de webdriver

def abrir_webdriver():
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Definição da função para obter dados de config.json


def obter_config():

    def definir_valor_var(configJson):
        opcoesVar = configJson["valores_var"]

        if len(opcoesVar) > 0:
            print("Opções de valores para [var]:\n")

            for i, valor in enumerate(opcoesVar):
                print (i, " - ", valor)

            sucesso = False

            while (sucesso == False):

                selected = input('\nInforme o número da opção para preencher [var] no arquivo de configurações, ou ENTER para deixar em branco:\n')

                if (selected != ""):
                    try:
                        selected = int(selected)
                        for i, valor in enumerate(opcoesVar):
                            if (selected == i):
                                return valor
                        
                        print_erro("O número informado não corresponde a uma opção.")
                        sucesso = False
                    except:
                        print_erro("Você não digitou um número inteiro ou ENTER para deixar em branco.")
                        sucesso = False
                else:
                    return ""
        else:
            return ""

    def atribuir_variaveis_config(configJson):

        # Define o valor de [var] (pergunta ao usuário)

        vVar = definir_valor_var(configJson)

        # Define valor variável de [hoje]
        vHojePonto = str(ajustar_data(today, '.'))
        vHojeBarra = str(ajustar_data(today, '/'))
        vHojeTraco = str(ajustar_data(today, '-'))

        # Define valor variável de [proximo_dia_util]
        if (tomorrow.weekday() == 5):
            vProximoUtilPonto = str(ajustar_data(tomorrow + timedelta(2), '.'))
        elif (tomorrow.weekday() == 6):
            vProximoUtilPonto = str(ajustar_data(tomorrow + timedelta(1), '.'))
        else:
            vProximoUtilPonto = str(ajustar_data(tomorrow, '.'))

        if (tomorrow.weekday() == 5):
            vProximoUtilBarra = str(ajustar_data(tomorrow + timedelta(2), '/'))
        elif (tomorrow.weekday() == 6):
            vProximoUtilBarra = str(ajustar_data(tomorrow + timedelta(1), '/'))
        else:
            vProximoUtilBarra = str(ajustar_data(tomorrow, '/'))

        if (tomorrow.weekday() == 5):
            vProximoUtilTraco = str(ajustar_data(tomorrow + timedelta(2), '-'))
        elif (tomorrow.weekday() == 6):
            vProximoUtilTraco = str(ajustar_data(tomorrow + timedelta(1), '-'))
        else:
            vProximoUtilTraco = str(ajustar_data(tomorrow, '-'))

        # Define o valor variável de [ano_assinatura] #########MELHORAR

        if (configJson['valores']['data_assinatura'].count("hoje") > 0):
            dataAssinaturaP = ajustar_data(today, '/')
        elif(configJson['valores']['data_assinatura'].count("proximo_dia_util") > 0):
            dataAssinaturaP = ajustar_data(tomorrow, '/')
        else:
            dataAssinaturaP = configJson['valores']['data_assinatura']

        dataAssinaturaArray = (dataAssinaturaP.split('/'))
        vAnoAssinatura = str(dataAssinaturaArray[2])

        # define o valor da variavel [hoje_dia]
        vHojeDia = str(day)

        if day < 10:
            vHojeDia0 = '0' + str(day)
        else:
            vHojeDia0 = str(day)

        # define o valor da variavel [hoje_mes]
        vHojeDia = str(month)

        if month < 10:
            vHojeMes0 = '0' + str(month)
        else:
            vHojeMes0 = str(month)

        # define o valor da variavel [hoje_ano]
        vHojeAno = str(year)

        # Define o valor da variável [mesatual_num-extenso]

        meses = {
            "1": '1 - JANEIRO',
            "2": "2 - FEVEREIRO",
            "3": "3 - MARÇO",
            "4": "4 - ABRIL",
            "5": "5 - MAIO",
            "6": "6 - JUNHO",
            "7": "7 - JULHO",
            "8": "8 - AGOSTO",
            "9": "9 - SETEMBRO",
            "10": "10 - OUTUBRO",
            "11": "11 - NOVEMBRO",
            "12": "12 - DEZEMBRO"
        }

        for key, value in meses.items():
            if (key == str(month)):
                vMesAtualNumExtenso = value
                break

        for key, value in meses.items():
            if (key == str(month)):
                if month < 10:
                    vMesAtualNumExtenso0 = '0' + value
                    break
                else:
                    vMesAtualNumExtenso0 = value
                    break

        import ast

        configJsonStr = str(configJson)

        configJsonStr = configJsonStr.replace("[var]", vVar)
        configJsonStr = configJsonStr.replace("[hoje.]", vHojePonto)
        configJsonStr = configJsonStr.replace("[hoje/]", vHojeBarra)
        configJsonStr = configJsonStr.replace("[hoje-]", vHojeTraco)
        configJsonStr = configJsonStr.replace("[hoje_dia]", vHojeDia)
        configJsonStr = configJsonStr.replace("[hoje_dia0]", vHojeDia0)
        configJsonStr = configJsonStr.replace("[hoje_mes]", vHojeDia)
        configJsonStr = configJsonStr.replace("[hoje_mes0]", vHojeDia0)
        configJsonStr = configJsonStr.replace("[hoje_ano]", vHojeAno)
        configJsonStr = configJsonStr.replace("[proximo_dia_util.]", vProximoUtilPonto)
        configJsonStr = configJsonStr.replace("[proximo_dia_util/]", vProximoUtilBarra)
        configJsonStr = configJsonStr.replace("[proximo_dia_util-]", vProximoUtilTraco)
        configJsonStr = configJsonStr.replace("[mesatual_num_extenso]", vMesAtualNumExtenso)
        configJsonStr = configJsonStr.replace("[mesatual_num_extenso0]", vMesAtualNumExtenso0)
        configJsonStr = configJsonStr.replace("[ano_assinatura]", vAnoAssinatura)

        configJson = ast.literal_eval(configJsonStr)

        return configJson

    try:
        with open('config_publicador.json', 'r', encoding="utf-8") as temp_config_json_file:
            configJson = json.load(temp_config_json_file)
            
            if configJson["dir_config"]:
                dirConfigSource = configJson["dir_config"][0]

                if (dirConfigSource == "local"):
                    dirConfigPath = configJson["dir_config"][1]
                    with open(dirConfigPath, 'r', encoding="utf-8") as config_json_file:
                        configJson = json.load(config_json_file)
                        configJson = atribuir_variaveis_config(configJson)

                elif (dirConfigSource == "remoto"):
                    dirConfigPath = configJson["dir_config"][1]
                    import urllib.request
                    with urllib.request.urlopen(dirConfigPath) as url:
                        configJson = json.loads(url.read().decode())
                        configJson = atribuir_variaveis_config(configJson)
            else:
                with open('config_publicador.json', 'r', encoding="utf-8") as config_json_file:
                    configJson = json.load(config_json_file)
                    configJson = atribuir_variaveis_config(configJson)
     
    except Exception as e:
        print_erro('Não foi possível importar os dados de config.json.\nVerifique se o arquivo está configurado corretamente.\nMensagem retornada pelo sistema: ' + repr(e))
        input_seguir('Aperte ENTER para encerrar a aplicação...')
        navegador.quit()
        sys.exit()



    if (configJson):
        return configJson
    else:
        print_erro('Não foi possível importar os dados de config.json. Verifique se o arquivo está configurado corretamente. Em caso de dúvidas, consulte a documentação.')
        input_seguir('Aperte ENTER para encerrar a aplicação...')
        navegador.quit()
        sys.exit()

# Define função que exibe os dados de config.json para o usuário


def exibir_valores_config():
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

# Define função para obter dados de portaria


def obter_lista_arquivos(diretorioArquivos):

    try:

        listaDeArquivos = {
            'arquivosAceitos': [],
            'arquivosRejeitados': []
        }

        for nomeArquivo in os.listdir(diretorioArquivos):
            if (nomeArquivo.count("~") == 0 and nomeArquivo.count(".rtf") > 0):
                listaDeArquivos['arquivosAceitos'].append(nomeArquivo)
            else:
                listaDeArquivos['arquivosRejeitados'].append(nomeArquivo)

        return listaDeArquivos

    except Exception as e:

        return repr(e)

# Define funções de acesso ao SIGEPE


def fazer_login():

    def acessar_pagina_login():

        navegador.get(
            "https://admsistema.sigepe.planejamento.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")

        tituloPagina = navegador.title

        return tituloPagina

    def configurar_habilitacao():

        habilitacaoConfig = configJson['config']['habilitacao_sigepe']

        habilitacaoAtual = navegador.find_element(
            By.XPATH, '//*[@id="j_idt62:habDisponiveisLabel"]')

        print('Habilitação atual:', habilitacaoAtual.text)

        if (habilitacaoAtual.text != str(habilitacaoConfig)):
            habilitacaoAtual.click()
            habilitacao = navegador.find_element(
                By.XPATH, str("//*[text()='" + habilitacaoConfig + "']"))
            habilitacao.click()
            time.sleep(0.5)
            novaHabilitacao = halfwait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="j_idt62:habDisponiveisLabel"]')))
            print('Habilitação alterada para:', novaHabilitacao.text)

    acessar_pagina_login()

    sucesso = False

    while (sucesso == False):

        print('Informe seus dados para faze login no SIGEPE: \n')

        usuario = input('CPF do usuário (somente números): ')

        senha = getpass.getpass('Senha do SIGEPE: ')

        print('Aguarde...')

        campoUsuario = navegador.find_element(
            By.XPATH, '//*[@id="cpfUsuario"]')

        campoUsuario.click()

        campoUsuario.send_keys(usuario)

        campoSenha = navegador.find_element(By.XPATH, '//*[@id="password"]')

        campoSenha.click()

        campoSenha.send_keys(senha)

        botaoAcessar = navegador.find_element(
            By.XPATH, '//*[@id="botaoCredenciais"]')

        botaoAcessar.click()

        if (navegador.find_element(By.XPATH, '//*[@id="idBreadCrumb0"]/span')):

            paginaAtual = navegador.find_element(
                By.XPATH, '//*[@id="idBreadCrumb0"]/span')

            print('Você está em:', paginaAtual.text)

            configurar_habilitacao()

            navegador.get(
                "https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")

            paginaAtual = navegador.find_element(
                By.XPATH, '//*[@id="idBreadCrumb4"]/span')

            print('Você está em:', paginaAtual.text, '\n')

            print_sucesso('Acesso ao Sigepe realizado')

            sucesso = True

        elif(navegador.find_element(By.XPATH, '//*[@id="msg_alerta"]')):

            erroLogin = navegador.find_element(
                By.XPATH, '//*[@id="msg_alerta"] \n')

            print_erro(erroLogin.text + '. Tente novamente.')

            sucesso = False

        else:

            print(
                'Não foi possível fazer login (erro não identificado). Tente novamente. \n')

            sucesso = False

# Define as funções relacionadas com manipulação dos arquivos das portarias


def obter_texto_portaria(nomeArquivo):
    from striprtf.striprtf import rtf_to_text

    with open(str(diretorioArquivos) + str(nomeArquivo), encoding='cp1252') as arquivo:
        conteudo = arquivo.read()
        portaria = rtf_to_text(conteudo)
        arquivo.close()

    return portaria


def obter_numero_portaria(textoPortaria):

    A = textoPortaria.split(
        configJson['delimitadores']['numero_portaria'][0], 1)

    B = A[1].split(configJson['delimitadores']['numero_portaria'][1], 1)

    numPortaria = B[0]

    return numPortaria


def obter_siape(textoPortaria):
    textoPortariaSplit = textoPortaria.split(
        configJson['delimitadores']['siape'][0], 1)
    matriculaSiape = textoPortariaSplit[1].split(
        configJson['delimitadores']['siape'][1], 1)
    matriculaSiape = matriculaSiape[0]

    return matriculaSiape


def obter_tema(textoPortaria):
    for key in configJson['temas_assuntos']:
        if (textoPortaria.count(key) > 0):
            temaBgp = configJson['temas_assuntos'][key]['tema_bgp']
            nivelAssuntoBgp = configJson['temas_assuntos'][key]['nivel_assunto_bgp']
            temaArrowDown = configJson['temas_assuntos'][key]['arrow_down']
            temaAssunto = {
                'tema': temaBgp, 'nivel_assunto': nivelAssuntoBgp, 'arrow_down': temaArrowDown}

            return temaAssunto
            break


def formatar_portaria_para_publicar(textoPortaria):

    if (configJson['delimitadores']['cabecalho'][1] == "var_ano_assinatura"):
        anoAssinatura = (dataAssinatura.split('/'))
        anoAssinatura = anoAssinatura[2]
        fimCabecalho = anoAssinatura
    else:
        fimCabecalho = configJson['delimitadores']['cabecalho'][1]

    textoPortaria = limpar_quebras_de_linha(textoPortaria)

    textoPortariaSemCabecalho = textoPortaria.split(
        str(fimCabecalho), 1)  # Remover cabeçalho (usa ano como limite)

    # Descarta o cabeçalho, fica só com o que vem depois do ano
    textoPortariaSemCabecalho = textoPortariaSemCabecalho[1]

    # Separa o texto em dois, antes e depois do dois-pontos do cabeçalho
    textoPortariaSemCabecalho = textoPortariaSemCabecalho.split(
        configJson['delimitadores']['preliminar_portaria'][1], 1)

    # Define parte de cima do texto da portaria
    textoPreliminarPortaria = textoPortariaSemCabecalho[0] + \
        configJson['delimitadores']['preliminar_portaria'][1]

    # Define parte de baixo do texto da portaria
    textoNormativoPortaria = textoPortariaSemCabecalho[1]

    # Parte preliminar, índice 0, parte normativa, índice 1
    textoPortaria = [textoPreliminarPortaria, textoNormativoPortaria]

    return textoPortaria


def renomear_arquivo(nomeArquivoCompleto):
    nomeArquivoArray = nomeArquivoCompleto.split('.', 1)
    nomeArquivo = nomeArquivoArray[0]
    extensaoArquivo = str('.' + nomeArquivoArray[1])
    novoNomeArquivoCompleto = str(
        nomeArquivo + " " + termoNomeArquivo + extensaoArquivo)

    file_oldname = os.path.join(diretorioArquivos, nomeArquivoCompleto)
    file_newname_newfile = os.path.join(
        diretorioArquivos, novoNomeArquivoCompleto)

    os.rename(file_oldname, file_newname_newfile)

    return novoNomeArquivoCompleto


def copiar_mover_arquivo(nomeArquivo):

    try:
        origem = str(diretorioArquivos + nomeArquivo)
        destino = str(diretorioDestinoArquivos + nomeArquivo)

        if (operacao == "M"):
            shutil.move(origem, destino)
            return diretorioDestinoArquivos
        elif (operacao == "C"):
            shutil.copy(origem, destino)
            return diretorioDestinoArquivos
        else:
            return "ARQUIVO NÃO COPIADO/MOVIDO. INFORME 'M' OU 'C' EM CONFIG.JSON"

    except Exception as e:
        print_erro(
            'Não foi possível copiar ou mover arquivo. Retorno do sistema: ')
        print_erro(repr(e))

# Início da aplicação

limpar_terminal_exibir_cabecalho()

input_seguir('Aperte ENTER para iniciar...')

limpar_terminal_exibir_cabecalho()

print_titulo('CONFIGURAÇÃO DO NAVEGADOR (WEBDRIVER)')

# Importa webdriver

navegador = abrir_webdriver()
navegador.minimize_window()

# Define os tempos de espera

halfwait = WebDriverWait(navegador, 10)
wait = WebDriverWait(navegador, 20)
longwait = WebDriverWait(navegador, 40)

print('\nConfiguração do navegador concluída')
print('\n----------------------------------')

limpar_terminal_exibir_cabecalho()
print_titulo('CONFIGURAÇÃO DOS VALORES PARA O LOTE DE ARQUIVOS')

configJson = obter_config()

dataAssinatura = configJson['valores']['data_assinatura']
dataPublicacao = configJson['valores']['data_publicacao']
edicaoBGP = configJson['valores']['edicao_bgp']
tipoAssinatura = configJson['valores']['tipo_assinatura']
especie = configJson['valores']['especie']
tipoNumero = configJson['valores']['tipo_preenchimento']
orgao = configJson['valores']['orgao']
upag = configJson['valores']['upag']
uorg = configJson['valores']['uorg']
responsavelAssinatura = configJson['valores']['responsavel_assinatura']
cargoResponsavelAssinatura = configJson['valores']['cargo_responsavel']

#valoresErrados = []

# if (edicaoBGP != "Normal" or edicaoBGP != "Extraordinária"):
#    valoresErrados.append(edicaoBGP)
#    valoresErrados.append("- Normal\n- Extraordinária")

# if (tipoAssinatura != "Digital" or tipoAssinatura != "Manual"):
#    valoresErrados.append(tipoAssinatura)
#    valoresErrados.append("- Digital\n- Manual")
#
#    print('ERRO: Não houve arquivos aceitos no diretório. Verifique o formato dos arquivos.')
#    input('Aperte ENTER para encerrar a aplicação...')
#    sys.exit()

limpar_terminal_exibir_cabecalho()
print_titulo('CONFIGURAÇÃO DOS VALORES PARA O LOTE DE ARQUIVOS')
exibir_valores_config()

print('\n----------------------------------')
input_seguir('\nAperte ENTER para continuar...')

# Obtém lista de arquivos a serem publicados

limpar_terminal_exibir_cabecalho()

print_titulo('LISTA DE ARQUIVOS PARA PUBLICAÇÃO')

diretorioArquivos = configJson['config']['diretorio_arquivos']
diretorioDestinoArquivos = configJson['config']['diretorio_arquivo_destino']
termoNomeArquivo = configJson['config']['adicionar_termo_nome_arquivo']
operacao = configJson['config']['copiar_ou_mover']

listaDeArquivos = obter_lista_arquivos(diretorioArquivos)

print('- Diretório de origem:')
print_color('cinza', diretorioArquivos + '\n')

if (operacao == "C"):
    print('- Operação a ser realizada após publicação:')
    print_color('cinza', 'COPIAR\n')
    print('- Diretório de destino:')
    print_color('cinza', diretorioDestinoArquivos + '\n')
elif(operacao == "M"):
    print('- Operação a ser realizada após publicação:')
    print_color('cinza', 'MOVER\n')
    print('- Diretório de destino:')
    print_color('cinza', diretorioDestinoArquivos + '\n')

if (termoNomeArquivo != ""):
    print('- Termo a ser adicionado ao título do arquivo:')
    print_color('cinza', termoNomeArquivo + '\n')

print('\n----------------------------------\n')

if (type(listaDeArquivos) is dict):

    arquivosAceitos = listaDeArquivos['arquivosAceitos']
    arquivosRejeitados = listaDeArquivos['arquivosRejeitados']

    if (len(arquivosAceitos) > 0):

        print(len(arquivosAceitos), 'ARQUIVO(S) PARA PUBLICAÇÃO: \n')

        for arquivoAceito in arquivosAceitos:
            print(arquivoAceito)

    else:
        print_erro('Não houve arquivos aceitos no diretório. Verifique o formato dos arquivos.')
        input_seguir('Aperte ENTER para encerrar a aplicação...')
        navegador.quit()
        sys.exit()

    if (len(arquivosRejeitados) > 0):
        print(len(arquivosRejeitados), 'arquivo(s) REJEITADOS: \n')

        for arquivoRejeitado in arquivosRejeitados:
            print(arquivoRejeitado)

        print('\nOs arquivos rejeitados não serão publicados.')

    print('\n----------------------------------')
    input_seguir('\nAperte ENTER para continuar...')
    limpar_terminal_exibir_cabecalho()

else:
    print_erro(
        'Não foi possível importar a lista de arquivos.\nRetorno do sistema: ' + listaDeArquivos)
    input_seguir('Aperte ENTER para encerrar a aplicação...')
    navegador.quit()
    sys.exit()


# Fazer login no SIGEPE

print_titulo('LOGIN NO SIGEPE')

fazer_login()

print('\n----------------------------------')
input_seguir('\nAperte ENTER para *iniciar* a publicação das portarias...')

limpar_terminal_exibir_cabecalho()

print_titulo('PUBLICAÇÃO DAS PORTARIAS')

# Preencher formulários com dados dos arquivos e publicar

listaPortariasPublicadas = []
listaPortariasNaoPublicadas = []
listaPortariasSemResultado = []

for nomeArquivo in arquivosAceitos:

    try:

        print('\n----------------------------------\n')

        textoPortaria = obter_texto_portaria(nomeArquivo)

        numPortaria = obter_numero_portaria(textoPortaria)

        textoPortariaFormatado = formatar_portaria_para_publicar(textoPortaria)

        print(numPortaria, '- Iniciando preenchimento da portaria...')
        print_color('cinza', '~~~~~~')
        print_color('cinza', textoPortariaFormatado[0])
        print_color('cinza', textoPortariaFormatado[1])
        print_color('cinza', '~~~~~~')

        aguardar_loading()

        # Edição do boletim

        try:
            edicaoNormal = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:radEdicao"]/tbody/tr/td[2]/label')))
            edicaoExtraordinaria = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:radEdicao"]/tbody/tr/td[4]/label')))

            if (edicaoBGP == "Normal"):
                edicaoNormal.click()
            elif (edicaoBGP == "Extraordinária"):
                edicaoExtraordinaria.click()

            aguardar_loading()

            print(numPortaria, '- Tipo assinatura selecionado:', edicaoBGP)

            aguardar_loading()

        except Exception as e:
            print_erro(str(numPortaria + "- Falha ao preencher edição do boletim"))
            print(repr(e))

        # Tipo de assinatura

        try:
            tipoAssinaturaDigital = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:radTipoAssinatura"]/tbody/tr/td[2]/label')))
            tipoAssinaturaManual = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:radTipoAssinatura"]/tbody/tr/td[4]/label')))

            if (tipoAssinatura == "Manual"):
                tipoAssinaturaManual.click()
            elif (tipoAssinatura == "Digital"):
                tipoAssinaturaDigital.click()

            aguardar_loading()

            print(numPortaria, '- Tipo assinatura selecionado:', tipoAssinatura)

            aguardar_loading()

        except Exception as e:
            print_erro(str(numPortaria + "- Falha ao preencher tipo de assinatura"))
            print(repr(e))

        # Tipo de preenchimento do número

        try:
            campoTipoNumero = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTipoPreenchimento_label"]')))

            campoTipoNumero.click()

            time.sleep(0.3)

            campoBuscarTipoNumero = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTipoPreenchimento_filter"]')))

            campoBuscarTipoNumero.send_keys(tipoNumero)

            time.sleep(1.5)

            campoBuscarTipoNumero.send_keys(Keys.ENTER)

            aguardar_loading()

            print(numPortaria, '- Tipo de preenchimento do número selecionado: ',
                  campoTipoNumero.text)

        except Exception as e:
            print_erro(str(numPortaria + "- Falha ao preencher tipo de número"))
            print(repr(e))

        # Tema

        if (obter_tema(textoPortariaFormatado[1])):
            temaAssunto = obter_tema(textoPortariaFormatado[1])
        else:
            print_erro('!!!TEMA NÃO IDENTIFICADO!!!')

        try:

            campoTema = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_label"]')))

            campoTema.click()

            time.sleep(0.3)

            campoBuscarTema = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_filter"]')))

            campoBuscarTema.send_keys(temaAssunto['tema'])

            time.sleep(1.5)

            if (temaAssunto['arrow_down'] > 0):
                cont = 1
                while cont <= temaAssunto['arrow_down']:
                    campoBuscarTema.send_keys(Keys.ARROW_DOWN)
                    cont = cont + 1

            campoBuscarTema.send_keys(Keys.ENTER)

            aguardar_loading()

            campoTemaPreenchido = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_label"]')))

            print(numPortaria, '- Tema selecionado: ', campoTemaPreenchido.text)

        except Exception as e:
            print_erro(str(numPortaria + "- Falha ao preencher tema"))
            print(repr(e))

        # Assunto

        try:

            time.sleep(0.3)

            botaoProcurarAssunto = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnSelecionarClassificacaoAssunto"]')))

            botaoProcurarAssunto.click()

            janelaSelecionarAssunto = wait.until(EC.element_to_be_clickable(
                (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:idDlgSelecionarAssunto')))

            time.sleep(0.3)

            navegador.execute_script(
                "document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:treeClassificacao_selection').setAttribute('type', 'text');")

            time.sleep(0.3)

            campoNivelTemaOculto = wait.until(EC.element_to_be_clickable(
                (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:treeClassificacao_selection')))

            campoNivelTemaOculto.send_keys(temaAssunto['nivel_assunto'])

            time.sleep(0.3)

            botaoSelecionarAssunto = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnSelecionar"]/span')))

            botaoSelecionarAssunto.click()

            aguardar_loading()

            campoAssuntoPreenchido = wait.until(EC.element_to_be_clickable(
                (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:txtClassificacao')))

            print(numPortaria, '- Assunto selecionado: ',
                  campoAssuntoPreenchido.get_attribute("value"))

            time.sleep(0.3)

        except Exception as e:
            print_erro(str(numPortaria + "- Falha ao preencher assunto"))
            print(repr(e))

        # Número do ato

        try:
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNumeroAto"]')))

            navegador.execute_script(
                "campoDataAssinatura = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNumeroAto')")

            navegador.execute_script(
                "campoDataAssinatura.value = '" + numPortaria + "'")

            aguardar_loading()

            print(numPortaria, '- Número do ato preenchido')

        except Exception as e:
            print_erro(str(numPortaria + "- Falha ao preencher número do ato"))
            print(repr(e))

        # Data de assinatura

        try:
            if (tipoAssinatura == "Manual"):

                wait.until(EC.element_to_be_clickable(
                    (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataAssinatura_input')))

                navegador.execute_script(
                    "campoDataAssinatura = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataAssinatura_input')")

                navegador.execute_script(
                    "campoDataAssinatura.value = '" + dataAssinatura + "'")

                aguardar_loading()

                print(numPortaria, '- Data de assinatura preenchida: ',
                      dataAssinatura)

            else:
                print(
                    numPortaria, '- Tipo de assinatura é digital. Data de assinatura não é preenchida.')

        except Exception as e:
            print_erro(str(numPortaria + "- Falha ao preencher data de assinatura"))
            print(repr(e))

        # Data de publicação

        if (edicaoBGP == "Normal"):

            try:

                wait.until(EC.element_to_be_clickable(
                    (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataParaPublicacao_input')))

                navegador.execute_script(
                    "campoDataPublicacao = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataParaPublicacao_input')")

                navegador.execute_script(
                    "campoDataPublicacao.value = '" + dataPublicacao + "'")

                aguardar_loading()

                print(numPortaria, '- Data da publicação preenchida: ',
                      dataPublicacao)

            except Exception as e:
                print_erro(str(numPortaria + "- Falha ao preencher data de publicação"))
                print(repr(e))

        else:
            print(
                numPortaria, "- Data de publicação preechida: hoje (edição extraordinária)")

        # Espécie

        try:
            campoEspecie = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selEspecie_label"]')))

            aguardar_loading()

            campoEspecie.click()

            time.sleep(0.3)

            campoBuscarEspecie = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selEspecie_filter"]')))

            campoBuscarEspecie.send_keys(especie)

            time.sleep(1.5)

            campoBuscarEspecie.send_keys(Keys.ENTER)

            aguardar_loading()

            print(numPortaria, '- Espécie selecionada: ', campoEspecie.text)

        except:
            print(str(numPortaria + "- Falha ao preencher espécie"))

        # Texto do ato/portaria (iframe)

        try:
            navegador.switch_to.frame(0)

            campoTextoPortaria = wait.until(
                EC.element_to_be_clickable((By.TAG_NAME, 'body')))

            campoTextoPortaria.click()

            time.sleep(0.3)

            campoTextoPortaria.send_keys(textoPortariaFormatado[1])

            time.sleep(0.3)

            campoTextoPortaria.send_keys(Keys.ENTER)

            time.sleep(0.3)

            campoTextoPortaria.send_keys(textoPortariaFormatado[0])

            time.sleep(0.3)

            navegador.switch_to.default_content()

            aguardar_loading()

            print(numPortaria, '- Texto da portaria preenchido')

        except Exception as e:
            print_erro(str(numPortaria + "- Falha ao preencher texto da portaria"))
            print(repr(e))

        # Órgãos elaboradores

        try:
            print(numPortaria, '- Iniciando preenchimento do órgão/autoridade...')

            # Há dois modelos de janela para selecionar uorg/upag/autoridade no SIGEPE

            try:  # Gatilho para modelo novo é o XPATH do botão para abrir janela, pois são diferentes
                botaoIncluirOrgaoElabAnt = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt395"]/span')))

                print(numPortaria,
                      '- [obs:] Cadastro pelo modelo antigo de janela')

                botaoIncluirOrgaoElabAnt.click()

                aguardar_loading()

                campoUpag = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadePagadora_label"]')))

                campoUpag.click()

                time.sleep(0.3)

                campoBuscarUpag = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadePagadora_filter"]')))

                campoBuscarUpag.send_keys(upag)

                time.sleep(1.5)

                campoBuscarUpag.send_keys(Keys.ENTER)

                aguardar_loading()

                print(numPortaria, '- UPAG preenchida: ', campoUpag.text)

                time.sleep(0.5)

                campoUorg = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadeOrganizacional_label"]')))

                campoUorg.click()

                time.sleep(0.5)

                campoBuscarUorg = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadeOrganizacional_filter"]')))

                campoBuscarUorg.send_keys(uorg)

                time.sleep(1.5)

                campoBuscarUorg.send_keys(Keys.ENTER)

                aguardar_loading()

                print(numPortaria, '- UORG preenchido: ', campoUorg.text)

                campoResponsavelAssinatura = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNomeResponsavel"]')))

                campoResponsavelAssinatura.send_keys(responsavelAssinatura)

                campoCargoResponsavelAssinatura = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptCargoResponsavel"]')))

                campoCargoResponsavelAssinatura.send_keys(
                    cargoResponsavelAssinatura)

                botaoGravarOrgao = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt699"]/span')))

                botaoGravarOrgao.click()

                aguardar_loading()

            except:
                botaoIncluirOrgaoElab = navegador.find_element(
                    By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt396"]')

                print(numPortaria,
                      '- [obs:] Cadastro pelo novo modelo de janela')

                botaoIncluirOrgaoElab.click()

                aguardar_loading()

                janelaOrgaosElaboradores = wait.until(EC.element_to_be_clickable(
                    (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:dlgIncluirOrgaoElaborador')))

                campoUpag = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt446_label"]')))

                campoUpag.click()

                time.sleep(5)

                campoBuscarUpag = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt446_filter"]')))

                campoBuscarUpag.send_keys(upag)

                time.sleep(1.5)

                campoBuscarUpag.send_keys(Keys.ENTER)

                aguardar_loading()

                print(numPortaria, '- UPAG preenchida: ', campoUpag.text)

                campoUorg = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt453_label"]')))

                campoUorg.click()

                time.sleep(5)

                campoBuscarUorg = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt453_filter"]')))

                campoBuscarUorg.send_keys(uorg)

                time.sleep(1.5)

                campoBuscarUorg.send_keys(Keys.ENTER)

                aguardar_loading()

                print(numPortaria, '- UORG preenchido: ', campoUorg.text)

                campoResponsavelAssinatura = wait.until(EC.invisibility_of_element_located(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt463"]')))

                campoResponsavelAssinatura.send_keys(responsavelAssinatura)

                botaoPesquisarAutoridade = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt492"]/span')))

                botaoPesquisarAutoridade.click()

                aguardar_loading()

                radiusSelecionarAutoridade = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt494:dataTableResultado_data"]/tr/td[1]/div/div/div[2]/span')))

                radiusSelecionarAutoridade.click()

                aguardar_loading()

                botaoSelecionarAutoridade = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt538"]/span')))

                botaoSelecionarAutoridade.click()

                aguardar_loading()

            responsavelAssinaturaSelecionado = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:tblResponsaveis:0:j_idt416:txtContent"]')))

            CargoResponsavelAssinaturaSelecionado = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:tblResponsaveis:0:j_idt418:txtContent"]')))

            print(numPortaria, '- Responsável pela assinatura preenchido: ',
                  responsavelAssinaturaSelecionado.text, " - ", CargoResponsavelAssinaturaSelecionado.text)

        except Exception as e:
            print_erro(str(numPortaria + "- Falha ao preencher órgão elaborador"))
            print(repr(e))

        # Interessado

        try:
            siapeInteressado = obter_siape(textoPortaria)

            print(numPortaria, '- Interessado identificado: ', siapeInteressado)
            print(numPortaria, '- Iniciando busca e preenchimento do interessado...')

            botaoAbrirInteressados = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[text()="Incluir interessado"]')))

            botaoAbrirInteressados.click()

            aguardar_loading()

            campoMatricula = wait.until(EC.element_to_be_clickable(
                (By.ID,  'frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt434:j_idt466')))

            campoMatricula.click()

            time.sleep(0.2)

            campoMatricula.send_keys(str(siapeInteressado))

            botaoPesquisarInteressado = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[text()="Pesquisar"]')))

            botaoPesquisarInteressado.click()

            aguardar_loading()

            checkboxSelecionarServidor = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt494:dataTableResultado:j_idt499"]/div/div/div[2]')))

            checkboxSelecionarServidor.click()

            # Função .click() do Selenium não está funcionando nessos botões abaixo. Usando Javascript:

            time.sleep(0.3)

            navegador.execute_script(
                "botaoIncluirServidor = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt494:j_idt517');")

            navegador.execute_script("botaoIncluirServidor.click();")

            aguardar_loading()

            navegador.execute_script(
                "botaoSelecionarServidor = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt538');")

            navegador.execute_script("botaoSelecionarServidor.click();")

            aguardar_loading()

            nomeServidorCadastrado = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:tblInteressados:0:j_idt1451:txtContent"]')))

            print(numPortaria, '- Servidor interessado cadastrado: ',
                  str(siapeInteressado), '-', nomeServidorCadastrado.text)

        except Exception as e:
            print_erro(str(numPortaria + " - Falha ao preencher interessado"))
            print(repr(e))

        # ENVIAR PARA PUBLICAÇÃO

        botaoGravarOrgao = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnEnviarPublicacao"]/span')))

        botaoGravarOrgao.click()

        print(numPortaria, '- Enviando para publicação...')

        aguardar_loading()

    except Exception as e:
        print_erro(str(numPortaria + "- Não foi possível publicar a portaria"))
        print(repr(e))

    finally:

        try:
            mensagemErro = navegador.find_element(
                By.XPATH, '//*[@id="msgCadastrarAto"]/div[2]/ul/li/span[2]')
            print_erro(numPortaria + ' - ' + mensagemErro.text)
            listaPortariasNaoPublicadas.append(
                numPortaria + ' - ' + mensagemErro.text)
        except:
            try:
                mensagemSucesso = navegador.find_element(
                    By.XPATH, '//*[@id="idFormMsg:idMensagem"]/div/ul/li/span[2]')
                print_sucesso(numPortaria + ' - ' + mensagemSucesso.text)
                listaPortariasPublicadas.append(numPortaria)

                if (configJson['config']['copiar_ou_mover'] != ""):
                    nomeArquivo = renomear_arquivo(nomeArquivo)
                    print(numPortaria, '- Arquivo renomeado para:', nomeArquivo)

                if (configJson['config']['copiar_ou_mover'] != ""):
                    novoDiretorio = copiar_mover_arquivo(nomeArquivo)
                    print(numPortaria, '- Arquivo copiado/movido para:', novoDiretorio)

            except:
                mensagemErro = 'Resultado não identificado! Verifique se a portaria foi publicada.'
                print_erro(numPortaria + ' - ' + mensagemErro)
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
print_titulo("PUBLICAÇÕES CONCLUÍDAS!")

if (quantidadePortariasPublicadas > 0):
    print()
    print("Quantidade de portarias publicadas: " +
          str(quantidadePortariasPublicadas))
    for portaria in listaPortariasPublicadas:
        print(portaria)

if (quantidadePortariasNaoPublicadas > 0):
    print()
    print("Quantidade de portarias não publicadas: " +
          str(quantidadePortariasNaoPublicadas))
    for portaria in listaPortariasNaoPublicadas:
        print(portaria)

if (quantidadePortariasSemResultado > 0):
    print()
    print("Quantidade de portarias sem resultado identificado: " +
          str(quantidadePortariasSemResultado))
    for portaria in listaPortariasSemResultado:
        print(portaria)
    print('IMPORTANTE: Verifique se as portarias sem resultado foram cadastradas para publicação no SIGEPE')

navegador.quit()
input_seguir('\n\nAperte ENTER para encerrar a aplicação...')
