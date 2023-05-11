from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from tkinter import *
from tkinter import messagebox
from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows

class Webdriver:
  @staticmethod
  def start():
    try:
      chrome_service = Service(ChromeDriverManager().install())
      chrome_service.creationflags = CREATE_NO_WINDOW
      opcoes = Options()
      opcoes.add_argument('ignore-certificate-errors')
      opcoes.add_argument("start-maximized")
      # opcoes.add_argument("--headless")
      opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
      return webdriver.Chrome(ChromeDriverManager().install(), service = chrome_service, options=opcoes)
    except Exception as e:
      error = str(e)
      errors = {
        "chromeNotFound": "cannot find chrome binary",
        "outdatedChrome": "this version of chromedriver only supports Chrome version"
      }
      if errors["chromeNotFound"] in str(e).lower():
        error = "O Google Chrome não está instalado em seu computador. Instale este navegador para executar o Publicador Sigepe."
      if errors["outdatedChrome"] in str(e).lower():
        error = "Seu navegador está desatualizado. Atualize o Google Chrome para executar o Publicador Sigepe."
      messagebox.showerror("Erro ao abrir navegador", error)
      try:
        nav.quit()
      except:
        pass

  nav = start.__func__()
  wait = {'half': WebDriverWait(nav, 10), 'regular': WebDriverWait(nav, 20), 'long': WebDriverWait(nav, 40)}