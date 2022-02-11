from modulos.config import wait
from modulos.publicador.valores_configurados import tipoAssinatura
from modulos.publicador.valores_configurados import dataAssinatura
from modulos.publicador.valores_configurados import dataPublicacao
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.publicador import numPortaria
from selenium.webdriver.common.keys import Keys

# Data de assinatura

if (tipoAssinatura == "Manual"):

    campoDataAssinatura = wait.until(EC.element_to_be_clickable(
        (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataAssinatura_input')))

    cont = 1
    while cont <= 8:
        campoDataAssinatura.send_keys(Keys.BACKSPACE)
        cont = cont + 1

    campoDataAssinatura.send_keys(dataAssinatura)

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    print(numPortaria, '- Data de assinatura preenchida: ', dataAssinatura)

else:
    print(numPortaria, '- Tipo de assinatura é digital. Data de assinatura não é preenchida.')

# Data de publicação

campoDataPublicacao = wait.until(EC.element_to_be_clickable(
    (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptDataParaPublicacao_input')))

campoDataPublicacao.click()

cont = 1
while cont <= 8:
    campoDataPublicacao.send_keys(Keys.BACKSPACE)
    cont = cont + 1

campoDataPublicacao.send_keys(dataPublicacao)

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

print(numPortaria, '- Data da publicação preenchida: ', dataPublicacao)
