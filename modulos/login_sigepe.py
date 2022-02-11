from modulos.config import navegador
from modulos.config import halfwait
import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def fazer_login_sigepe():

    navegador.get("https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")

    print('Acessando a página de login do SIGEPE...')

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
        print('Reinicie e tente novamente')
        navegador.quit()
    except:
        nomePaginaPublicacao = navegador.find_element(By.XPATH, '//*[@id="barra-infos"]/div[3]/div')
        print('Página acessada: ', nomePaginaPublicacao.text)
        print()