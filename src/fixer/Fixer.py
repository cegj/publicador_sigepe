from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import shutil
import urllib.request, json 

class Fixer:
  def __init__(self):
    self.root = Tk()
    self.root.title("Corrigir Publicador Sigepe")
    self.root.iconbitmap("static/ico.ico")
    self.root["padx"] = 20
    self.root["pady"] = 20
    self.root.resizable(False, False)
    self.files = []
    self.janelaFixer()

  def janelaFixer(self):
    titulo = Label(
      self.root,
      text="Publicador Sigepe",
      font=("Segoe UI", "13", "bold"),
      anchor=CENTER
    )
    titulo.pack(padx=5, pady=5)

    btn = Button(
      self.root,
      text="Corrigir pela web",
      font=("Segoe UI", "10"),
      width=25,
      command=self.fixFromWeb
      )
    btn.pack(padx=5, pady=5)
   
    ou = Label(
      self.root,
      text="ou",
      font=("Segoe UI", "12"),
      anchor=CENTER
    )
    ou.pack(padx=5, pady=5)

    titulo.pack(padx=5, pady=5)
    btn = Button(
      self.root,
      text="Selecionar arquivos",
      font=("Segoe UI", "10"),
      width=25,
      command=self.getFiles
      )
    btn.pack(padx=5, pady=5)
    self.listbox = Listbox(
      self.root,
      height = 5,
      width = 30,
      bg = "white",
      font = "Helvetica",
      fg = "gray",
      activestyle="none"
    )
    self.listbox.pack(padx=5, pady=5)
    self.listbox.bind("<Key>", self.deleteFiles)

    btn = Button(
      self.root,
      text="Atualizar arquivos",
      font=("Segoe UI", "10"),
      width=20,
      command=self.moveFiles
      )
    btn.pack(padx=5, pady=5)

    self.root.mainloop()

  def getFiles(self, event = None):
    acceptableFilenames = [
      "errors.json",
      "urls.json",
      "webdriversettings.json",
      "xpaths.json",
      "afterpublishingconfig.json",
      "autotheme.json",
      "delimiters.json",
      "removefromcontent.json",
      "userconfig.json"
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
      self.files.append(file)
      self.listbox.insert(END, filename)
    if (len(fails) > 0):
        message = "Os seguintes arquivos não foram adicionados pois já estão na lista ou têm nome inválido:\n\n"
        for fail in fails:
          message += f"{fail}\n"
        messagebox.showerror("Arquivos não adicionados", message)
 
  def deleteFiles(self, event = None):
    if (event.keysym == "Delete"):
      try:
        def deleteFromFiles(filename):
          for file in self.files:
            if (os.path.basename(file.name) == filename):
              self.files.remove(file)
        filenameToDelete = self.listbox.get(ANCHOR)
        deleteFromFiles(filenameToDelete)
        self.listbox.delete(ANCHOR)
      except Exception as e:
        messagebox.showerror("Erro ao excluir arquivo", e)

  def moveFiles(self):
    success = []
    fails = []
    appFiles = ["errors.json", "urls.json", "webdriversettings.json", "xpaths.json"]
    userFiles = ["afterpublishingconfig.json", "autotheme.json", "delimiters.json", "removefromcontent.json", "userconfig.json"]
    for file in self.files:
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
        message = "Todas as correções foram aplicadas"
      if (len(fails) > 0):
        message = "As seguintes correções foram aplicadas: \n"
        for file in success:
          message += f"\n{file}"
        message = "\n\nAs seguintes correções não foram aplicadas: \n"
        for file in fails:
          message += f"\n{file[0]}: {file[1]}"
    if (len(success) == 0):
        message = "Nenhuma correção foi aplicada.\n"
        message = "Os seguintes arquivos retornaram erro: \n"
        for file in fails:
          message += f"\n{file[0]}: {file[1]}"
    messagebox.showinfo("Concluído", message)
    if (len(fails) == 0):
      self.root.destroy()

  def fixFromWeb(self):
    try:
      filenames = ["errors.json", "urls.json", "webdriversettings.json", "xpaths.json"]
      for filename in filenames:
        with urllib.request.urlopen(f"https://github.cegj.dev/publicador_sigepe_jsons/config/app/{filename}") as url:
          content = json.load(url)
          dest = os.path.normpath(os.path.join(os.path.expanduser('~'), f"AppData/Local/Programs/Publicador Sigepe/config/app/{filename}"))
          string = json.dumps(content, ensure_ascii=False, indent=4, separators=(',',':'))
          jsonFile = open(dest, "w", encoding="utf-8")
          jsonFile.write(string)
          jsonFile.close()
      messagebox.showinfo("Concluído", "Arquivos atualizados com sucesso")
      self.root.destroy()
    except Exception as e:
      messagebox.showinfo("Ocorreu um erro", e)

start = Fixer()