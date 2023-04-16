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

class Delimitadores:
  def __init__(self):
      self.delimiters = copy(uc.UserConfig.obterDelimitadoresSalvos())
      self.master = i.Interfaces.novaJanela()
      self.delimitadoresContainer = Frame(self.master)
      self.delimitadoresContainer.pack()
      self.janelaDelimitadores()


  # def handleMudarHabilitacao(self):
  #   sigepe_novaHabilitacaoBotao = nav.find_element(By.XPATH, f"//*[contains(text(), '{self.seletorHabilitacoes.get()}')]")
  #   sigepe_novaHabilitacaoBotao.click()
  #   time.sleep(2)
  #   self.master.destroy()
  #   self.sessao_habilitacao.sessaoHabilitacaoContainer.destroy()
  #   self.sessao_habilitacao.habilitacao()

  # def handleFecharJanela(self):
  #   sigepe_fecharHabilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['fecharHabilitacaoBotao'])
  #   sigepe_fecharHabilitacaoBotao.click()
  #   self.master.destroy()

  def janelaDelimitadores(self):
    # tituloContainer = Frame(self.delimitadoresContainer)
    # tituloContainer.grid(row=0, column=1, sticky='w')
    # tituloInformacao = Label(
    #   tituloContainer,
    #   text="Informação:",
    #   font=appConfig.fontes["normal"]
    #   )
    # tituloInformacao.grid(column=1, row=0, padx=10, pady=5, sticky='w')
    # tituloAntes = Label(
    #   tituloContainer,
    #   text="Antes:",
    #   font=appConfig.fontes["normal"]
    #   )
    # tituloAntes.grid(column=2, row=0, padx=10, pady=5, sticky='w')
    # tituloDepois = Label(
    #   tituloContainer,
    #   text="Depois:",
    #   font=appConfig.fontes["normal"]
    #   )
    # tituloDepois.grid(column=3, row=0, padx=10, pady=5, sticky='w')
    self.numero_documento()
    self.titulo_documento()
    self.matricula_siape()
    self.salvar_delimitadores()

  def numero_documento(self):
    try:
      def setBeforeValue(a=None, b=None, c=None):
        self.delimiters["numero_documento"][0] = beforeValue.get()
      def setAfterValue(a=None, b=None, c=None):
        self.delimiters["numero_documento"][1] = afterValue.get()
      container = Frame(self.delimitadoresContainer)
      container.grid(row=1, column=1, sticky='w')
      label = Label(
        container,
        text="Número do documento:",
        font=appConfig.fontes["normal"]
        )
      label.grid(column=1, row=0, padx=10, pady=5, sticky='w')
      beforeValue = StringVar()
      beforeValue.trace_add("write", setBeforeValue)
      beforeInput = Entry(
        container,
        width=20,
        textvariable=beforeValue,
        font=appConfig.fontes["normal"]
        )
      beforeValue.set(self.delimiters["numero_documento"][0])
      beforeInput.grid(column=2, row=0)
      afterValue = StringVar()
      afterValue.trace_add("write", setAfterValue)
      afterInput = Entry(
        container,
        width=20,
        textvariable=afterValue,
        font=appConfig.fontes["normal"]
        )
      afterValue.set(self.delimiters["numero_documento"][1])
      afterInput.grid(column=3, row=0)
    except Exception as e:
      messagebox.showerror("Erro em Delimitadores", e)
      self.master.destroy()

  def titulo_documento(self):
    try:
      def setBeforeValue(a=None, b=None, c=None):
        self.delimiters["titulo_documento"][0] = beforeValue.get()
      def setAfterValue(a=None, b=None, c=None):
        self.delimiters["titulo_documento"][1] = afterValue.get()
      container = Frame(self.delimitadoresContainer)
      container.grid(row=2, column=1, sticky='w')
      label = Label(
        container,
        text="Título do documento:",
        font=appConfig.fontes["normal"]
        )
      label.grid(column=1, row=0, padx=10, pady=5, sticky='w')
      beforeValue = StringVar()
      beforeValue.trace_add("write", setBeforeValue)
      beforeInput = Entry(
        container,
        width=20,
        textvariable=beforeValue,
        font=appConfig.fontes["normal"]
        )
      beforeValue.set(self.delimiters["titulo_documento"][0])
      beforeInput.grid(column=2, row=0)
      afterValue = StringVar()
      afterValue.trace_add("write", setAfterValue)
      afterInput = Entry(
        container,
        width=20,
        textvariable=afterValue,
        font=appConfig.fontes["normal"]
        )
      afterValue.set(self.delimiters["titulo_documento"][1])
      afterInput.grid(column=3, row=0)
    except Exception as e:
      messagebox.showerror("Erro em Delimitadores", e)
      self.master.destroy()

  def matricula_siape(self):
    try:
      def setBeforeValue(a=None, b=None, c=None):
        self.delimiters["matricula_siape"][0] = beforeValue.get()
      def setAfterValue(a=None, b=None, c=None):
        self.delimiters["matricula_siape"][1] = afterValue.get()
      container = Frame(self.delimitadoresContainer)
      container.grid(row=3, column=1, sticky='w')
      label = Label(
        container,
        text="Matrícula SIAPE:",
        font=appConfig.fontes["normal"]
        )
      label.grid(column=1, row=0, padx=10, pady=5, sticky='w')
      beforeValue = StringVar()
      beforeValue.trace_add("write", setBeforeValue)
      beforeInput = Entry(
        container,
        width=20,
        textvariable=beforeValue,
        font=appConfig.fontes["normal"]
        )
      beforeValue.set(self.delimiters["matricula_siape"][0])
      beforeInput.grid(column=2, row=0)
      afterValue = StringVar()
      afterValue.trace_add("write", setAfterValue)
      afterInput = Entry(
        container,
        width=20,
        textvariable=afterValue,
        font=appConfig.fontes["normal"]
        )
      afterValue.set(self.delimiters["matricula_siape"][1])
      afterInput.grid(column=3, row=0)

    except Exception as e:
      messagebox.showerror("Erro em Delimitadores", e)
      self.master.destroy()


  def salvar_delimitadores(self):
    def salvar():
      try:
        uc.UserConfig.salvarDelimitadores(self.delimiters)
        self.master.destroy()
      except Exception as e:
        messagebox.showerror("Erro ao gravar delimitadores", e)

    container = Frame(self.delimitadoresContainer)
    container.grid(row=4, column=1, sticky='w')
    salvarDelimitadoresBtn = Button(
      container,
      text="Salvar",
      font=appConfig.fontes["botao"],
      width=20,
      command=salvar
    )
    salvarDelimitadoresBtn.grid(column=1, row=0, padx=10, pady=5, sticky='w')