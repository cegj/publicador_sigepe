from tkinter import *
from models import AppConfig as ac
from views import RemoverTermosConteudo as rtc

class AbrirRemocaoTermosBtn:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construir()

  def construir(self):
    btn = Button(
      self.container,
      text="Config. remoção de termos",
      font=ac.AppConfig.fontes["botao"],
      width=25,
      command=self.abrirJanela
      )
    btn.pack(side=LEFT, padx=10)

  def abrirJanela(self, event = None):
    rtc.RemoverTermosConteudo()