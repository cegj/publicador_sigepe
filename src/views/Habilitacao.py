from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import appConfig
from Webdriver import nav
from appXpaths import xpaths
from selenium.webdriver.common.by import By
import time
from views import Interfaces as i
from views import Sessao as s
from helpers import goTo as gt
from helpers import checkExistsByXpath as cebx

class Habilitacao(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.master = Frame(self.root)
    self.master.pack()
    self.habilitacaoContainer = Frame(self.master)
    self.habilitacaoContainer.pack()
    self.janelaHabilitacao()

  @staticmethod
  def checarAcessoHabilitacao():
    try:
      gt.goTo("https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")
      if(cebx.checkExistsByXpath(xpaths["habilitacao"]["acessoNegadoHeader"])):
        gt.goTo("https://admsistema.sigepe.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")
        return False
      else:
        return True
    except Exception as e:
        messagebox.showerror("Erro ao verificar o acesso da habilitação selecionada", e)

  def handleMudarHabilitacao(self, event = None):
    if (self.sigepe_habilitacaoBotao.text == self.seletorHabilitacoes.get()):
      messagebox.showinfo("Não houve alteração", f"A habilitação {self.seletorHabilitacoes.get()} já é a habilitação ativa no Sigepe no momento.")
    else:
      sigepe_novaHabilitacaoBotao = nav.find_element(By.XPATH, f"//*[contains(text(), '{self.seletorHabilitacoes.get()}')]")
      sigepe_novaHabilitacaoBotao.click()
      time.sleep(2)
      if (Habilitacao.checarAcessoHabilitacao()):
        self.root.destroy()
        sessao = s.Sessao()
        sessao.sessao()
      else:
        messagebox.showinfo("Habilitação sem acesso", f"A habilitação {self.seletorHabilitacoes.get()} não tem acesso ao módulo Publicação do Sigepe. Selecione outra.")
        self.root.destroy()
        novaInstancia = Habilitacao()

  def handleFecharJanela(self):
    confirmarFechar = messagebox.askquestion("Confirmar saída", "Tem certeza de que deseja fechar? Caso confirme, a aplicação será encerrada.")
    if (confirmarFechar == 'yes'):
      nav.quit()
      self.root.destroy()

  def janelaHabilitacao(self):
    try:
      gt.goTo("https://admsistema.sigepe.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")
      self.sigepe_habilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['habilitacaoBotao'])
      self.sigepe_habilitacaoBotao.click()
      sigepe_HabilitacoesLinks = nav.find_elements(By.XPATH, xpaths['habilitacao']['habilitacoesLinks'])

      listaHabilitacoes = []
      for habilitacao in sigepe_HabilitacoesLinks:
        listaHabilitacoes.append(habilitacao.text)

      label = ttk.Label(self.habilitacaoContainer, text="Selecione a habilitação:")
      label.pack()
      valorSelecionado = StringVar()
      self.seletorHabilitacoes = ttk.Combobox(
        self.habilitacaoContainer,
        textvariable=valorSelecionado,
        values=listaHabilitacoes,
        state="readonly",
        width=50)
      self.seletorHabilitacoes.pack(fill=X, expand=YES)

      botaoSelecionarHabilitacao = Button(
        self.habilitacaoContainer,
        text="Alterar habilitação",
        font=appConfig.fontes["botao"],
        width=20,
        command=self.handleMudarHabilitacao
      )
      botaoSelecionarHabilitacao.pack()
      self.root.bind('<Return>', self.handleMudarHabilitacao)
      self.root.protocol("WM_DELETE_WINDOW", self.handleFecharJanela)
      self.root.mainloop()

    except Exception as e:
      messagebox.showerror("Erro em Habilitações", e)
      self.master.destroy()
      self.janelaHabilitacao()