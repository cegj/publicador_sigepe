from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from controllers import Webdriver as wd
import time
from models import UserConfig as uc
from models import AppConfig as ac
from controllers import Variaveis as v
import datetime

class Assunto:
  @staticmethod
  def preencher(data):
    try:
      sigepe_buscarAssuntoBtn = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarAssuntoBtn"])),
        message="Não foi possível localizar ou clicar no botão 'Buscar assunto'")
      sigepe_buscarAssuntoBtn.click()
      wd.Webdriver.waitLoadingModal()
      assuntoBtn = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[text()='{data}']")),
        message="Não foi possível localizar ou clicar no elemento referente ao assunto especificado")
      assuntoBtn.click()
      sigepe_selecionarAssuntoBtn = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarAssuntoBtn"])),
        message="Não foi possível localizar ou clicar no botão 'Selecionar assunto'")
      sigepe_selecionarAssuntoBtn.click()
      wd.Webdriver.waitLoadingModal()
      time.sleep(0.3)
      sigepe_assuntoSelecionadoInput = wd.Webdriver.wait["regular"].until(EC.presence_of_element_located((
        By.XPATH, ac.AppConfig.xpaths["publicacao"]["assuntoSelecionadoInput"])),
        message="Não foi possível localizar ou clicar no campo 'Assunto selecionado'")
      assuntoSelecionado = sigepe_assuntoSelecionadoInput.get_attribute('value')
      return {"log": f"Assunto selecionado: {assuntoSelecionado}", "type": "n"}
     
    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "assunto")

  @staticmethod
  def buscar(filetext):
    try:
      termos = v.Variaveis.atribuirValorVariaveis(uc.UserConfig.obterAutoTemasAssuntos())
      for termo, obj in termos.items():
        if termo.lower() in filetext.lower():
          return {"log": f"Assunto identificado: {obj['assunto']}", "type": "n", "return": obj["assunto"]}
      raise Exception("não foi localizado um termo correspondente a um assunto no conteúdo do documento.")
    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "assunto")
