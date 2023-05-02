from selenium.webdriver.common.by import By
from Webdriver import nav

def getScreenshotByXpath(xpath, filename):
  loc = nav.find_element(
  By.XPATH, xpath).screenshot(f'{filename}.png')
  nav.minimize_window()
  return f'{filename}.png'
