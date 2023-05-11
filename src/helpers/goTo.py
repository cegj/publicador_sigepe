from selenium.webdriver.common.by import By
from controllers import Webdriver as wd
from tkinter import messagebox
from helpers import checkExistsByXpath as cebx

def goTo(url):
    try:
        wd.Webdriver.nav.get(url)
        if(cebx.checkExistsByXpath('//*[@id="details-button"]')): #If Chrome SSL Error
            detailsBtn = wd.Webdriver.nav.find_element(
                By.XPATH, '//*[@id="details-button"]')
            detailsBtn.click()
            proceedLink = wd.Webdriver.nav.find_element(
                By.XPATH, '//*[@id="proceed-link"]')
            proceedLink.click()
    except Exception as e:
      messagebox.showerror("Erro ao acessar página", e)