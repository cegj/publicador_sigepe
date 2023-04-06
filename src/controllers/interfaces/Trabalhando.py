from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import appConfig
from Webdriver import nav
from appXpaths import xpaths
from selenium.webdriver.common.by import By
import time
from controllers import Interfaces as i
from controllers.interfaces import Habilitacao as h
from controllers import Interfaces as i
from controllers import UserConfig as uc
from copy import copy

class Trabalhando:
  def __init__(self, message):
      self.master = i.Interfaces.novaJanela()
      self.container = Frame(self.master)
      self.container.pack()
      self.message = message
      self.janelaTrabalhando()

  def janelaTrabalhando(self):
    messageLabel = Label(self.container, text=self.message)
    messageLabel.pack()

  def destroy(self):
    self.master.destroy()