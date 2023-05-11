from controllers import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

class Especie:
  @staticmethod
  def preencher(data):
    try:
      time.sleep(1)
      sigepe_campoEspecie = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["especieSelect"])))

      wd.Webdriver.waitLoadingModal()

      sigepe_campoEspecie.click()

      time.sleep(0.3)

      sigepe_campoBuscarEspecie = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarEspecieInput"])))

      sigepe_campoBuscarEspecie.send_keys(data)

      time.sleep(1.5)

      sigepe_campoBuscarEspecie.send_keys(Keys.ENTER)

      wd.Webdriver.waitLoadingModal()

      return {"log": f"Espécie selecionada: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao selecionar espécie: {e}", "type": "e", "e": e}

