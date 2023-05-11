from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from tkinter import *
from tkinter import messagebox
from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from controllers import AppConfig as ac

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
      driver = webdriver.Chrome(ChromeDriverManager().install(), service = chrome_service, options=opcoes)
      driver.minimize_window()
      return driver
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

  @staticmethod
  def checkExistsByXpath(xpath):
    try:
      Webdriver.nav.find_element(By.XPATH, xpath)
    except NoSuchElementException:
      return False
    return True
  
  @staticmethod
  def getScreenshotByXpath(xpath, filename):
    try:
      loc = Webdriver.nav.find_element(
      By.XPATH, xpath).screenshot(f'{filename}.png')
      Webdriver.nav.minimize_window()
      return f'{filename}.png'
    except Exception as e:
      messagebox.showerror("Erro ao obter screenshot", e)
      return False

  @staticmethod
  def waitLoadingModal():
    loadingMoral = WebDriverWait(Webdriver.nav, 300).until(EC.invisibility_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths['general']['loadingModal'])))
    return None
  
  @staticmethod
  def go(url):
    try:
      Webdriver.nav.get(url)
      if(Webdriver.checkExistsByXpath('//*[@id="details-button"]')): #If Chrome SSL Error
        detailsBtn = Webdriver.nav.find_element(
            By.XPATH, '//*[@id="details-button"]')
        detailsBtn.click()
        proceedLink = Webdriver.nav.find_element(
            By.XPATH, '//*[@id="proceed-link"]')
        proceedLink.click()
    except Exception as e:
      messagebox.showerror("Erro ao acessar página", e)
  
  nav = start.__func__()
  wait = {'half': WebDriverWait(nav, 10), 'regular': WebDriverWait(nav, 20), 'long': WebDriverWait(nav, 40)}