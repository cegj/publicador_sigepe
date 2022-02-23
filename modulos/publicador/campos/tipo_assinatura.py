from modulos.publicador.valores_configurados import tipoAssinatura
from modulos.config import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.funcoes import aguardar_loading

def preencher_tipo_assinatura(numPortaria):
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

    except:
        print("ERRO: Falha ao preencher tipo de assinatura")
