from modulos.config import wait
from modulos.publicador.valores_configurados import tipoAssinatura
from modulos.publicador.valores_configurados import dataAssinatura
from modulos.publicador.valores_configurados import dataPublicacao
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modulos.funcoes import aguardar_loading


# Data de assinatura

def preencher_data_assinatura(numPortaria):
    if (tipoAssinatura == "Manual"):

        campoDataAssinatura = wait.until(EC.element_to_be_clickable(
            (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataAssinatura_input')))

        cont = 1
        while cont <= 8:
            campoDataAssinatura.send_keys(Keys.BACKSPACE)
            cont = cont + 1

        campoDataAssinatura.send_keys(dataAssinatura)

        aguardar_loading()

        print(numPortaria, '- Data de assinatura preenchida: ', dataAssinatura)

    else:
        print(numPortaria, '- Tipo de assinatura é digital. Data de assinatura não é preenchida.')

# Data de publicação

def preencher_data_publicacao(numPortaria):

    campoDataPublicacao = wait.until(EC.element_to_be_clickable(
        (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataParaPublicacao_input')))

    campoDataPublicacao.click()

    cont = 1
    while cont <= 8:
        campoDataPublicacao.send_keys(Keys.BACKSPACE)
        cont = cont + 1

    campoDataPublicacao.send_keys(dataPublicacao)

    aguardar_loading()

    print(numPortaria, '- Data da publicação preenchida: ', dataPublicacao)
