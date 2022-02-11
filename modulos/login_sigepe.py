from modulos.config import navegador
from modulos.config import halfwait
import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


navegador.get("https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf");

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

botaoAcessar.click()

print('Fazendo login no Sigepe...')

try:
    erroLogin = halfwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="msg_alerta"]')))
    print('ERRO: ', erroLogin.text)
    print('Reinicie e tente novamente')
    navegador.quit()
except:
    nomePaginaPublicacao = halfwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="barra-infos"]/div[3]/div')))
    print('Página acessada: ', nomePaginaPublicacao.text)
    print()