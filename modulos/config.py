##Importação do arquivo de configurações config.json

##Fazer as substituições das variáveis no arquivo config.json

  def atribuir_variaveis_config(configjson):
    if (configjson.find('[hoje.]')):
      subst = str(ajusta_data(today, '.'))
      configjson = configjson.replace('[hoje, .]', subst)
    
    if (configjson.find('[hoje/]')):
      subst = str(ajusta_data(today, '/'))
      configjson = configjson.replace('[hoje/]', subst)

    if (configjson.find('[hoje-]')):
      subst = str(ajusta_data(today, '-'))
      configjson = configjson.replace('[hoje-]', subst)

    if (configjson.find('[amanha_util.]')):
        if (tomorrow.weekday() == 5): #5 = sábado
            return ajusta_data(tomorrow + timedelta(2), '.')
        elif (tomorrow.weekday() == 6): #6 = domingo
            return ajusta_data(tomorrow + timedelta(1), '.')
        else:
            return ajusta_data(tomorrow, '.')

    if (configjson.find('[amanha_util/]')):
        if (tomorrow.weekday() == 5): #5 = sábado
            return ajusta_data(tomorrow + timedelta(2), '/')
        elif (tomorrow.weekday() == 6): #6 = domingo
            return ajusta_data(tomorrow + timedelta(1), '/')
        else:
            return ajusta_data(tomorrow, '/')

    if (configjson.find('[amanha_util-]')):
        if (tomorrow.weekday() == 5): #5 = sábado
            return ajusta_data(tomorrow + timedelta(2), '-')
        elif (tomorrow.weekday() == 6): #6 = domingo
            return ajusta_data(tomorrow + timedelta(1), '-')
        else:
            return ajusta_data(tomorrow, '-')
    
    if (configjson.find('[ano_assinatura]')):
        from modulos.publicador.valores_configurados import dataAssinatura
        anoAssinatura = (dataAssinatura.split('/'))
        anoAssinatura = anoAssinatura[2]
        configjson = configjson.replace('[ano_assinatura]', anoAssinatura)

    return configjson

import json

with open('config.json', 'r', encoding="utf-8") as config_json:
    config_json = json.load(config_json)
    config_json = atribuir_variaveis_config(config_json)


##Configuração do webdriver

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
navegador.minimize_window()

##Configuração dos tempos de espera

from selenium.webdriver.support.ui import WebDriverWait
halfwait = WebDriverWait(navegador, 10)
wait = WebDriverWait(navegador, 20)
longwait = WebDriverWait(navegador, 40)
