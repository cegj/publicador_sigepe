from models import AppConfig as ac
from models import UserConfig as uc
from views import Interfaces as i
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from copy import copy
from controllers import ObterDoSigepe as ods

class SigepeTrabalhando:
  def __init__(self, thread, msg = "Aguardando resposta do Sigepe..."):
    # super().__init__()
    self.thread = thread
    self.msg = msg
    self.trabalhando()

  def trabalhando(self):
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

  def destroy(self):
    self.master.destroy()