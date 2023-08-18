from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from models import AppConfig as ac
from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows
from webdriver_manager.chrome import ChromeDriverManager

class Chrome:
  @staticmethod
  def setup():
    try:
      service = Service()
      service.creation_flags = CREATE_NO_WINDOW
      options = webdriver.ChromeOptions()
      options.add_argument("ignore-certificate-errors")
      for option in ac.AppConfig.webdriverSettings["chromiumOptions"]:
        options.add_argument(option)
      driver = webdriver.Chrome(service=service, options=options)
      if (ac.AppConfig.webdriverSettings["minimizeOnStart"] == "true"): driver.minimize_window()
      return [True, driver]
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
      try:
        driver.quit()
      except:
        pass
      return [False, error]