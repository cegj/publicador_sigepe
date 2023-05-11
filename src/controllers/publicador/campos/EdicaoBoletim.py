from controllers import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class EdicaoBoletim:
  @staticmethod
  def preencher(data):
    try:
      edicaoNormal = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["edicaoBoletimNormalLabel"])))
      edicaoExtraordinaria = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["edicaoBoletimExtraordinariaLabel"])))

      if (data == "Normal"):
          edicaoNormal.click()
      elif (data == "Extraordinária"):
          edicaoExtraordinaria.click()

      wd.Webdriver.waitLoadingModal()
      return {"log": f"Edição do boletim selecionada: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher edição do boletim: {e}", "type": "e", "e": e}