from views import Interfaces as i
from controllers import Acesso as a
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
from models import AppConfig as ac
from controllers import Webdriver as wd
from helpers import ThreadWithReturn as thread
from views import SigepeTrabalhando as st

class Login(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.login()

  def login(self):
    def handleEntrar():
      a.Acesso.fazerLogin(cpfInput, senhaInput, captchaInput, self.root)
    t = thread.ThreadWithReturn(target=wd.Webdriver.go, args=(ac.AppConfig.urls["areaDeTrabalho"],))
    t.start()
    working = st.SigepeTrabalhando(t, "Abrindo página de acesso ao Sigepe...")
    t.join()

    loginContainer = Frame(self.root)
    loginContainer.pack()
    loginContainerTitulo = Label(
      loginContainer, text="Entrar no Sigepe",
      font=ac.AppConfig.fontes["titulo"])
    loginContainerTitulo.pack()

    cpfContainer = Frame(
      loginContainer,
      pady=5)
    cpfContainer.pack()
    cpfLabel = Label(
      cpfContainer,
      text="CPF",
      font=ac.AppConfig.fontes["normal"])
    cpfLabel.pack()
    cpfInput = Entry(
      cpfContainer,
      width=20,
      font=ac.AppConfig.fontes["normal"])
    cpfInput.pack()

    senhaContainer = Frame(
      loginContainer,
      pady=5)
    senhaContainer.pack()
    senhaLabel = Label(
      senhaContainer,
      text="Senha",
      font=ac.AppConfig.fontes["normal"])
    senhaLabel.pack()
    senhaInput = Entry(
      senhaContainer,
      width=20,
      font=ac.AppConfig.fontes["normal"],
      show="*")
    senhaInput.pack()

    if(wd.Webdriver.checkExistsByXpath(ac.AppConfig.xpaths['login']['recaptcha'])):
      messagebox.showerror("Erro fatal", "Não foi possível acessar o Sigepe devido a tentativas sucessivas com erro. Para evitar o bloqueio da sua conta, o Publicador Sigepe será encerrado. Inicie novamente.")
      self.handleFecharJanela()

    captchaInput = None
    if(wd.Webdriver.checkExistsByXpath(ac.AppConfig.xpaths['login']['captchaImg'])):
        captchaContainer = Frame(
          loginContainer,
          pady=5)
        captchaContainer.pack()
        captchaLabel = Label(
          captchaContainer,
          text="Confirme o código",
          font=ac.AppConfig.fontes["normal"])
        captchaLabel.pack()
        imgFileName = wd.Webdriver.getScreenshotByXpath(ac.AppConfig.xpaths['login']['captchaImg'], 'captcha')
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
          font=ac.AppConfig.fontes["normal"])
        captchaInput.pack()

    botaoEntrar = Button(
      loginContainer,
      text="Entrar",
      font=ac.AppConfig.fontes["botao"],
      width=12,
      command=handleEntrar)
    botaoEntrar.pack()

    infoLabel = ttk.Label(
      loginContainer,
      text="Para iniciar o Publicador, entre com o seu\nusuário e senha do Sigepe/Sigac.",
      background="#fff9d9",
      foreground="#85701d",
      padding=4,
      justify=CENTER)
    infoLabel.pack(pady="8")

    def handleEnter(event = None):
      handleEntrar()

    self.root.bind('<Return>', handleEnter)
    self.root.protocol("WM_DELETE_WINDOW", self.handleFecharJanela)
    self.root.mainloop()

  def handleFecharJanela(self):
    wd.Webdriver.nav.quit()
    self.root.destroy()
