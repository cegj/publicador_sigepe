from tkinter import *
from controllers import Usuario
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class Application:
    def __init__(self, master=None):
      self.master = master
      root.title("Publicador Sigepe")
      root.geometry('400x300')
      self.opcoes = Options()
      self.opcoes.add_argument("start-maximized")
      self.opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
      self.nav = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.opcoes)
      self.nav.minimize_window()
      self.wait = {'half': WebDriverWait(self.nav, 10), 'regular': WebDriverWait(self.nav, 20), 'long': WebDriverWait(self.nav, 40)}

    def executar(self):
      usuario = Usuario.Usuario(self.nav)
      usuario.exibirTelaLogin(self.master)
      self.master.mainloop()

      
root = Tk()
app = Application(root)
app.executar()
