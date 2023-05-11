from controllers import AppConfig as ac
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
import time
from selenium.webdriver.common.keys import Keys

class OrgaoElaborador:
  @staticmethod
  def preencher(orgao, upag, uorg, responsavel, cargo):
    try:
      sigepe_botaoIncluirOrgaoElab = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["incluirOrgaoElaboradorBotao"])))
      sigepe_botaoIncluirOrgaoElab.click()
      wfl.waitForLoading()
      tipo = OrgaoElaborador.definirTipoDeCadastro()
      if (tipo == 1):
        result = OrgaoElaborador.preencherTipo1(orgao, upag, uorg, responsavel, cargo)
        return result
      elif (tipo == 2):
        result = OrgaoElaborador.preencherTipo2(responsavel)
        return result
      else:
        raise Exception("Não foi possível definir o tipo de janela de cadastro")

    except Exception as e:
      return {"log": f"Falha ao preencher órgão elaborador: {e}", "type": "e", "e": e}

  @staticmethod
  def preencherTipo1(orgao, upag, uorg, responsavel, cargo):
    sigepe_campoOrgao = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["orgaoElaboradorSelect_t1"])))
    sigepe_campoOrgao.click()
    time.sleep(0.3)
    sigepe_campoBuscarOrgao = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarOrgaoElaboradorInput_t1"])))
    sigepe_campoBuscarOrgao.send_keys(orgao)
    time.sleep(1.5)
    sigepe_campoBuscarOrgao.send_keys(Keys.ENTER)
    wfl.waitForLoading()

    sigepe_campoUpag = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["upagSelect_t1"])))
    sigepe_campoUpag.click()
    time.sleep(0.3)
    sigepe_campoBuscarUpag = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarUpagInput_t1"])))
    sigepe_campoBuscarUpag.send_keys(upag)
    time.sleep(1.5)
    sigepe_campoBuscarUpag.send_keys(Keys.ENTER)
    wfl.waitForLoading()

    sigepe_campoUorg = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["uorgSelect_t1"])))
    sigepe_campoUorg.click()
    time.sleep(0.3)
    sigepe_campoBuscarUorg = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarUorgInput_t1"])))
    sigepe_campoBuscarUorg.send_keys(uorg)
    time.sleep(1.5)
    sigepe_campoBuscarUorg.send_keys(Keys.ENTER)
    wfl.waitForLoading()

    sigepe_campoResponsavel = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["responsavelAssinaturaInput_t1"])))
    sigepe_campoResponsavel.send_keys(responsavel)

    sigepe_campoCargoResponsavel = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["cargoResponsavelInput_t1"])))
    sigepe_campoCargoResponsavel.send_keys(cargo)

    sigepe_botaoGravarOrgaoElab = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["botaoGravarOrgaoElaborador_t1"])))
    nav.execute_script("arguments[0].click();", sigepe_botaoGravarOrgaoElab);
    wfl.waitForLoading()

    sigepe_responsavelSelecionado = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["responsavelSelecionado_t1"])))
    return {"log": f"Órgão elaborador preenchido: {sigepe_responsavelSelecionado.text}", "type": "n"}

  @staticmethod
  def preencherTipo2(responsavel):
    sigepe_campoNomeResponsavel = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["nomeResponsavelOrgaoElaboradorInput_t2"])))
    sigepe_campoNomeResponsavel.send_keys(responsavel)
    time.sleep(0.3)
    sigepe_campoNomeResponsavel.send_keys(Keys.ENTER)
    wfl.waitForLoading()

    sigepe_radioSelecionarResponsavel = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarResponsavelRadio_t2"])))
    sigepe_radioSelecionarResponsavel.click()
    wfl.waitForLoading()

    sigepe_botaoSelecionarResponsavel = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarResponsavelBotao_t2"])))
    sigepe_botaoSelecionarResponsavel.click()
    wfl.waitForLoading()

    sigepe_responsavelSelecionado = wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["responsavelSelecionado_t2"])))

    return {"log": f"Órgão elaborador preenchido: {sigepe_responsavelSelecionado.text}", "type": "n"}

  @staticmethod
  def definirTipoDeCadastro():
    tipo = None
    try:
      wfl.waitForLoading()
      tipo1JanelaTitulo = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["janelaOrgaoElaboradorTitulo_t1"])))
      tipo = 1
    except:
      try:
        wfl.waitForLoading()
        tipo2JanelaTitulo = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["janelaOrgaoElaboradorTitulo_t2"])))
        tipo = 2
      except:
        pass
    finally:
      return tipo