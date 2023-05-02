from appXpaths import xpaths
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl

class DataAssinatura:
  @staticmethod
  def preencher(data):
    try:
      sigepe_campoDataAssinatura = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["dataAssinaturaCampo"])))

      sigepe_campoDataAssinatura.click()

      sigepe_campoDataAssinatura.send_keys(data)

      wfl.waitForLoading()

      return {"log": f"Data de assinatura preenchida: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher data de assinatura: {e}", "type": "e", "e": e}