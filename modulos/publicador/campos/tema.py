from modulos.funcoes import obter_tema
from modulos.publicador.publicador import textoPortariaFormatado
from modulos.config import wait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.publicador import numPortaria
from selenium.webdriver.common.keys import Keys

if (obter_tema(textoPortariaFormatado[1])):
    temaAssunto = obter_tema(textoPortariaFormatado[1])
else:
    print('!!!TEMA NÃO IDENTIFICADO!!!')

campoTema = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_label"]')))

campoTema.click()

time.sleep(0.3)

campoBuscarTema = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_filter"]')))

campoBuscarTema.send_keys(temaAssunto['tema'])

time.sleep(1)

if (temaAssunto['arrow_down'] > 0):
    cont = 1
    while cont <= temaAssunto['arrow_down']:
        campoBuscarTema.send_keys(Keys.ARROW_DOWN)
        cont = cont + 1

campoBuscarTema.send_keys(Keys.ENTER)

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

campoTemaPreenchido = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:selTema_label"]')))

print(numPortaria, '- Tema selecionado: ', campoTemaPreenchido.text)
