from modulos.funcoes import obter_siape
from modulos.publicador.publicador import textoPortaria
from modulos.config import navegador
from modulos.config import wait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.publicador import numPortaria

siapeInteressado = obter_siape(textoPortaria)

print(numPortaria, '- Interessado identificado: ', siapeInteressado)
print('Iniciando busca e preenchimento do interessado...')

botaoAbrirInteressados = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt1415"]/span')))

botaoAbrirInteressados.click()

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

campoMatricula = wait.until(EC.element_to_be_clickable(
    (By.ID,  'frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt434:j_idt466')))

campoMatricula.click()

time.sleep(0.2)

campoMatricula.send_keys(str(siapeInteressado))

botaoPesquisarInteressado = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt492"]/span')))

botaoPesquisarInteressado.click()

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

checkboxSelecionarServidor = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt494:dataTableResultado:j_idt499"]/div/div/div[2]')))

checkboxSelecionarServidor.click()

# Função .click() do Selenium não está funcionando nessos botões abaixo. Usando Javascript:

time.sleep(0.3)

navegador.execute_script(
    "botaoIncluirServidor = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt494:j_idt517');")

navegador.execute_script("botaoIncluirServidor.click();")

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

botaoSelecionarServidor = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt538"]/span')))

navegador.execute_script(
    "botaoSelecionarServidor = document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorInteressado:j_idt538');")

navegador.execute_script("botaoSelecionarServidor.click();")

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

nomeServidorCadastrado = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:tblInteressados:0:j_idt1427:txtContent"]')))

print(numPortaria, '- Servidor interessado cadastrado: ',
      str(siapeInteressado), '-', nomeServidorCadastrado.text)
