from modulos.config import wait
from modulos.config import navegador
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modulos.funcoes import aguardar_loading

def preencher_tema(temaAssunto, numPortaria):

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