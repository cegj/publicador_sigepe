print('----------------------------------')
print('----------------------------------')
print('PUBLICADOR DE PORTARIAS NO SIGEPE')
print('----------------------------------')
print('----------------------------------')
print()
print('*****Por Carlos E. Gaspar Jr.*****')
print('******** github.com/cegj/ ********')
print()

print()
print('------------------------------------')
print()
print('Realizando configurações iniciais...')

from modulos.config import *

print('Configurações iniciais concluídas')

print()
print('------------------------------------')
print()

from modulos.lista_arquivos import diretorioPortarias, listaDeArquivos

print('O diretório de portarias é: ', diretorioPortarias)
print('Para alterá-lo, edite config.json')
print()
print('Lista de arquivos no diretório:')
for arquivo in listaDeArquivos:
  if ".rtf" in arquivo:
    print(arquivo)
  else:
    print('ATENÇÃO: Formato incorreto, converta para RTF antes de continuar: ' + arquivo)
print()
print('Quantidade de arquivos válidos no diretório: ', len(listaDeArquivos), 'arquivos')
print()
input('**Aperte ENTER para prosseguir**')
print()
print('------------------------------------')
print()

## Fazer login no SIGEPE

from modulos.login_sigepe import *

print()
print('------------------------------------')
print()

## Preencher formulários com dados dos arquivos e publicar

from modulos.publicador.publicador import *
        
navegador.quit()