from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import appConfig
from Webdriver import nav
from appXpaths import xpaths
from selenium.webdriver.common.by import By
import time
from views import Interfaces as i
from views import Habilitacao as h
from views import Interfaces as i
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

  def termos(self):
    def setValue(a=None, b=None, c=None):
      self.config["termos"] = self.termosInput.get("1.0", END)
    termosLabel = Label(
      self.termosContainer,
      text="Termos para remover do conteúdo:",
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
    infoLabel = Label(
      self.termosContainer,
      text="Para informar diferentes termos, separe-os com ponto-e-vírgula",
      font=appConfig.fontes["normal"]
      )
    infoLabel.pack()


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