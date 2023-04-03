from tkinter import *
from controllers.interfaces import Login as l
from controllers import Usuario
from controllers import Sessao

class Application:
    def __init__(self):
      #self.master = master
      pass

    def executar(self):
      l.Login.login()
      #self.master.mainloop()
      
app = Application()
app.executar()