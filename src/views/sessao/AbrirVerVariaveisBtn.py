from tkinter import *
import appConfig
from views import VerVariaveis as vv

class AbrirVerVariaveisBtn:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construir()

  def construir(self):
    btn = Button(
      self.container,
      text="Ver variáveis",
      font=appConfig.fontes["botao"],
      width=20,
      command=self.abrirJanela
      )
    btn.pack(side=LEFT, padx=10)

  def abrirJanela(self, event = None):
    vv.VerVariaveis()