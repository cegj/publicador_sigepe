class Config:

    ##Importação do arquivo de configurações config.json
    def obterDados():
        import json

        with open('config.json', 'r', encoding="utf-8") as config_json:
           config_json = json.load(config_json)

        return config_json

    ##Configuração do webdriver 
    def abrirWebdriver():

        try: 
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager

            options = Options()
            options.add_argument("start-maximized")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            navegador.minimize_window()

            return navegador

        except Exception as e:
            return repr(e)

    navegador = abrirWebdriver()
    
    from selenium.webdriver.support.ui import WebDriverWait
    halfwait = WebDriverWait(navegador, 10)
    wait = WebDriverWait(navegador, 20)
    longwait = WebDriverWait(navegador, 40)






