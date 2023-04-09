from selenium.common.exceptions import NoSuchElementException
from Webdriver import nav
from selenium.webdriver.common.by import By

def checkExistsByXpath(xpath):
    try:
        nav.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True