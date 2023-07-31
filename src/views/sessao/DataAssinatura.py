from tkinter import *
from models import AppConfig as ac

class DataAssinatura:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(side=LEFT, padx=10)
    label = Label(
      self.subcontainer,
      text="Data de assinatura",
      font=ac.AppConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    self.value = StringVar()
    self.value.trace_add("write", self.setValue)
    self.sessao.dataAssinaturaInput = Entry(
      self.subcontainer,
      width=13,
      textvariable=self.value,
      font=ac.AppConfig.fontes["normal"]
      )
    self.value.set(self.sessao.userConfig["valores_sigepe"]["data_assinatura"])
    self.sessao.dataAssinaturaInput.pack(side=LEFT)

  def setValue(self, a=None, b=None, c=None):
    self.sessao.userConfig["valores_sigepe"]["data_assinatura"] = self.value.get()
