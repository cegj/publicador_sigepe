from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys

class TipoNumero:
  @staticmethod
  def preencher(data):
    try:
      campoTipoNumero = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["tipoNumeroCampo"])))
      campoTipoNumero.click()
      time.sleep(0.3)
      campoBuscarTipoNumero = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["tipoNumeroBuscar"])))
      campoBuscarTipoNumero.send_keys(data)
      time.sleep(1.5)
      campoBuscarTipoNumero.send_keys(Keys.ENTER)
      wfl.waitForLoading()
      return {"log": f"Tipo de preenchimento do número selecionado: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher tipo de preenchimento do número: {e}", "type": "e", "e": e}