from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys
from helpers import checkExistsByXpath as cebx

class OrgaoElaborador:
  @staticmethod
  def preencher(upag, uorg, responsavel, cargo):
    try:
      sigepe_botaoIncluirOrgaoElab = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["incluirOrgaoElaboradorBotao"])))
      sigepe_botaoIncluirOrgaoElab.click()
      wfl.waitForLoading()

      tipo = OrgaoElaborador.definirTipoDeCadastro()

      if (tipo == 1):
        pass
      elif (tipo == 2):
        sigepe_campoNomeResponsavel = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["nomeResponsavelOrgaoElaboradorInput_t2"])))
        sigepe_campoNomeResponsavel.send_keys(responsavel)
        time.sleep(0.3)
        sigepe_campoNomeResponsavel.send_keys(Keys.ENTER)
        wfl.waitForLoading()

        sigepe_radioSelecionarResponsavel = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["selecionarResponsavelRadio_t2"])))
        sigepe_radioSelecionarResponsavel.click()
        wfl.waitForLoading()

        sigepe_botaoSelecionarResponsavel = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["selecionarResponsavelBotao_t2"])))
        sigepe_botaoSelecionarResponsavel.click()
        wfl.waitForLoading()

        sigepe_botaoSelecionarResponsavel = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["responsavelSelecionado_t2"])))

        return {"log": f"Órgão elaborador preenchido: {sigepe_botaoSelecionarResponsavel.text()}", "type": "n"}
      else:
        raise Exception("Não foi possível definir o tipo de janela de cadastro")

    except Exception as e:
      return {"log": f"Falha ao preencher órgão elaborador: {e}", "type": "e", "e": e}

  @staticmethod
  def definirTipoDeCadastro():
    tipo = 0
    try:
      wfl.waitForLoading()
      tipo1JanelaTitulo = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["janelaOrgaoElaboradorTitulo_t1"])))
      tipo = 1
    except:
      wfl.waitForLoading()
      tipo1JanelaTitulo = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["janelaOrgaoElaboradorTitulo_t2"])))
      tipo = 2
    finally:
      return tipo