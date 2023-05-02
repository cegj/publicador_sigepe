from tkinter import *
import appConfig
from controllers import UserConfig as uc

class ManterDadosBtn:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construir()

  def construir(self):
    btn = Button(
      self.container,
      text="Manter dados",
      font=appConfig.fontes["botao"],
      width=20,
      command=lambda: uc.UserConfig.salvarConfiguracoes(self.sessao.userConfig)
      )
    btn.pack(side=LEFT, padx=10)