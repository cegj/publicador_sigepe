from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl

class EdicaoBoletim:
  @staticmethod
  def preencher(data):
    try:
      edicaoNormal = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["edicaoBoletimNormalLabel"])))
      edicaoExtraordinaria = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["edicaoBoletimExtraordinariaLabel"])))

      if (data == "Normal"):
          edicaoNormal.click()
      elif (data == "Extraordinária"):
          edicaoExtraordinaria.click()

      wfl.waitForLoading()
      return {"log": f"Edição do boletim selecionada: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher edição do boletim: {e}", "type": "e", "e": e}