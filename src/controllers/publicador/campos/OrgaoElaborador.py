from controllers import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

class OrgaoElaborador:
  @staticmethod
  def preencher(orgao, upag, uorg, responsavel, cargo):
    try:
      sigepe_botaoIncluirOrgaoElab = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["incluirOrgaoElaboradorBotao"])),
        message="Não foi possível localizar ou clicar no botão 'Incluir órgão elaborador'")
      sigepe_botaoIncluirOrgaoElab.click()
      wd.Webdriver.waitLoadingModal()
      tipo = OrgaoElaborador.definirTipoDeCadastro()
      if (tipo == 1):
        result = OrgaoElaborador.preencherTipo1(orgao, upag, uorg, responsavel, cargo)
        return result
      elif (tipo == 2):
        result = OrgaoElaborador.preencherTipo2(responsavel)
        return result
      else:
        raise Exception("Não foi possível definir o tipo de janela de cadastro de órgão elaborador")

    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "órgão elaborador")

  @staticmethod
  def preencherTipo1(orgao, upag, uorg, responsavel, cargo):
    sigepe_campoOrgao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["orgaoElaboradorSelect_t1"])),
      message="Não foi possível localizar ou clicar no campo 'Órgão' de órgão elaborador (t1)")
    sigepe_campoOrgao.click()
    time.sleep(0.3)
    sigepe_campoBuscarOrgao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarOrgaoElaboradorInput_t1"])),
      message="Não foi possível localizar ou clicar no campo 'Buscar órgão' de órgão elaborador (t1)")
    sigepe_campoBuscarOrgao.send_keys(orgao)
    time.sleep(1.5)
    sigepe_campoBuscarOrgao.send_keys(Keys.ENTER)
    wd.Webdriver.waitLoadingModal()

    sigepe_campoUpag = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["upagSelect_t1"])),
      message="Não foi possível localizar ou clicar no campo 'Upag' de órgão elaborador (t1)")
    sigepe_campoUpag.click()
    time.sleep(0.3)
    sigepe_campoBuscarUpag = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarUpagInput_t1"])),
      message="Não foi possível localizar ou clicar no campo 'Buscar upag' de órgão elaborador (t1)")
    sigepe_campoBuscarUpag.send_keys(upag)
    time.sleep(1.5)
    sigepe_campoBuscarUpag.send_keys(Keys.ENTER)
    wd.Webdriver.waitLoadingModal()

    sigepe_campoUorg = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["uorgSelect_t1"])),
      message="Não foi possível localizar ou clicar no campo 'Uorg' de órgão elaborador (t1)")
    sigepe_campoUorg.click()
    time.sleep(0.3)
    sigepe_campoBuscarUorg = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarUorgInput_t1"])),
      message="Não foi possível localizar ou clicar no campo 'Buscar uorg' de órgão elaborador (t1)")
    sigepe_campoBuscarUorg.send_keys(uorg)
    time.sleep(1.5)
    sigepe_campoBuscarUorg.send_keys(Keys.ENTER)
    wd.Webdriver.waitLoadingModal()

    sigepe_campoResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["responsavelAssinaturaInput_t1"])),
      message="Não foi possível localizar ou clicar no campo 'Responsável pela assinatura' de órgão elaborador (t1)")
    sigepe_campoResponsavel.send_keys(responsavel)

    sigepe_campoCargoResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["cargoResponsavelInput_t1"])),
      message="Não foi possível localizar ou clicar no campo 'Cargo do responsável' de órgão elaborador (t1)")
    sigepe_campoCargoResponsavel.send_keys(cargo)

    sigepe_botaoGravarOrgaoElab = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["botaoGravarOrgaoElaborador_t1"])),
      message="Não foi possível localizar ou clicar no botão 'Gravar' de órgão elaborador (t1)")
    wd.Webdriver.nav.execute_script("arguments[0].click();", sigepe_botaoGravarOrgaoElab);
    wd.Webdriver.waitLoadingModal()

    sigepe_responsavelSelecionado = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["responsavelSelecionado_t1"])),
      message="Não foi possível localizar ou clicar no elemento referente ao órgão elaborador selecionado (t1)")
    return {"log": f"Órgão elaborador preenchido: {sigepe_responsavelSelecionado.text}", "type": "n"}

  @staticmethod
  def preencherTipo2(responsavel):
    sigepe_campoNomeResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["nomeResponsavelOrgaoElaboradorInput_t2"])),
      message="Não foi possível localizar ou clicar no campo 'Nome do responsável' de órgão elaborador (t2)")
    sigepe_campoNomeResponsavel.send_keys(responsavel)
    time.sleep(0.3)
    sigepe_campoNomeResponsavel.send_keys(Keys.ENTER)
    wd.Webdriver.waitLoadingModal()

    sigepe_radioSelecionarResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarResponsavelRadio_t2"])),
      message="Não foi possível localizar ou clicar no seletor do 'Responsável' de órgão elaborador (t2)")
    sigepe_radioSelecionarResponsavel.click()
    wd.Webdriver.waitLoadingModal()

    sigepe_botaoSelecionarResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarResponsavelBotao_t2"])),
      message="Não foi possível localizar ou clicar no botão 'Selecionar' de órgão elaborador (t2)")
    sigepe_botaoSelecionarResponsavel.click()
    wd.Webdriver.waitLoadingModal()

    sigepe_responsavelSelecionado = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
      (By.XPATH, ac.AppConfig.xpaths["publicacao"]["responsavelSelecionado_t2"])),
      message="Não foi possível localizar ou clicar no elemento referente ao órgão elaborador selecionado (t2)")

    return {"log": f"Órgão elaborador preenchido: {sigepe_responsavelSelecionado.text}", "type": "n"}

  @staticmethod
  def definirTipoDeCadastro():
    tipo = None
    try:
      wd.Webdriver.waitLoadingModal()
      tipo1JanelaTitulo = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["janelaOrgaoElaboradorTitulo_t1"])))
      tipo = 1
    except:
      try:
        wd.Webdriver.waitLoadingModal()
        tipo2JanelaTitulo = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["janelaOrgaoElaboradorTitulo_t2"])))
        tipo = 2
      except:
        pass
    finally:
      return tipo