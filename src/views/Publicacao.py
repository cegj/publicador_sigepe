from views import Interfaces as i
from controllers import UserConfig as uc
from controllers import AppConfig as ac
from controllers import Publicador as p
from tkinter import *
import tkinter.scrolledtext as st
from copy import copy
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from controllers import Webdriver as wd

class Publicacao:
  def __init__(self, sessao):
      self.afterpublishingconfig = copy(uc.UserConfig.obterConfigPosPublicacaoSalvos())
      self.delimiters = copy(uc.UserConfig.obterDelimitadoresSalvos())
      self.config = sessao.userConfig
      self.files = sessao.files
      self.sessao = sessao
      self.master = i.Interfaces.novaJanela()
      self.publicacaoContainer = Frame(self.master)
      self.publicacaoContainer.pack()
      self.janelaPublicacao()
      self.master.protocol("WM_DELETE_WINDOW", self.handleFecharJanela)
      publicador = p.Publicador(self)

  def janelaPublicacao(self):
    self.pendingFiles()
    self.successFiles()
    self.failFiles()
    self.logbox()
    self.resultbox()
    self.contentbox()

  def pendingFiles(self):
    pendingFilesContainer = Frame(self.publicacaoContainer)
    pendingFilesContainer.grid(row=1, column=1, pady=10, padx=10)
    pendingFilesLabel = Label(
      pendingFilesContainer,
      text="Arquivos na fila",
      font=ac.AppConfig.fontes["normal"]
    )
    pendingFilesLabel.pack()
    self.pendingFilesList = Listbox(
      pendingFilesContainer,
      height = 10,
      width = 40,
      bg = "white",
      font = "Helvetica",
      fg = "gray",
      activestyle="none"
    )
    self.pendingFilesList.pack()

  def successFiles(self):
    successFilesContainer = Frame(self.publicacaoContainer)
    successFilesContainer.grid(row=1, column=2, pady=10, padx=10)
    successFilesLabel = Label(
      successFilesContainer,
      text="Arquivos publicados",
      font=ac.AppConfig.fontes["normal"]
    )
    successFilesLabel.pack()
    self.successFilesList = Listbox(
      successFilesContainer,
      height = 10,
      width = 40,
      bg = "white",
      font = "Helvetica",
      fg = "green",
      activestyle="none"
    )
    self.successFilesList.pack()

  def failFiles(self):
    failFilesContainer = Frame(self.publicacaoContainer)
    failFilesContainer.grid(row=1, column=3, pady=10, padx=10)
    failFilesLabel = Label(
      failFilesContainer,
      text="Arquivos não publicados",
      font=ac.AppConfig.fontes["normal"]
    )
    failFilesLabel.pack()
    self.failFilesList = Listbox(
      failFilesContainer,
      height = 10,
      width = 40,
      bg = "white",
      font = "Helvetica",
      fg = "red",
      activestyle="none"
    )
    self.failFilesList.pack()

  def logbox(self):
    logboxContainer = Frame(self.publicacaoContainer)
    logboxContainer.grid(row=2, column=1, pady=10, padx=10)
    logBoxLabel = Label(
      logboxContainer,
      text="Todos os logs",
      font=ac.AppConfig.fontes["normal"],
    )
    logBoxLabel.pack()
    self.logbox = st.ScrolledText(
      logboxContainer,
      width=50,
      height=10,
      font=ac.AppConfig.fontes["log"],
      spacing3=5
      )
    self.logbox.pack()

  def resultbox(self):
    resultBoxContainer = Frame(self.publicacaoContainer)
    resultBoxContainer.grid(row=2, column=2, pady=10, padx=10)
    fileContentLabel = Label(
      resultBoxContainer,
      text="Logs em destaque",
      font=ac.AppConfig.fontes["normal"]
    )
    fileContentLabel.pack()
    self.resultBox = st.ScrolledText(
      resultBoxContainer,
      width=50,
      height=10,
      font=ac.AppConfig.fontes["log"],
      spacing3=5
      )
    self.resultBox.pack()

  def contentbox(self):
    fileContentContainer = Frame(self.publicacaoContainer)
    fileContentContainer.grid(row=2, column=3, pady=10, padx=10)
    fileContentLabel = Label(
      fileContentContainer,
      text="Conteúdo do documento atual",
      font=ac.AppConfig.fontes["normal"]
    )
    fileContentLabel.pack()
    self.fileContentBox = st.ScrolledText(
      fileContentContainer,
      width=50,
      height=10,
      font=ac.AppConfig.fontes["log"],
      spacing3=5
      )
    self.fileContentBox.pack()

  def btns(self):
    btnsContainer = Frame(self.publicacaoContainer)
    btnsContainer.grid(row=3, column=3, columnspan=3, pady=10, padx=10)

    salvarLogsBtn = Button(
      btnsContainer,
      text="Salvar logs da publicação",
      font=ac.AppConfig.fontes["botao"],
      width=25,
      command=self.saveLogs
      )
    salvarLogsBtn.grid(row=1, column=1, pady=10, padx=10)

    fecharBtn = Button(
      btnsContainer,
      text="Fechar",
      font=ac.AppConfig.fontes["botao"],
      width=20,
      command=self.close
      )
    fecharBtn.grid(row=1, column=2, pady=10, padx=10)

  def saveLogs(self):
    fileTitle = f"Logs de publicação - {datetime.now()}"
    fileTitle = fileTitle.split('.')[0].replace(':', '-')
    logs = self.logbox.get("1.0", END)
    extension = [('Arquivo de texto puro', '*.txt')]
    logFile = filedialog.asksaveasfile(title="Salvar logs da publicação", filetypes = extension, defaultextension = extension, initialfile=fileTitle)
    if (logFile): logFile.write(logs)

  def close(self):
    answer = messagebox.askyesnocancel("Publicador Sigepe", "Deseja encerrar completamente o Publicador Sigepe?\n\nCaso selecione Não, somente a publicação atual será fechada.")
    if (answer == True):
      wd.Webdriver.nav.quit()
      self.sessao.root.destroy()
      self.master.destroy()
    elif (answer == False):
      self.master.destroy()

  def handleFecharJanela(self):
    if (self.pendingFilesList.size() > 0):
      confirmarFechar = messagebox.askquestion("Publicador Sigepe", "A publicação será interrompida. Confirmar saída?")
      if (confirmarFechar == 'yes'):
        self.master.destroy()
    else:
      self.master.destroy()


  def insertLog(self, logtext, tag = None, docNumber = ""):
    self.logbox.configure(state='normal')
    self.logbox.insert(INSERT, f"{docNumber} - {logtext}\n", tag)
    self.logbox.tag_config('e', background="#efcccc", foreground="#680000") #error
    self.logbox.tag_config('s', background="#ccefcc", foreground="#006800") #success
    self.logbox.tag_config('a', background="#efeecc", foreground="#585500") #alert
    self.logbox.tag_config('em', background="#ccdff0", foreground="#002e57") #emphasis
    self.logbox.configure(state='disabled')
    self.logbox.yview(END)

  def insertFileText(self, filetext):
    self.fileContentBox.configure(state='normal')
    self.fileContentBox.delete('0.0', END)
    self.fileContentBox.insert(INSERT, filetext)
    self.fileContentBox.configure(state='disabled')

  def insertResult(self, filename, logtext, tag = None, docNumber = ""):
    self.resultBox.configure(state='normal')
    self.resultBox.insert(INSERT, f"{docNumber} - [{filename}]: {logtext}\n", tag)
    self.resultBox.tag_config('e', background="#efcccc", foreground="#680000") #error
    self.resultBox.tag_config('s', background="#ccefcc", foreground="#006800") #success
    self.resultBox.tag_config('a', background="#efeecc", foreground="#585500") #alert
    self.resultBox.tag_config('em', background="#ccdff0", foreground="#002e57") #emphasis
    self.resultBox.insert(INSERT, "")
    self.resultBox.configure(state='disabled')
    self.resultBox.yview(END)

  def insertOnPendingFiles(self, filename):
    self.pendingFilesList.insert(END, filename)

  def moveToSuccessFiles(self, filename):
    indexOfFilename = self.pendingFilesList.get(0, END).index(filename)
    self.pendingFilesList.delete(indexOfFilename)
    self.successFilesList.insert(END, filename)

  def moveToFailFiles(self, filename):
    indexOfFilename = self.pendingFilesList.get(0, END).index(filename)
    self.pendingFilesList.delete(indexOfFilename)
    self.failFilesList.insert(END, filename)

  def showBtns(self):
    self.btns()

  def showConcludeMessage(self):
    messagebox.showinfo("Publicador Sigepe", "Publicação concluída!")