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

class Habilitacao:
  def __init__(self, habilitacao):
      self.master = i.Interfaces.novaJanela()
      self.habilitacaoContainer = Frame(self.master)
      self.habilitacaoContainer.pack()
      self.sessao_habilitacao = habilitacao
      self.janelaHabilitacao()

  def handleMudarHabilitacao(self):
    sigepe_novaHabilitacaoBotao = nav.find_element(By.XPATH, f"//*[contains(text(), '{self.seletorHabilitacoes.get()}')]")
    sigepe_novaHabilitacaoBotao.click()
    time.sleep(2)
    self.master.destroy()
    self.sessao_habilitacao.sessaoHabilitacaoContainer.destroy()
    self.sessao_habilitacao.habilitacao()

  def handleFecharJanela(self):
    sigepe_fecharHabilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['fecharHabilitacaoBotao'])
    sigepe_fecharHabilitacaoBotao.click()
    self.master.destroy()

  def janelaHabilitacao(self):
    try:
      sigepe_habilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['habilitacaoBotao'])
      sigepe_habilitacaoBotao.click()
      sigepe_HabilitacoesLinks = nav.find_elements(By.XPATH, xpaths['habilitacao']['habilitacoesLinks'])

      listaHabilitacoes = []
      for habilitacao in sigepe_HabilitacoesLinks:
        listaHabilitacoes.append(habilitacao.text)
      listaHabilitacoes.pop(0)

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

    except Exception as e:
      messagebox.showerror("Erro em Habilitações", e)
      self.master.destroy()
      self.janelaHabilitacao()

    self.master.protocol("WM_DELETE_WINDOW", self.handleFecharJanela)
