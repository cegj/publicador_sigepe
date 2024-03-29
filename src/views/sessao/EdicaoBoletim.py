from tkinter import *
from tkinter import ttk
from models import AppConfig as ac

class EdicaoBoletim:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(side=LEFT, padx=10)
    label = Label(
      self.subcontainer,
      text="Edição do boletim",
      font=ac.AppConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    self.selected = StringVar()
    self.selected.set(self.sessao.userConfig["valores_sigepe"]["edicao_bgp"])
    options = ["Normal", "Extraordinária"]
    seletor = ttk.Combobox(
      self.subcontainer,
      textvariable=self.selected,
      values=options,
      state="readonly",
      width=10,
      font=ac.AppConfig.fontes["normal"]
      )
    seletor.pack(side=LEFT)
    seletor.bind("<<ComboboxSelected>>", self.setSelected)

  def setSelected(self, Event = None):
    self.sessao.userConfig["valores_sigepe"]["edicao_bgp"] = self.selected.get()
    self.sessao.handleFieldState("edicao_bgp", "normal", "dataPublicacaoInput")