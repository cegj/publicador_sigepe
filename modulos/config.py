import sys

class Config:        

    def __init__(self):
        self.configJson = self.obterConfig()
        self.navegador = self.abrirWebdriver()
        self.dataAssinatura = self.configJson['config']['data_assinatura']
        self.dataPublicacao = self.configJson['config']['data_publicacao']
        self.edicaoBGP = self.configJson['valores']['edicao_bgp']
        self.tipoAssinatura = self.configJson['valores']['tipo_assinatura']
        self.especie = self.configJson['valores']['especie']
        self.tipoNumero = self.configJson['valores']['tipo_preenchimento']
        self.orgao = self.configJson['valores']['orgao']
        self.upag = self.configJson['valores']['upag']
        self.uorg = self.configJson['valores']['uorg']
        self.responsavelAssinatura = self.configJson['valores']['responsavel_assinatura']
        self.cargoResponsavelAssinatura = self.configJson['valores']['cargo_responsavel']


    ##Importação do arquivo de configurações config.json
    def obterConfig():
        
        def atribuirVariaveis(configJson):

            from modulos.Utilidades import Utilidades as Ut

            # Define valor variável de [hoje]
            vHojePonto = str(Ut.ajustarData(Ut.today, '.'))
            vHojeBarra = str(Ut.ajustarData(Ut.today, '/'))
            vHojeTraco = str(Ut.ajustarData(Ut.today, '-'))
          
            # Define valor variável de [proximo_dia_util]
            if (Ut.tomorrow.weekday() == 5):
                vProximoUtilPonto = str(Ut.ajustarData(Ut.tomorrow + Ut.timedelta(2), '.')) 
            elif (Ut.tomorrow.weekday() == 6):
                vProximoUtilPonto = str(Ut.ajustarData(Ut.tomorrow + Ut.timedelta(1), '.')) 
            else:
                vProximoUtilPonto = str(Ut.ajustarData(Ut.tomorrow, '.')) 

            if (Ut.tomorrow.weekday() == 5):
                vProximoUtilBarra = str(Ut.ajustarData(Ut.tomorrow + Ut.timedelta(2), '/')) 
            elif (Ut.tomorrow.weekday() == 6):
                vProximoUtilBarra = str(Ut.ajustarData(Ut.tomorrow + Ut.timedelta(1), '/')) 
            else:
                vProximoUtilBarra = str(Ut.ajustarData(Ut.tomorrow, '/')) 

            if (Ut.tomorrow.weekday() == 5):
                vProximoUtilTraco = str(Ut.ajustarData(Ut.tomorrow + Ut.timedelta(2), '-')) 
            elif (Ut.tomorrow.weekday() == 6):
                vProximoUtilTraco = str(Ut.ajustarData(Ut.tomorrow + Ut.timedelta(1), '-')) 
            else:
                vProximoUtilTraco = str(Ut.ajustarData(Ut.tomorrow, '-')) 

            # Define o valor variável de [ano_assinatura]
                
                dataAssinaturaArray = (dataAssinatura.split('/'))
                vAnoAssinatura = str(dataAssinaturaArray[2])

            import ast

            configJsonStr = str(configJson)

            configJsonStr = configJsonStr.replace("[hoje.]", vHojePonto)
            configJsonStr = configJsonStr.replace("[hoje/]", vHojeBarra)
            configJsonStr = configJsonStr.replace("[hoje-]", vHojeTraco)
            configJsonStr = configJsonStr.replace("[proximo_dia_util.]", vProximoUtilPonto)
            configJsonStr = configJsonStr.replace("[proximo_dia_util/]", vProximoUtilBarra)
            configJsonStr = configJsonStr.replace("[proximo_dia_util-]", vProximoUtilTraco)
            configJsonStr = configJsonStr.replace("[ano_assinatura]", vAnoAssinatura)

            configJson = ast.literal_eval(configJsonStr)

            return configJson

        import json

        with open('config.json', 'r', encoding="utf-8") as config_json_file:
            configJson = json.load(config_json_file)
            configJson = atribuirVariaveis(configJson)

        if (configJson):
            return configJson
        else:
            print('ERRO: Não foi possível importar os dados de config.json. Verifique se o arquivo está configurado corretamente. Em caso de dúvidas, consulte a documentação.')
            input('Aperte ENTER para encerrar a aplicação...')
            sys.exit()

    #Variaveis com os valores de configJson

    def exibeValoresConfigurados(self):
        print('VALORES CONFIGURADOS: \n')
        print('Edição do BGP: ', self.edicaoBGP)
        print('TIpo de assinatura:', self.tipoAssinatura)
        print('Espécie:', self.especie)
        print('Tipo de preenchimento do número: ', self.tipoNumero)
        print('Data de assinatura (emissão): ', self.dataAssinatura)
        print('Data de publicação: ', self.dataPublicacao)
        print('Órgão: ', self.orgao)
        print('UPAG: ', self.upag)
        print('UORG: ', self.uorg)
        print('Responsável pela assinatura: ', self.responsavelAssinatura)
        print('Cargo do responsável pela assinatura: ', self.cargoResponsavelAssinatura)
        print('Para alterá-los, edite config.json e reinicie a aplicação')
        print()

        if (self.dadoIncorreto == True):
            print('Há dados inválidos em config.json. Corrija e inicie novamente')
            self.navegador.quit()
            print('Sessão encerrada')
            input('Aperte ENTER para encerrar a aplicação...')
            sys.exit()

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
    
    # Valores de espera

    halfwait = WebDriverWait(navegador, 10)
    wait = WebDriverWait(navegador, 20)
    longwait = WebDriverWait(navegador, 40)






