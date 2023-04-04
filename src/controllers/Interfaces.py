from tkinter import *
import appConfig

class Interfaces:
  def __init__(self):
    self.root = Tk()
    self.root.title(appConfig.appTitulo)
    self.root.geometry('850x800')
    self.root["padx"] = appConfig.pad["x"]
    self.root["pady"] = appConfig.pad["y"]

  def novaJanela():
    master = Tk()
    master.title(appConfig.appTitulo)
    master["padx"] = appConfig.pad["x"]
    master["pady"] = appConfig.pad["y"]
    return master







