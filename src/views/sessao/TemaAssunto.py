from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from controllers import ObterDoSigepe as ods
from models import AppConfig as ac
from views import TemaAutomatico as ta
from helpers import ThreadWithReturn as thread
from views import SigepeTrabalhando as st

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
      font=ac.AppConfig.fontes["normal"]
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
      if (not self.sessao.sigepe_temas):
        t = thread.ThreadWithReturn(target=ods.ObterDoSigepe.temas)
        t.start()
        working = st.SigepeTrabalhando(t, "Buscando lista de temas no Sigepe...")
        self.sessao.sigepe_temas = t.join()
      self.tipoManual()
    elif (self.tipoSelecionado.get() == "Buscar no conteúdo do documento"):
      if (hasattr(self, 'temaAutomaticoContainer')): self.temaAutomaticoContainer.destroy()
      if (hasattr(self, 'assuntoManualContainer')): self.assuntoManualContainer.destroy()
      if (hasattr(self, 'temaManualContainer')): self.temaManualContainer.destroy()
      self.tipoAutomatico()

  def tipoAutomatico(self):
    def abrirJanela():
      janela = ta.TemaAutomatico(self.sessao)
    self.temaAutomaticoContainer = Frame(self.subcontainer)
    self.temaAutomaticoContainer.pack(side=LEFT, padx=5)
    self.botaoConfigTemaAutomatico = Button(
      self.temaAutomaticoContainer,
      text="Configurar busca de temas",
      font=ac.AppConfig.fontes["botao"],
      width=30,
      command=abrirJanela
      )
    self.botaoConfigTemaAutomatico.pack(side=LEFT)

  def tipoManual(self):
    try:
      self.temaManualContainer = Frame(self.subcontainer)
      self.temaManualContainer.pack(side=LEFT, padx=5)
      self.temaSelected = StringVar()
      self.temaSelected.set(self.sessao.userConfig["valores_sigepe"]["tema"])
      seletorTema = ttk.Combobox(
        self.temaManualContainer,
        textvariable=self.temaSelected,
        values=self.sessao.sigepe_temas,
        state="readonly",
        width=27,
        font=ac.AppConfig.fontes["normal"]
        )
      seletorTema.pack(side=LEFT)
      self.setTemaManual()
      seletorTema.bind("<<ComboboxSelected>>", self.setTemaManual)
    except Exception as e:
      print(e)

  def setTemaManual(self, event = None):
    self.sessao.userConfig["valores_sigepe"]["tema"] = self.temaSelected.get()
    if (hasattr(self, 'assuntoManualContainer')): self.assuntoManualContainer.destroy()
    if (self.sessao.userConfig["valores_sigepe"]["tema"]):
      t = thread.ThreadWithReturn(target=ods.ObterDoSigepe.assuntos, args=(self.temaSelected.get(),))
      t.start()
      working = st.SigepeTrabalhando(t, "Buscando assuntos relacionados ao tema no Sigepe...")
      self.sigepe_assuntos = t.join()
    else: self.sigepe_assuntos = []
    self.assuntoManual()

  def assuntoManual(self):
    self.assuntoManualContainer = Frame(self.subcontainer)
    self.assuntoManualContainer.pack(side=LEFT, padx=5)
    assuntoLabel = Label(
      self.assuntoManualContainer,
      text="Assunto",
      font=ac.AppConfig.fontes["normal"]
      )
    assuntoLabel.pack(side=LEFT)
    self.assuntoSelected = StringVar()
    if (self.sessao.userConfig["valores_sigepe"]["tema"]): listaAssuntos = self.sigepe_assuntos
    else: listaAssuntos = []
    if (not self.sessao.userConfig["valores_sigepe"]["assunto"] in listaAssuntos):
      self.sessao.userConfig["valores_sigepe"]["assunto"] = ""
    self.assuntoSelected.set(self.sessao.userConfig["valores_sigepe"]["assunto"])    
    seletorAssunto = ttk.Combobox(
      self.assuntoManualContainer,
      textvariable=self.assuntoSelected,
      values=listaAssuntos,
      state="readonly",
      width=20,
      font=ac.AppConfig.fontes["normal"]
      )
    seletorAssunto.pack(side=LEFT)
    seletorAssunto.bind("<<ComboboxSelected>>", self.setAssuntoManual)

  def setAssuntoManual(self, event = None):
    self.sessao.userConfig["valores_sigepe"]["assunto"] = self.assuntoSelected.get()
