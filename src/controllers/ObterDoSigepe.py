from Webdriver import nav
from Webdriver import wait
from controllers import AppConfig as ac
from helpers import waitForLoading as wfl 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from tkinter import messagebox

class ObterDoSigepe():
  @staticmethod
  def temas():
    sigepe_temas = nav.find_elements(By.XPATH, ac.AppConfig.xpaths['publicacao']['temas'])
    listaTemas = []
    for tema in sigepe_temas:
      tema = tema.get_attribute('innerText')
      count = listaTemas.count(tema)
      if (count > 0):
        listaTemas.append(tema + f' //{count + 1}')
      else:
        listaTemas.append(tema)
    return listaTemas

  @staticmethod
  def assuntos(tema):
    try:
      url = ac.AppConfig.urls["cadastrarAtoPublicacao"]
      if (nav.current_url != url):
        gt.goTo(url)
      temaSplitted = tema.split('//')
      sigepe_temaSelect = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, ac.AppConfig.xpaths["publicacao"]["temaSelect"])))
      sigepe_temaSelect.click()
      time.sleep(0.3)
      sigepe_buscarTemaInput = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarTemaInput"])))
      sigepe_buscarTemaInput.send_keys(Keys.CONTROL, 'a')
      sigepe_buscarTemaInput.send_keys(Keys.BACKSPACE)
      time.sleep(0.3)
      sigepe_buscarTemaInput.send_keys(temaSplitted[0])
      time.sleep(1.5)
      if (len(temaSplitted) == 2):
        i = 1
        while (i < int(temaSplitted[1])):
          sigepe_buscarTemaInput.send_keys(Keys.ARROW_DOWN)
          time.sleep(0.3)
          i += 1
      sigepe_buscarTemaInput.send_keys(Keys.ENTER)
      wfl.waitForLoading()
      time.sleep(0.3)
      sigepe_buscarAssuntoBtn = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, ac.AppConfig.xpaths["publicacao"]["buscarAssuntoBtn"])))
      sigepe_buscarAssuntoBtn.click()
      wfl.waitForLoading()
      sigepe_assuntos = wait["regular"].until(EC.visibility_of_all_elements_located((By.XPATH, ac.AppConfig.xpaths["publicacao"]["assuntosBtns"])))
      listaAssuntos = []
      for assunto in sigepe_assuntos:
        assunto = assunto.get_attribute('innerText')
        count = listaAssuntos.count(assunto)
        if (count > 0):
          listaAssuntos.append(assunto + f' //{count + 1}')
        else:
          listaAssuntos.append(assunto)
      ultimoNivelAssunto = sigepe_assuntos[-1]
      ultimoNivelAssunto.click()
      sigepe_selecionarAssuntoBtn = wait["regular"].until(EC.element_to_be_clickable((By.XPATH, ac.AppConfig.xpaths["publicacao"]["selecionarAssuntoBtn"])))
      sigepe_selecionarAssuntoBtn.click()
      return listaAssuntos
    except Exception as e:
      messagebox.showerror("Erro ao buscar assunto", e)
      return None

  @staticmethod
  def botaoHabilitacao():
    try:
      btn = nav.find_element(By.XPATH, ac.AppConfig.xpaths['habilitacao']['habilitacaoBotao'])
      return btn
    except Exception as e:
      messagebox.showerror("Erro ao obter botão de habilitação no Sigepe", e)
      return None

  @staticmethod
  def orgaosAtoCorrelacionado():
    url = ac.AppConfig.urls["cadastrarAtoPublicacao"]
    if (nav.current_url != url):
      gt.goTo(url)
    sigepe_orgaosAtoCorrelacionado = nav.find_elements(By.XPATH, ac.AppConfig.xpaths['publicacao']['orgaosAtoCorrelacionado'])
    lista = []
    for orgao in sigepe_orgaosAtoCorrelacionado:
      orgao = orgao.get_attribute('innerText')
      count = lista.count(orgao)
      if (count > 0):
        lista.append(orgao + f' //{count + 1}')
      else:
        listaTemas.append(orgao)
    return lista