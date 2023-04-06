from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import appConfig
from Webdriver import nav
from appXpaths import xpaths
from selenium.webdriver.common.by import By
import time
from controllers import Interfaces as i
from controllers.interfaces import Habilitacao as h
from controllers import Interfaces as i
from controllers import UserConfig as uc
from copy import copy

class Pospublicacao:
  def __init__(self):
      self.afterpublishingconfig = copy(uc.UserConfig.obterConfigPosPublicacaoSalvos())
      self.master = i.Interfaces.novaJanela()
      self.posPublicacaoContainer = Frame(self.master)
      self.posPublicacaoContainer.pack()
      self.janelaPospublicacao()

  def janelaPospublicacao(self):
    self.copiar_mover()
    self.adicionar_ao_nome_arquivo()
    self.salvar_configuracoes()

  def copiar_mover(self):
    def setCopyMoveOption(event = None):
      self.afterpublishingconfig["copiar_ou_mover"] = copyMoveSelected.get()
      if (copyMoveSelected.get() == "Não copiar nem mover"):
        destinoInput["state"]=DISABLED
        botaoDiretorioDestino["state"]=DISABLED
      else:
        destinoInput["state"]=NORMAL
        botaoDiretorioDestino["state"]=NORMAL
    def getTargetPath():
      targetPath.set(filedialog.askdirectory())
      self.afterpublishingconfig["destino"] = targetPath.get()
    copyMoveLabel = Label(
      self.posPublicacaoContainer,
      text="Após publicar",
      font=appConfig.fontes["normal"]
      )
    copyMoveLabel.grid(column=1, row=1, padx=10, pady=5, sticky='w')
    copyMoveOptionsList = ["Copiar para...", "Mover para...", "Não copiar nem mover"]
    if self.afterpublishingconfig["copiar_ou_mover"] not in copyMoveOptionsList:
          self.afterpublishingconfig["copiar_ou_mover"] = "Não copiar nem mover"
    copyMoveOptionsList.remove(self.afterpublishingconfig["copiar_ou_mover"])
    copyMoveSelected = StringVar()
    copyMoveSelected.set(self.afterpublishingconfig["copiar_ou_mover"])
    copyMoveOptions = OptionMenu(
      self.posPublicacaoContainer,
      copyMoveSelected,
      copyMoveSelected.get(),
      *copyMoveOptionsList,
      command=setCopyMoveOption
    )
    copyMoveOptions.grid(column=2, row=1, padx=10, pady=5, sticky='w')
    targetPath = StringVar()
    targetPath.set(self.afterpublishingconfig["destino"])
    destinoInput = Entry(
      self.posPublicacaoContainer,
      textvariable=targetPath,
      width=50,
      font=appConfig.fontes["normal"],
      )
    destinoInput.grid(column=3, row=1)
    botaoDiretorioDestino = Button(
      self.posPublicacaoContainer,
      text="Alterar destino",
      font=appConfig.fontes["botao"],
      width=20,
      command=getTargetPath
      )
    botaoDiretorioDestino.grid(column=4, row=1, padx=10, pady=5, sticky='w')

  def adicionar_ao_nome_arquivo(self):
    def setValue(a=None, b=None, c=None):
      self.afterpublishingconfig["adicionar_ao_nome_arquivo"] = value.get()
    addToFilenameLabel = Label(
      self.posPublicacaoContainer,
      text="Adicionar ao nome do arquivo:",
      font=appConfig.fontes["normal"]
      )
    addToFilenameLabel.grid(column=1, columnspan=2, row=2, padx=10, pady=5, sticky='w')
    value = StringVar()
    value.trace_add("write", setValue)
    addToFilenameInput = Entry(
      self.posPublicacaoContainer,
      width=40,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.afterpublishingconfig["adicionar_ao_nome_arquivo"])
    addToFilenameInput.grid(column=3, row=2, columnspan=2, sticky="w")

  def salvar_configuracoes(self):
    def salvar():
      try:
        uc.UserConfig.salvarConfigPosPublicacao(self.afterpublishingconfig)
        self.master.destroy()
      except Exception as e:
        messagebox.showerror("Erro ao gravar configurações de pós-publicação", e)

    container = Frame(self.posPublicacaoContainer)
    container.grid(row=4, column=1, columnspan=3)
    self.salvarConfigBtn = Button(
      container,
      text="Salvar",
      font=appConfig.fontes["botao"],
      width=20,
      command=salvar
    )
    self.salvarConfigBtn.grid(column=1, row=0, padx=10, pady=5)