from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions as selenium_exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
from tkinter import messagebox
from models import AppConfig as ac
from models import UserConfig as uc
import re    
from controllers.webdriver.Chrome import Chrome
from controllers.webdriver.Edge import Edge
from controllers.webdriver.Firefox import Firefox
from views.configuracoes import Navegador as n

class Webdriver:
  @staticmethod
  def start():
    def getBrowser(browserName):
      if (browserName == "chrome"):
        return Chrome.setup()
      elif (browserName == "edge"):
        return Edge.setup()
      elif (browserName == "firefox"):
        return Firefox.setup()
    success = False
    while success == False:
      try:
        browserName = uc.UserConfig.obterNavegador()
        if (browserName == "chrome" or browserName == "edge" or browserName == "firefox"):
          setup = getBrowser(browserName)
          if setup[0]:
            success = True
            return setup[1]
          else: raise Exception(setup[1])
        else:
          raise Exception("Não existe um navegador definido para executar o Publicador Sigepe. Defina um navegador.")
      except Exception as e:
        messagebox.showerror("Erro ao abrir navegador", e)
        n.Navegador()
        quit()

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