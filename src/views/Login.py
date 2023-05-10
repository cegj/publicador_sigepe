from views import Interfaces as i
from controllers import Acesso as a
from tkinter import *
from tkinter import messagebox
import appConfig
from helpers import checkExistsByXpath as cebx
from helpers import getScreenshotByXpath as gebx
from helpers import goTo as gt
from PIL import ImageTk, Image
import os
from appXpaths import xpaths
from Webdriver import nav

class Login(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.login()

  def login(self):
    def handleEntrar():
      a.Acesso.fazerLogin(cpfInput, senhaInput, captchaInput, self.root)

    loginContainer = Frame(self.root)
    loginContainer.pack()
    loginContainerTitulo = Label(
      loginContainer, text="Entrar no Sigepe",
      font=appConfig.fontes["titulo"])
    loginContainerTitulo.pack()

    gt.goTo("https://admsistema.sigepe.planejamento.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")
    
    cpfContainer = Frame(
      loginContainer,
      pady=5)
    cpfContainer.pack()
    cpfLabel = Label(
      cpfContainer,
      text="CPF",
      font=appConfig.fontes["normal"])
    cpfLabel.pack()
    cpfInput = Entry(
      cpfContainer,
      width=20,
      font=appConfig.fontes["normal"])
    cpfInput.pack()

    senhaContainer = Frame(
      loginContainer,
      pady=5)
    senhaContainer.pack()
    senhaLabel = Label(
      senhaContainer,
      text="Senha",
      font=appConfig.fontes["normal"])
    senhaLabel.pack()
    senhaInput = Entry(
      senhaContainer,
      width=20,
      font=appConfig.fontes["normal"],
      show="*")
    senhaInput.pack()

    if(cebx.checkExistsByXpath(xpaths['login']['recaptcha'])):
      messagebox.showerror("Erro fatal", "Não foi possível acessar o Sigepe devido a tentativas sucessivas com erro. Para evitar o bloqueio da sua conta, o Publicador Sigepe será encerrado. Inicie novamente.")
      self.handleFecharJanela()

    captchaInput = None
    if(cebx.checkExistsByXpath(xpaths['login']['captchaImg'])):
        captchaContainer = Frame(
          loginContainer,
          pady=5)
        captchaContainer.pack()
        captchaLabel = Label(
          captchaContainer,
          text="Confirme o código",
          font=appConfig.fontes["normal"])
        captchaLabel.pack()
        imgFileName = gebx.getScreenshotByXpath(xpaths['login']['captchaImg'], 'captcha')
        imgFile = Image.open(imgFileName)
        captchaImg = ImageTk.PhotoImage(imgFile)
        captchaImgLabel = Label(
          captchaContainer,
          image=captchaImg)
        captchaImgLabel.image = captchaImg
        captchaImgLabel.pack()
        os.remove(imgFileName)
        captchaInput = Entry(
          captchaContainer,
          width=20,
          font=appConfig.fontes["normal"])
        captchaInput.pack()

    botaoEntrar = Button(
      loginContainer,
      text="Entrar",
      font=appConfig.fontes["botao"],
      width=12,
      command=handleEntrar)
    botaoEntrar.pack()

    def handleEnter(event = None):
      handleEntrar()

    self.root.bind('<Return>', handleEnter)
    self.root.protocol("WM_DELETE_WINDOW", self.handleFecharJanela)
    self.root.mainloop()

  def handleFecharJanela(self):
    nav.quit()
    self.root.destroy()
