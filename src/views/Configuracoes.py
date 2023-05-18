from tkinter import *
from tkinter import messagebox
from views import Interfaces as i
from models import AppConfig as ac
from views.configuracoes import Delimitadores as d
from views.configuracoes import Pospublicacao as pp
from views.configuracoes import RemoverTermosConteudo as rtc
from views.configuracoes import VerVariaveis as vv
import webbrowser
from threading import Thread

class Configuracoes:
  def __init__(self):
      self.master = i.Interfaces.novaJanela()
      self.container = Frame(self.master)
      self.container.pack()
      self.janelaConfiguracoes()

  def janelaConfiguracoes(self):
    titulo = Label(
      self.container,
      text="Configurações",
      font=ac.AppConfig.fontes["titulo"],
      anchor=CENTER
    )
    titulo.pack()

    self.delimitadores()
    self.pos_publicacao()
    self.remocao_termos()
    self.variaveis()
    self.ajuda()

  def delimitadores(self):
    btn = Button(
      self.container,
      text="Delimitadores",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=d.Delimitadores
      )
    btn.pack(padx=10, pady=7)

  def pos_publicacao(self):
    btn = Button(
      self.container,
      text="Pós-publicação",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=pp.Pospublicacao
      )
    btn.pack(padx=10, pady=7)

  def remocao_termos(self):
    btn = Button(
      self.container,
      text="Remoção de termos",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=rtc.RemoverTermosConteudo
      )
    btn.pack(padx=10, pady=7)

  def variaveis(self):
    btn = Button(
      self.container,
      text="Lista de variáveis",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=vv.VerVariaveis
      )
    btn.pack(padx=10, pady=7)

  def ajuda(self):
    def abrirAjuda():
      webbrowser.open_new_tab("https://cegj.notion.site/Publicador-Sigepe-v1-1-1-Documenta-o-b43e1fcd6f9f46dbb7c14924d62a1c69")

    btn = Button(
      self.container,
      text="Ajuda",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=lambda: Thread(target=abrirAjuda).start()
      )
    btn.pack(padx=10, pady=7)