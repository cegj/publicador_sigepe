from tkinter import *
import appConfig

class Interfaces:
  def __init__(self):
    self.root = Tk()
    self.root.title(appConfig.appTitulo + ' ' + appConfig.appVersao)
    self.root.iconbitmap("static/ico.ico")
    self.root["padx"] = appConfig.pad["x"]
    self.root["pady"] = appConfig.pad["y"]
    self.root.resizable(False, False)

  @staticmethod
  def novaJanela():
    master = Toplevel()
    master.grab_set()
    master.title(appConfig.appTitulo)
    master.iconbitmap("static/ico.ico")
    master["padx"] = appConfig.pad["x"]
    master["pady"] = appConfig.pad["y"]
    master.resizable(False, False)
    return master







