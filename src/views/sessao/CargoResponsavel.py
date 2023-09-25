from tkinter import *
from models import AppConfig as ac

class CargoResponsavel:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(side=LEFT, padx=10)
    label = Label(
      self.subcontainer,
      text="Cargo do responsável",
      font=ac.AppConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    self.value = StringVar()
    self.value.trace_add("write", self.setValue)
    self.sessao.cargoResponsavelInput = Entry(
      self.subcontainer,
      width=20,
      textvariable=self.value,
      font=ac.AppConfig.fontes["normal"]
      )
    self.value.set(self.sessao.userConfig["valores_sigepe"]["cargo_responsavel"])
    self.sessao.cargoResponsavelInput.pack(side=LEFT, expand=True)

  def setValue(self, a=None, b=None, c=None):
    self.sessao.userConfig["valores_sigepe"]["cargo_responsavel"] = self.value.get()