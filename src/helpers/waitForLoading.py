from controllers import Webdriver as wd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from controllers import AppConfig as ac

def waitForLoading():
    loadingMoral = WebDriverWait(wd.Webdriver.nav, 300).until(EC.invisibility_of_element_located(
        (By.XPATH, ac.AppConfig.xpaths['general']['loadingModal'])))
    return None