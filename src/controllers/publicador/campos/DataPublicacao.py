from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys

class DataPublicacao:
  @staticmethod
  def preencher(data):
    try:
      sigepe_campoDataPublicacao = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["dataPublicacaoCampo"])))

      sigepe_campoDataPublicacao.click()

      sigepe_campoDataPublicacao.send_keys(data)

      wfl.waitForLoading()

      return {"log": f"Data de publicação preenchida: {data}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao preencher data de publicação: {e}", "type": "e", "e": e}