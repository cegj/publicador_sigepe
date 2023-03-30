from tkinter import *
from tkinter import messagebox
from selenium.webdriver.common.by import By
from helpers import checkExistsByXpath as cebx
from helpers import getScreenshotByXpath as gebx
from controllers import Interfaces as i
from Webdriver import nav
from Master import master

class Usuario:
    def __init__(self):
        pass

    @staticmethod
    def fazerLogin(cpfInput, senhaInput, captchaInput, loginContainer):
        try:
            cpf = cpfInput.get()
            senha = senhaInput.get()
            campoUsuario = nav.find_element(
                By.XPATH, '//*[@id="cpfUsuario"]')
            campoUsuario.click()
            campoUsuario.send_keys(cpf)
            campoSenha = nav.find_element(By.XPATH, '//*[@id="password"]')
            campoSenha.click()
            campoSenha.send_keys(senha)

            if(cebx.checkExistsByXpath('//*[@id="captchaImg"]')):
                captcha = captchaInput.get()
                campoCaptcha = nav.find_element(By.XPATH, '//*[@id="j_captcha_response"]')
                campoCaptcha.click()
                campoCaptcha.send_keys(captcha)

            botaoAcessar = nav.find_element(
                By.XPATH, '//*[@id="botaoCredenciais"]')
            botaoAcessar.click()

            if (cebx.checkExistsByXpath('//*[@id="msg_alerta"]')):
                erroLogin = nav.find_element(By.XPATH, '//*[@id="msg_alerta"]')
                raise Exception('Mensagem do Sigepe: ' + erroLogin.text)

            if (cebx.checkExistsByXpath('//*[@id="content-title"]/span')):
                erroLogin = nav.find_element(By.XPATH, '//*[@id="content-title"]/span')
                if (erroLogin.text == "Primeiro Acesso - Identificação de Usuário"):
                    raise Exception("Mensagem do Sigepe: Usuário foi identificado como primeiro acesso. Verifique se o CPF foi preenchido corretamente ou faça o seu cadastro no Sigepe.")
                else:
                    raise Exception('Mensagem do Sigepe: ' + erroLogin.text)
                return False

            loginContainer.destroy()
            messagebox.showinfo("Sucesso", "O acesso ao Sigepe foi realizado com sucesso")
            return True

        except Exception as e:
            messagebox.showerror("Erro", e)
            loginContainer.destroy()
            i.Interfaces.login()




            


# def fazer_login():

#     def acessar_pagina_login():

#         navegador.get(
#             "https://admsistema.sigepe.planejamento.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")

#         tituloPagina = navegador.title

#         return tituloPagina

#     def configurar_habilitacao():

#         habilitacaoConfig = configJson['config']['habilitacao_sigepe']

#         habilitacaoAtual = navegador.find_element(
#             By.XPATH, '//*[@id="j_idt62:habDisponiveisLabel"]')

#         print('Habilitação atual:', habilitacaoAtual.text)

#         if (habilitacaoAtual.text != str(habilitacaoConfig)):
#             habilitacaoAtual.click()
#             habilitacao = navegador.find_element(
#                 By.XPATH, str("//*[text()='" + habilitacaoConfig + "']"))
#             habilitacao.click()
#             time.sleep(0.5)
#             novaHabilitacao = halfwait.until(EC.visibility_of_element_located(
#                 (By.XPATH, '//*[@id="j_idt62:habDisponiveisLabel"]')))
#             print('Habilitação alterada para:', novaHabilitacao.text)

#     acessar_pagina_login()

#     sucesso = False

#     while (sucesso == False):

#         print('Informe seus dados para faze login no SIGEPE: \n')

#         usuario = input('CPF do usuário (somente números): ')

#         senha = getpass.getpass('Senha do SIGEPE: ')

#         print('Aguarde...')

#         campoUsuario = navegador.find_element(
#             By.XPATH, '//*[@id="cpfUsuario"]')

#         campoUsuario.click()

#         campoUsuario.send_keys(usuario)

#         campoSenha = navegador.find_element(By.XPATH, '//*[@id="password"]')

#         campoSenha.click()

#         campoSenha.send_keys(senha)

#         botaoAcessar = navegador.find_element(
#             By.XPATH, '//*[@id="botaoCredenciais"]')

#         botaoAcessar.click()

#         if (navegador.find_element(By.XPATH, '//*[@id="idBreadCrumb0"]/span')):

#             paginaAtual = navegador.find_element(
#                 By.XPATH, '//*[@id="idBreadCrumb0"]/span')

#             print('Você está em:', paginaAtual.text)

#             configurar_habilitacao()

#             navegador.get(
#                 "https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")

#             paginaAtual = navegador.find_element(
#                 By.XPATH, '//*[@id="idBreadCrumb4"]/span')

#             print('Você está em:', paginaAtual.text, '\n')

#             print_sucesso('Acesso ao Sigepe realizado')

#             sucesso = True

#         elif(navegador.find_element(By.XPATH, '//*[@id="msg_alerta"]')):

#             erroLogin = navegador.find_element(
#                 By.XPATH, '//*[@id="msg_alerta"] \n')

#             print_erro(erroLogin.text + '. Tente novamente.')

#             sucesso = False

#         else:

#             print(
#                 'Não foi possível fazer login (erro não identificado). Tente novamente. \n')

#             sucesso = False
