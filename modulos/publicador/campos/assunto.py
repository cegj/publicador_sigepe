from modulos.config import navegador
import time
from modulos.config import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.funcoes import aguardar_loading

def preencher_assunto(temaAssunto, numPortaria):

    try:

        time.sleep(0.3)

        botaoProcurarAssunto = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnSelecionarClassificacaoAssunto"]')))

        botaoProcurarAssunto.click()

        janelaSelecionarAssunto = wait.until(EC.element_to_be_clickable(
            (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:idDlgSelecionarAssunto')))

        time.sleep(0.3)

        navegador.execute_script(
            "document.getElementById('frmCadastrarAto:cadastradorDeAtoParaPublicacao:treeClassificacao_selection').setAttribute('type', 'text');")

        time.sleep(0.3)

        campoNivelTemaOculto = wait.until(EC.element_to_be_clickable(
            (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:treeClassificacao_selection')))

        campoNivelTemaOculto.send_keys(temaAssunto['nivel_assunto'])

        time.sleep(0.3)

        botaoSelecionarAssunto = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnSelecionar"]/span')))

        botaoSelecionarAssunto.click()

        aguardar_loading()

        campoAssuntoPreenchido = wait.until(EC.element_to_be_clickable(
            (By.ID, 'frmCadastrarAto:cadastradorDeAtoParaPublicacao:txtClassificacao')))

        print(numPortaria, '- Assunto selecionado: ',
            campoAssuntoPreenchido.get_attribute("value"))

        time.sleep(0.3)

    except:
        print('ERRO: Falha ao preencher assunto!')