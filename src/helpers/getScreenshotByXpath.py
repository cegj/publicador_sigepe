from selenium.webdriver.common.by import By
from controllers import Webdriver as wd

def getScreenshotByXpath(xpath, filename):
  loc = wd.Webdriver.nav.find_element(
  By.XPATH, xpath).screenshot(f'{filename}.png')
  wd.Webdriver.nav.minimize_window()
  return f'{filename}.png'
