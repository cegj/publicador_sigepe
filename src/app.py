from tkinter import *
from controllers.interfaces import Login as l

class Application:
    def __init__(self):
      pass

    def executar(self):
      start = l.Login()
      
app = Application()
app.executar()