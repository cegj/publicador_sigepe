from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions as selenium_exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
from tkinter import messagebox
from models import AppConfig as ac
import re    

class Webdriver:
  @staticmethod
  def start():
    try:
      chrome_service = Service()
      chrome_service.creation_flags = CREATE_NO_WINDOW
      options = Options()
      for option in ac.AppConfig.webdriverSettings["options"]:
        options.add_argument(option)
      driver = webdriver.Chrome(service = chrome_service, options=options)
      if (ac.AppConfig.webdriverSettings["minimizeOnStart"] == "true"): driver.minimize_window()
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
  def checkErrorsLoadedPage():
    errors = ac.AppConfig.errors
    src = Webdriver.nav.page_source
    for error in errors:
      if re.search(error[0], src, re.IGNORECASE):
        return [False, error[1]]
    return [True]

  @staticmethod
  def go(url):
    try:
      Webdriver.nav.get(url)
      errorCheck = Webdriver.checkErrorsLoadedPage()
      if (not errorCheck[0]):
        raise Exception(errorCheck[1])
    except Exception as e:
      messagebox.showerror("Erro ao acessar página", e)

  @staticmethod
  def waitLoadingModal():
    loadingMoral = WebDriverWait(Webdriver.nav, 300).until(EC.invisibility_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths['general']['loadingModal'])))
    return None

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
      By.XPATH, xpath).screenshot(f'temp/{filename}.png')
      Webdriver.nav.minimize_window()
      return f'temp/screenshot/{filename}.png'
    except Exception as e:
      messagebox.showerror("Erro ao obter screenshot", e)
      return False

  @staticmethod
  def getFullScreenshot(filename):
    try:
      originalSize = Webdriver.nav.get_window_size()
      requiredWidth = Webdriver.nav.execute_script('return document.body.parentNode.scrollWidth')
      requiredHeight = Webdriver.nav.execute_script('return document.body.parentNode.scrollHeight')
      Webdriver.nav.set_window_size(requiredWidth, requiredHeight)
      Webdriver.nav.save_screenshot(f"temp/screenshot/{filename}.png")
      Webdriver.nav.set_window_size(originalSize['width'], originalSize['height'])
      return [True, filename]
    except Exception as e:
      messagebox.showerror("Erro ao obter screenshot da tela", e)
      return [False, e.args[0]]

  @staticmethod
  def handleExceptions(ex, fieldname = ""):
    try:
      initialTxt = ""
      if (fieldname): initialTxt = f"Falha ao selecionar {fieldname}"
      else: initialTxt = "Falha no navegador"

      template = "".join([initialTxt, ": {0} {1}"])

      exType = type(ex).__name__
      exMessage = ""
      match exType:
        case "TimeoutException":
          exMessage = "o tempo máximo para executar a ação expirou."
        case "NoSuchElementException":
          exMessage = "um elemento não foi encontrado na página."
        case "InvalidSelectorException":
          exMessage = "o seletor informado para localizar um elemento é inválido."
        case "ElementNotInteractableException":
          exMessage = "um elemento foi encontrado na página, mas não está disponível para interação."
        case "ElementNotSelectableException":
          exMessage = "um elemento foi encontrado na página, mas não é selecionável."
        case "ElementNotVisibleException":
          exMessage = "um elemento foi encontrado, mas não está visível na página."
        case "StaleElementReferenceException":
          exMessage = "um elemento está obsoleto, ou seja, não está mais disponível na página para interação."
        case "ElementClickInterceptedException":
          exMessage = "o clique foi interceptado por outro elemento da página."
        case "InvalidArgumentException":
          exMessage = "um comando possui argumentos inválidos."
        case "InvalidElementStateException":
          exMessage = "o estado do elemento na página é incompatível com o comando realizado."
        case "NoSuchWindowException":
          exMessage = "a janela do navegador não foi localizada."
        case "InsecureCertificateException":
          exMessage = "a página retornou um erro de certificado de segurança inválido."
        case "InvalidCoordinatesException":
          exMessage = "as coordenadas informadas para interação com um elemento são inválidas."
        case "InvalidCoordinatesException":
          exMessage = "as coordenadas informadas para interação com um elemento são inválidas."
        case "InvalidSessionIdException":
          exMessage = "o ID da sessão não está na lista de sessões ativas, o que significa que a seção não existe ou está inativa."
        case "InvalidSwitchToTargetException":
          exMessage = "não foi possível alterar para um determinado frame ou janela pois ele não foi localizado."
        case "NoSuchFrameException":
          exMessage = "não foi possível alterar para um determinado frame pois ele não foi localizado."
        case "NoSuchWindowException":
          exMessage = "não foi possível alterar para uma determinada janela pois ele não foi localizado."
        case "InvalidSwitchToTargetException":
          exMessage = "ocorreu um erro ao executar um código de Javascript na página."
        case "NoSuchAttributeException":
          exMessage = "o atributo de um elemento não pôde ser encontrado."
        case "ScreenshotException":
          exMessage = "não foi possível obter uma captura de tela."
        case "UnexpectedAlertPresentException":
          exMessage = "um alerta inesperado foi exibido pela página."
        case "UnexpectedTagNameException":
          exMessage = "o nome de uma classe não localizou elementos."
        case _:
          pass

      especificMessage = ex.args[0]

      msg = template.format(exMessage, especificMessage)

      return {"log": msg, "type": "e", "e": ex}
    except Exception as e:
      print(e)

  nav = start.__func__()
  wait = {'half': WebDriverWait(nav, 5), 'regular': WebDriverWait(nav, 10), 'long': WebDriverWait(nav, 20)}