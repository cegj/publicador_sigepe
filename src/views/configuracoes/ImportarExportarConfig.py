from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from views import Interfaces as i
from models import UserConfig as uc
from models import AppConfig as ac
from copy import copy
import os
import shutil
import json 

class ImportarExportarConfig:
  def __init__(self):
      # self.delimiters = copy(uc.UserConfig.obterDelimitadoresSalvos())
      self.master = i.Interfaces.novaJanela()
      self.container = Frame(self.master)
      self.container.pack(pady="5")
      self.janelaImportarExportar()

  def janelaImportarExportar(self):
    self.importar()
    separator = ttk.Separator(self.container,orient='horizontal')
    separator.pack(fill='x', pady=10)
    self.exportar()
    infoLabel = ttk.Label(
      self.container,
      text="É possível exportar as suas configurações do usuário\npara importá-las em outras instalações do Publicador\nou para manter uma cópia de segurança.\nOs arquivos exportados também podem ser\nimportados por meio desta função.",
      background="#fff9d9",
      foreground="#85701d",
      padding=4,
      justify=CENTER)
    infoLabel.pack(pady="5")


  def exportar(self):
    exportarContainer = Frame(self.container)
    exportarContainer.pack()
    label = Label(
      exportarContainer,
      text="Exportar configurações",
      font=("Segoe UI", "12"),
      anchor=CENTER
    )
    label.pack(padx=5, pady=5)
    btn = Button(
      exportarContainer,
      text="Exportar",
      font=("Segoe UI", "10"),
      width=25,
      command=self.exportFiles
      )
    btn.pack(padx=5, pady=5)

  def exportFiles(self):
    try:
      targetPath = os.path.normcase(filedialog.askdirectory(title="Pasta de destino das configurações"))
      targetPath = os.path.normcase(f"{targetPath}/publicador_sigepe_configuracoes_copia") 
      os.mkdir(targetPath)
      originPath = os.path.normpath(os.path.join(os.path.expanduser('~'), f"AppData/Local/Programs/Publicador Sigepe/config/user"))
      files = []
      for file_path in os.listdir(originPath):
        if os.path.isfile(os.path.join(originPath, file_path)):
          files.append(file_path)
      for fileName in files:
        origin = os.path.join(originPath, fileName)
        target = os.path.join(targetPath, fileName)
        shutil.copy(origin, target)
      messagebox.showinfo("Exportação concluída", 'Os arquivos das suas configurações de usuário foram exportados com sucesso na pasta selecionada.\n\nUse a opção "Importar configurações" para replicar estas configurações em outra instalação do Publicador Sigepe.')
    except Exception as e:
      messagebox.showerror("Erro exportar configurações", e)

  def importar(self):
    importarContainer = Frame(self.container)
    importarContainer.pack()
    self.filesToImport = []
    label = Label(
      importarContainer,
      text="Importar configurações",
      font=("Segoe UI", "12"),
      anchor=CENTER
    )
    label.pack(padx=5, pady=5)
    btn = Button(
      importarContainer,
      text="Selecionar arquivos",
      font=("Segoe UI", "10"),
      width=25,
      command=self.getFilesToImport
      )
    btn.pack(padx=5, pady=5)
    self.listbox = Listbox(
      importarContainer,
      height = 5,
      width = 30,
      bg = "white",
      font = "Helvetica",
      fg = "gray",
      activestyle="none"
    )
    self.listbox.pack(padx=5, pady=5)
    self.listbox.bind("<Key>", self.deleteFilesToImport)
    btn = Button(
      importarContainer,
      text="Importar",
      font=("Segoe UI", "10"),
      width=20,
      command=self.importFiles
      )
    btn.pack(padx=5, pady=5)

  def getFilesToImport(self, event = None):
    acceptableFilenames = [
      "errors.json",
      "urls.json",
      "webdriversettings.json",
      "xpaths.json",
      "afterpublishingconfig.json",
      "autotheme.json",
      "delimiters.json",
      "removefromcontent.json",
      "userconfig.json",
      "browser.json"
    ]

    selectedFiles = filedialog.askopenfiles(mode='r', title="Selecionar arquivos corrigidos", filetypes=[("Arquivo JSON", ".json")])
    fails = []
    for file in selectedFiles:
      filename = os.path.basename(file.name)
      if (filename in self.listbox.get(0, END)):
        fails.append(filename)
        continue
      if (filename not in acceptableFilenames):
        fails.append(filename)
        continue
      self.filesToImport.append(file)
      self.listbox.insert(END, filename)
    if (len(fails) > 0):
        message = "Os seguintes arquivos não foram adicionados pois já estão na lista ou têm nome inválido:\n\n"
        for fail in fails:
          message += f"{fail}\n"
        messagebox.showerror("Arquivos não adicionados", message)

  def deleteFilesToImport(self, event = None):
    if (event.keysym == "Delete"):
      try:
        def deleteFromFiles(filename):
          for file in self.filesToImport:
            if (os.path.basename(file.name) == filename):
              self.filesToImport.remove(file)
        filenameToDelete = self.listbox.get(ANCHOR)
        deleteFromFiles(filenameToDelete)
        self.listbox.delete(ANCHOR)
      except Exception as e:
        messagebox.showerror("Erro ao excluir arquivo", e)

  def importFiles(self):
    success = []
    fails = []
    appFiles = ["errors.json", "urls.json", "webdriversettings.json", "xpaths.json"]
    userFiles = ["afterpublishingconfig.json", "autotheme.json", "delimiters.json", "removefromcontent.json", "userconfig.json", "browser.json"]
    for file in self.filesToImport:
      filename = os.path.basename(file.name)
      if (filename in appFiles):
        folder = "app"
      if (filename in userFiles):
        folder = "user"
      src = os.path.abspath(file.name)
      dest = os.path.normpath(os.path.join(os.path.expanduser('~'), f"AppData/Local/Programs/Publicador Sigepe/config/{folder}/{filename}"))
      try:
        shutil.copy(src, dest)
        success.append(filename)
      except Exception as e:
        fails.append([filename, e])
    
    if (len(success) > 0):
      if (len(fails) == 0):
        message = "Todas as configurações foram importadas."
      if (len(fails) > 0):
        message = "As seguintes configurações foram importadas: \n"
        for file in success:
          message += f"\n{file}"
        message = "\n\nAs seguintes configurações não foram importadas: \n"
        for file in fails:
          message += f"\n{file[0]}: {file[1]}"
    if(len(success) > 0):
      message += "\n\nExecute novamente o Publicador Sigepe para iniciá-lo com as novas configurações."
    if (len(success) == 0):
        message = "Nenhuma configuração foi importada.\n"
        message = "Os seguintes arquivos retornaram erro: \n"
        for file in fails:
          message += f"\n{file[0]}: {file[1]}"
    messagebox.showinfo("Importação concluída", message)
    self.listbox.delete(0, END)
    self.filesToImport = []


