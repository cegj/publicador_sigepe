from models import AppConfig as ac
from models import UserConfig as uc
from views import Interfaces as i
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from copy import copy
from controllers import ObterDoSigepe as ods

class SigepeTrabalhando:
  def __init__(self, thread, msg = "Aguardando resposta do Sigepe...", asRoot = False):
    # super().__init__()
    self.thread = thread
    self.msg = msg
    self.asRoot = asRoot
    self.trabalhando()

  def trabalhando(self):
    if (self.asRoot):
      self.master = Tk()
      self.master.title(ac.AppConfig.nome + ' ' + ac.AppConfig.versao)
      self.master.iconbitmap("static/ico.ico")
      self.master["padx"] = ac.AppConfig.pad["x"]
      self.master["pady"] = ac.AppConfig.pad["y"]
      self.master.resizable(False, False)
    else:
      self.master = i.Interfaces.novaJanela()
    self.container = Frame(self.master)
    self.container.pack()

    label = Label(
      self.container,
      text=self.msg,
      font=ac.AppConfig.fontes["normal"]
    )
    label.pack()

    pb = ttk.Progressbar(
      self.container,
      orient='horizontal',
      mode='indeterminate',
      length=280
    )
    pb.pack()
    pb.start()

    def disable_event():
      pass
    self.master.protocol("WM_DELETE_WINDOW", disable_event)

    while(self.thread.is_alive()):
      self.master.update()
    self.destroy()

    if (self.asRoot): self.master.mainloop()

  def destroy(self):
    self.master.destroy()