from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import appConfig
from views import Habilitacao as h
from views import Publicacao as p
import os

class ArquivosPublicar:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(padx=10)
    self.btnsContainer = Frame(self.container)
    self.btnsContainer.pack(padx=10)
    self.listbox = Listbox(
      self.subcontainer,
      height = 12,
      width = 40,
      bg = "white",
      activestyle = 'dotbox',
      font = "Helvetica",
      fg = "gray"
    )
    self.listbox.pack(anchor=CENTER, pady=10)
    self.listbox.bind("<Key>", self.deleteFiles)
    self.selecionarArquivosBtn()
    self.publicarBtn()

  def getFiles(self, event = None):
    self.sessao.files = filedialog.askopenfiles(mode='r', title="Selecionar arquivos para publicação", filetypes=[("Documentos RTF (Rich Text Format)", ".rtf")])
    for file in self.sessao.files:
      self.listbox.insert(END, os.path.basename(file.name))

  def deleteFiles(self, event = None):
    if (event.keysym == "Delete"):
      try:
        def deleteFromFiles(filename):
          for file in self.sessao.files:
            if (os.path.basename(file.name) == filename):
              self.sessao.files.remove(file)
              break
        filenameToDelete = self.listbox.get(ANCHOR)
        deleteFromFiles(filenameToDelete)
        self.listbox.delete(ANCHOR)
      except Exception as e:
        messagebox.showerror("Erro ao excluir arquivo", e)

  def selecionarArquivosBtn(self):
    btn = Button(
      self.btnsContainer,
      text="Selecionar arquivos",
      font=appConfig.fontes["botao"],
      width=20,
      command=self.getFiles
      )
    btn.pack(side=LEFT, padx=10)

  def publicarBtn(self):
    btn = Button(
      self.btnsContainer,
      text="Publicar",
      font=appConfig.fontes["botao"],
      width=20,
      bg="#429321",
      fg="white",
      command=self.iniciarPublicacao
      )
    btn.pack(side=LEFT, padx=10)

  def iniciarPublicacao(self, event = None):
    if (len(self.sessao.files) > 0):
      p.Publicacao(self.sessao)
    else:
      messagebox.showerror("Erro", "Nenhum arquivo selecionado para publicação. Selecione os arquivos para continuar.")


