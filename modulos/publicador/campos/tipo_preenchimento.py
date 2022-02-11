from modulos.publicador.valores_configurados import tipoNumero
import time
from modulos.config import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.publicador import numPortaria
from selenium.webdriver.common.keys import Keys

campoTipoNumero = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTipoPreenchimento_label"]')))

campoTipoNumero.click()

time.sleep(0.3)

campoBuscarTipoNumero = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTipoPreenchimento_filter"]')))

campoBuscarTipoNumero.send_keys(tipoNumero)

time.sleep(1)

campoBuscarTipoNumero.send_keys(Keys.ENTER)

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

print(numPortaria, '- Tipo de preenchimento do número selecionado: ',
      campoTipoNumero.text)
