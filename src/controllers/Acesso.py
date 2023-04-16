from tkinter import *
from tkinter import messagebox
from selenium.webdriver.common.by import By
from helpers import checkExistsByXpath as cebx
from helpers import getScreenshotByXpath as gebx
from controllers.interfaces import Sessao as s
from Webdriver import nav
from appXpaths import xpaths
from controllers.interfaces import Login as l
from controllers.interfaces import Habilitacao as h
from controllers import UserConfig as uc
import time

class Acesso:
    def __init__(self):
        pass

    @staticmethod
    def fazerLogin(cpfInput, senhaInput, captchaInput, loginContainer):
        try:
            cpf = cpfInput.get()
            senha = senhaInput.get()
            campoUsuario = nav.find_element(By.XPATH, xpaths['login']['usuarioInput'])
            campoUsuario.click()
            campoUsuario.send_keys(cpf)
            campoSenha = nav.find_element(By.XPATH, xpaths['login']['senhaInput'])
            campoSenha.click()
            campoSenha.send_keys(senha)

            if(cebx.checkExistsByXpath('//*[@id="captchaImg"]')):
                captcha = captchaInput.get()
                campoCaptcha = nav.find_element(By.XPATH, xpaths['login']['captchaInput'])
                campoCaptcha.click()
                campoCaptcha.send_keys(captcha)

            botaoAcessar = nav.find_element(By.XPATH, xpaths['login']['acessarBnt'])
            botaoAcessar.click()

            if (cebx.checkExistsByXpath('//*[@id="msg_alerta"]')):
                erroLogin = nav.find_element(By.XPATH, xpaths['login']['loginError'])
                raise Exception(erroLogin.text)

            if (cebx.checkExistsByXpath(xpaths['login']['novoUsuarioPageTitle'])):
                erroLogin = nav.find_element(By.XPATH, xpaths['login']['novoUsuarioPageTitle'])
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
            sigepe_habilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['habilitacaoBotao'])
            sigepe_habilitacaoBotao.click()
            xPathHabInicial = f"//*[contains(text(), '{userConfig['habilitacao']['inicial']}')]"
            if (cebx.checkExistsByXpath(xPathHabInicial)):
                sigepe_novaHabilitacaoBotao = wait["regular"].until(EC.element_to_be_clickable(
                (By.XPATH, xPathHabInicial)))
                sigepe_novaHabilitacaoBotao.click()
                wfl.waitForLoading()
                time.sleep(2)
            else:
                messagebox.showinfo("Não foi possível definir habilitação inicial", f"A habilitação salva nas suas configurações ({userConfig['habilitacao']['inicial']}) está indisponível ou não existe. O Publicador será iniciado com a habilitação definida pelo Sigepe.")
        except Exception as e:
            messagebox.showerror("Erro ao definir habilitação inicial", e)