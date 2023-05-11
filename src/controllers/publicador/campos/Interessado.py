from controllers import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class Interessado:
  @staticmethod
  def preencher(data):
    try:
      sigepe_botaoIncluirInteressado = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["incluirInteressadoBotao"])))
      sigepe_botaoIncluirInteressado.click()
      wd.Webdriver.waitLoadingModal()

      sigepe_campoMatricula = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["matriculaInteressadoInput"])))
      sigepe_campoMatricula.click()
      time.sleep(0.2)
      sigepe_campoMatricula.send_keys(data)

      sigepe_botaoPesquisarInteressado = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["pesquisarInteressadoBotao"])))
      sigepe_botaoPesquisarInteressado.click()
      wd.Webdriver.waitLoadingModal()

      sigepe_checkboxSelecionarServidor = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarInteressadoCheckbox"])))
      sigepe_checkboxSelecionarServidor.click()
      time.sleep(0.3)

      sigepe_botaoIncluirNaLista = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["incluirInteressadoNaListaBotao"])))
      wd.Webdriver.nav.execute_script("arguments[0].click();", sigepe_botaoIncluirNaLista);
      wd.Webdriver.waitLoadingModal()

      sigepe_botaoSelecionarAto = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarServidorBotao"])))
      wd.Webdriver.nav.execute_script("arguments[0].click();", sigepe_botaoSelecionarAto);
      wd.Webdriver.waitLoadingModal()

      interessadoSelecionado = wd.Webdriver.wait["regular"].until(EC.presence_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["interessadoSelecionado"])))

      return {"log": f"Interessado selecionado: {interessadoSelecionado.text}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao selecionar interessado: {e}", "type": "e", "e": e}

