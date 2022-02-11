from modulos.config import navegador
from modulos.publicador.publicador import textoPortariaFormatado
from modulos.config import wait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.publicador import numPortaria
from selenium.webdriver.common.keys import Keys

# Texto do ato/portaria

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

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

print(numPortaria, '- Texto da portaria preenchido')
