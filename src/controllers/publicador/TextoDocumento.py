from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys

class TextoDocumento:
  @staticmethod
  def preencher(data):
    try:
      nav.switch_to.frame(0)

      sigepe_campoTextoPortaria = wait["regular"].until(
          EC.element_to_be_clickable((By.XPATH, xpaths["publicacao"]["textoDocumentoTextarea"])))

      sigepe_campoTextoPortaria.click()

      time.sleep(0.3)

      sigepe_campoTextoPortaria.send_keys(data)

      nav.switch_to.default_content()

      wfl.waitForLoading()

      return {"log": f"Texto do documento preenchido", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher texto do documento: {e}", "type": "e", "e": e}

