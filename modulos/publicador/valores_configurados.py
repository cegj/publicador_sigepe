from modulos.config import config_json
from modulos.config import navegador

##Verifica e exibe para o usuário as informações de config.json

##Define órgão, UORG, UPAG e autoridade

dadoIncorreto = False

if (config_json['valores']['edicao_bgp'] == "Normal" or config_json['valores']['edicao_bgp'] == "Extraordinária"):
    edicaoBGP = config_json['valores']['edicao_bgp']
else:
    edicaoBGP = '*** Tipo de edição',config_json['valores']['edicao_bgp'],'inválido. O valor deve ser "Normal" ou "Extraordinário"'
    dadoIncorreto = True

if (config_json['valores']['tipo_assinatura'] == "Manual") or (config_json['valores']['tipo_assinatura'] == "Digital"):
    tipoAssinatura = config_json['valores']['tipo_assinatura']
else:
    tipoAssinatura = '*** Tipo de assinatura',config_json['valores']['tipo_assinatura'],'inválido. O valor deve ser "Manual" ou "Digital"'
    dadoIncorreto = True

especie = config_json['valores']['especie']
tipoNumero = config_json['valores']['tipo_preenchimento']
dataAssinatura = config_json["valores"]["data_assinatura"]
dataAssinatura = config_json["valores"]["data_publicacao"]
orgao = config_json['valores']['orgao']
upag = config_json['valores']['upag']
uorg = config_json['valores']['uorg']
responsavelAssinatura = config_json['valores']['responsavel_assinatura']
cargoResponsavelAssinatura = config_json['valores']['cargo_responsavel']

print()
print('VALORES CONFIGURADOS:')
print()
print('Edição do BGP: ', edicaoBGP)
print('TIpo de assinatura:', tipoAssinatura)
print('Espécie:', especie)
print('Tipo de preenchimento do número: ', tipoNumero)
print('Data de assinatura (emissão): ', dataAssinatura)
print('Data de publicação: ', dataPublicacao)
print('Órgão: ', orgao)
print('UPAG: ', upag)
print('UORG: ', uorg)
print('Responsável pela assinatura: ', responsavelAssinatura)
print('Cargo do responsável pela assinatura: ', cargoResponsavelAssinatura)
print('Para alterá-los, edite config.json e reinicie a aplicação')
print()
if (dadoIncorreto == True):
    print('Há dados inválidos em config.json. Corrija e inicie novamente')
    navegador.quit()
    print('Sessão encerrada')
else:
    print('------------------------------------')
    input('****Aperte ENTER para para iniciar publicação das portarias****')