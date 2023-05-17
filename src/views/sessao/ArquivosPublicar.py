from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from controllers import AppConfig as ac
from views import Publicacao as p
from views import CriarCorrelacao as cc
import os
from helpers import validateFields as vf

class ArquivosPublicar:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()
    self.sessao.files = []

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(padx=10)
    self.btnsContainer = Frame(self.container)
    self.btnsContainer.pack(padx=10)
    self.listbox = Listbox(
      self.subcontainer,
      height = 10,
      width = 40,
      bg = "white",
      font = "Helvetica",
      fg = "gray",
      activestyle="none"
    )
    self.listbox.pack(anchor=CENTER, pady=7)
    self.listbox.bind("<Key>", self.deleteFiles)
    self.listbox.bind("<Double-Button-1>", self.createCorrelation)
    self.acao()
    self.selecionarArquivosBtn()
    self.publicarBtn()

  def getFiles(self, event = None):
    selectedFiles = filedialog.askopenfiles(mode='r', title="Selecionar arquivos para publicação", filetypes=[("Documentos RTF (Rich Text Format)", ".rtf")])
    fails = []
    for file in selectedFiles:
      filename = os.path.basename(file.name)
      if (filename in self.listbox.get(0, END)):
        fails.append(filename)
        continue
      else:
        self.sessao.files.append(file)
        self.listbox.insert(END, filename)
        corrFilepath = os.path.join(os.path.dirname(file.name), os.path.basename(file.name).split('.')[0] + ".txt")
        if (os.path.exists(corrFilepath)): self.listbox.itemconfig(END, foreground="#64006b", selectbackground="#64006b")
    if (len(fails) > 0):
        message = "Os seguintes arquivos não foram adicionados pois existem arquivos com o mesmo nome na lista:\n\n"
        for fail in fails:
          message += f"{fail}\n"

        messagebox.showerror("Arquivos não adicionados", message)


  def deleteFiles(self, event = None):
    if (event.keysym == "Delete"):
      try:
        def deleteFromFiles(filename):
          for file in self.sessao.files:
            if (os.path.basename(file.name) == filename):
              self.sessao.files.remove(file)
              corrFilepath = os.path.join(os.path.dirname(file.name), os.path.basename(file.name).split('.')[0] + ".txt")
              if (os.path.exists(corrFilepath)): os.remove(corrFilepath)
              break
        filenameToDelete = self.listbox.get(ANCHOR)
        deleteFromFiles(filenameToDelete)
        self.listbox.delete(ANCHOR)
      except Exception as e:
        messagebox.showerror("Erro ao excluir arquivo", e)

  def createCorrelation(self, event = None):
    try:
      filename = self.listbox.get(ANCHOR)
      cc.CriarCorrelacao(self.sessao, self.listbox, filename)
    except Exception as e:
      messagebox.showerror("Erro ao abrir Criar correlação", e)


  def acao(self):
    container = Frame(self.subcontainer)
    container.pack(side=LEFT, padx=10, pady=10)
    label = Label(
      container,
      text="Ação",
      font=ac.AppConfig.fontes["normal"]
      )
    label.pack(side=LEFT)
    self.selected = StringVar()
    self.selected.set(self.sessao.userConfig["acao"])
    options = ["Enviar para análise", "Enviar para assinatura / publicação", "Gravar rascunho"]
    seletor = ttk.Combobox(
      container,
      textvariable=self.selected,
      values=options,
      state="readonly",
      width=30,
      font=ac.AppConfig.fontes["normal"]
      )
    seletor.pack(side=LEFT)
    seletor.bind("<<ComboboxSelected>>", self.setSelected)

  def setSelected(self, Event = None):
    self.sessao.userConfig["acao"] = self.selected.get()

  def selecionarArquivosBtn(self):
    btn = Button(
      self.btnsContainer,
      text="Selecionar arquivos",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=self.getFiles
      )
    btn.pack(side=LEFT, padx=10)

  def publicarBtn(self):
    btn = Button(
      self.btnsContainer,
      text="Publicar",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      bg="#429321",
      fg="white",
      command=self.iniciarPublicacao
      )
    btn.pack(side=LEFT, padx=10)

  def iniciarPublicacao(self, event = None):
    if (vf.validateFields(self.sessao.userConfig)):
      if (self.sessao.userConfig["acao"] != ""):
        if (len(self.sessao.files) > 0): p.Publicacao(self.sessao)
        else: messagebox.showerror("Erro", "Nenhum arquivo selecionado para publicação.\nSelecione os arquivos antes de iniciar a publicação.")
      else: messagebox.showerror("Erro", "Nenhuma ação selecionada.\nSelecione uma ação antes de iniciar a publicação.")


