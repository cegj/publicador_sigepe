from modulos.config import navegador
from modulos.config import wait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modulos.funcoes import aguardar_loading


# Texto do ato/portaria

def preencher_texto_ato(textoPortariaFormatado, numPortaria):
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
