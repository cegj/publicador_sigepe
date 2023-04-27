from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import appConfig
from Webdriver import nav
from appXpaths import xpaths
from selenium.webdriver.common.by import By
import time
from views import Interfaces as i
from views import Habilitacao as h
from views import Interfaces as i
from controllers import UserConfig as uc
from copy import copy
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
      font=appConfig.fontes["normal"]
      )
    label.pack()
    self.textbox = Text(
      self.container,
      width=30,
      height=13,
      font=appConfig.fontes["normal"]
      )
    for key, value in self.variaveis.items():
      self.textbox.insert(END, f"[{key}]: {value}\n")
    self.textbox.pack()