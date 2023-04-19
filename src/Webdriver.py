from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from tkinter import *
from tkinter import messagebox

try:
  opcoes = Options()
  opcoes.add_argument('ignore-certificate-errors')
  opcoes.add_argument("start-maximized")
  # opcoes.add_argument("--headless")
  opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
  nav = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcoes)
  wait = {'half': WebDriverWait(nav, 10), 'regular': WebDriverWait(nav, 20), 'long': WebDriverWait(nav, 40)}
  nav.minimize_window()
except Exception as e:
  messagebox.showerror("Erro ao abrir navegador", f"Atualize o navegador!\n{e}")
  try:
    nav.quit()
  except:
    pass
