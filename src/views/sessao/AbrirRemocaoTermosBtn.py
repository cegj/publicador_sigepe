from tkinter import *
import appConfig
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
      font=appConfig.fontes["botao"],
      width=25,
      command=self.abrirJanela
      )
    btn.pack(side=LEFT, padx=10)

  def abrirJanela(self, event = None):
    rtc.RemoverTermosConteudo()