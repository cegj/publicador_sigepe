from Webdriver import nav
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from appXpaths import xpaths

def waitForLoading():
    loadingMoral = WebDriverWait(nav, 300).until(EC.invisibility_of_element_located(
        (By.XPATH, xpaths['general']['loadingModal'])))
    return None