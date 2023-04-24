from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import appConfig
from Webdriver import nav
from Webdriver import wait
from appXpaths import xpaths
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from tkinter import filedialog
from views import Interfaces as i
from views import Habilitacao as h
from views import Delimitadores as d
from views import Pospublicacao as pp
from views import RemoverTermosConteudo as rtc
from views import Publicacao as p
from views import TemaAutomatico as ta
from views.sessao import Habilitacao as s_h
from views.sessao import EdicaoBoletim as s_eb
from views.sessao import TipoAssinatura as s_ta
from views.sessao import Especie as s_e
from views.sessao import TipoNumero as s_tn
from views.sessao import TemaAssunto as s_tas
from views.sessao import DataAssinatura as s_da
from views.sessao import DataPublicacao as s_dp
from views.sessao import Orgao as s_or
from views.sessao import Upag as s_up
from views.sessao import Uorg as s_uo
from views.sessao import ResponsavelAssinatura as s_ra
from views.sessao import CargoResponsavel as s_cr
from views.sessao import ManterDadosBtn as s_mdb
from views.sessao import AbrirDelimitadoresBtn as s_adb
from views.sessao import AbrirPospublicacaoBtn as s_apb
from views.sessao import AbrirRemocaoTermosBtn as s_art
from views.sessao import ArquivosPublicar as s_ap
from copy import copy
from controllers import UserConfig as uc
from helpers import goTo as gt
from helpers import checkExistsByXpath as cebx
from helpers import waitForLoading as wfl
import os
from threading import Thread
from controllers import ObterDoSigepe as ods

class Sessao(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.userConfig = copy(uc.UserConfig.obterConfiguracoesSalvas())
    self.files = []

  def handleFecharJanela(self):
    confirmarFechar = messagebox.askquestion("Confirmar saída", "Tem certeza de que deseja fechar? Caso confirme, a aplicação será encerrada.")
    if (confirmarFechar == 'yes'):
      nav.quit()
      self.root.destroy()

  def sessao(self):
    gt.goTo("https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")
    self.sessaoContainer = Frame(self.root)
    self.sessaoContainer.grid()

    self.coluna1 = Frame(self.sessaoContainer)
    self.coluna1.grid(row=1, column=1, sticky="w")
    self.coluna2 = Frame(self.sessaoContainer)
    self.coluna2.grid(row=1, column=2, sticky="w")

    self.linha1c1 = Frame(self.coluna1)
    self.linha1c1.pack(pady=7)
    self.linha2c1 = Frame(self.coluna1)
    self.linha2c1.pack(anchor=W, pady=7)
    self.linha3c1 = Frame(self.coluna1)
    self.linha3c1.pack(anchor=W, pady=7)
    self.linha4c1 = Frame(self.coluna1)
    self.linha4c1.pack(anchor=W, pady=7)
    self.linha5c1 = Frame(self.coluna1)
    self.linha5c1.pack(anchor=W, pady=7)
    self.linha6c1 = Frame(self.coluna1)
    self.linha6c1.pack(anchor=W, pady=7)
    self.linha7c1 = Frame(self.coluna1)
    self.linha7c1.pack(anchor=W, pady=7)
    self.linha8c1 = Frame(self.coluna1)
    self.linha8c1.pack(anchor=W, pady=7)
    self.linha1c2 = Frame(self.coluna2)
    self.linha1c2.pack(pady=7)
    self.linha2c2 = Frame(self.coluna2)
    self.linha2c2.pack(anchor=W, pady=7)

    tituloDadosPublicacao = Label(
      self.linha1c1,
      text="Dados da publicação",
      font=appConfig.fontes["titulo"],
      anchor=CENTER
    )
    tituloDadosPublicacao.pack()

    s_h.Habilitacao(self, self.linha2c1)
    s_eb.EdicaoBoletim(self, self.linha3c1)
    s_ta.TipoAssinatura(self, self.linha3c1)
    s_tn.TipoNumero(self, self.linha3c1)
    s_e.Especie(self, self.linha4c1)
    s_da.DataAssinatura(self, self.linha4c1)
    s_dp.DataPublicacao(self, self.linha4c1)
    s_tas.TemaAssunto(self, self.linha5c1)
    s_or.Orgao(self, self.linha6c1)
    s_up.Upag(self, self.linha6c1)
    s_uo.Uorg(self, self.linha6c1)
    s_ra.ResponsavelAssinatura(self, self.linha7c1)
    s_cr.CargoResponsavel(self, self.linha7c1)
    s_mdb.ManterDadosBtn(self, self.linha8c1)
    s_adb.AbrirDelimitadoresBtn(self, self.linha8c1)
    s_apb.AbrirPospublicacaoBtn(self, self.linha8c1)
    s_art.AbrirRemocaoTermosBtn(self, self.linha8c1)

    tituloArquivos = Label(
      self.linha1c2,
      text="Arquivos",
      font=appConfig.fontes["titulo"],
      anchor=CENTER
    )
    tituloArquivos.pack()
    s_ap.ArquivosPublicar(self, self.linha2c2)
    self.root.protocol("WM_DELETE_WINDOW", self.handleFecharJanela)
    self.root.mainloop()