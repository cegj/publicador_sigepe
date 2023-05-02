from tkinter import *
import appConfig

class Orgao:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(side=LEFT, padx=10)
    label = Label(
      self.subcontainer,
      text="Órgão",
      font=appConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    self.value = StringVar()
    self.value.trace_add("write", self.setValue)
    entry = Entry(
      self.subcontainer,
      width=27,
      textvariable=self.value,
      font=appConfig.fontes["normal"]
      )
    self.value.set(self.sessao.userConfig["valores_sigepe"]["orgao"])
    entry.pack(side=LEFT)

  def setValue(self, a=None, b=None, c=None):
    self.sessao.userConfig["valores_sigepe"]["orgao"] = self.value.get()