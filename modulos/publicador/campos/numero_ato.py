from modulos.config import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.funcoes import aguardar_loading


def preencher_numero_ato(numPortaria):
    campoNumeroAto = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNumeroAto"]')))

    campoNumeroAto.send_keys(str(numPortaria))

    aguardar_loading()

    print(numPortaria, '- Número do ato preenchido')
