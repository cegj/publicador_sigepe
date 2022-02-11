from modulos.config import wait
from modulos.publicador.valores_configurados import especie
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modulos.funcoes import aguardar_loading

def preencher_especie(numPortaria):
    campoEspecie = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selEspecie_label"]')))

    campoEspecie.click()

    time.sleep(0.3)

    campoBuscarEspecie = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selEspecie_filter"]')))

    campoBuscarEspecie.send_keys(especie)

    time.sleep(1.5)

    campoBuscarEspecie.send_keys(Keys.ENTER)

    aguardar_loading()

    print(numPortaria, '- Espécie selecionada: ', campoEspecie.text)
