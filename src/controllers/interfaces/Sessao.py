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
from controllers import Interfaces as i
from controllers.interfaces import Habilitacao as h
from controllers.interfaces import Delimitadores as d
from copy import copy
from controllers import UserConfig as uc
from helpers import goTo as gt
from helpers import checkExistsByXpath as cebx
from helpers import waitForLoading as wfl
import os

class Sessao(i.Interfaces):
  def __init__(self):
    super().__init__()
    self.userConfig = copy(uc.UserConfig.obterConfiguracoesSalvas())
    self.files = []

  def irParaPaginaPublicacao(self):
    try:
      gt.goTo("https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")
      if(cebx.checkExistsByXpath(xpaths["habilitacao"]["acessoNegadoHeader"])):
        messagebox.showerror("Acesso negado", "A habilitação não possui acesso ao módulo de Publicação. Selecione uma habilitação com acesso.")
        gt.goTo("https://admsistema.sigepe.gov.br/sigepe-as-web/private/areaTrabalho/index.jsf")
    except Exception as e:
        messagebox.showerror("Erro ao acessar Cadastrar Ato para Publicação", e)


  def sessao(self):
    self.sessaoContainer = Frame(self.root)
    self.sessaoContainer.grid()
    sessaoContainerTitulo = Label(self.sessaoContainer, text="Publicar documentos")
    sessaoContainerTitulo.configure(anchor="center")
    sessaoContainerTitulo["font"] = appConfig.fontes["titulo"]
    sessaoContainerTitulo.grid(column=1, row=0, columnspan=2)
    self.botoesContainer = Frame(self.sessaoContainer)
    self.botoesContainer.grid(row=13, column=1, sticky='w')
    self.definirHabilitacaoInicial()
    self.habilitacao()
    # self.diretorio_origem()
    self.diretorio_destino()
    self.edicao_bgp()
    self.tipo_assinatura()
    self.especie()
    self.tipo_preenchimento_numero()
    self.tema()
    self.assunto()
    self.data_assinatura()
    self.data_publicacao()
    self.orgao()
    self.upag()
    self.uorg()
    self.responsavel_assinatura()
    self.cargo_responsavel()
    self.salvar_configuracoes()
    self.abrir_edicao_delimitadores()
    self.arquivos()
    self.publicar()
    self.root.mainloop()

  def definirHabilitacaoInicial(self):
    sigepe_habilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['habilitacaoBotao'])
    sigepe_habilitacaoBotao.click()
    sigepe_novaHabilitacaoBotao = nav.find_element(By.XPATH, f"//*[contains(text(), '{self.userConfig['habilitacao']['inicial']}')]")
    sigepe_novaHabilitacaoBotao.click()
    time.sleep(2)

  def habilitacao(self):
    def abrirJanelaHabilitacao():
      janelaHabilitacao = h.Habilitacao(self)
    self.sessaoHabilitacaoContainer = Frame(self.sessaoContainer)
    self.sessaoHabilitacaoContainer.grid(row=1, column=1, columnspan=2, sticky='w')
    sigepe_habilitacaoBotao = nav.find_element(By.XPATH, xpaths['habilitacao']['habilitacaoBotao'])
    habilitacaoAtual = Label(
      self.sessaoHabilitacaoContainer,
      text=f"Habilitação atual: {sigepe_habilitacaoBotao.text}",
      anchor="w",
      font=appConfig.fontes["normal"])
    habilitacaoAtual.grid(column=0, row=1, columnspan=2, padx=10, pady=5, sticky='w')
    self.userConfig["habilitacao"]["inicial"] = sigepe_habilitacaoBotao.text
    botaoAlterarHabilitacao = Button(self.sessaoHabilitacaoContainer)
    botaoAlterarHabilitacao["text"] = "Alterar habilitação"
    botaoAlterarHabilitacao["font"] = appConfig.fontes["botao"]
    botaoAlterarHabilitacao["width"] = 20
    botaoAlterarHabilitacao["command"] = abrirJanelaHabilitacao
    botaoAlterarHabilitacao.grid(column=3, row=1, padx=10, pady=5, sticky='w')
    self.irParaPaginaPublicacao()

    # originPath = StringVar()
    # originPath.set(self.userConfig["dir"]["origem"])
    # def getOriginPath():
    #   originPath.set(filedialog.askdirectory())
    #   self.userConfig["dir"]["origem"] = originPath.get()
    # self.diretorioOrigemContainer = Frame(self.sessaoContainer)
    # self.diretorioOrigemContainer.grid(row=2, column=1, columnspan=2, sticky='w')
    # origemLabel = Label(
    #   self.diretorioOrigemContainer,
    #   text="Pasta de origem",
    #   font=appConfig.fontes["normal"]
    #   )
    # origemLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    # origemInput = Entry(
    #   self.diretorioOrigemContainer,
    #   textvariable=originPath,
    #   width=50,
    #   font=appConfig.fontes["normal"]
    #   )
    # origemInput.grid(column=2, row=0)
    # botaoDiretorioOrigem = Button(
    #   self.diretorioOrigemContainer,
    #   text="Alterar",
    #   font=appConfig.fontes["botao"],
    #   width=20,
    #   command=getOriginPath
    #   )
    # botaoDiretorioOrigem.grid(column=3, row=0, padx=10, pady=5, sticky='w')

  def diretorio_destino(self):
    targetPath = StringVar()
    targetPath.set(self.userConfig["dir"]["destino"])
    def getTargetPath():
      targetPath.set(filedialog.askdirectory())
      self.userConfig["dir"]["destino"] = targetPath.get()
    self.diretorioDestinoContainer = Frame(self.sessaoContainer)
    self.diretorioDestinoContainer.grid(row=3, column=1, columnspan=2, sticky='w')
    destinoLabel = Label(
      self.diretorioDestinoContainer,
      text="Pasta de destino",
      font=appConfig.fontes["normal"]
      )
    destinoLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    destinoInput = Entry(
      self.diretorioDestinoContainer,
      textvariable=targetPath,
      width=50,
      font=appConfig.fontes["normal"]
      )
    destinoInput.grid(column=2, row=0)
    botaoDiretorioDestino = Button(
      self.diretorioDestinoContainer,
      text="Alterar",
      font=appConfig.fontes["botao"],
      width=20,
      command=getTargetPath
      )
    botaoDiretorioDestino.grid(column=3, row=0, padx=10, pady=5, sticky='w')

  def edicao_bgp(self):
    def setSelected(event):
      self.userConfig["valores_sigepe"]["edicao_bgp"] = selected.get()
    self.edicaoBgpContainer = Frame(self.sessaoContainer)
    self.edicaoBgpContainer.grid(row=4, column=1, sticky='w')
    edicaoBgpLabel = Label(
      self.edicaoBgpContainer,
      text="Edição do boletim",
      font=appConfig.fontes["normal"]
      )
    edicaoBgpLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    selected = StringVar()
    selected.set(self.userConfig["valores_sigepe"]["edicao_bgp"])
    options = ["Normal", "Extraordinária"]
    seletorEdicaoBgp = ttk.Combobox(
      self.edicaoBgpContainer,
      textvariable=selected,
      values=options,
      state="readonly",
      width=20,
      font=appConfig.fontes["normal"]
      )
    seletorEdicaoBgp.grid(column=2, row=0)
    seletorEdicaoBgp.bind("<<ComboboxSelected>>", setSelected)

  def tipo_assinatura(self):
    def setSelected(event):
      self.userConfig["valores_sigepe"]["tipo_assinatura"] = selected.get()
    self.tipoAssinaturaContainer = Frame(self.sessaoContainer)
    self.tipoAssinaturaContainer.grid(row=4, column=2, sticky='w')
    tipoAssinaturaLabel = Label(
      self.tipoAssinaturaContainer,
      text="Tipo de assinatura",
      font=appConfig.fontes["normal"]
      )
    tipoAssinaturaLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    selected = StringVar()
    selected.set(self.userConfig["valores_sigepe"]["tipo_assinatura"])
    options = ["Digital", "Manual"]
    seletorTipoAssinatura = ttk.Combobox(
      self.tipoAssinaturaContainer,
      textvariable=selected,
      values=options,
      state="readonly",
      width=20,
      font=appConfig.fontes["normal"]
      )
    seletorTipoAssinatura.grid(column=2, row=0)
    seletorTipoAssinatura.bind("<<ComboboxSelected>>", setSelected)

  def especie(self):
    def setSelected(event):
      self.userConfig["valores_sigepe"]["especie"] = selected.get()
    self.especieContainer = Frame(self.sessaoContainer)
    self.especieContainer.grid(row=6, column=1, sticky='w')
    especieLabel = Label(
      self.especieContainer,
      text="Espécie",
      font=appConfig.fontes["normal"]
      )
    especieLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    selected = StringVar()
    selected.set(self.userConfig["valores_sigepe"]["especie"])
    options = ["Acordo Coletivo", "Apostila", "Ata", "Despacho", "Diretriz", "Edital", "Instrução Normativa", "Orientação Normativa", "Portaria", "Recomendação", "Resolução"]
    seletorEspecie = ttk.Combobox(
      self.especieContainer,
      textvariable=selected,
      values=options,
      state="readonly",
      width=20,
      font=appConfig.fontes["normal"]
      )
    seletorEspecie.grid(column=2, row=0)
    seletorEspecie.bind("<<ComboboxSelected>>", setSelected)

  def tipo_preenchimento_numero(self):
    def setSelected(event):
      self.userConfig["valores_sigepe"]["tipo_preenchimento"] = selected.get()
    self.tipoPreenchimentoContainer = Frame(self.sessaoContainer)
    self.tipoPreenchimentoContainer.grid(row=6, column=2, sticky='w')
    tipoPreenchimentoLabel = Label(
      self.tipoPreenchimentoContainer,
      text="Tipo de número",
      font=appConfig.fontes["normal"]
      )
    tipoPreenchimentoLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    selected = StringVar()
    selected.set(self.userConfig["valores_sigepe"]["tipo_preenchimento"])
    options = ["Automático", "Manual", "Sem Número"]
    seletorTipoPreenchimento = ttk.Combobox(
      self.tipoPreenchimentoContainer,
      textvariable=selected,
      values=options,
      state="readonly",
      width=10,
      font=appConfig.fontes["normal"]
      )
    seletorTipoPreenchimento.grid(column=2, row=0)
    seletorTipoPreenchimento.bind("<<ComboboxSelected>>", setSelected)


  def obterAssunto(self, tema):
    try:
      sigepe_temaSelect = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, xpaths["publicacao"]["temaSelect"])))
      sigepe_temaSelect.click()
      time.sleep(0.3)
      sigepe_buscarTemaInput = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, xpaths["publicacao"]["buscarTemaInput"])))
      sigepe_buscarTemaInput.send_keys(tema)
      time.sleep(1.5)
      sigepe_buscarTemaInput.send_keys(Keys.ENTER)
      wfl.waitForLoading()
      time.sleep(0.3)
      sigepe_buscarAssuntoBtn = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, xpaths["publicacao"]["buscarAssuntoBtn"])))
      sigepe_buscarAssuntoBtn.click()
      wfl.waitForLoading()
      sigepe_assuntosBtns = wait["regular"].until(EC.visibility_of_all_elements_located((By.XPATH, xpaths["publicacao"]["assuntosBtns"])))
      ultimoNivelAssunto = sigepe_assuntosBtns[-1]
      ultimoNivelAssunto.click()
      sigepe_selecionarAssuntoBtn = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, xpaths["publicacao"]["selecionarAssuntoBtn"])))
      sigepe_selecionarAssuntoBtn.click()
      return ultimoNivelAssunto.text
    except Exception as e:
      messagebox.showerror("Erro ao buscar assunto", e)
      return None

  def tema(self):
    def setTemaAssunto(event = None):
      self.userConfig["valores_sigepe"]["tema"] = selected.get()
      if (hasattr(self, 'assuntoContainer')):
        self.assuntoContainer.destroy()
      self.assuntoObtido = self.obterAssunto(selected.get())
      self.assunto()

    self.temaContainer = Frame(self.sessaoContainer)
    self.temaContainer.grid(row=7, column=1, columnspan=2, sticky='w')
    temaLabel = Label(
      self.temaContainer,
      text="Tema",
      font=appConfig.fontes["normal"]
      )

    temaLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    selected = StringVar()
    selected.set(self.userConfig["valores_sigepe"]["tema"])    
    sigepe_temas = nav.find_elements(By.XPATH, xpaths['publicacao']['temas'])
    listaTemas = []
    for tema in sigepe_temas:
      listaTemas.append(tema.get_attribute('innerText'))

    options = listaTemas
    seletorTema = ttk.Combobox(
      self.temaContainer,
      textvariable=selected,
      values=options,
      state="readonly",
      width=80,
      font=appConfig.fontes["normal"]
      )
    seletorTema.grid(column=2, row=0)
    setTemaAssunto()
    seletorTema.bind("<<ComboboxSelected>>", setTemaAssunto)

  def assunto(self):
    self.assuntoContainer = Frame(self.sessaoContainer)
    self.assuntoContainer.grid(row=8, column=1, columnspan=2, sticky='w')
    assuntoLabel = Label(
      self.assuntoContainer,
      text="Assunto",
      font=appConfig.fontes["normal"]
      )
    assuntoLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    if (hasattr(self, "assuntoObtido")): 
      assuntoSelecionado = Label(
        self.assuntoContainer,
        text= self.assuntoObtido if len(self.assuntoObtido) <= 70 else f"{self.assuntoObtido[1:70]}...",
        anchor="w",
        font=appConfig.fontes["normal"])
      assuntoSelecionado.grid(column=1, row=0, padx=10, pady=5, sticky='w')

  def data_assinatura(self):
    def setValue(a=None, b=None, c=None):
      self.userConfig["valores_sigepe"]["data_assinatura"] = value.get()
    self.dataAssinaturaContainer = Frame(self.sessaoContainer)
    self.dataAssinaturaContainer.grid(row=9, column=1, sticky='w')
    dataAssinaturaLabel = Label(
      self.dataAssinaturaContainer,
      text="Data de assinatura",
      font=appConfig.fontes["normal"]
      )
    dataAssinaturaLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    value = StringVar()
    value.trace_add("write", setValue)
    dataAssinaturaInput = Entry(
      self.dataAssinaturaContainer,
      width=20,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.userConfig["valores_sigepe"]["data_assinatura"])
    dataAssinaturaInput.grid(column=2, row=0)

  def data_publicacao(self):
    def setValue(a=None, b=None, c=None):
      self.userConfig["valores_sigepe"]["data_publicacao"] = value.get()
    self.dataPublicacaoContainer = Frame(self.sessaoContainer)
    self.dataPublicacaoContainer.grid(row=9, column=2, sticky='w')
    dataPublicacaoLabel = Label(
      self.dataPublicacaoContainer,
      text="Data de publicação",
      font=appConfig.fontes["normal"]
      )
    dataPublicacaoLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    value = StringVar()
    value.trace_add("write", setValue)
    dataPublicacaoInput = Entry(
      self.dataPublicacaoContainer,
      width=20,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.userConfig["valores_sigepe"]["data_publicacao"])
    dataPublicacaoInput.grid(column=2, row=0)

  def orgao(self):
    def setValue(a=None, b=None, c=None):
      self.userConfig["valores_sigepe"]["orgao"] = value.get()
    self.orgaoContainer = Frame(self.sessaoContainer)
    self.orgaoContainer.grid(row=10, column=1, columnspan=2, sticky='w')
    orgaoLabel = Label(
      self.orgaoContainer,
      text="Órgão",
      font=appConfig.fontes["normal"]
      )
    orgaoLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    value = StringVar()
    value.trace_add("write", setValue)
    orgaoInput = Entry(
      self.orgaoContainer,
      width=50,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.userConfig["valores_sigepe"]["orgao"])
    orgaoInput.grid(column=2, row=0)

  def upag(self):
    def setValue(a=None, b=None, c=None):
      self.userConfig["valores_sigepe"]["upag"] = value.get()
    self.upagContainer = Frame(self.sessaoContainer)
    self.upagContainer.grid(row=11, column=1, sticky='w')
    upagLabel = Label(
      self.upagContainer,
      text="UPAG",
      font=appConfig.fontes["normal"]
      )
    upagLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    value = StringVar()
    value.trace_add("write", setValue)
    upagInput = Entry(
      self.upagContainer,
      width=20,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.userConfig["valores_sigepe"]["upag"])
    upagInput.grid(column=2, row=0)

  def uorg(self):
    def setValue(a=None, b=None, c=None):
      self.userConfig["valores_sigepe"]["uorg"] = value.get()
    self.uorgContainer = Frame(self.sessaoContainer)
    self.uorgContainer.grid(row=11, column=2, sticky='w')
    uorgLabel = Label(
      self.uorgContainer,
      text="UORG",
      font=appConfig.fontes["normal"]
      )
    uorgLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    value = StringVar()
    value.trace_add("write", setValue)
    uorgInput = Entry(
      self.uorgContainer,
      width=20,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.userConfig["valores_sigepe"]["uorg"])
    uorgInput.grid(column=2, row=0)

  def responsavel_assinatura(self):
    def setValue(a=None, b=None, c=None):
      self.userConfig["valores_sigepe"]["responsavel_assinatura"] = value.get()
    self.responsavelAssinaturaContainer = Frame(self.sessaoContainer)
    self.responsavelAssinaturaContainer.grid(row=12, column=1, sticky='w')
    responsavelAssinaturaLabel = Label(
      self.responsavelAssinaturaContainer,
      text="Responsável pela assinatura",
      font=appConfig.fontes["normal"]
      )
    responsavelAssinaturaLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    value = StringVar()
    value.trace_add("write", setValue)
    responsavelAssinaturaInput = Entry(
      self.responsavelAssinaturaContainer,
      width=20,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.userConfig["valores_sigepe"]["responsavel_assinatura"])
    responsavelAssinaturaInput.grid(column=2, row=0)

  def cargo_responsavel(self):
    def setValue(a=None, b=None, c=None):
      self.userConfig["valores_sigepe"]["cargo_responsavel"] = value.get()
    self.cargoResponsavelContainer = Frame(self.sessaoContainer)
    self.cargoResponsavelContainer.grid(row=12, column=2, sticky='w')
    cargoResponsavelLabel = Label(
      self.cargoResponsavelContainer,
      text="Cargo do responsável",
      font=appConfig.fontes["normal"]
      )
    cargoResponsavelLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
    value = StringVar()
    value.trace_add("write", setValue)
    cargoResponsavelInput = Entry(
      self.cargoResponsavelContainer,
      width=20,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.userConfig["valores_sigepe"]["cargo_responsavel"])
    cargoResponsavelInput.grid(column=2, row=0)

  def salvar_configuracoes(self):
    botaoSalvarConfiguracoes = Button(
      self.botoesContainer,
      text="Manter configurações",
      font=appConfig.fontes["botao"],
      width=20,
      command=lambda: uc.UserConfig.salvarConfiguracoes(self.userConfig)
      )
    botaoSalvarConfiguracoes.grid(column=1, row=0, padx=10, pady=5, sticky='w')

  def abrir_edicao_delimitadores(self):
    def abrirJanelaEdicao():
      janelaEdicao = d.Delimitadores()
    editarDeliminatoresBtn = Button(
      self.botoesContainer,
      text="Editar delimitadores",
      font=appConfig.fontes["botao"],
      width=20,
      command=abrirJanelaEdicao
      )
    editarDeliminatoresBtn.grid(column=2, row=0, padx=10, pady=5, sticky='w')

  def arquivos(self):
    def getFiles():
      listbox.delete(0, 'end')
      self.files = filedialog.askopenfiles(mode='r', title="Selecionar arquivos para publicação", filetypes=[("Documentos RTF (Rich Text Format)", ".rtf")])
      for index, file in enumerate(self.files):
        listbox.insert(index, os.path.basename(file.name))

    self.arquivosContainer = Frame(self.sessaoContainer)
    self.arquivosContainer.grid(row=0, column=3, rowspan=14, sticky='w')
    listbox = Listbox(
      self.arquivosContainer,
      height = 20,
      width = 40,
      bg = "white",
      activestyle = 'dotbox',
      font = "Helvetica",
      fg = "gray"
    )
    listbox.grid(column=1, columnspan=2, row=1, padx=10, pady=5, sticky='')

    botaoDiretorioOrigem = Button(
      self.arquivosContainer,
      text="Selecionar arquivos",
      font=appConfig.fontes["botao"],
      width=20,
      command=getFiles
      )
    botaoDiretorioOrigem.grid(column=1, row=2, padx=10, pady=5, sticky='')

  def publicar(self):
    botaoDiretorioOrigem = Button(
      self.arquivosContainer,
      text="Publicar",
      font=appConfig.fontes["botao"],
      width=20,
      bg="#429321",
      fg="white"
      )
    botaoDiretorioOrigem.grid(column=2, row=2, padx=10, pady=5, sticky='')
