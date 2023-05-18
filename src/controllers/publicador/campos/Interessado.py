from models import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class Interessado:
  @staticmethod
  def preencher(data):
    try:
      sigepe_botaoIncluirInteressado = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["incluirInteressadoBotao"])),
        message="Não foi possível localizar ou clicar no botão 'Incluir interessado'")
      sigepe_botaoIncluirInteressado.click()
      wd.Webdriver.waitLoadingModal()

      sigepe_campoMatricula = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["matriculaInteressadoInput"])),
        message="Não foi possível localizar ou clicar no campo 'Matrícula' do interessado")
      sigepe_campoMatricula.click()
      time.sleep(0.2)
      sigepe_campoMatricula.send_keys(data)

      sigepe_botaoPesquisarInteressado = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["pesquisarInteressadoBotao"])),
        message="Não foi possível localizar ou clicar no botão 'Pesquisar' do interessado")
      sigepe_botaoPesquisarInteressado.click()
      wd.Webdriver.waitLoadingModal()

      sigepe_checkboxSelecionarServidor = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarInteressadoCheckbox"])),
        message="Não foi possível localizar ou clicar no seletor do interessado")
      sigepe_checkboxSelecionarServidor.click()
      time.sleep(0.3)

      sigepe_botaoIncluirNaLista = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["incluirInteressadoNaListaBotao"])),
        message="Não foi possível localizar ou clicar no botão 'Incluir na lista' do interessado")
      wd.Webdriver.nav.execute_script("arguments[0].click();", sigepe_botaoIncluirNaLista);
      wd.Webdriver.waitLoadingModal()

      sigepe_botaoSelecionarAto = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarServidorBotao"])),
        message="Não foi possível localizar ou clicar no botão 'Selecionar' do interessado")
      wd.Webdriver.nav.execute_script("arguments[0].click();", sigepe_botaoSelecionarAto);
      wd.Webdriver.waitLoadingModal()

      interessadoSelecionado = wd.Webdriver.wait["regular"].until(EC.presence_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["interessadoSelecionado"])),
        message="Não foi possível localizar ou clicar no elemento referente ao interessado selecionado")

      return {"log": f"Interessado selecionado: {interessadoSelecionado.text}", "type": "n"}

    except Exception as e:
      return wd.Webdriver.handleExceptions(e, "interessado")

