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

class RemoverTermosConteudo:
  def __init__(self):
      self.config = copy(uc.UserConfig.obterTermosConteudoRemover())
      self.master = i.Interfaces.novaJanela()
      self.termosContainer = Frame(self.master)
      self.termosContainer.pack()
      self.janelaTermosRemover()

  def janelaTermosRemover(self):
    self.termos()
    self.salvar_configuracoes()

  # def copiar_mover(self):
  #   def setCopyMoveOption(event = None):
  #     self.config["copiar_ou_mover"] = copyMoveSelected.get()
  #     if (copyMoveSelected.get() == "Não copiar nem mover"):
  #       destinoInput["state"]=DISABLED
  #       botaoDiretorioDestino["state"]=DISABLED
  #     else:
  #       destinoInput["state"]=NORMAL
  #       botaoDiretorioDestino["state"]=NORMAL
  #   def getTargetPath():
  #     targetPath.set(filedialog.askdirectory())
  #     self.config["destino"] = targetPath.get()
  #   copyMoveLabel = Label(
  #     self.termosContainer,
  #     text="Após publicar",
  #     font=appConfig.fontes["normal"]
  #     )
  #   copyMoveLabel.grid(column=1, row=1, padx=10, pady=5, sticky='w')
  #   copyMoveOptionsList = ["Copiar para...", "Mover para...", "Não copiar nem mover"]
  #   if self.config["copiar_ou_mover"] not in copyMoveOptionsList:
  #         self.config["copiar_ou_mover"] = "Não copiar nem mover"
  #   copyMoveOptionsList.remove(self.config["copiar_ou_mover"])
  #   copyMoveSelected = StringVar()
  #   copyMoveSelected.set(self.config["copiar_ou_mover"])
  #   copyMoveOptions = OptionMenu(
  #     self.termosContainer,
  #     copyMoveSelected,
  #     copyMoveSelected.get(),
  #     *copyMoveOptionsList,
  #     command=setCopyMoveOption
  #   )
  #   copyMoveOptions.grid(column=2, row=1, padx=10, pady=5, sticky='w')
  #   targetPath = StringVar()
  #   targetPath.set(self.config["destino"])
  #   destinoInput = Entry(
  #     self.termosContainer,
  #     textvariable=targetPath,
  #     width=50,
  #     font=appConfig.fontes["normal"],
  #     )
  #   destinoInput.grid(column=3, row=1)
  #   botaoDiretorioDestino = Button(
  #     self.termosContainer,
  #     text="Alterar destino",
  #     font=appConfig.fontes["botao"],
  #     width=20,
  #     command=getTargetPath
  #     )
  #   botaoDiretorioDestino.grid(column=4, row=1, padx=10, pady=5, sticky='w')

  def termos(self):
    def setValue(a=None, b=None, c=None):
      self.config["termos"] = self.termosInput.get("1.0", END)
    termosLabel = Label(
      self.termosContainer,
      text="Termos para remover:",
      font=appConfig.fontes["normal"]
      )
    termosLabel.pack()
    self.termosInput = Text(
      self.termosContainer,
      width=40,
      height=10,
      font=appConfig.fontes["normal"]
      )
    self.termosInput.insert(END, self.config["termos"])
    self.termosInput.pack()

  def salvar_configuracoes(self):
    def salvar():
      try:
        termos = self.termosInput.get("1.0", END).replace("\n", "")
        self.config["termos"] = termos
        uc.UserConfig.salvarTermosConteudoRemover(self.config)
        self.master.destroy()
      except Exception as e:
        messagebox.showerror("Erro ao gravar termos para remover do conteúdo", e)

    container = Frame(self.termosContainer)
    container.pack()
    self.salvarConfigBtn = Button(
      container,
      text="Salvar",
      font=appConfig.fontes["botao"],
      width=20,
      command=salvar
    )
    self.salvarConfigBtn.pack()