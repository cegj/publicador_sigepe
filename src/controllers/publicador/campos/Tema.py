from models import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from models import UserConfig as uc
from controllers import Variaveis as v

class Tema:
  @staticmethod
  def preencher(data):
    try:
      temaSplitted = data.split('//')
      campoTema = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["temaSelect"])),
        message="Não foi possível localizar ou clicar no campo 'Tema'")
      campoTema.click()
      time.sleep(0.3)

      campoBuscarTema = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarTemaInput"])),
        message="Não foi possível localizar ou clicar no campo 'Buscar tema'")
      wd.Webdriver.nav.execute_script("arguments[0].setAttribute('value',arguments[1])",campoBuscarTema, "")
      time.sleep(0.3)
      campoBuscarTema.send_keys(temaSplitted[0])
      time.sleep(1.5)

      if (len(temaSplitted) == 2):
        i = 1
        while (i < int(temaSplitted[1])):
          campoBuscarTema.send_keys(Keys.ARROW_DOWN)
          time.sleep(0.3)
          i += 1

      campoBuscarTema.send_keys(Keys.ENTER)
      wd.Webdriver.waitLoadingModal()

      campoTemaPreenchido = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["temaSelect"])),
        message="Não foi possível localizar ou clicar no campo 'Tema' preenchido")

      return {"log": f"Tema selecionado: {campoTemaPreenchido.text}", "type": "n"}

    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "tema")

  @staticmethod
  def buscar(filetext):
    try:
      termos = v.Variaveis.atribuirValorVariaveis(uc.UserConfig.obterAutoTemasAssuntos())
      for termo, obj in termos.items():
        if termo.lower() in filetext.lower():
          return {"log": f"Tema identificado: {obj['tema']}", "type": "n", "return": obj["tema"]}
      raise Exception("não foi localizado um termo correspondente a um tema no conteúdo do documento.")
    except Exception as e:
      return {"log": f"Falha ao selecionar tema: {e}", "type": "e", "e": e, "return": False}
