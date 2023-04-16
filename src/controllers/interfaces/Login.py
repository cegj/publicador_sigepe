from controllers import Interfaces as i
from controllers import Acesso as a
from tkinter import *
import appConfig
from helpers import checkExistsByXpath as cebx
from helpers import getScreenshotByXpath as gebx
from helpers import goTo as gt
from PIL import ImageTk, Image
# from controllers import Acesso as a
import os
from appXpaths import xpaths

class Login(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.login()

  def login(self):
    loginContainer = Frame(self.root)
    loginContainer.pack()
    loginContainerTitulo = Label(loginContainer, text="Entrar no Sigepe")
    loginContainerTitulo["font"] = appConfig.fontes["titulo"]
    loginContainerTitulo.pack ()

    gt.goTo("https://admsistema.sigepe.planejamento.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")
    
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
    if(cebx.checkExistsByXpath(xpaths['login']['captchaImg'])):
        captchaContainer = Frame(loginContainer)
        captchaContainer["pady"] = 5
        captchaContainer.pack()
        captchaLabel = Label(captchaContainer, text="Confirme o código", font=appConfig.fontes["normal"])
        imgFileName = gebx.getScreenshotByXpath(xpaths['login']['captchaImg'], 'captcha')
        imgFile = Image.open(imgFileName)
        captchaImg = ImageTk.PhotoImage(imgFile)
        captchaImgLabel = Label(captchaContainer, image = captchaImg)
        captchaImgLabel.image = captchaImg
        captchaImgLabel.pack()
        # os.remove(imgFileName)
        captchaInput = Entry(captchaContainer)
        captchaInput["width"] = 20
        captchaInput["font"] = appConfig.fontes["normal"]
        captchaInput.pack()

    botaoLogin = Button(loginContainer)
    botaoLogin["text"] = "Entrar"
    botaoLogin["font"] = appConfig.fontes["botao"]
    botaoLogin["width"] = 12
    botaoLogin["command"] = lambda: a.Acesso.fazerLogin(cpfInput, senhaInput, captchaInput, self.root)
    botaoLogin.pack()

    def handleEnter(event = None):
      a.Acesso.fazerLogin(cpfInput, senhaInput, captchaInput, self.root)

    self.root.bind('<Return>', handleEnter)
    self.root.mainloop()