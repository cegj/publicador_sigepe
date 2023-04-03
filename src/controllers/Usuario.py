from tkinter import *
from tkinter import messagebox
from selenium.webdriver.common.by import By
from helpers import checkExistsByXpath as cebx
from helpers import getScreenshotByXpath as gebx
from controllers.interfaces import Sessao as s
from Webdriver import nav
from appXpaths import xpaths

class Usuario:
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
                raise Exception('Mensagem do Sigepe: ' + erroLogin.text)

            if (cebx.checkExistsByXpath(xpaths['login']['novoUsuarioPageTitle'])):
                erroLogin = nav.find_element(By.XPATH, xpaths['login']['novoUsuarioPageTitle'])
                if (erroLogin.text == "Primeiro Acesso - Identificação de Usuário"):
                    raise Exception("Mensagem do Sigepe: Usuário foi identificado como primeiro acesso. Verifique se o CPF foi preenchido corretamente ou faça o seu cadastro no Sigepe.")
                else:
                    raise Exception('Mensagem do Sigepe: ' + erroLogin.text)
                return False

            loginContainer.destroy()
            # messagebox.showinfo("Sucesso", "O acesso ao Sigepe foi realizado com sucesso")
            sessao = s.Sessao()
            sessao.sessao()
            return True

        except Exception as e:
            messagebox.showerror("Erro", e)
            loginContainer.destroy()
            i.Interfaces.login()