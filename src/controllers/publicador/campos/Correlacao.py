from controllers import AppConfig as ac
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

class Correlacao:
  @staticmethod
  def preencher(data):
    try:
      command1 = "for (const li of document.querySelectorAll('li')) { if (li.textContent.includes('"
      command2 = "')) { li.click() } }"

      sigepe_botaoIncluirCorrelacao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["incluirCorrelacaoBotao"])))
      sigepe_botaoIncluirCorrelacao.click()
      wd.Webdriver.waitLoadingModal()


      sigepe_campoAcao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["acaoCorrelacaoSelect"])))
      sigepe_campoAcao.click()
      time.sleep(0.3)

      sigepe_buscarAcao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarAcaoCorrelacaoInput"])))
      sigepe_buscarAcao.send_keys(data['acao'])
      time.sleep(1.5)
      sigepe_buscarAcao.send_keys(Keys.ENTER)
      wd.Webdriver.waitLoadingModal()

      sigepe_buscarAtoBotao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarAtoCorrelacaoBotao"])))
      sigepe_buscarAtoBotao.click()
      wd.Webdriver.waitLoadingModal()

      sigepe_campoOrigem = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["origemAtoCorrelacaoSelect"])))
      sigepe_campoOrigem.click()
      time.sleep(0.5)
      wd.Webdriver.waitLoadingModal()
      wd.Webdriver.nav.execute_script("".join([command1, data['origem'], command2]))
      wd.Webdriver.waitLoadingModal()

      sigepe_campoOrgaoResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["orgaoResponsavelAtoCorrelacaoSelect"])))
      sigepe_campoOrgaoResponsavel.click()
      time.sleep(0.3)

      sigepe_buscarOrgaoResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarOrgaoResponsavelInput"])))
      wd.Webdriver.nav.execute_script("".join([command1, data['orgao'], command2]))
      wd.Webdriver.waitLoadingModal()

      sigepe_campoUpagResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["upagResponsavelAtoCorrelacaoSelect"])))
      sigepe_campoUpagResponsavel.click()
      time.sleep(0.3)

      sigepe_buscarUpagResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarUpagResponsavelInput"])))
      wd.Webdriver.nav.execute_script("".join([command1, data['upag'], command2]))
      wd.Webdriver.waitLoadingModal()
      time.sleep(1.3)

      sigepe_campoUorgResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["uorgResponsavelAtoCorrelacaoSelect"])))
      sigepe_campoUorgResponsavel.click()
      time.sleep(0.3)

      sigepe_buscarUorgResponsavel = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarUorgResponsavelInput"])))
      wd.Webdriver.nav.execute_script("".join([command1, data['uorg'], command2]))
      wd.Webdriver.waitLoadingModal()

      sigepe_campoNumeroAtoCorrelacionado = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["numeroAtoCorrelacaoInput"])))
      sigepe_campoNumeroAtoCorrelacionado.click()
      time.sleep(0.2)
      sigepe_campoNumeroAtoCorrelacionado.send_keys(data['numero'])

      sigepe_campoAnoDe = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["anoDeAtoCorrelacaoInput"])))
      sigepe_campoAnoDe.click()
      time.sleep(0.2)
      sigepe_campoAnoDe.send_keys(data['ano'])

      sigepe_campoAnoAte = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["anoAteCorrelacaoInput"])))
      sigepe_campoAnoAte.click()
      time.sleep(0.2)
      sigepe_campoAnoAte.send_keys(data['ano'])

      sigepe_botaoPesquisarAto = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["pesquisarAtoCorrelacaoBotao"])))
      sigepe_botaoPesquisarAto.click()
      wd.Webdriver.waitLoadingModal()

      sigepe_radioSelecionarAto = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["atoCorrelacaoRadio"])))
      sigepe_radioSelecionarAto.click()
      time.sleep(0.3)

      sigepe_botaoSelecionarAto = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarAtoCorrelacaoBotao"])))
      # sigepe_botaoGravarAto.click()
      wd.Webdriver.nav.execute_script("arguments[0].click();", sigepe_botaoSelecionarAto);
      wd.Webdriver.waitLoadingModal()

      sigepe_botaoGravarAto = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["gravarAtoCorrelacaoBotao"])))
      # sigepe_botaoGravarAto.click()
      wd.Webdriver.nav.execute_script("arguments[0].click();", sigepe_botaoGravarAto);
      wd.Webdriver.waitLoadingModal()

      sigepe_acaoSelecionada = wd.Webdriver.wait["regular"].until(EC.presence_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["atoCorrelacaoAcaoSelecionada"])))

      sigepe_especieSelecionada = wd.Webdriver.wait["regular"].until(EC.presence_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["atoCorrelacaoEspecieSelecionada"])))

      sigepe_numeroSelecionado = wd.Webdriver.wait["regular"].until(EC.presence_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["atoCorrelacaoNumeroSelecionado"])))

      selecionado = f"{sigepe_acaoSelecionada.text} {sigepe_especieSelecionada.text} {sigepe_numeroSelecionado.text}"

      return {"log": f"Correlação selecionada: {selecionado}", "type": "n"}

    except Exception as e:
      print(e)
      return {"log": f"Falha ao selecionar correlação: {e}", "type": "e", "e": e}

  @staticmethod
  def apagarArquivo(file):
    path = os.path.dirname(file.name)
    filename = os.path.basename(file.name)
    correlationFilename = filename.split('.')[0] + ".txt"
    correlationFullpath = os.path.join(path, correlationFilename)
    os.remove(correlationFullpath)
