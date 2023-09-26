from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from views import Interfaces as i
from models import UserConfig as uc
from models import AppConfig as ac
from copy import copy

class RemoverTermosConteudo:
  def __init__(self):
      self.config = copy(uc.UserConfig.obterTermosConteudoRemover())
      self.master = i.Interfaces.novaJanela()
      self.termosContainer = Frame(self.master)
      self.termosContainer.pack()
      self.janelaTermosRemover()

  def janelaTermosRemover(self):
    self.termos()
    self.salvar_configuracoes()

  def termos(self):
    def setValue(a=None, b=None, c=None):
      self.config["termos"] = self.termosInput.get("1.0", END)
    termosLabel = Label(
      self.termosContainer,
      text="Termos para remover do conteúdo",
      font=ac.AppConfig.fontes["normal"]
      )
    termosLabel.pack()
    self.termosInput = Text(
      self.termosContainer,
      width=40,
      height=10,
      font=ac.AppConfig.fontes["normal"]
      )
    self.termosInput.insert(END, self.config["termos"])
    self.termosInput.pack()

  def salvar_configuracoes(self):
    def salvar():
      try:
        termos = self.termosInput.get("1.0", END).replace("\n", "")
        self.config["termos"] = termos
        uc.UserConfig.salvarTermosConteudoRemover(self.config)
        self.master.destroy()
      except Exception as e:
        messagebox.showerror("Erro ao gravar termos para remover do conteúdo", e)

    container = Frame(self.termosContainer)
    container.pack()
    self.salvarConfigBtn = Button(
      container,
      text="Salvar",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=salvar
    )
    self.salvarConfigBtn.pack(pady="5")

    infoLabel = ttk.Label(
      container,
      text="Todos os termos informados acima encontrados no conteúdo\ndos documentos serão removidos ao realizar a publicação.\nPara informar diferentes termos, separe-os com ponto-e-vírgula.\nEste recurso não afeta o conteúdo dos arquivos.",
      background="#fff9d9",
      foreground="#85701d",
      padding=4,
      justify=CENTER)
    infoLabel.pack(pady="5")