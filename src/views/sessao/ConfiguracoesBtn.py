from tkinter import *
from models import AppConfig as ac
from views import Configuracoes as c

class ConfiguracoesBtn:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construir()

  def construir(self):
    btn = Button(
      self.container,
      text="Configurações",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=self.abrirJanela
      )
    btn.pack(side=LEFT, padx=10)

  def abrirJanela(self, event = None):
    c.Configuracoes()