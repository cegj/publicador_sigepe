from controllers import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

class ConteudoDocumento:
  @staticmethod
  def preencher(data):
    try:
      wd.Webdriver.nav.switch_to.frame(0)
      sigepe_campoTextoPortaria = wd.Webdriver.wait["long"].until(
          EC.element_to_be_clickable((By.XPATH, ac.AppConfig.xpaths["publicacao"]["conteudoDocumentoTextarea"])))
      sigepe_campoTextoPortaria.click()
      time.sleep(0.3)
      for part in reversed(data.split('\n')):
        sigepe_campoTextoPortaria.send_keys(part)
        sigepe_campoTextoPortaria.send_keys(Keys.ENTER)
      time.sleep(0.3)
      wd.Webdriver.nav.switch_to.default_content()
      wd.Webdriver.waitLoadingModal()
      return {"log": f"Conteúdo do documento preenchido", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher conteúdo do documento: {e}", "type": "e", "e": e}