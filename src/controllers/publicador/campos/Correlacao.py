from controllers import AppConfig as ac
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
from selenium.webdriver.common.keys import Keys
import time
import os

class Correlacao:
  @staticmethod
  def preencher(data):
    try:
      command1 = "for (const li of document.querySelectorAll('li')) { if (li.textContent.includes('"
      command2 = "')) { li.click() } }"

      sigepe_botaoIncluirCorrelacao = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["incluirCorrelacaoBotao"])))
      sigepe_botaoIncluirCorrelacao.click()
      wfl.waitForLoading()


      sigepe_campoAcao = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["acaoCorrelacaoSelect"])))
      sigepe_campoAcao.click()
      time.sleep(0.3)

      sigepe_buscarAcao = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarAcaoCorrelacaoInput"])))
      sigepe_buscarAcao.send_keys(data['acao'])
      time.sleep(1.5)
      sigepe_buscarAcao.send_keys(Keys.ENTER)
      wfl.waitForLoading()

      sigepe_buscarAtoBotao = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarAtoCorrelacaoBotao"])))
      sigepe_buscarAtoBotao.click()
      wfl.waitForLoading()

      sigepe_campoOrigem = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["origemAtoCorrelacaoSelect"])))
      sigepe_campoOrigem.click()
      time.sleep(0.5)
      wfl.waitForLoading()
      nav.execute_script("".join([command1, data['origem'], command2]))
      wfl.waitForLoading()

      sigepe_campoOrgaoResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["orgaoResponsavelAtoCorrelacaoSelect"])))
      sigepe_campoOrgaoResponsavel.click()
      time.sleep(0.3)

      sigepe_buscarOrgaoResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarOrgaoResponsavelInput"])))
      nav.execute_script("".join([command1, data['orgao'], command2]))
      wfl.waitForLoading()

      sigepe_campoUpagResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["upagResponsavelAtoCorrelacaoSelect"])))
      sigepe_campoUpagResponsavel.click()
      time.sleep(0.3)

      sigepe_buscarUpagResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarUpagResponsavelInput"])))
      nav.execute_script("".join([command1, data['upag'], command2]))
      wfl.waitForLoading()
      time.sleep(1.3)

      sigepe_campoUorgResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["uorgResponsavelAtoCorrelacaoSelect"])))
      sigepe_campoUorgResponsavel.click()
      time.sleep(0.3)

      sigepe_buscarUorgResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarUorgResponsavelInput"])))
      nav.execute_script("".join([command1, data['uorg'], command2]))
      wfl.waitForLoading()

      sigepe_campoNumeroAtoCorrelacionado = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["numeroAtoCorrelacaoInput"])))
      sigepe_campoNumeroAtoCorrelacionado.click()
      time.sleep(0.2)
      sigepe_campoNumeroAtoCorrelacionado.send_keys(data['numero'])

      sigepe_campoAnoDe = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["anoDeAtoCorrelacaoInput"])))
      sigepe_campoAnoDe.click()
      time.sleep(0.2)
      sigepe_campoAnoDe.send_keys(data['ano'])

      sigepe_campoAnoAte = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["anoAteCorrelacaoInput"])))
      sigepe_campoAnoAte.click()
      time.sleep(0.2)
      sigepe_campoAnoAte.send_keys(data['ano'])

      sigepe_botaoPesquisarAto = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["pesquisarAtoCorrelacaoBotao"])))
      sigepe_botaoPesquisarAto.click()
      wfl.waitForLoading()

      sigepe_radioSelecionarAto = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["atoCorrelacaoRadio"])))
      sigepe_radioSelecionarAto.click()
      time.sleep(0.3)

      sigepe_botaoSelecionarAto = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarAtoCorrelacaoBotao"])))
      # sigepe_botaoGravarAto.click()
      nav.execute_script("arguments[0].click();", sigepe_botaoSelecionarAto);
      wfl.waitForLoading()

      sigepe_botaoGravarAto = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["gravarAtoCorrelacaoBotao"])))
      # sigepe_botaoGravarAto.click()
      nav.execute_script("arguments[0].click();", sigepe_botaoGravarAto);
      wfl.waitForLoading()

      sigepe_acaoSelecionada = wait["regular"].until(EC.presence_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["atoCorrelacaoAcaoSelecionada"])))

      sigepe_especieSelecionada = wait["regular"].until(EC.presence_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths["publicacao"]["atoCorrelacaoEspecieSelecionada"])))

      sigepe_numeroSelecionado = wait["regular"].until(EC.presence_of_element_located(
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
