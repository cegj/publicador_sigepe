from tkinter import *
import appConfig
from helpers import checkExistsByXpath as cebx
from helpers import getScreenshotByXpath as gebx
from PIL import ImageTk, Image
from controllers import Usuario
from Webdriver import nav
from Master import master
import os

class Interfaces:
  @staticmethod
  def login():
    loginContainer = Frame(master)
    loginContainer.pack()
    loginContainerTitle = Label(loginContainer, text="Fazer login no Sigepe")
    loginContainerTitle["font"] = appConfig.fontes["titulo"]
    loginContainerTitle.pack ()

    nav.get("https://admsistema.sigepe.planejamento.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")
    
    cpfContainer = Frame(loginContainer)
    cpfContainer["pady"] = 5
    cpfContainer.pack()
    cpfLabel = Label(cpfContainer,text="CPF", font=appConfig.fontes["normal"])
    cpfLabel.pack()
    cpfInput = Entry(cpfContainer)
    cpfInput["width"] = 20
    cpfInput["font"] = appConfig.fontes["normal"]
    cpfInput.pack()

    senhaContainer = Frame(loginContainer)
    senhaContainer["pady"] = 5
    senhaContainer.pack()
    senhaLabel = Label(senhaContainer,text="Senha", font=appConfig.fontes["normal"])
    senhaLabel.pack()
    senhaInput = Entry(senhaContainer)
    senhaInput["width"] = 20
    senhaInput["font"] = appConfig.fontes["normal"]
    senhaInput["show"] = "*"
    senhaInput.pack()

    captchaInput = None
    if(cebx.checkExistsByXpath('//*[@id="captchaImg"]')):
        captchaContainer = Frame(loginContainer)
        captchaContainer["pady"] = 5
        captchaContainer.pack()
        captchaLabel = Label(captchaContainer, text="Confirme o código", font=appConfig.fontes["normal"])
        imgFileName = gebx.getScreenshotByXpath('//*[@id="captchaImg"]')
        imgFile = Image.open(imgFileName)
        captchaImg = ImageTk.PhotoImage(imgFile)
        captchaImg = Label(captchaContainer, image = captchaImg)
        captchaImg.image = captchaImg
        captchaImg.pack()
        os.remove(imgFileName)
        captchaInput = Entry(captchaContainer)
        captchaInput["width"] = 20
        captchaInput["font"] = appConfig.fontes["normal"]
        captchaInput.pack()

    botaoLogin = Button(loginContainer)
    botaoLogin["text"] = "Autenticar"
    botaoLogin["font"] = ("Segoe UI", "10")
    botaoLogin["width"] = 12
    botaoLogin["command"] = lambda: Usuario.Usuario.fazerLogin(cpfInput, senhaInput, captchaInput, loginContainer)
    botaoLogin.pack()
