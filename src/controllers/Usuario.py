from tkinter import *
import appConfig
from selenium.webdriver.common.by import By

class Usuario:
    def __init__(self, nav):
        self.appConfig = appConfig.AppConfig()
        self.nav = nav
        self.cpf = ""
        self.senha = ""

    def exibirTelaLogin(self, master=None):
        self.loginContainer = Frame(master)
        self.loginContainer.pack()
        self.loginContainerTitle = Label(self.loginContainer, text="Fazer login no Sigepe")
        self.loginContainerTitle["font"] = self.appConfig.fontes["titulo"]
        self.loginContainerTitle.pack ()

        self.cpfContainer = Frame(self.loginContainer)
        self.cpfContainer["pady"] = 5
        self.cpfContainer.pack()
        self.cpfLabel = Label(self.cpfContainer,text="CPF", font=self.appConfig.fontes["normal"])
        self.cpfLabel.pack()
        self.cpfInput = Entry(self.cpfContainer)
        self.cpfInput["width"] = 20
        self.cpfInput["font"] = self.appConfig.fontes["normal"]
        self.cpfInput.pack()

        self.senhaContainer = Frame(self.loginContainer)
        self.senhaContainer["pady"] = 5
        self.senhaContainer.pack()
        self.senhaLabel = Label(self.senhaContainer,text="Senha", font=self.appConfig.fontes["normal"])
        self.senhaLabel.pack()
        self.senhaInput = Entry(self.senhaContainer)
        self.senhaInput["width"] = 20
        self.senhaInput["font"] = self.appConfig.fontes["normal"]
        self.senhaInput["show"] = "*"
        self.senhaInput.pack()

        self.botaoLogin = Button(self.loginContainer)
        self.botaoLogin["text"] = "Autenticar"
        self.botaoLogin["font"] = ("Segoe UI", "10")
        self.botaoLogin["width"] = 12
        self.botaoLogin["command"] = self.fazerLogin
        self.botaoLogin.pack()

    def fazerLogin(self):
        self.cpf = self.cpfInput.get()
        self.senha = self.senhaInput.get()
        self.nav.get("https://admsistema.sigepe.planejamento.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")
        campoUsuario = self.nav.find_element(
            By.XPATH, '//*[@id="cpfUsuario"]')
        campoUsuario.click()
        campoUsuario.send_keys(self.cpf)
        campoSenha = self.nav.find_element(By.XPATH, '//*[@id="password"]')
        campoSenha.click()
        campoSenha.send_keys(self.senha)
        botaoAcessar = self.nav.find_element(
            By.XPATH, '//*[@id="botaoCredenciais"]')
        botaoAcessar.click()

        if(self.nav.find_element(By.XPATH, '//*[@id="msg_alerta"]')):
            erroLogin = self.nav.find_element(By.XPATH, '//*[@id="msg_alerta"]')

            self.errorContainer = Frame(self.loginContainer)
            self.errorMsg = Label(self.errorContainer, text=erroLogin.text)
            print(erroLogin.text)
            self.errorMsg.pack()

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
