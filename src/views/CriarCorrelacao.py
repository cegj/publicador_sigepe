from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import appConfig
from views import Interfaces as i
from copy import copy
from appXpaths import xpaths
import os

class CriarCorrelacao:
  def __init__(self, sessao, listbox, filename):
    self.sessao = sessao
    self.filesListbox = listbox
    self.filename = filename
    for file in self.sessao.files:
      if (os.path.basename(file.name) == self.filename):
        self.filepath = os.path.dirname(file.name)
        break
    self.values = {
      "acao": "",
      "origem": "",
      "orgao": "",
      "upag": "",
      "uorg": "",
      "numero": "",
      "ano": ""
    }
    self.corrFilename = self.filename.split('.')[0] + ".txt"
    self.corrFilepath = os.path.join(self.filepath, self.corrFilename)
    self.dadosEdicao = self.verificarSeExiste()
    self.master = i.Interfaces.novaJanela()
    self.container = Frame(self.master)
    self.container.pack()
    self.janelaCriarCorrelacao()

  def janelaCriarCorrelacao(self):
    labelTitulo = Label(
      self.container,
      text="Criar correlação para o documento",
      font=appConfig.fontes["titulo"]
      )
    labelTitulo.pack()
    self.acao()
    self.origem()
    self.orgao()
    self.upag()
    self.uorg()
    self.numero()
    self.ano_publicacao()
    self.botaoCriar()
    if (self.dadosEdicao): self.botaoApagar()

  def acao(self):
    def setSelected(event = None):
      self.values["acao"] = selected.get()
    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7, anchor=W)
    label = Label(
      subcontainer,
      text="Ação:",
      font=appConfig.fontes["normal"]
      )
    label.grid(row=1, column=1, sticky="w")
    selected = StringVar()
    options = [
      "Adita o",
      "Altera o",
      "Anula o",
      "Prejudica o",
      "Rejeita o",
      "Retifica o",
      "Revigora o",
      "Revoga Parcialmente o",
      "Revoga o",
      "Suspende a eficácia do",
      "Torna insubsistente o",
      "Torna parcialmente insubsistente o",
      "Torna sem efeito o",
      "Vide"
    ]
    if (self.dadosEdicao): selected.set(self.dadosEdicao["acao"])
    else: selected.set("")
    setSelected()
    seletor = ttk.Combobox(
      subcontainer,
      textvariable=selected,
      values=options,
      state="readonly",
      width=20,
      font=appConfig.fontes["normal"]
      )
    seletor.grid(row=1, column=2, sticky="w")
    seletor.bind("<<ComboboxSelected>>", setSelected)

  def origem(self):
    def setSelected(event = None):
      self.values["origem"] = selected.get()
    container = Frame(self.container)
    container.pack(padx=10, pady=7, anchor=W)
    label = Label(
      container,
      text="Origem:",
      font=appConfig.fontes["normal"]
      )
    label.grid(row=1, column=1, sticky="w")
    selected = StringVar()
    options = [
      "Executivo Estadual/Distrital",
      "Executivo Federal",
      "Executivo Municipal",
      "Judiciário Estadual/Distrital",
      "Judiciário Federal",
      "Legislativo Estadual/Distrital",
      "Legislativo Federal",
      "Legislativo Municipal"
    ]
    if (self.dadosEdicao): selected.set(self.dadosEdicao["origem"])
    else: selected.set("Executivo Federal")
    setSelected()
    seletor = ttk.Combobox(
      container,
      textvariable=selected,
      values=options,
      state="readonly",
      width=20,
      font=appConfig.fontes["normal"]
      )
    seletor.grid(row=1, column=2, sticky="w")
    seletor.bind("<<ComboboxSelected>>", setSelected)

  def orgao(self):
    def setValue(a=None, b=None, c=None):
      self.values["orgao"] = value.get()
    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7, anchor=W)
    label = Label(
      subcontainer,
      text="Órgão",
      font=appConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    value = StringVar()
    value.trace_add("write", setValue)
    if (self.dadosEdicao): value.set(self.dadosEdicao["orgao"])
    else: value.set(self.sessao.userConfig["valores_sigepe"]["orgao"])
    entry = Entry(
      subcontainer,
      width=27,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    entry.pack(side=LEFT)

  def upag(self):
    def setValue(a=None, b=None, c=None):
      self.values["upag"] = value.get()
    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7, anchor=W)
    label = Label(
      subcontainer,
      text="UPAG",
      font=appConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    value = StringVar()
    value.trace_add("write", setValue)
    if (self.dadosEdicao): value.set(self.dadosEdicao["upag"])
    else: value.set(self.sessao.userConfig["valores_sigepe"]["upag"])
    entry = Entry(
      subcontainer,
      width=27,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    entry.pack(side=LEFT)

  def uorg(self):
    def setValue(a=None, b=None, c=None):
      self.values["uorg"] = value.get()
    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7, anchor=W)
    label = Label(
      subcontainer,
      text="UORG",
      font=appConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    value = StringVar()
    value.trace_add("write", setValue)
    if (self.dadosEdicao): value.set(self.dadosEdicao["uorg"])
    else: value.set(self.sessao.userConfig["valores_sigepe"]["uorg"])
    entry = Entry(
      subcontainer,
      width=27,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    entry.pack(side=LEFT)

  def numero(self):
    def setValue(a=None, b=None, c=None):
      self.values["numero"] = value.get()
    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7, anchor=W)
    label = Label(
      subcontainer,
      text="Número do ato",
      font=appConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    value = StringVar()
    value.trace_add("write", setValue)
    if (self.dadosEdicao): value.set(self.dadosEdicao["numero"])
    entry = Entry(
      subcontainer,
      width=20,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    entry.pack(side=LEFT)

  def ano_publicacao(self):
    def setValue(a=None, b=None, c=None):
      self.values["ano"] = value.get()
    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7, anchor=W)
    label = Label(
      subcontainer,
      text="Ano de publicação",
      font=appConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    value = StringVar()
    value.trace_add("write", setValue)
    if (self.dadosEdicao): value.set(self.dadosEdicao["ano"])
    entry = Entry(
      subcontainer,
      width=18,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    entry.pack(side=LEFT)

  def botaoCriar(self):
    if (self.dadosEdicao): text = "Salvar mudanças"
    else: text = "Criar correlação"
    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7)
    botao = Button(
      subcontainer,
      text=text,
      font=appConfig.fontes["botao"],
      width=20,
      command=self.criar
    )
    botao.pack()

  def botaoApagar(self):
    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7)
    botao = Button(
      subcontainer,
      text="Apagar correlação",
      font=appConfig.fontes["botao"],
      width=20,
      command=self.apagar
    )
    botao.pack()

  def criar(self):
    try:
      emptyFields = []
      for key, value in self.values.items():
        if (value == "" or value == None): raise Exception("Para criar uma correlação, todos os campos devem ser preenchidos.")
      fileContent = f"#ACAO={self.values['acao']}\n#ORIGEM={self.values['origem']}\n#ORGAO={self.values['orgao']}\n#UPAG={self.values['upag']}\n#UORG={self.values['uorg']}\n#NUMERO={self.values['numero']}\n#ANO={self.values['ano']}"
      txtfile = open(self.corrFilepath, "w", encoding="utf-8")
      txtfile.write(fileContent)
      txtfile.close()
      self.filesListbox.itemconfig(ANCHOR, foreground="#64006b", selectbackground="#64006b")
      self.master.destroy()
    except Exception as e:
      messagebox.showerror("Erro ao criar correlação", e)

  def apagar(self):
    try:
      os.remove(self.corrFilepath)
      self.filesListbox.itemconfig(ANCHOR, foreground="gray", selectbackground="")
      self.master.destroy()
    except Exception as e:
      messagebox.showerror("Erro apagar correlação", e)

  def verificarSeExiste(self):
    try:
      corrFile = open(self.corrFilepath, 'r', encoding="utf-8")
      contentArr = corrFile.read().replace('\n', '').strip().split('#')
      del contentArr[0]
      corrFile.close()
      contentObj = {}
      for value in contentArr:
        keyValue = value.split("=")
        contentObj[keyValue[0].lower()] = keyValue[1]
      return contentObj
    except Exception as e:
      return False