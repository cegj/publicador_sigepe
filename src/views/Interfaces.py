from tkinter import *
from controllers import AppConfig as ac

class Interfaces:
  def __init__(self):
    self.root = Tk()
    self.root.title(ac.AppConfig.nome + ' ' + ac.AppConfig.versao)
    self.root.iconbitmap("static/ico.ico")
    self.root["padx"] = ac.AppConfig.pad["x"]
    self.root["pady"] = ac.AppConfig.pad["y"]
    self.root.resizable(False, False)

  @staticmethod
  def novaJanela():
    master = Toplevel()
    master.grab_set()
    master.title(ac.AppConfig.nome)
    master.iconbitmap("static/ico.ico")
    master["padx"] = ac.AppConfig.pad["x"]
    master["pady"] = ac.AppConfig.pad["y"]
    master.resizable(False, False)
    return master







