from tkinter import *
from tkinter import ttk
import appConfig
from Webdriver import nav
from appXpaths import xpaths
# from appUserConfig import userConfig
from selenium.webdriver.common.by import By
import time
from tkinter import filedialog
from controllers import Interfaces as i
from controllers.interfaces import Habilitacao as h
from copy import copy
from controllers import UserConfig as uc

class Sessao(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.userConfig = copy(uc.UserConfig.obterConfiguracoesSalvas())

  def sessao(self):
    self.sessaoContainer = Frame(self.root)
    self.sessaoContainer.grid()
    sessaoContainerTitulo = Label(self.sessaoContainer, text="Publicar documentos")
    sessaoContainerTitulo.configure(anchor="center")
    sessaoContainerTitulo["font"] = appConfig.fontes["titulo"]
    sessaoContainerTitulo.grid(column=0, row=0, columnspan=4)
    self.habilitacao()
    self.diretorio_origem()
    self.diretorio_destino()
    self.edicao_bgp()
    self.salvar_configuracoes()
    self.root.mainloop()

  def habilitacao(self):
    def abrirJanelaHabilitacao():
      janelaHabilitacao = h.Habilitacao(self)

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
    botaoAlterarHabilitacao["command"] = abrirJanelaHabilitacao
    botaoAlterarHabilitacao.grid(column=3, row=1, padx=10, pady=5, sticky='w')

  def diretorio_origem(self):
    originPath = StringVar()
    originPath.set(self.userConfig["dir"]["origem"])
    def getOriginPath():
      originPath.set(filedialog.askdirectory())
      self.userConfig["dir"]["origem"] = originPath.get()
    self.diretorioOrigemContainer = Frame(self.sessaoContainer)
    self.diretorioOrigemContainer.grid(row=2, column=0, sticky='w')
    origemLabel = Label(
      self.diretorioOrigemContainer,
      text="Pasta de origem",
      font=appConfig.fontes["normal"]
      )
    origemLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    origemInput = Entry(
      self.diretorioOrigemContainer,
      textvariable=originPath,
      width=50,
      font=appConfig.fontes["normal"]
      )
    origemInput.grid(column=2, row=0)
    botaoDiretorioOrigem = Button(
      self.diretorioOrigemContainer,
      text="Alterar",
      font=appConfig.fontes["botao"],
      width=20,
      command=getOriginPath
      )
    botaoDiretorioOrigem.grid(column=3, row=0, padx=10, pady=5, sticky='w')

  def diretorio_destino(self):
    targetPath = StringVar()
    targetPath.set(self.userConfig["dir"]["destino"])
    def getTargetPath():
      targetPath.set(filedialog.askdirectory())
      self.userConfig["dir"]["destino"] = targetPath.get()
    self.diretorioDestinoContainer = Frame(self.sessaoContainer)
    self.diretorioDestinoContainer.grid(row=3, column=0, sticky='w')
    destinoLabel = Label(
      self.diretorioDestinoContainer,
      text="Pasta de destino",
      font=appConfig.fontes["normal"]
      )
    destinoLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    destinoInput = Entry(
      self.diretorioDestinoContainer,
      textvariable=targetPath,
      width=50,
      font=appConfig.fontes["normal"]
      )
    destinoInput.grid(column=2, row=0)
    botaoDiretorioDestino = Button(
      self.diretorioDestinoContainer,
      text="Alterar",
      font=appConfig.fontes["botao"],
      width=20,
      command=getTargetPath
      )
    botaoDiretorioDestino.grid(column=3, row=0, padx=10, pady=5, sticky='w')

  def salvar_configuracoes(self):
    self.salvarConfiguracoesContainer = Frame(self.sessaoContainer)
    self.salvarConfiguracoesContainer.grid(row=10, column=0, sticky='w')
    botaoSalvarConfiguracoes = Button(
      self.salvarConfiguracoesContainer,
      text="Manter configurações",
      font=appConfig.fontes["botao"],
      width=20,
      command=lambda: uc.UserConfig.salvarConfiguracoes(self.userConfig)
      )
    botaoSalvarConfiguracoes.grid(column=3, row=0, padx=10, pady=5, sticky='w')


  def edicao_bgp(self):

    def setSelected(event):
      print(selected.get())
      self.userConfig["valores_sigepe"]["edicao_bgp"] = selected.get()

    self.edicaoBgpContainer = Frame(self.sessaoContainer)
    self.edicaoBgpContainer.grid(row=4, column=0, sticky='w')
    edicaoBgpLabel = Label(
      self.edicaoBgpContainer,
      text="Edição do boletim",
      font=appConfig.fontes["normal"]
      )
    edicaoBgpLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    selected = StringVar()
    selected.set(self.userConfig["valores_sigepe"]["edicao_bgp"])
    options = ["Normal", "Extraordinária"]
    seletorEdicaoBgp = ttk.Combobox(
      self.edicaoBgpContainer,
      textvariable=selected,
      values=options,
      state="readonly",
      width=50,
      font=appConfig.fontes["normal"]
      )
    seletorEdicaoBgp.grid(column=2, row=0)
    seletorEdicaoBgp.bind("<<ComboboxSelected>>", setSelected)