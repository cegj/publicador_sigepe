from controllers import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TipoAssinatura:
  @staticmethod
  def preencher(data):
    try:
      tipoAssinaturaDigital = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["tipoAssinaturaDigitalLabel"])))
      tipoAssinaturaManual = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["tipoAssinaturaManualLabel"])))

      if (data == "Manual"):
          tipoAssinaturaManual.click()
      elif (data == "Digital"):
          tipoAssinaturaDigital.click()

      wd.Webdriver.waitLoadingModal()
      return {"log": f"Tipo de assinatura selecionado: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher tipo de assinatura: {e}", "type": "e", "e": e}