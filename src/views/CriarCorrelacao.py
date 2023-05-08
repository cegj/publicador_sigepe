from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import appConfig
from views import Interfaces as i
from copy import copy
from appXpaths import xpaths
import os

class CriarCorrelacao:
  def __init__(self, sessao, filename):
    self.sessao = sessao
    self.filename = filename
    self.master = i.Interfaces.novaJanela()
    self.container = Frame(self.master)
    self.container.pack()
    self.values = {
      "acao": "",
      "origem": "",
      "orgao": "",
      "upag": "",
      "uorg": "",
      "numero": "",
      "ano": ""
    }
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

  def acao(self):
    def setSelected(event = None):
      self.values["acao"] = self.acaoSelected.get()
    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7, anchor=W)
    label = Label(
      subcontainer,
      text="Ação:",
      font=appConfig.fontes["normal"]
      )
    label.grid(row=1, column=1, sticky="w")
    self.acaoSelected = StringVar()
    options = [
      "Adita o",
      "Altera o",
      "Anula o",
      "Prejudica o",
      "Rejeita o",
      "Retifica o",
      "Revigora o",
      "Revoga Parcialmente o"
      "Revoga o",
      "Suspende a eficácia do",
      "Torna insubsistente o",
      "Torna parcialmente insubsistente o",
      "Torna sem efeito o",
      "Vide"
    ]
    seletor = ttk.Combobox(
      subcontainer,
      textvariable=self.acaoSelected,
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
    selected.set("Executivo Federal")
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
    entry = Entry(
      subcontainer,
      width=27,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.sessao.userConfig["valores_sigepe"]["orgao"])
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
    entry = Entry(
      subcontainer,
      width=27,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.sessao.userConfig["valores_sigepe"]["upag"])
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
    entry = Entry(
      subcontainer,
      width=27,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    value.set(self.sessao.userConfig["valores_sigepe"]["uorg"])
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
    entry = Entry(
      subcontainer,
      width=23,
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
    entry = Entry(
      subcontainer,
      width=23,
      textvariable=value,
      font=appConfig.fontes["normal"]
      )
    entry.pack(side=LEFT)

  def botaoCriar(self):
    def criar():
      try:
        emptyFields = []
        for key, value in self.values.items():
          if (value == "" or value == None): emptyFields.append(key)
        if (len(emptyFields) > 0): raise Exception("Para criar uma correlação, todos os campos devem ser preenchidos.")

        fileContent = f"#ACAO={self.values['acao']}\n#ORIGEM={self.values['origem']}\n#ORGAO={self.values['orgao']}\n#UPAG={self.values['upag']}\n#UORG={self.values['uorg']}\n#NUMERO={self.values['numero']}\n#ANO={self.values['ano']}"
        for file in self.sessao.files:
          if (os.path.basename(file.name) == self.filename):
            path = os.path.dirname(file.name)
            break
        correlationFilename = self.filename.split(".")[0] + ".txt"
        fullpath = os.path.join(path, correlationFilename)
        txtfile = open(fullpath, "w", encoding="utf-8")
        n = txtfile.write(fileContent)
        txtfile.close()
        self.master.destroy()
        messagebox.showinfo("Sucesso", f"A correlação para o arquivo {self.filename} foi criada com sucesso")
      except Exception as e:
        messagebox.showerror("Erro ao criar correlação", e)

    subcontainer = Frame(self.container)
    subcontainer.pack(padx=10, pady=7)
    botao = Button(
      subcontainer,
      text="Criar correlação",
      font=appConfig.fontes["botao"],
      width=20,
      command=criar
    )
    botao.pack()