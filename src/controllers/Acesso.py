from tkinter import *
from tkinter import messagebox
from selenium.webdriver.common.by import By
from controllers import Webdriver as wd
from views import Sessao as s
from views import Login as l
from views import Habilitacao as h
from controllers import AppConfig as ac
from controllers import UserConfig as uc
import time
from selenium.webdriver.support import expected_conditions as EC

class Acesso:
    def __init__(self):
        pass

    @staticmethod
    def fazerLogin(cpfInput, senhaInput, captchaInput, loginContainer):
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

            if (wd.Webdriver.checkExistsByXpath('//*[@id="msg_alerta"]')):
                erroLogin = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['login']['loginError'])
                raise Exception(erroLogin.text)

            if (wd.Webdriver.checkExistsByXpath(ac.AppConfig.xpaths['login']['novoUsuarioPageTitle'])):
                erroLogin = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['login']['novoUsuarioPageTitle'])
                if (erroLogin.text == "Primeiro Acesso - Identificação de Usuário"):
                    raise Exception("Usuário foi identificado como de primeiro acesso. Verifique se o CPF foi preenchido corretamente ou faça o seu cadastro no Sigepe.")
                else:
                    raise Exception(erroLogin.text)
                return False

            loginContainer.destroy()
            Acesso.definirHabilitacaoInicial()
            if (h.Habilitacao.checarAcessoHabilitacao()):
                sessao = s.Sessao()
                sessao.sessao()
            else:
                messagebox.showinfo("Habilitação sem acesso", "A habilitação definida pelo Sigepe não tem acesso ao módulo Publicação. Selecione uma nova habilitação para continuar.")
                seletorHabilitacao = h.Habilitacao();

            return True

        except Exception as e:
            messagebox.showerror("Erro ao realizar acesso", e)
            loginContainer.destroy()
            l.Login()
    
    @staticmethod
    def definirHabilitacaoInicial():
        try:
            userConfig = uc.UserConfig.obterConfiguracoesSalvas()
            sigepe_habilitacaoBotao = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['habilitacao']['habilitacaoBotao'])
            sigepe_habilitacaoBotao.click()
            xPathHabInicial = f"//*[contains(text(), '{userConfig['habilitacao']['inicial']}')]"
            if (wd.Webdriver.checkExistsByXpath(xPathHabInicial)):
                sigepe_novaHabilitacaoBotao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
                (By.XPATH, xPathHabInicial)))
                sigepe_novaHabilitacaoBotao.click()
                wd.Webdriver.waitLoadingModal()
                time.sleep(2)
            else:
                messagebox.showinfo("Não foi possível definir habilitação inicial", f"A habilitação salva nas suas configurações ({userConfig['habilitacao']['inicial']}) está indisponível ou não existe. O Publicador será iniciado com a habilitação definida pelo Sigepe.")
        except Exception as e:
            messagebox.showerror("Erro ao definir habilitação inicial", e)