from tkinter import *
from tkinter import ttk
import appConfig

class Especie:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(side=LEFT, padx=10)
    label = Label(
      self.subcontainer,
      text="Espécie",
      font=appConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    self.selected = StringVar()
    self.selected.set(self.sessao.userConfig["valores_sigepe"]["especie"])
    options = ["Acordo Coletivo", "Apostila", "Ata", "Despacho", "Diretriz", "Edital", "Instrução Normativa", "Orientação Normativa", "Portaria", "Recomendação", "Resolução"]
    seletor = ttk.Combobox(
      self.subcontainer,
      textvariable=self.selected,
      values=options,
      state="readonly",
      width=20,
      font=appConfig.fontes["normal"]
      )
    seletor.pack(side=LEFT)
    seletor.bind("<<ComboboxSelected>>", self.setSelected)

  def setSelected(self, Event = None):
    self.sessao.userConfig["valores_sigepe"]["especie"] = self.selected.get()