from tkinter import *
from tkinter import ttk
from Webdriver import nav
from selenium.webdriver.common.by import By
from controllers import ObterDoSigepe as ods
import appConfig
from views import Habilitacao as h
from views import TemaAutomatico as ta

class TemaAssunto:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.subcontainer = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.subcontainer)
    self.subcontainer.pack(side=LEFT, padx=10)
    temaLabel = Label(
      self.subcontainer,
      text="Tema",
      font=appConfig.fontes["normal"]
      )
    temaLabel.pack(side=LEFT)
    self.seletorTipoTemaAssunto()

  def seletorTipoTemaAssunto(self):      
    tipoTemaOptionsList = ["Selecionar manualmente", "Buscar no conteúdo do documento"]
    if self.sessao.userConfig["tipo_tema_assunto"] not in tipoTemaOptionsList:
          self.sessao.userConfig["tipo_tema_assunto"] = "Selecionar manualmente"
    tipoTemaOptionsList.remove(self.sessao.userConfig["tipo_tema_assunto"])
    self.tipoSelecionado = StringVar()
    self.tipoSelecionado.set(self.sessao.userConfig["tipo_tema_assunto"])
    optionMenu = OptionMenu(
      self.subcontainer,
      self.tipoSelecionado,
      self.tipoSelecionado.get(),
      *tipoTemaOptionsList,
      command=self.setTipoSelecionado
    )
    optionMenu.pack(side=LEFT)
    self.setTipoSelecionado()
  
  def setTipoSelecionado(self, event = None):
    self.sessao.userConfig["tipo_tema_assunto"] = self.tipoSelecionado.get()
    if (self.tipoSelecionado.get() == "Selecionar manualmente"):
      if (hasattr(self, 'temaManualContainer')): self.temaManualContainer.destroy()
      if (hasattr(self, 'assuntoManualContainer')): self.assuntoManualContainer.destroy()
      if (hasattr(self, 'temaAutomaticoContainer')): self.temaAutomaticoContainer.destroy()
      self.tipoManual()
    elif (self.tipoSelecionado.get() == "Buscar no conteúdo do documento"):
      if (hasattr(self, 'temaAutomaticoContainer')): self.temaAutomaticoContainer.destroy()
      if (hasattr(self, 'assuntoManualContainer')): self.assuntoManualContainer.destroy()
      if (hasattr(self, 'temaManualContainer')): self.temaManualContainer.destroy()
      self.tipoAutomatico()

  def tipoAutomatico(self):
    def abrirJanela():
      janela = ta.TemaAutomatico()
    self.temaAutomaticoContainer = Frame(self.subcontainer)
    self.temaAutomaticoContainer.pack(side=LEFT, padx=5)
    self.botaoConfigTemaAutomatico = Button(
      self.temaAutomaticoContainer,
      text="Configurar busca de temas",
      font=appConfig.fontes["botao"],
      width=30,
      command=abrirJanela
      )
    self.botaoConfigTemaAutomatico.pack(side=LEFT)

  def tipoManual(self):
    self.temaManualContainer = Frame(self.subcontainer)
    self.temaManualContainer.pack(side=LEFT, padx=5)
    self.temaSelected = StringVar()
    self.temaSelected.set(self.sessao.userConfig["valores_sigepe"]["tema"])    
    listaTemas = ods.ObterDoSigepe.temas()
    seletorTema = ttk.Combobox(
      self.temaManualContainer,
      textvariable=self.temaSelected,
      values=listaTemas,
      state="readonly",
      width=40,
      font=appConfig.fontes["normal"]
      )
    seletorTema.pack(side=LEFT)
    self.setTemaManual()
    seletorTema.bind("<<ComboboxSelected>>", self.setTemaManual)

  def setTemaManual(self, event = None):
    self.sessao.userConfig["valores_sigepe"]["tema"] = self.temaSelected.get()
    if (hasattr(self, 'assuntoManualContainer')): self.assuntoManualContainer.destroy()
    self.assuntoManual()

  def assuntoManual(self):
    self.assuntoManualContainer = Frame(self.subcontainer)
    self.assuntoManualContainer.pack(side=LEFT, padx=5)
    assuntoLabel = Label(
      self.assuntoManualContainer,
      text="Assunto",
      font=appConfig.fontes["normal"]
      )
    assuntoLabel.pack(side=LEFT)
    self.assuntoSelected = StringVar()
    if (self.sessao.userConfig["valores_sigepe"]["tema"]): listaAssuntos = ods.ObterDoSigepe.assuntos(self.sessao.userConfig["valores_sigepe"]["tema"])
    else: listaAssuntos = []
    if (not self.sessao.userConfig["valores_sigepe"]["assunto"] in listaAssuntos):
      self.sessao.userConfig["valores_sigepe"]["assunto"] = ""
    self.assuntoSelected.set(self.sessao.userConfig["valores_sigepe"]["assunto"])    
    seletorAssunto = ttk.Combobox(
      self.assuntoManualContainer,
      textvariable=self.assuntoSelected,
      values=listaAssuntos,
      state="readonly",
      width=30,
      font=appConfig.fontes["normal"]
      )
    seletorAssunto.pack(side=LEFT)
    seletorAssunto.bind("<<ComboboxSelected>>", self.setAssuntoManual)

  def setAssuntoManual(self, event = None):
    self.sessao.userConfig["valores_sigepe"]["assunto"] = self.assuntoSelected.get()
