from tkinter import *
from controllers import Interfaces as i
from controllers import Usuario
from controllers import Sessao

class Application:
    def __init__(self):
      #self.master = master
      pass

    def executar(self):
      i.Interfaces.login()
      #self.master.mainloop()
      
app = Application()
app.executar()