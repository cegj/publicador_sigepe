from controllers import Interfaces as i
from controllers import UserConfig as uc
from controllers import Publicador as p
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
import appConfig
from copy import copy
import time ##for test
from threading import Thread

class Publicacao:
  def __init__(self, config, files):
      self.afterpublishingconfig = copy(uc.UserConfig.obterConfigPosPublicacaoSalvos())
      self.delimiters = copy(uc.UserConfig.obterDelimitadoresSalvos())
      self.config = config
      self.files = files
      self.master = i.Interfaces.novaJanela()
      self.publicacaoContainer = Frame(self.master)
      self.publicacaoContainer.pack()
      self.janelaPublicacao()
      publicador = p.Publicador(self)

  def janelaPublicacao(self):
    self.logbox = st.ScrolledText(
      self.publicacaoContainer,
      width=50,
      height=10,
      font=appConfig.fontes["normal"],
      )
    self.logbox.grid(row=0, column=0, pady=10, padx=10)

    self.fileContentBox = st.ScrolledText(
      self.publicacaoContainer,
      width=50,
      height=10,
      font=appConfig.fontes["normal"],
      )
    self.fileContentBox.grid(row=0, column=1, pady=10, padx=10)

  def insertLog(self, logtext, tag = None, docNumber = ""):
    self.logbox.configure(state='normal')
    self.logbox.insert(INSERT, f"{docNumber} - {logtext}\n", tag)
    self.logbox.tag_config('e', background="#c23b3b", foreground="white") #error
    self.logbox.tag_config('s', background="#489c2f", foreground="white") #success
    self.logbox.tag_config('a', background="#e6e483") #alert
    self.logbox.configure(state='disabled')
    self.logbox.yview(END)

  def insertFileText(self, filetext):
    self.fileContentBox.configure(state='normal')
    self.fileContentBox.delete('0.0', END)
    self.fileContentBox.insert(INSERT, filetext)
    self.fileContentBox.configure(state='disabled')