from models import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Numero:
  @staticmethod
  def preencher(data):
    try:
      sigepe_campoNumero = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["numeroCampo"])),
        message="Não foi possível localizar ou clicar no campo 'Número do ato'")
      sigepe_campoNumero.click()
      sigepe_campoNumero.send_keys(data)
      wd.Webdriver.waitLoadingModal()

      return {"log": f"Número do documento preenchido: {data}", "type": "n"}

    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "número do ato")
