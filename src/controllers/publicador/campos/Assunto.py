from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from controllers import UserConfig as uc
from controllers import AppConfig as ac
from controllers import Variaveis as v

class Assunto:
  @staticmethod
  def preencher(data):
    try:
      sigepe_buscarAssuntoBtn = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable((By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarAssuntoBtn"])))
      sigepe_buscarAssuntoBtn.click()
      wfl.waitForLoading()
      assuntoBtn = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='{data}']")))
      assuntoBtn.click()
      sigepe_selecionarAssuntoBtn = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable((By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarAssuntoBtn"])))
      sigepe_selecionarAssuntoBtn.click()
      wfl.waitForLoading()
      time.sleep(0.3)
      sigepe_assuntoSelecionadoInput = wd.Webdriver.wait["regular"].until(EC.presence_of_element_located((By.XPATH, ac.AppConfig.xpaths["publicacao"]["assuntoSelecionadoInput"])))
      assuntoSelecionado = sigepe_assuntoSelecionadoInput.get_attribute('value')
      return {"log": f"Assunto selecionado: {assuntoSelecionado}", "type": "n"}
      
    except Exception as e:
      return {"log": f"Falha ao selecionar assunto: {e}", "type": "e", "e": e}

  @staticmethod
  def buscar(filetext):
    try:
      termos = v.Variaveis.atribuirValorVariaveis(uc.UserConfig.obterAutoTemasAssuntos())
      for termo, obj in termos.items():
        if termo.lower() in filetext.lower():
          return {"log": f"Assunto identificado: {obj['assunto']}", "type": "n", "return": obj["assunto"]}
      raise Exception("não foi localizado um termo correspondente a um assunto no conteúdo do documento.")
    except Exception as e:
      return {"log": f"Falha ao selecionar tema: {e}", "type": "e", "e": e}
