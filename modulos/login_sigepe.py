from modulos.config import navegador, config_json, halfwait
from modulos.funcoes import limpar_quebras_linha
import getpass
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def fazer_login_sigepe():

    print('Acessando a página de login do SIGEPE...')

    navegador.get("https://admsistema.sigepe.planejamento.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")

    tituloPagina = navegador.title

    print('Você está em:', tituloPagina)

    usuario = input('CPF do usuário (somente números): ')

    senha = getpass.getpass('Senha do SIGEPE: ')

    campoUsuario = navegador.find_element(By.XPATH, '//*[@id="cpfUsuario"]')

    campoUsuario.click()

    campoUsuario.send_keys(usuario)

    campoSenha = navegador.find_element(By.XPATH, '//*[@id="password"]')

    campoSenha.click()

    campoSenha.send_keys(senha)

    botaoAcessar = navegador.find_element(By.XPATH, '//*[@id="botaoCredenciais"]')

    print('Fazendo login no Sigepe...')

    botaoAcessar.click()

    try:
        erroLogin = navegador.find_element(By.XPATH, '//*[@id="msg_alerta"]')
        print('ERRO: ', erroLogin.text)
        print('Encerre e tente novamente')
        navegador.quit()
    except:
        paginaAtual = navegador.find_element(By.XPATH, '//*[@id="idBreadCrumb0"]/span')
        print('Você está em:', paginaAtual.text)

        habilitacaoConfig = config_json['config']['habilitacao_sigepe']

        habilitacaoAtual = navegador.find_element(By.XPATH, '//*[@id="j_idt62:habDisponiveisLabel"]')

        print('Habilitação atual:', habilitacaoAtual.text)

        if (habilitacaoAtual.text != str(habilitacaoConfig)):
            habilitacaoAtual.click()
            habilitacao = navegador.find_element(By.XPATH, str("//*[text()='" + habilitacaoConfig + "']"))
            habilitacao.click()
            time.sleep(0.5)
            novaHabilitacao = halfwait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="j_idt62:habDisponiveisLabel"]')))
            print('Habilitação alterada para:', novaHabilitacao.text)

        time.sleep(0.5)

        navegador.get("https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")
        paginaAtual = navegador.find_element(By.XPATH, '//*[@id="idBreadCrumb4"]/span')
        print('Você está em:', paginaAtual.text)
        print()
        print('Acesso realizado com sucesso')