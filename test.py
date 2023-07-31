from threading import Thread
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from tkinter import *
import time

def navigate():
  try:
    master = Toplevel()
    master.grab_set()
    master.title("Aguarde")
    container = Frame(master)
    container.pack()
    label = Label(master, text="Aguarde...")
    label.pack()
    nav.get("https://g1.globo.com")
    master.destroy()
  except Exception as e:
    print("Erro ao abrir navegador", f"Atualize o navegador!\n{e}")

class Aguarde:
  def __init__(self):
    pass 

  def execute(self):
    print("b")
    self.root = Tk()
    self.root.title("Aguarde")
    master = Toplevel()
    master.grab_set()
    master.title("Aguarde")
    container = Frame(self.root)
    container.pack()
    label = Label(self.root, text="Aguarde...")
    label.pack()
    button = Button(self.root, text="Abrir", command=lambda: Thread(target=navigate).start())
    button.pack()
    master.destroy()
    mainloop()

  def destroy(self):
    self.root.destroy()

print("a")
opcoes = Options()
opcoes.add_argument("start-maximized")
opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
nav = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcoes)
nav.minimize_window()

a = Aguarde()
a.execute()