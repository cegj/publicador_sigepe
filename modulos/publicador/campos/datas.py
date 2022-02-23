from modulos.config import wait
from modulos.config import navegador
from modulos.publicador.valores_configurados import tipoAssinatura
from modulos.publicador.valores_configurados import dataAssinatura
from modulos.publicador.valores_configurados import dataPublicacao
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modulos.funcoes import aguardar_loading


# Data de assinatura

def preencher_data_assinatura(numPortaria):
    try:
        if (tipoAssinatura == "Manual"):
            
            wait.until(EC.element_to_be_clickable((By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataAssinatura_input')))
            
            navegador.execute_script("campoDataAssinatura = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataAssinatura_input')")
            
            navegador.execute_script("campoDataAssinatura.value = '" + dataAssinatura + "'")
            
            aguardar_loading()
            
            print(numPortaria, '- Data de assinatura preenchida: ', dataAssinatura)

        else:
            print(numPortaria, '- Tipo de assinatura é digital. Data de assinatura não é preenchida.')
    
    except:
        print("ERRO: Falha ao preencher data de assinatura")

# Data de publicação

def preencher_data_publicacao(numPortaria):

    try:
        wait.until(EC.element_to_be_clickable((By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataParaPublicacao_input')))
            
        navegador.execute_script("campoDataPublicacao = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataParaPublicacao_input')")
            
        navegador.execute_script("campoDataPublicacao.value = '" + dataPublicacao + "'")
            
        aguardar_loading()
            
        print(numPortaria, '- Data da publicação preenchida: ', dataPublicacao)
    except:
        print("ERRO: Falha ao preencher data de publicação")