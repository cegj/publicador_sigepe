from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver import EdgeOptions
from models import AppConfig as ac
from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows

class Edge:
  @staticmethod
  def setup():
    try:
      service = Service(EdgeChromiumDriverManager().install())
      service.creation_flags = CREATE_NO_WINDOW
      options = EdgeOptions()
      options.use_chromium = True
      options.add_argument("ignore-certificate-errors")
      for option in ac.AppConfig.webdriverSettings["chromiumOptions"]:
        options.add_argument(option)
      driver = webdriver.Edge(service=service, options=options)
      if (ac.AppConfig.webdriverSettings["minimizeOnStart"] == "true"): driver.minimize_window()
      return [True, driver]
    except Exception as e:
      error = str(e)
      # errors = {
      #   "chromeNotFound": "cannot find chrome binary",
      #   "outdatedChrome": "this version of chromedriver only supports Chrome version"
      # }
      # if errors["chromeNotFound"] in str(e).lower():
      #   error = "O Google Chrome não está instalado em seu computador. Instale este navegador para executar o Publicador Sigepe."
      # if errors["outdatedChrome"] in str(e).lower():
      #   error = "Seu navegador está desatualizado. Atualize o Google Chrome para executar o Publicador Sigepe."
      try:
        driver.quit()
      except:
        pass
      return [False, error]