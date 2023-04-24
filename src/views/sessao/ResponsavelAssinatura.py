from tkinter import *
from tkinter import ttk
from Webdriver import nav
from selenium.webdriver.common.by import By
from controllers import ObterDoSigepe as ods
import appConfig
from views import Habilitacao as h

class ResponsavelAssinatura:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(side=LEFT, padx=10)
    label = Label(
      self.subcontainer,
      text="Responsável pela assinatura",
      font=appConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    self.value = StringVar()
    self.value.trace_add("write", self.setValue)
    entry = Entry(
      self.subcontainer,
      width=32,
      textvariable=self.value,
      font=appConfig.fontes["normal"]
      )
    self.value.set(self.sessao.userConfig["valores_sigepe"]["responsavel_assinatura"])
    entry.pack(side=LEFT, expand=True)

  def setValue(self, a=None, b=None, c=None):
    self.sessao.userConfig["valores_sigepe"]["responsavel_assinatura"] = self.value.get()