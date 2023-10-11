from views import Login as l
from controllers import CheckUpdates as c
import requests
from tkinter import messagebox
import sys
from models import AppConfig as ac

class Application:
    def __init__(self):
      pass

    def executar(self):
      self.checkConnection()
      c.CheckUpdates.checkRelease()
      c.CheckUpdates.checkXpaths()
      c.CheckUpdates.checkUrls()
      c.CheckUpdates.checkErrors()
      c.CheckUpdates.checkWebdriverSettings()
      start = l.Login()

    def checkConnection(self):
      try:
        response = requests.get(ac.AppConfig.urls["areaDeTrabalho"], timeout=5)
        return True
      except requests.ConnectionError:
        messagebox.showerror(f"{ac.AppConfig.nome} {ac.AppConfig.versao}", "Não foi possível estabelecer uma conexão com o Sigepe. Isso pode ocorrer por falha da sua conexão com a internet ou por indisponibilidade do Sigepe.")
        sys.exit() 

app = Application()
app.executar()