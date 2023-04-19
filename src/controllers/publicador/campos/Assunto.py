from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys

class Assunto:
  @staticmethod
  def preencher(data):
    try:
      sigepe_buscarAssuntoBtn = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, xpaths["publicacao"]["buscarAssuntoBtn"])))
      sigepe_buscarAssuntoBtn.click()
      wfl.waitForLoading()
      assuntoBtn = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='{data}']")))
      assuntoBtn.click()
      sigepe_selecionarAssuntoBtn = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, xpaths["publicacao"]["selecionarAssuntoBtn"])))
      sigepe_selecionarAssuntoBtn.click()
      wfl.waitForLoading()
      time.sleep(0.3)
      sigepe_assuntoSelecionadoInput = wait["regular"].until(EC.presence_of_element_located((By.XPATH, xpaths["publicacao"]["assuntoSelecionadoInput"])))
      assuntoSelecionado = sigepe_assuntoSelecionadoInput.get_attribute('value')
      return {"log": f"Assunto selecionado: {assuntoSelecionado}", "type": "n"}
      
    except Exception as e:
      return {"log": f"Falha ao selecionar assunto: {e}", "type": "e", "e": e}