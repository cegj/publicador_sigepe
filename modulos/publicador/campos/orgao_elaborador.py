from modulos.config import navegador
from modulos.config import wait
from modulos.publicador.valores_configurados import upag
from modulos.publicador.valores_configurados import uorg
from modulos.publicador.valores_configurados import responsavelAssinatura
from modulos.publicador.valores_configurados import cargoResponsavelAssinatura
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.publicador import numPortaria
from selenium.webdriver.common.keys import Keys

print(numPortaria, '- Iniciando preenchimento do órgão/autoridade...')

# Há dois modelos de janela para selecionar uorg/upag/autoridade no SIGEPE

try:  # Gatilho para modelo novo é o XPATH do botão para abrir janela, pois são diferentes
    botaoIncluirOrgaoElabAnt = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt395"]/span')))

    print(numPortaria, '- [obs:] Cadastro pelo modelo antigo de janela')

    botaoIncluirOrgaoElabAnt.click()

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    campoUpag = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadePagadora_label"]')))

    campoUpag.click()

    time.sleep(0.3)

    campoBuscarUpag = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadePagadora_filter"]')))

    campoBuscarUpag.send_keys(upag)

    time.sleep(1)

    campoBuscarUpag.send_keys(Keys.ENTER)

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    print(numPortaria, '- UPAG preenchida: ', campoUpag.text)

    time.sleep(0.5)

    campoUorg = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadeOrganizacional_label"]')))

    campoUorg.click()

    time.sleep(0.5)

    campoBuscarUorg = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:sltUnidadeOrganizacional_filter"]')))

    campoBuscarUorg.send_keys(uorg)

    time.sleep(1.5)

    campoBuscarUorg.send_keys(Keys.ENTER)

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    print(numPortaria, '- UORG preenchido: ', campoUorg.text)

    campoResponsavelAssinatura = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptNomeResponsavel"]')))

    campoResponsavelAssinatura.send_keys(responsavelAssinatura)

    campoCargoResponsavelAssinatura = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:iptCargoResponsavel"]')))

    campoCargoResponsavelAssinatura.send_keys(cargoResponsavelAssinatura)

    botaoGravarOrgao = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt699"]/span')))

    botaoGravarOrgao.click()

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

except:
    botaoIncluirOrgaoElab = navegador.find_element(
        By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:j_idt396"]')

    print(numPortaria, '- [obs:] Cadastro pelo novo modelo de janela')

    botaoIncluirOrgaoElab.click()

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    janelaOrgaosElaboradores = wait.until(EC.element_to_be_clickable(
        (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:dlgIncluirOrgaoElaborador')))

    campoUpag = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt446_label"]')))

    campoUpag.click()

    time.sleep(5)

    campoBuscarUpag = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt446_filter"]')))

    campoBuscarUpag.send_keys(upag)

    time.sleep(1.5)

    campoBuscarUpag.send_keys(Keys.ENTER)

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    print(numPortaria, '- UPAG preenchida: ', campoUpag.text)

    campoUorg = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt453_label"]')))

    campoUorg.click()

    time.sleep(5)

    campoBuscarUorg = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt453_filter"]')))

    campoBuscarUorg.send_keys(uorg)

    time.sleep(1.5)

    campoBuscarUorg.send_keys(Keys.ENTER)

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    print(numPortaria, '- UORG preenchido: ', campoUorg.text)

    campoResponsavelAssinatura = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt434:j_idt463"]')))

    campoResponsavelAssinatura.send_keys(responsavelAssinatura)

    botaoPesquisarAutoridade = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt492"]/span')))

    botaoPesquisarAutoridade.click()

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    radiusSelecionarAutoridade = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt494:dataTableResultado_data"]/tr/td[1]/div/div/div[2]/span')))

    radiusSelecionarAutoridade.click()

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    botaoSelecionarAutoridade = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:seletorResponsavel:j_idt538"]/span')))

    botaoSelecionarAutoridade.click()

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

responsavelAssinaturaSelecionado = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:tblResponsaveis:0:j_idt416:txtContent"]')))

CargoResponsavelAssinaturaSelecionado = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:tblResponsaveis:0:j_idt418:txtContent"]')))

print(numPortaria, '- Responsável pela assinatura preenchido: ',
    responsavelAssinaturaSelecionado.text, " - ", CargoResponsavelAssinaturaSelecionado.text)
