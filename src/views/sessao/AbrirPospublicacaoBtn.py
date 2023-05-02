from tkinter import *
import appConfig
from views import Pospublicacao as pp

class AbrirPospublicacaoBtn:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construir()

  def construir(self):
    btn = Button(
      self.container,
      text="Configurar pós-publicação",
      font=appConfig.fontes["botao"],
      width=25,
      command=self.abrirJanela
      )
    btn.pack(side=LEFT, padx=10)

  def abrirJanela(self, event = None):
    pp.Pospublicacao()