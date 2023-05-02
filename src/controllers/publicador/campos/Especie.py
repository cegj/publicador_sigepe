from appXpaths import xpaths
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys

class Especie:
  @staticmethod
  def preencher(data):
    try:
      sigepe_campoEspecie = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["especieSelect"])))

      wfl.waitForLoading()

      sigepe_campoEspecie.click()

      time.sleep(0.3)

      sigepe_campoBuscarEspecie = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["buscarEspecieInput"])))

      sigepe_campoBuscarEspecie.send_keys(data)

      time.sleep(1.5)

      sigepe_campoBuscarEspecie.send_keys(Keys.ENTER)

      wfl.waitForLoading()

      return {"log": f"Espécie selecionada: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao selecionar espécie: {e}", "type": "e", "e": e}

