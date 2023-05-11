from selenium.common.exceptions import NoSuchElementException
from controllers import Webdriver as wd
from selenium.webdriver.common.by import By

def checkExistsByXpath(xpath):
    try:
        wd.Webdriver.nav.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True