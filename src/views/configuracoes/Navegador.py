from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from controllers import Webdriver as wd
from models import AppConfig as ac
from selenium.webdriver.common.by import By
import time
from views import Interfaces as i
from views import Sessao as s
from helpers import ThreadWithReturn as thread
from views import SigepeTrabalhando as st
from models import UserConfig as uc

class Navegador(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.master = Frame(self.root)
    self.master.pack()
    self.navegadorContainer = Frame(self.master)
    self.navegadorContainer.pack()
    self.listaNavegadores = ["Google Chrome (recomendado)", "Microsoft Edge", "Mozilla Firefox"]
    self.janelaNavegador()

  def handleSalvarNavegador(self):
    try:
      value = self.seletorNavegadores.get()
      match value:
        case "Google Chrome (recomendado)":
          valueToStore = "chrome"
        case "Microsoft Edge":
          valueToStore = "edge"
        case "Mozilla Firefox":
          valueToStore = "firefox"
        case _:
          valueToStore = "chrome"
      uc.UserConfig.salvarNavegador({"browser": valueToStore})
      messagebox.showinfo("Sucesso", "Navegador definido com sucesso. Inicie o Publicador Sigepe novamente para executá-lo com o novo navegador.")
      self.root.destroy()
    except Exception as e:
      messagebox.showerror("Erro ao salvar navegador", e)


  def getCurrentBrowser(self):
    browserName = uc.UserConfig.obterNavegador()
    match browserName:
      case "chrome":
        return "Google Chrome"
      case "edge":
        return "Microsoft Edge"
      case "firefox":
        return "Mozilla Firefox"
      case _:
        return False

  def janelaNavegador(self):
    try:
      label = ttk.Label(self.navegadorContainer, text="Selecione um navegador:")
      label.pack()
      self.navegadorSelecionado = StringVar()
      self.seletorNavegadores = ttk.Combobox(
        self.navegadorContainer,
        textvariable=self.navegadorSelecionado,
        values=self.listaNavegadores,
        state="readonly",
        width=50)
      self.seletorNavegadores.pack(fill=X, expand=YES, pady="5")

      def get_values(event = None):
        print(self.seletorNavegadores.get())

      self.seletorNavegadores.bind("<<ComboboxSelected>>", get_values)

      botaoSelecionarNavegador = Button(
        self.navegadorContainer,
        text="Definir navegador",
        font=ac.AppConfig.fontes["botao"],
        width=20,
        command=self.handleSalvarNavegador 
      )
      botaoSelecionarNavegador.pack(pady="5")

      infoLabel = ttk.Label(
        self.navegadorContainer,
        text="O Publicador executa uma janela do navegador\nno plano de fundo para preencher as informações\ndos documentos no Sigepe e enviá-los para publicação.\n Ao selecionar um navegador, certifique-se de que ele\nestá instalado e atualizado em seu computador.",
        background="#fff9d9",
        foreground="#85701d",
        padding=4,
        justify=CENTER)
      infoLabel.pack(pady="5")
      currentBrowser = self.getCurrentBrowser()
      if (currentBrowser):
        label = ttk.Label(self.navegadorContainer,
        text=f"Navegador selecionado: {currentBrowser}",
        foreground="#454545")
        label.pack(pady="2")

      self.root.bind('<Return>', self.handleSalvarNavegador)
      self.root.mainloop()


    except Exception as e:
      messagebox.showerror("Erro em Navegador", e)
      self.root.destroy()
      self.janelaNavegador()