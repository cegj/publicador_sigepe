from tkinter import *
from tkinter import ttk
from models import AppConfig as ac
from views import Interfaces as i
from controllers import Variaveis as v

class VerVariaveis:
  def __init__(self):
      self.variaveis = v.Variaveis.obterValorVariaveis()
      self.master = i.Interfaces.novaJanela()
      self.container = Frame(self.master)
      self.container.pack()
      self.janelaVerVariaveis()

  def janelaVerVariaveis(self):
    self.boxVariaveis()

  def boxVariaveis(self):
    label = Label(
      self.container,
      text="Valores das variáveis disponíveis",
      font=ac.AppConfig.fontes["normal"]
      )
    label.pack()
    self.textbox = Text(
      self.container,
      width=32,
      height=13,
      font=ac.AppConfig.fontes["normal"]
      )
    for key, value in self.variaveis.items():
      self.textbox.insert(END, f"[{key}]: {value}\n")
    self.textbox.pack()

    infoLabel = ttk.Label(
      self.container,
      text="As variáveis podem ser utilizadas para preencher as\nconfigurações do Publicador Sigepe com valores dinâmicos,\nque serão atualizados para o valor correspondente\nsempre que o Publicador Sigepe for executado.",
      background="#fff9d9",
      foreground="#85701d",
      padding=4,
      justify=CENTER)
    infoLabel.pack(pady="5")