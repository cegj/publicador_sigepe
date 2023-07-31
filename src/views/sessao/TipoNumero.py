from tkinter import *
from tkinter import ttk
from models import AppConfig as ac

class TipoNumero:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(side=LEFT, padx=10)
    label = Label(
      self.subcontainer,
      text="Tipo de número",
      font=ac.AppConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    self.selected = StringVar()
    self.selected.set(self.sessao.userConfig["valores_sigepe"]["tipo_preenchimento"])
    options = ["Automático", "Manual", "Sem Número"]
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
    self.sessao.userConfig["valores_sigepe"]["tipo_preenchimento"] = self.selected.get()