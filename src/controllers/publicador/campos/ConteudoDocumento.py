from controllers import AppConfig as ac
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys

class ConteudoDocumento:
  @staticmethod
  def preencher(data):
    try:
      nav.switch_to.frame(0)
      sigepe_campoTextoPortaria = wait["long"].until(
          EC.element_to_be_clickable((By.XPATH, ac.AppConfig.xpaths["publicacao"]["conteudoDocumentoTextarea"])))
      sigepe_campoTextoPortaria.click()
      time.sleep(0.3)
      for part in reversed(data.split('\n')):
        sigepe_campoTextoPortaria.send_keys(part)
        sigepe_campoTextoPortaria.send_keys(Keys.ENTER)
      time.sleep(0.3)
      nav.switch_to.default_content()
      wfl.waitForLoading()
      return {"log": f"Conteúdo do documento preenchido", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher conteúdo do documento: {e}", "type": "e", "e": e}