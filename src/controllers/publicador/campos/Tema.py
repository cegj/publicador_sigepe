from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys

class Tema:
  @staticmethod
  def preencher(data):
    try:
      temaSplitted = data.split('//')
      campoTema = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["temaSelect"])))
      campoTema.click()
      time.sleep(0.3)

      campoBuscarTema = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["buscarTemaInput"])))
      nav.execute_script("arguments[0].setAttribute('value',arguments[1])",campoBuscarTema, "")
      time.sleep(0.3)
      campoBuscarTema.send_keys(temaSplitted[0])
      time.sleep(1.5)

      if (len(temaSplitted) == 2):
        i = 1
        while (i < int(temaSplitted[1])):
          campoBuscarTema.send_keys(Keys.ARROW_DOWN)
          time.sleep(0.3)
          i += 1

      campoBuscarTema.send_keys(Keys.ENTER)
      wfl.waitForLoading()

      campoTemaPreenchido = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["temaSelect"])))

      return {"log": f"Tema selecionado: {campoTemaPreenchido.text}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao selecionar tema: {e}", "type": "e", "e": e}