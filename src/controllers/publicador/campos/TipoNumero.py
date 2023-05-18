from models import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

class TipoNumero:
  @staticmethod
  def preencher(data):
    try:
      campoTipoNumero = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["tipoNumeroCampo"])),
        message="Não foi possível localizar ou clicar no campo 'Tipo de número'")
      campoTipoNumero.click()
      time.sleep(0.3)
      campoBuscarTipoNumero = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["tipoNumeroBuscar"])),
        message="Não foi possível localizar ou clicar no campo 'Buscar tipo de número'")
      campoBuscarTipoNumero.send_keys(data)
      time.sleep(1.5)
      campoBuscarTipoNumero.send_keys(Keys.ENTER)
      wd.Webdriver.waitLoadingModal()
      return {"log": f"Tipo de preenchimento do número selecionado: {data}", "type": "n"}

    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "tipo de número do ato")
