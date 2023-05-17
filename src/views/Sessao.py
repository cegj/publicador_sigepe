from tkinter import *
from tkinter import messagebox
from controllers import Webdriver as wd
from views import Interfaces as i
from views.sessao import Habilitacao as s_h
from views.sessao import Acao as s_a
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
from views.sessao import ConfiguracoesBtn as s_cb
from views.sessao import ArquivosPublicar as s_ap
from copy import copy
from controllers import UserConfig as uc
from controllers import AppConfig as ac

class Sessao(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.userConfig = copy(uc.UserConfig.obterConfiguracoesSalvas())
    self.files = []

  def handleFecharJanela(self):
    confirmarFechar = messagebox.askquestion("Confirmar saída", "Tem certeza de que deseja fechar?\n\nCaso confirme, a aplicação será encerrada.")
    if (confirmarFechar == 'yes'):
      wd.Webdriver.nav.quit()
      self.root.destroy()

  def sessao(self):
    wd.Webdriver.go(ac.AppConfig.urls["cadastrarAtoPublicacao"])
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
      font=ac.AppConfig.fontes["titulo"],
      anchor=CENTER
    )
    tituloDadosPublicacao.pack()

    s_h.Habilitacao(self, self.linha2c1)
    # s_a.Acao(self, self.linha2c1)
    s_eb.EdicaoBoletim(self, self.linha3c1)
    s_ta.TipoAssinatura(self, self.linha3c1)
    s_tn.TipoNumero(self, self.linha3c1)
    s_e.Especie(self, self.linha4c1)
    s_da.DataAssinatura(self, self.linha4c1)
    self.handleFieldState("tipo_assinatura", "manual", "dataAssinaturaInput")
    s_dp.DataPublicacao(self, self.linha4c1)
    self.handleFieldState("edicao_bgp", "normal", "dataPublicacaoInput")
    s_tas.TemaAssunto(self, self.linha5c1)
    s_or.Orgao(self, self.linha6c1)
    s_up.Upag(self, self.linha6c1)
    s_uo.Uorg(self, self.linha6c1)
    s_ra.ResponsavelAssinatura(self, self.linha7c1)
    s_cr.CargoResponsavel(self, self.linha7c1)
    s_mdb.ManterDadosBtn(self, self.linha8c1)
    s_cb.ConfiguracoesBtn(self, self.linha8c1)

    tituloArquivos = Label(
      self.linha1c2,
      text="Arquivos",
      font=ac.AppConfig.fontes["titulo"],
      anchor=CENTER
    )
    tituloArquivos.pack()
    s_ap.ArquivosPublicar(self, self.linha2c2)
    self.root.protocol("WM_DELETE_WINDOW", self.handleFecharJanela)
    self.root.mainloop()

  def handleFieldState(self, fieldName, valueToEnable, target):
    try:
      field = getattr(self, target)
      if (self.userConfig["valores_sigepe"][fieldName].lower() == valueToEnable.lower()): field.config(state=NORMAL)
      else: field.config(state=DISABLED)
    except Exception as e:
      print(e)