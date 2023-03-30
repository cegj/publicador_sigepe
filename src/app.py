from tkinter import *
from controllers import Interfaces as i
from controllers import Usuario
from controllers import ConfiguracaoSessao
from Master import master

class Application:
    def __init__(self):
      self.master = master

    def executar(self):
      i.Interfaces.login()
      self.master.mainloop()
      
app = Application()
app.executar()