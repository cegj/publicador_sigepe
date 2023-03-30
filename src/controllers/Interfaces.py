from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import appConfig
from helpers import checkExistsByXpath as cebx
from helpers import getScreenshotByXpath as gebx
from PIL import ImageTk, Image
from controllers import Usuario
from Webdriver import nav
import os

class Interfaces:

  def novaJanela():
    master = Tk()
    master.title(appConfig.appTitulo)
    master["padx"] = appConfig.pad["x"]
    master["pady"] = appConfig.pad["y"]
    return master

  @staticmethod
  def login():
    master = Interfaces.novaJanela()
    loginContainer = Frame(master)
    loginContainer.pack()
    loginContainerTitulo = Label(loginContainer, text="Fazer login no Sigepe")
    loginContainerTitulo["font"] = appConfig.fontes["titulo"]
    loginContainerTitulo.pack ()

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
    botaoLogin["command"] = lambda: Usuario.Usuario.fazerLogin(cpfInput, senhaInput, captchaInput, master)
    botaoLogin.pack()

    master.mainloop()

  @staticmethod
  def sessao():
    master = Interfaces.novaJanela()
    master.geometry('400x200')
    sessaoContainer = Frame(master)
    sessaoContainer.pack()
    sessaoContainerTitulo = Label(sessaoContainer, text="Publicar documentos")
    sessaoContainerTitulo["font"] = appConfig.fontes["titulo"]
    sessaoContainerTitulo.pack ()

    habilitacaoContainer = Frame(master)
    habilitacaoContainer.pack()
    label = ttk.Label(habilitacaoContainer, text="Selecione a habilitação:")
    label.pack()
    habilitacaoSelecionada = StringVar()
    seletorHabilitacoes = ttk.Combobox(habilitacaoContainer, textvariable=habilitacaoSelecionada)
    seletorHabilitacoes['values'] = ('GESTOR - UNIDADE PAGADORA:UFES:DGPPROGEP', 'GESTOR - UNIDADE PAGADORA:UFES:HUCAMSUP', 'GESTOR - ÓRGÃO:UFES')
    seletorHabilitacoes['state'] = 'readonly'
    #seletorHabilitacoes.bind('<<ComboboxSelected>>', callback)
    seletorHabilitacoes.pack(fill=X, expand=YES)
    botaoSelecionarHabilitacao = Button(habilitacaoContainer)
    botaoSelecionarHabilitacao["text"] = "OK"
    botaoSelecionarHabilitacao["font"] = ("Segoe UI", "10")
    botaoSelecionarHabilitacao["width"] = 12
    botaoSelecionarHabilitacao["command"] = lambda: messagebox.showinfo(title="Teste", message=f"Habilitacao selecionada: {habilitacaoSelecionada.get()}")
    botaoSelecionarHabilitacao.pack()
    master.mainloop()





