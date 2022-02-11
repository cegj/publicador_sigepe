from modulos.publicador.valores_configurados import tipoAssinatura
from modulos.config import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.publicador.publicador import numPortaria

tipoAssinaturaDigital = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:radTipoAssinatura"]/tbody/tr/td[2]/label')))
tipoAssinaturaManual = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:radTipoAssinatura"]/tbody/tr/td[4]/label')))

if (tipoAssinatura == "Manual"):
    tipoAssinaturaManual.click()
elif (tipoAssinatura == "Digital"):
    tipoAssinaturaDigital.click()

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

print(numPortaria, '- Tipo assinatura selecionado:', tipoAssinatura)

modalAguarde = wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))
