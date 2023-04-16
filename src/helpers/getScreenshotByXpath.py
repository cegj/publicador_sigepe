from selenium.webdriver.common.by import By
import cv2
import os
from Webdriver import nav

def getScreenshotByXpath(xpath, filename):
  loc = nav.find_element(
  By.XPATH, xpath).screenshot(f'{filename}.jpg')
  nav.minimize_window()
  return f'{filename}.jpg'
