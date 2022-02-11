from modulos.config import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.publicador import numPortaria

campoNumeroAto = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNumeroAto"]')))

campoNumeroAto.send_keys(str(numPortaria))

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

print(numPortaria, '- Número do ato preenchido')
