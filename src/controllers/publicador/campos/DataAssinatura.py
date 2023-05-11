from controllers import AppConfig as ac
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from controllers import Webdriver as wd

class DataAssinatura:
  @staticmethod
  def preencher(data):
    try:
      sigepe_campoDataAssinatura = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["dataAssinaturaCampo"])))

      sigepe_campoDataAssinatura.click()

      sigepe_campoDataAssinatura.send_keys(data)

      wd.Webdriver.waitLoadingModal()

      return {"log": f"Data de assinatura preenchida: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher data de assinatura: {e}", "type": "e", "e": e}