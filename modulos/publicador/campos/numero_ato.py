from modulos.config import wait
from modulos.config import navegador
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.funcoes import aguardar_loading


def preencher_numero_ato(numPortaria):
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNumeroAto"]')))
        
        navegador.execute_script("campoDataAssinatura = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNumeroAto')")
        
        navegador.execute_script("campoDataAssinatura.value = '" + numPortaria + "'")

        aguardar_loading()

        print(numPortaria, '- Número do ato preenchido')
    except:
        print("ERRO: Falha ao preencher número do ato")