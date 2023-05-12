from controllers import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class DataPublicacao:
  @staticmethod
  def preencher(data):
    try:
      sigepe_campoDataPublicacao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["dataPublicacaoCampo"])),
        message="Não foi possível localizar ou clicar no campo 'Data de publicação'")
      sigepe_campoDataPublicacao.click()
      sigepe_campoDataPublicacao.send_keys(data)
      wd.Webdriver.waitLoadingModal()
      return {"log": f"Data de publicação preenchida: {data}", "type": "n"}

    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "data de publicação")
