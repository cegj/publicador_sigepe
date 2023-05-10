import appConfig
from controllers import UserConfig as uc
from views import Interfaces as i
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from copy import copy
from controllers import ObterDoSigepe as ods

class TemaAutomatico:
  def __init__(self):
      self.autoThemes = copy(uc.UserConfig.obterAutoTemasAssuntos())
      self.master = i.Interfaces.novaJanela()
      self.temaAutomaticoContainer = Frame(self.master)
      self.temaAutomaticoContainer.pack()
      self.janelaTemaAutomatico()
      self.sigepe_temas = ods.ObterDoSigepe.temas()

  def janelaTemaAutomatico(self):
    self.listaTemasCadastrados()
    self.btns()

  def updateThemesList(self):
    self.themesList.delete(0, END)
    for theme in self.autoThemes.keys():
      self.themesList.insert(END, theme)

  def janelaCadastroEdicao(self, editItemKey = None):
    def save():
      if (editItemKey):
        newEditItemKey = self.termToFindValue.get() 
        if (newEditItemKey != editItemKey):
          self.autoThemes[newEditItemKey] = self.autoThemes[editItemKey]
          del self.autoThemes[editItemKey]
        self.autoThemes[newEditItemKey]["tema"] = self.temaSelected.get()
        self.autoThemes[newEditItemKey]["assunto"] = self.assuntoSelected.get()
        uc.UserConfig.salvarAutoTemasAssuntos(self.autoThemes)
      else:
        self.autoThemes[self.termToFindValue.get()] = {
          "tema": self.temaSelected.get(),
          "assunto": self.assuntoSelected.get()}
        uc.UserConfig.salvarAutoTemasAssuntos(self.autoThemes)
      self.editWindow.destroy()
      self.updateThemesList()

    def delete():
      answer = messagebox.askyesno("Confirmar exclusão", f"Deseja realmente apagar o termo {editItemKey}?")
      if (answer == True):
        del self.autoThemes[editItemKey]
        uc.UserConfig.salvarAutoTemasAssuntos(self.autoThemes)
        self.editWindow.destroy()
        self.updateThemesList()

    def assunto():
      self.sigepe_assuntos = ods.ObterDoSigepe.assuntos(self.temaSelected.get())
      self.assuntoContainer = Frame(self.editWindow)
      self.assuntoContainer.grid(row=3, column=1)
      assuntoLabel = Label(
        self.assuntoContainer,
        text="Assunto correspondente",
        font=appConfig.fontes["normal"]
        )
      assuntoLabel.pack()
      self.assuntoSelected = StringVar()
      if (editItemKey):
        if (not self.editItem["assunto"] in self.sigepe_assuntos): self.assuntoSelected.set("")
        else: self.assuntoSelected.set(self.editItem["assunto"]) 
      seletorAssunto = ttk.Combobox(
        self.assuntoContainer,
        textvariable=self.assuntoSelected,
        values=self.sigepe_assuntos,
        state="readonly",
        width=40,
        font=appConfig.fontes["normal"]
        )
      seletorAssunto.pack()

    def buildAssunto(Event = None):
      if (hasattr(self, 'assuntoContainer')): self.assuntoContainer.destroy()
      assunto()

    self.editWindow = i.Interfaces.novaJanela()

    if (editItemKey): self.editItem = self.autoThemes[editItemKey]
  
    self.termoContainer = Frame(self.editWindow)
    self.termoContainer.grid(row=1, column=1)
    termoLabel = Label(
      self.termoContainer,
      text="Termo para busca no conteúdo",
      font=appConfig.fontes["normal"]
      )
    termoLabel.pack()
    self.termToFindValue = StringVar()
    termoInput = Entry(
      self.termoContainer,
      width=42,
      textvariable=self.termToFindValue,
      font=appConfig.fontes["normal"]
      )
    if (editItemKey): self.termToFindValue.set(editItemKey)
    termoInput.pack()

    self.temaContainer = Frame(self.editWindow)
    self.temaContainer.grid(row=2, column=1)
    temaLabel = Label(
      self.temaContainer,
      text="Tema correspondente",
      font=appConfig.fontes["normal"]
      )
    temaLabel.pack()
    self.temaSelected = StringVar()
    if (editItemKey): self.temaSelected.set(self.editItem["tema"])    
    seletorTema = ttk.Combobox(
      self.temaContainer,
      textvariable=self.temaSelected,
      values=self.sigepe_temas,
      state="readonly",
      width=40,
      font=appConfig.fontes["normal"]
      )
    seletorTema.pack()
    seletorTema.bind("<<ComboboxSelected>>", buildAssunto)

    if (editItemKey): buildAssunto()

    botoesContainer = Frame(self.editWindow)
    botoesContainer.grid(row=4, column=1)
    if (editItemKey):
      botaoApagar = Button(
        botoesContainer,
        text="Apagar",
        font=appConfig.fontes["botao"],
        width=15,
        command=delete
        )
      botaoApagar.grid(column=1, row=1, padx=10, pady=10)
    
    botaoSalvar = Button(
      botoesContainer,
      text="Salvar",
      font=appConfig.fontes["botao"],
      width=15,
      command=save
      )
    botaoSalvar.grid(column=2, row=1, padx=10, pady=10)

  def listaTemasCadastrados(self):
    def abrirEdicao(Event = None):
      self.janelaCadastroEdicao(self.themesList.selection_get())

    self.themesList = Listbox(
      self.temaAutomaticoContainer,
      height = 15,
      width = 30,
      bg = "white",
      font = "Helvetica",
      fg = "gray",
      activestyle="none"
    )
    self.themesList.pack()
    self.themesList.bind('<Double-Button>', abrirEdicao)
    self.updateThemesList()

  def btns(self):
    self.botoesContainer = Frame(self.temaAutomaticoContainer)
    self.botoesContainer.pack()
    self.botaoCadastrarNovo = Button(
      self.botoesContainer,
      text="Cadastrar novo tema",
      font=appConfig.fontes["botao"],
      width=30,
      command=self.janelaCadastroEdicao
      )
    self.botaoCadastrarNovo.grid(column=1, row=1, padx=10, pady=5, sticky='w')
