from tkinter import *
from tkinter import messagebox
from selenium.webdriver.common.by import By
from controllers import Webdriver as wd
from views import Sessao as s
from views import Login as l
from views import Habilitacao as h
from models import AppConfig as ac
from models import UserConfig as uc
import time
from selenium.webdriver.support import expected_conditions as EC
from helpers import ThreadWithReturn as thread
from views import SigepeTrabalhando as st

class Acesso:
    def __init__(self):
        pass

    @staticmethod
    def fazerLogin(cpfInput, senhaInput, captchaInput, loginContainer):
        t = thread.ThreadWithReturn(target=Acesso.loginNoSigepe, args=(cpfInput, senhaInput, captchaInput, loginContainer))
        t.start()
        working = st.SigepeTrabalhando(t, "Entrando no Sigepe...")
        loginResult = t.join()
        if (loginResult[0]):
            loginContainer.destroy()
            t = thread.ThreadWithReturn(target=Acesso.definirHabilitacaoInicial)
            t.start()
            working = st.SigepeTrabalhando(t, "Configurando habilitação inicial...", True)
            habilitacaoInicialResult = t.join()
            t = thread.ThreadWithReturn(target=h.Habilitacao.checarAcessoHabilitacao)
            t.start()
            working = st.SigepeTrabalhando(t, "Verificando se habilitação inicial tem acesso ao módulo de Publicação...", True)
            habilitacaoValida = t.join()
            if (habilitacaoValida):
                sessao = s.Sessao()
                sessao.sessao()
            else:
                seletorHabilitacao = h.Habilitacao();
        if (not loginResult[0]):
            messagebox.showerror("Erro ao realizar acesso", loginResult[1])
            loginContainer.destroy()
            l.Login()

    @staticmethod
    def loginNoSigepe(cpfInput, senhaInput, captchaInput, loginContainer):
        try:
            cpf = cpfInput.get()
            senha = senhaInput.get()
            campoUsuario = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['login']['usuarioInput'])
            campoUsuario.click()
            campoUsuario.send_keys(cpf)
            campoSenha = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['login']['senhaInput'])
            campoSenha.click()
            campoSenha.send_keys(senha)

            if(wd.Webdriver.checkExistsByXpath('//*[@id="captchaImg"]')):
                captcha = captchaInput.get()
                campoCaptcha = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['login']['captchaInput'])
                campoCaptcha.click()
                campoCaptcha.send_keys(captcha)

            botaoAcessar = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['login']['acessarBnt'])
            botaoAcessar.click()

            checkLoadErrors = wd.Webdriver.checkErrorsLoadedPage() 
            if(not checkLoadErrors[0]):
                raise Exception(checkLoadErrors[1])

            if (wd.Webdriver.checkExistsByXpath('//*[@id="msg_alerta"]')):
                erroLogin = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['login']['loginError'])
                raise Exception(erroLogin.text)

            if (wd.Webdriver.checkExistsByXpath(ac.AppConfig.xpaths['login']['novoUsuarioPageTitle'])):
                erroLogin = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['login']['novoUsuarioPageTitle'])
                if (erroLogin.text == "Primeiro Acesso - Identificação de Usuário"):
                    raise Exception("Usuário foi identificado como de primeiro acesso. Verifique se o CPF foi preenchido corretamente ou faça o seu cadastro no Sigepe.")
                else:
                    raise Exception(erroLogin.text)
                return [False]
            return [True]
        except Exception as e:
            return [False, e]
    
    @staticmethod
    def definirHabilitacaoInicial():
        try:
            userConfig = uc.UserConfig.obterConfiguracoesSalvas()
            if (userConfig['habilitacao']['inicial'] != ""):
                sigepe_habilitacaoBotao = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['habilitacao']['habilitacaoBotao'])
                sigepe_habilitacaoBotao.click()
                xPathHabInicial = f"//*[contains(text(), '{userConfig['habilitacao']['inicial']}')]"
                if (wd.Webdriver.checkExistsByXpath(xPathHabInicial)):
                    sigepe_novaHabilitacaoBotao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
                    (By.XPATH, xPathHabInicial)))
                    sigepe_novaHabilitacaoBotao.click()
                    wd.Webdriver.waitLoadingModal()
                    time.sleep(2)
                    return [True]
                else:
                    raise Exception(f"A habilitação salva nas suas configurações ({userConfig['habilitacao']['inicial']}) está indisponível ou não existe. O Publicador será iniciado com a habilitação definida pelo Sigepe.")
            else:
                raise Exception("Não há uma habilitação salva nas suas configurações do Publicador.")
        except Exception as e:
                return [False, e]
