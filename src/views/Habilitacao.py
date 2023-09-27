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

class Habilitacao(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.master = Frame(self.root)
    self.master.pack()
    self.habilitacaoContainer = Frame(self.master)
    self.habilitacaoContainer.pack()
    t = thread.ThreadWithReturn(target=self.obterListaHabilitacoes)
    t.start()
    working = st.SigepeTrabalhando(t, "Buscando lista de habilitações disponíveis no Sigepe...")
    listaHabilitacoesResult = t.join()
    if (listaHabilitacoesResult[0]): self.listaHabilitacoes = listaHabilitacoesResult[1]
    else: messagebox.showerror("Erro ao buscar habilitações", listaHabilitacoesResult[1])
    self.janelaHabilitacao()

  @staticmethod
  def checarAcessoHabilitacao():
    try:
      wd.Webdriver.go(ac.AppConfig.urls["cadastrarAtoPublicacao"])
      if(wd.Webdriver.checkExistsByXpath(ac.AppConfig.xpaths["habilitacao"]["acessoNegadoHeader"])):
        wd.Webdriver.go(ac.AppConfig.urls["areaDeTrabalho"])
        return False
      else:
        return True
    except Exception as e:
        messagebox.showerror("Erro ao verificar o acesso da habilitação selecionada", e)

  def mudarHabilitacaoNoSigepe(self):
    try:
      sigepe_habilitacaoBotao = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['habilitacao']['habilitacaoBotao'])
      sigepe_habilitacaoBotao.click()
      if (sigepe_habilitacaoBotao.text == self.seletorHabilitacoes.get()):
        pass
      else:
        sigepe_novaHabilitacaoBotao = wd.Webdriver.nav.find_element(By.XPATH, f"//*[contains(text(), '{self.seletorHabilitacoes.get()}')]")
        sigepe_novaHabilitacaoBotao.click()
        time.sleep(2)
  
      checkLoadErrors = wd.Webdriver.checkErrorsLoadedPage() 
      if(not checkLoadErrors[0]):
        raise Exception(checkLoadErrors[1])

      if (Habilitacao.checarAcessoHabilitacao()):
        return [True]
      else:
        raise Exception(f"A habilitação {self.seletorHabilitacoes.get()} não tem acesso ao módulo Publicação do Sigepe. Selecione outra.")
    except Exception as e:
      return [False, e]

  def handleMudarHabilitacao(self, event = None):
    t = thread.ThreadWithReturn(target=self.mudarHabilitacaoNoSigepe)
    t.start()
    working = st.SigepeTrabalhando(t, "Definindo nova habilitação no Sigepe...")
    novaHabilitacaoResult = t.join()
    if (novaHabilitacaoResult[0]):
      self.root.destroy()
      sessao = s.Sessao()
    else:
      messagebox.showerror("Falha ao definir habilitação", novaHabilitacaoResult[1])

  def handleFecharJanela(self):
    confirmarFechar = messagebox.askquestion("Confirmar saída", "Tem certeza de que deseja fechar?\n\nCaso confirme, a aplicação será encerrada.")
    if (confirmarFechar == 'yes'):
      wd.Webdriver.nav.quit()
      self.root.destroy()

  def obterListaHabilitacoes(self):
    try:
      wd.Webdriver.go(ac.AppConfig.urls["areaDeTrabalho"])
      sigepe_habilitacaoBotao = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['habilitacao']['habilitacaoBotao'])
      sigepe_habilitacaoBotao.click()
      sigepe_HabilitacoesLinks = wd.Webdriver.nav.find_elements(By.XPATH, ac.AppConfig.xpaths['habilitacao']['habilitacoesLinks'])
      listaHabilitacoes = []
      for habilitacao in sigepe_HabilitacoesLinks:
        listaHabilitacoes.append(habilitacao.text)
      sigepe_fecharHabilitacoesBotao = wd.Webdriver.nav.find_element(By.XPATH, ac.AppConfig.xpaths['habilitacao']['fecharHabilitacaoBotao'])
      sigepe_fecharHabilitacoesBotao.click()
      return [True, listaHabilitacoes]
    except Exception as e:
      return [False, e]

  def janelaHabilitacao(self):
    try:
      label = ttk.Label(self.habilitacaoContainer, text="Selecione a habilitação:")
      label.pack()
      valorSelecionado = StringVar()
      self.seletorHabilitacoes = ttk.Combobox(
        self.habilitacaoContainer,
        textvariable=valorSelecionado,
        values=self.listaHabilitacoes,
        state="readonly",
        width=50)
      self.seletorHabilitacoes.pack(fill=X, expand=YES, pady="5")

      botaoSelecionarHabilitacao = Button(
        self.habilitacaoContainer,
        text="Definir habilitação",
        font=ac.AppConfig.fontes["botao"],
        width=20,
        command=self.handleMudarHabilitacao
      )
      botaoSelecionarHabilitacao.pack(pady="5")

      infoLabel = ttk.Label(
        self.habilitacaoContainer,
        text="A habilitação selecionada será utilizada para realizar\no cadastro dos documentos. Selecione uma habilitação\nque tenha acesso ao módulo de Publicação do Sigepe.",
        background="#fff9d9",
        foreground="#85701d",
        padding=4,
        justify=CENTER)
      infoLabel.pack(pady="5")

      self.root.bind('<Return>', self.handleMudarHabilitacao)
      self.root.protocol("WM_DELETE_WINDOW", self.handleFecharJanela)
      self.root.mainloop()

    except Exception as e:
      messagebox.showerror("Erro em Habilitações", e)
      self.master.destroy()
      self.janelaHabilitacao()