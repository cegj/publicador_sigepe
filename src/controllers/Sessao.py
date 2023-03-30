import appConfig
from selenium.webdriver.common.by import By

class Sessao:
  def __init__(self, master, nav):
    self.appConfig = appConfig.AppConfig()
    self.master = master
    self.nav = nav

  def configurarSessao(self):
    sigBotaoHabilitacao = self.nav.find_element(
    By.XPATH, '//*[@id="j_idt62:habDisponiveisLabel"]')

    sigBotaoHabilitacao.click()
