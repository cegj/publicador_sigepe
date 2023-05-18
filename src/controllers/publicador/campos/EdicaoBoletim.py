from models import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class EdicaoBoletim:
  @staticmethod
  def preencher(data):
    try:
      if (data == "Normal"):
          edicaoNormal = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
            (By.XPATH, ac.AppConfig.xpaths["publicacao"]["edicaoBoletimNormalLabel"])),
            message="Não foi possível localizar ou clicar na opção 'Edição normal'")
          edicaoNormal.click()
      elif (data == "Extraordinária"):
          edicaoExtraordinaria = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
            (By.XPATH, ac.AppConfig.xpaths["publicacao"]["edicaoBoletimExtraordinariaLabel"])),
            message="Não foi possível localizar ou clicar na opção 'Edição extraordinária'")
          edicaoExtraordinaria.click()
      wd.Webdriver.waitLoadingModal()
      return {"log": f"Edição do boletim selecionada: {data}", "type": "n"}

    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "edição do boletim")
