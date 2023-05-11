from controllers import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl

class Numero:
  @staticmethod
  def preencher(data):
    try:
      sigepe_campoNumero = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["numeroCampo"])))

      sigepe_campoNumero.click()

      sigepe_campoNumero.send_keys(data)

      wfl.waitForLoading()

      return {"log": f"Número do documento preenchido: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher número do documento: {e}", "type": "e", "e": e}