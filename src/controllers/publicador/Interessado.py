from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys

class Interessado:
  @staticmethod
  def preencher(data):
    try:
      sigepe_botaoIncluirInteressado = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["incluirInteressadoBotao"])))
      sigepe_botaoIncluirInteressado.click()
      wfl.waitForLoading()

      sigepe_campoMatricula = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["matriculaInteressadoInput"])))
      sigepe_campoMatricula.click()
      time.sleep(0.2)
      sigepe_campoMatricula.send_keys(data)
      sigepe_campoMatricula.send_keys(Keys.ENTER)
      wfl.waitForLoading()

      sigepe_checkboxSelecionarServidor = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["selecionarInteressadoCheckbox"])))
      sigepe_checkboxSelecionarServidor.click()

      time.sleep(0.3)

      sigepe_botaoIncluirNaLista = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["incluirInteressadoNaListaBotao"])))
      nav.execute_script("arguments[0].click();", sigepe_botaoIncluirNaLista);
      wfl.waitForLoading()

      sigepe_botaoSelecionarServidor = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["selecionarServidorBotao"])))
      nav.execute_script("arguments[0].click();", sigepe_botaoSelecionarServidor);
      wfl.waitForLoading()

      interessadoSelecionado = wait["regular"].until(EC.presence_of_element_located(
        (By.XPATH, xpaths["publicacao"]["interessadoSelecionado"])))

      return {"log": f"Interessado selecionado: {interessadoSelecionado.text}", "type": "n"}

    except Exception as e:
      return {"log": f"Falha ao selecionar interessado: {e}", "type": "e", "e": e}

