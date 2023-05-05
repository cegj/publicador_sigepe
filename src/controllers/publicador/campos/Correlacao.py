from appXpaths import xpaths
from Webdriver import nav
from Webdriver import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers import waitForLoading as wfl
from selenium.webdriver.common.keys import Keys
import time

class Correlacao:
  @staticmethod
  def preencher(data):
    try:
      sigepe_botaoIncluirCorrelacao = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["incluirCorrelacaoBotao"])))
      sigepe_botaoIncluirCorrelacao.click()
      wfl.waitForLoading()


      sigepe_campoAcao = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["acaoCorrelacaoSelect"])))
      sigepe_campoAcao.click()
      time.sleep(0.3)

      sigepe_buscarAcao = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["buscarAcaoCorrelacaoInput"])))
      sigepe_buscarAcao.send_keys(data['acao'])
      time.sleep(1.5)
      sigepe_buscarAcao.send_keys(Keys.ENTER)
      wfl.waitForLoading()

      sigepe_buscarAtoBotao = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["buscarAtoCorrelacaoBotao"])))
      sigepe_buscarAtoBotao.click()
      wfl.waitForLoading()

      sigepe_campoOrigem = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["origemAtoCorrelacaoSelect"])))
      sigepe_campoOrigem.click()
      time.sleep(0.5)
      wfl.waitForLoading()

      # sigepe_origemOption = wait["regular"].until(EC.element_to_be_clickable(
      #   (By.XPATH, f"//*[text()='{data['origem']}']")))
      # time.sleep(1)
      
      command1 = "for (const li of document.querySelectorAll('li')) { if (li.textContent.includes('"
      command2 = "')) { li.click() } }"

      nav.execute_script("".join([command1, data['origem'], command2]))

      # time.sleep(5)

      # nav.execute_script("arguments[0].click();", sigepe_origemOption);
      wfl.waitForLoading()

      sigepe_campoOrgaoResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["orgaoResponsavelAtoCorrelacaoSelect"])))
      sigepe_campoOrgaoResponsavel.click()
      time.sleep(0.3)

      sigepe_buscarOrgaoResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["buscarOrgaoResponsavelInput"])))
      sigepe_buscarOrgaoResponsavel.send_keys(data['orgao'])
      time.sleep(1.5)
      sigepe_buscarOrgaoResponsavel.send_keys(Keys.ENTER)
      wfl.waitForLoading()

      sigepe_campoUpagResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["upagResponsavelAtoCorrelacaoSelect"])))
      sigepe_campoUpagResponsavel.click()
      time.sleep(0.3)

      sigepe_buscarUpagResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["buscarUpagResponsavelInput"])))
      sigepe_buscarUpagResponsavel.send_keys(data['upag'])
      time.sleep(1.5)
      sigepe_buscarUpagResponsavel.send_keys(Keys.ENTER)
      wfl.waitForLoading()

      sigepe_campoUorgResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["uorgResponsavelAtoCorrelacaoSelect"])))
      sigepe_campoUorgResponsavel.click()
      time.sleep(0.3)

      sigepe_buscarUorgResponsavel = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["buscarUorgResponsavelInput"])))
      sigepe_buscarUorgResponsavel.send_keys(data['uorg'])
      time.sleep(1.5)
      sigepe_buscarUorgResponsavel.send_keys(Keys.ENTER)
      wfl.waitForLoading()

      sigepe_campoNumeroAtoCorrelacionado = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["numeroAtoCorrelacaoInput"])))
      sigepe_campoNumeroAtoCorrelacionado.click()
      time.sleep(0.2)
      sigepe_campoNumeroAtoCorrelacionado.send_keys(data['numero'])

      sigepe_campoAnoDe = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["anoDeAtoCorrelacaoInput"])))
      sigepe_campoAnoDe.click()
      time.sleep(0.2)
      sigepe_campoAnoDe.send_keys(data['ano'])

      sigepe_campoAnoAte = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["anoAteCorrelacaoInput"])))
      sigepe_campoAnoAte.click()
      time.sleep(0.2)
      sigepe_campoAnoAte.send_keys(data['ano'])

      sigepe_botaoPesquisarAto = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["pesquisarAtoCorrelacaoBotao"])))
      sigepe_botaoPesquisarAto.click()
      wfl.waitForLoading()

      sigepe_radioSelecionarAto = wait["regular"].until(EC.element_to_be_clickable(
          (By.XPATH, xpaths["publicacao"]["atoCorrelacaoRadio"])))
      sigepe_radioSelecionarAto.click()
      time.sleep(0.3)

      sigepe_botaoGravarAto = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["gravarAtoCorrelacaoBotao"])))
      sigepe_botaoGravarAto.click()
      wfl.waitForLoading()

      sigepe_atoCorrelacaoSelecionado = wait["regular"].until(EC.presence_of_element_located(
        (By.XPATH, xpaths["publicacao"]["sigepe_atoCorrelacaoSelecionado"])))

      sigepe_atoCorrelacaoSelecionado = nav.execute_script("return arguments[0].innerText.replaceAll('\n',"").replaceAll('\t'," ").trim();", atoCorrelacaoSelecionado);

      return {"log": f"Correlação selecionada: {sigepe_atoCorrelacaoSelecionado}", "type": "n"}

    except Exception as e:
      print(e)
      return {"log": f"Falha ao selecionar ato correlacionado: {e}", "type": "e", "e": e}

