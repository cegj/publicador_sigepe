from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from views import Interfaces as i
from models import UserConfig as uc
from models import AppConfig as ac
from copy import copy

class Delimitadores:
  def __init__(self):
      self.delimiters = copy(uc.UserConfig.obterDelimitadoresSalvos())
      self.master = i.Interfaces.novaJanela()
      self.delimitadoresContainer = Frame(self.master)
      self.delimitadoresContainer.pack(pady="5")
      self.janelaDelimitadores()

  def janelaDelimitadores(self):
    self.numero_documento()
    self.matricula_siape()
    self.salvar_delimitadores()
    infoLabel = ttk.Label(
      self.delimitadoresContainer,
      text="Os delimitadores são os termos que se encontram\nimediatamente antes e depois das informações que\nprecisam ser obtidas pelo Publicador Sigepe no\nconteúdo dos documentos a serem publicados.",
      background="#fff9d9",
      foreground="#85701d",
      padding=4,
      justify=CENTER)
    infoLabel.pack(pady="5")


  def numero_documento(self):
    try:
      def setBeforeValue(a=None, b=None, c=None):
        self.delimiters["numero_documento"][0] = beforeValue.get()
      def setAfterValue(a=None, b=None, c=None):
        self.delimiters["numero_documento"][1] = afterValue.get()
      container = Frame(self.delimitadoresContainer)
      container.pack(pady="5")
      label = Label(
        container,
        text="Número do documento",
        font=ac.AppConfig.fontes["normal"]
        )
      label.pack()

      fieldsContainer = Frame(container)
      fieldsContainer.pack(pady="2")

      beforeLabel = Label(
          fieldsContainer,
          text="Antes: ",
          font=ac.AppConfig.fontes["normal"]
          )
      beforeLabel.grid(row=1, column=1, sticky="W")

      beforeValue = StringVar()
      beforeValue.trace_add("write", setBeforeValue)
      beforeInput = Entry(
        fieldsContainer,
        width=22,
        textvariable=beforeValue,
        font=ac.AppConfig.fontes["normal"]
        )
      beforeValue.set(self.delimiters["numero_documento"][0])
      beforeInput.grid(row=1, column=2, sticky="W")

      afterLabel = Label(
          fieldsContainer,
          text="Depois: ",
          font=ac.AppConfig.fontes["normal"]
          )
      afterLabel.grid(row=2, column=1, sticky="W")

      afterValue = StringVar()
      afterValue.trace_add("write", setAfterValue)
      afterInput = Entry(
        fieldsContainer,
        width=22,
        textvariable=afterValue,
        font=ac.AppConfig.fontes["normal"]
        )
      afterValue.set(self.delimiters["numero_documento"][1])
      afterInput.grid(row=2, column=2, sticky="W")
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
      container.pack(pady="5")
      label = Label(
        container,
        text="Matrícula SIAPE",
        font=ac.AppConfig.fontes["normal"]
        )
      label.pack()

      fieldsContainer = Frame(container)
      fieldsContainer.pack(pady="2")

      beforeLabel = Label(
          fieldsContainer,
          text="Antes: ",
          font=ac.AppConfig.fontes["normal"]
          )
      beforeLabel.grid(row=1, column=1, sticky="W")

      beforeValue = StringVar()
      beforeValue.trace_add("write", setBeforeValue)
      beforeInput = Entry(
        fieldsContainer,
        width=20,
        textvariable=beforeValue,
        font=ac.AppConfig.fontes["normal"]
        )
      beforeValue.set(self.delimiters["matricula_siape"][0])
      beforeInput.grid(row=1, column=2, sticky="W")

      afterLabel = Label(
          fieldsContainer,
          text="Depois: ",
          font=ac.AppConfig.fontes["normal"]
          )
      afterLabel.grid(row=2, column=1, sticky="W")

      afterValue = StringVar()
      afterValue.trace_add("write", setAfterValue)
      afterInput = Entry(
        fieldsContainer,
        width=20,
        textvariable=afterValue,
        font=ac.AppConfig.fontes["normal"]
        )
      afterValue.set(self.delimiters["matricula_siape"][1])
      afterInput.grid(row=2, column=2, sticky="W")

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
    container.pack(pady="5")
    salvarDelimitadoresBtn = Button(
      container,
      text="Salvar",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=salvar
    )
    salvarDelimitadoresBtn.pack(pady="5")