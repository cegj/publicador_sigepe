from selenium.common.exceptions import NoSuchElementException
from Webdriver import nav

def checkExistsByXpath(xpath):
    try:
        nav.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True