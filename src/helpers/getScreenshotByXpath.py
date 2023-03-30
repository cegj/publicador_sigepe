from selenium.webdriver.common.by import By
import cv2
import os
from Webdriver import nav

def getScreenshotByXpath(xpath):
  loc = nav.find_element(
  By.XPATH, xpath).screenshot('captcha.png')
  nav.minimize_window()
  return 'captcha.png'
