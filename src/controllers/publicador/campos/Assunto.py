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
  def preencher():
    try:
      sigepe_buscarAssuntoBtn = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, xpaths["publicacao"]["buscarAssuntoBtn"])))
      sigepe_buscarAssuntoBtn.click()
      wfl.waitForLoading()
      sigepe_assuntosBtns = wait["regular"].until(EC.visibility_of_all_elements_located((By.XPATH, xpaths["publicacao"]["assuntosBtns"])))
      ultimoNivelAssunto = sigepe_assuntosBtns[-1]
      ultimoNivelAssunto.click()
      sigepe_selecionarAssuntoBtn = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, xpaths["publicacao"]["selecionarAssuntoBtn"])))
      sigepe_selecionarAssuntoBtn.click()
      return {"log": f"Assunto selecionado: {ultimoNivelAssunto.text}", "type": "n"}
      
    except Exception as e:
      return {"log": f"Falha ao selecionar assunto: {e}", "type": "e", "e": e}