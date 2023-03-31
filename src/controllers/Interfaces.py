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
from appXpaths import xpaths
from appUserConfig import userConfig
from selenium.webdriver.common.by import By
import time
from tkinter import filedialog

class Interfaces:
  def __init__(self):
    self.root = Tk()
    self.root.title(appConfig.appTitulo)
    self.root.geometry('700x200')
    self.root["padx"] = appConfig.pad["x"]
    self.root["pady"] = appConfig.pad["y"]

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
    if(cebx.checkExistsByXpath(xpaths['login']['captchaImg'])):
        captchaContainer = Frame(loginContainer)
        captchaContainer["pady"] = 5
        captchaContainer.pack()
        captchaLabel = Label(captchaContainer, text="Confirme o código", font=appConfig.fontes["normal"])
        imgFileName = gebx.getScreenshotByXpath(xpaths['login']['captchaImg'])
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
    botaoLogin["font"] = appConfig.fontes["botao"]
    botaoLogin["width"] = 12
    botaoLogin["command"] = lambda: Usuario.Usuario.fazerLogin(cpfInput, senhaInput, captchaInput, master)
    botaoLogin.pack()

    def handleEnter(event):
      Usuario.Usuario.fazerLogin(cpfInput, senhaInput, captchaInput, master)

    master.bind('<Return>', handleEnter)

    master.mainloop()

  def sessao(self):
    self.sessaoContainer = Frame(self.root)
    self.sessaoContainer.grid()
    sessaoContainerTitulo = Label(self.sessaoContainer, text="Publicar documentos")
    sessaoContainerTitulo.configure(anchor="center")
    sessaoContainerTitulo["font"] = appConfig.fontes["titulo"]
    sessaoContainerTitulo.grid(column=0, row=0, columnspan=4)
    self.sessao_habilitacao()
    self.sessao_diretorios()
    self.root.mainloop()

  def sessao_habilitacao(self):
    self.sessaoHabilitacaoContainer = Frame(self.sessaoContainer)
    self.sessaoHabilitacaoContainer.grid(row=1, column=0, sticky='w')
    sigepe_habilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['habilitacaoBotao'])
    habilitacaoAtual = Label(
      self.sessaoHabilitacaoContainer,
      text=f"Habilitação atual: {sigepe_habilitacaoBotao.text}",
      anchor="w",
      font=appConfig.fontes["normal"])
    habilitacaoAtual.grid(column=0, row=1, columnspan=2, padx=10, pady=5, sticky='w')
    botaoAlterarHabilitacao = Button(self.sessaoHabilitacaoContainer)
    botaoAlterarHabilitacao["text"] = "Alterar habilitação"
    botaoAlterarHabilitacao["font"] = appConfig.fontes["botao"]
    botaoAlterarHabilitacao["width"] = 20
    botaoAlterarHabilitacao["command"] = lambda: self.habilitacao()
    botaoAlterarHabilitacao.grid(column=3, row=1, padx=10, pady=5, sticky='w')

  def sessao_diretorios(self):
    originPath = StringVar()
    originPath.set(userConfig["dir"]["origem"])
    def getOriginPath():
      originPath.set(filedialog.askdirectory())
    self.sessaoDiretorioContainer = Frame(self.sessaoContainer)
    self.sessaoDiretorioContainer.grid(row=2, column=0, sticky='w')
    origemLabel = Label(
      self.sessaoDiretorioContainer,
      text="Pasta de origem",
      font=appConfig.fontes["normal"]
      )
    origemLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    origemInput = Entry(
      self.sessaoDiretorioContainer,
      textvariable=originPath,
      width=50,
      font=appConfig.fontes["normal"]
      )
    origemInput.grid(column=2, row=0)
    botaoDiretorioOrigem = Button(
      self.sessaoDiretorioContainer,
      text="Alterar",
      font=appConfig.fontes["botao"],
      width=20,
      command=getOriginPath
      )
    botaoDiretorioOrigem.grid(column=3, row=0, padx=10, pady=5, sticky='w')

  def habilitacao(self):
    try:
      def handleMudarHabilitacao():
        sigepe_novaHabilitacaoBotao = nav.find_element(By.XPATH, f"//*[contains(text(), '{seletorHabilitacoes.get()}')]")
        sigepe_novaHabilitacaoBotao.click()
        time.sleep(2)
        master.destroy()
        self.sessaoHabilitacaoContainer.destroy()
        self.sessao_habilitacao()

      def handleFecharJanela():
        sigepe_fecharHabilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['fecharHabilitacaoBotao'])
        sigepe_fecharHabilitacaoBotao.click()
        master.destroy()

      master = Interfaces.novaJanela()
      habilitacaoContainer = Frame(master)
      habilitacaoContainer.pack()

      sigepe_habilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['habilitacaoBotao'])
      sigepe_habilitacaoBotao.click()
      sigepe_HabilitacoesLinks = nav.find_elements(By.XPATH, xpaths['habilitacao']['habilitacoesLinks'])

      listaHabilitacoes = []
      for habilitacao in sigepe_HabilitacoesLinks:
        listaHabilitacoes.append(habilitacao.text)
      listaHabilitacoes.pop(0)

      label = ttk.Label(habilitacaoContainer, text="Selecione a habilitação:")
      label.pack()
      valorSelecionado = StringVar()
      seletorHabilitacoes = ttk.Combobox(
        habilitacaoContainer,
        textvariable=valorSelecionado,
        values=listaHabilitacoes,
        state="readonly",
        width=50)
      seletorHabilitacoes.pack(fill=X, expand=YES)
      botaoSelecionarHabilitacao = Button(
        habilitacaoContainer,
        text="OK",
        font=appConfig.fontes["botao"],
        width=20,
        command=handleMudarHabilitacao
      )
      botaoSelecionarHabilitacao.pack()

    except Exception as e:
      messagebox.showerror("Erro", e)
      master.destroy()

    master.protocol("WM_DELETE_WINDOW", handleFecharJanela)








