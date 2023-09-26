from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from views import Interfaces as i
from models import UserConfig as uc
from models import AppConfig as ac
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
    separator = ttk.Separator(self.posPublicacaoContainer,orient='horizontal')
    separator.pack(fill='x', pady=10)
    self.adicionar_ao_nome_arquivo()
    separator = ttk.Separator(self.posPublicacaoContainer,orient='horizontal')
    separator.pack(fill='x', pady=10)
    self.salvar_configuracoes()

    infoLabel = ttk.Label(
      self.posPublicacaoContainer,
      text="As ações pós-publicação serão executadas sempre que um\narquivo for publicado com sucesso. Elas permitem copiar ou\nmover o arquivo para uma nova pasta, e adicionar um termo\nao nome do arquivo após a publicação. Caso haja falha na\npublicação do arquivo, as ações não são realizadas.",
      background="#fff9d9",
      foreground="#85701d",
      padding=4,
      justify=CENTER)
    infoLabel.pack(pady="5")

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
      path = filedialog.askdirectory()
      targetPath.set(path)
    def setPathOnChange(a=None, b=None, c=None):
      self.afterpublishingconfig["destino"] = targetPath.get()

    copyMoveContainer = Frame(self.posPublicacaoContainer)
    copyMoveContainer.pack()

    copyMoveLabel = Label(
      copyMoveContainer,
      text="Copiar ou mover para outra pasta:",
      font=ac.AppConfig.fontes["normal"]
      )
    copyMoveLabel.pack(pady="2")
    copyMoveOptionsList = ["Copiar para...", "Mover para...", "Não copiar nem mover"]
    if self.afterpublishingconfig["copiar_ou_mover"] not in copyMoveOptionsList:
          self.afterpublishingconfig["copiar_ou_mover"] = "Não copiar nem mover"
    copyMoveOptionsList.remove(self.afterpublishingconfig["copiar_ou_mover"])
    copyMoveSelected = StringVar()
    copyMoveSelected.set(self.afterpublishingconfig["copiar_ou_mover"])
    copyMoveOptions = OptionMenu(
      copyMoveContainer,
      copyMoveSelected,
      copyMoveSelected.get(),
      *copyMoveOptionsList,
      command=setCopyMoveOption
    )
    copyMoveOptions.pack(pady="2")
    targetPath = StringVar()
    targetPath.trace_add("write", setPathOnChange)
    targetPath.set(self.afterpublishingconfig["destino"])
    botaoDiretorioDestino = Button(
      copyMoveContainer,
      text="Selecionar destino",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=getTargetPath
      )
    botaoDiretorioDestino.pack(pady="2")
    destinoInput = Entry(
      copyMoveContainer,
      textvariable=targetPath,
      width=40,
      font=ac.AppConfig.fontes["normal"],
      )
    destinoInput.pack(pady="2")

  def adicionar_ao_nome_arquivo(self):
    def setValue(a=None, b=None, c=None):
      self.afterpublishingconfig["adicionar_ao_nome_arquivo"] = value.get()

    addToFilenameContainer = Frame(self.posPublicacaoContainer)
    addToFilenameContainer.pack()

    addToFilenameLabel = Label(
      addToFilenameContainer,
      text="Adicionar termo ao nome do arquivo:",
      font=ac.AppConfig.fontes["normal"]
      ) 
    addToFilenameLabel.pack(pady="2")
    value = StringVar()
    value.trace_add("write", setValue)
    addToFilenameInput = Entry(
      addToFilenameContainer,
      width=40,
      textvariable=value,
      font=ac.AppConfig.fontes["normal"]
      )
    value.set(self.afterpublishingconfig["adicionar_ao_nome_arquivo"])
    addToFilenameInput.pack(pady="2")

  def salvar_configuracoes(self):
    def salvar():
      try:
        uc.UserConfig.salvarConfigPosPublicacao(self.afterpublishingconfig)
        self.master.destroy()
      except Exception as e:
        messagebox.showerror("Erro ao gravar configurações de pós-publicação", e)

    container = Frame(self.posPublicacaoContainer)
    container.pack()
    self.salvarConfigBtn = Button(
      container,
      text="Salvar",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=salvar
    )
    self.salvarConfigBtn.pack(pady="10")