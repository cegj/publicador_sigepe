from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl

class TipoAssinatura:
  @staticmethod
  def preencher(data):
    try:
      tipoAssinaturaDigital = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["tipoAssinaturaDigitalLabel"])))
      tipoAssinaturaManual = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["tipoAssinaturaManualLabel"])))

      if (data == "Manual"):
          tipoAssinaturaManual.click()
      elif (data == "Digital"):
          tipoAssinaturaDigital.click()

      wfl.waitForLoading()
      return {"log": f"Tipo de assinatura selecionado: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher tipo de assinatura: {e}", "type": "e", "e": e}