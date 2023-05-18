from models import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TipoAssinatura:
  @staticmethod
  def preencher(data):
    try:
      if (data == "Manual"):
        tipoAssinaturaManual = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["tipoAssinaturaManualLabel"])),
          message="Não foi possível localizar ou clicar na opção 'Manual' de tipo de assinatura")
        tipoAssinaturaManual.click()
      elif (data == "Digital"):
        tipoAssinaturaDigital = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["tipoAssinaturaDigitalLabel"])),
          message="Não foi possível localizar ou clicar na opção 'Digital' de tipo de assinatura")
        tipoAssinaturaDigital.click()
      wd.Webdriver.waitLoadingModal()

      return {"log": f"Tipo de assinatura selecionado: {data}", "type": "n"}

    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "tipo de assinatura")
