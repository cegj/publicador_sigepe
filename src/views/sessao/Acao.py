from tkinter import *
from tkinter import ttk
import appConfig

class Acao:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(side=LEFT, padx=10)
    label = Label(
      self.subcontainer,
      text="Ação",
      font=appConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    self.selected = StringVar()
    self.selected.set(self.sessao.userConfig["acao"])
    options = ["Enviar para análise", "Enviar para assinatura / publicação", "Gravar rascunho"]
    seletor = ttk.Combobox(
      self.subcontainer,
      textvariable=self.selected,
      values=options,
      state="readonly",
      width=30,
      font=appConfig.fontes["normal"]
      )
    seletor.pack(side=LEFT)
    seletor.bind("<<ComboboxSelected>>", self.setSelected)

  def setSelected(self, Event = None):
    self.sessao.userConfig["acao"] = self.selected.get()