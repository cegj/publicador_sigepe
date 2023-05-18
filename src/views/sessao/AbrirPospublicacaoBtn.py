from tkinter import *
from models import AppConfig as ac
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
      font=ac.AppConfig.fontes["botao"],
      width=25,
      command=self.abrirJanela
      )
    btn.pack(side=LEFT, padx=10)

  def abrirJanela(self, event = None):
    pp.Pospublicacao()