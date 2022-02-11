from modulos.funcoes import obter_texto_portaria, obter_numero_portaria, formatar_portaria_para_publicar
from modulos.lista_arquivos import listaDeArquivos
import time
from modulos.config import wait
from modulos.config import halfwait
from modulos.config import navegador
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from modulos.publicador.valores_configurados import *

listaPortariasPublicadas = []
listaPortariasNaoPublicadas = []
listaPortariasSemResultado = []

# Verifica os valores de config.json e informa ao usuário


# Inicia o processo de preenchimento e publicação das portarias

for nomeArquivo in listaDeArquivos:

    print()
    print('------------------------------------')
    print()

    textoPortaria = obter_texto_portaria(nomeArquivo)

    numPortaria = obter_numero_portaria(textoPortaria)

    textoPortariaFormatado = formatar_portaria_para_publicar(textoPortaria)

    print(numPortaria, '- Iniciando cadastro da portaria...')

    print(textoPortariaFormatado[0])
    print(textoPortariaFormatado[1])

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    # Tipo de assinatura (manual)

    from modulos.publicador.campos.tipo_assinatura import *

    ##Espécie (portaria)

    from modulos.publicador.campos.especie import *

    # Tipo de preenchimento do número

    from modulos.publicador.campos.tipo_preenchimento import *

    # Tema

    from modulos.publicador.campos.tema import *

    # Assunto

    from modulos.publicador.campos.assunto import *

    # Número do ato

    from modulos.publicador.campos.numero_ato import *

    # Datas

    from modulos.publicador.campos.datas import *

    # Texto do ato/portaria (iframe)

    from modulos.publicador.campos.texto_ato import *

    # Órgãos elaboradores

    from modulos.publicador.campos.orgao_elaborador import *

    # Interessado

    from modulos.publicador.campos.interessado import *

    # ENVIAR PARA PUBLICAÇÃO

    botaoGravarOrgao = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmCadastrarAto:cadastradorDeAtoParaPublicacao:btnEnviarPublicacao"]/span')))

    botaoGravarOrgao.click()

    print(numPortaria, '- Enviando para publicação...')

    modalAguarde = wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@id="j_idt154:j_idt155:ajaxStatusModal"]')))

    try:
        mensagemErro = halfwait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="msgCadastrarAto"]/div[2]/ul/li/span[2]')))
        print(numPortaria, '- ERRO:', mensagemErro.text)
        listaPortariasNaoPublicadas.append(numPortaria)
    except:
        try:
            mensagemSucesso = navegador.find_element(
                By.XPATH, '//*[@id="idFormMsg:idMensagem"]/div/ul/li/span[2]')
            print(numPortaria, '- SUCESSO:', mensagemSucesso.text)
            listaPortariasPublicadas.append(numPortaria)
            time.sleep(0.3)
        except:
            mensagemErro = 'Resultado não identificado! Verifique se a portaria foi publicada.'
            print(numPortaria, '- ERRO:', mensagemErro.text)
            listaPortariasSemResultado.append(numPortaria)

    navegador.get(
        "https://bgp.sigepe.planejamento.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")


# RESULTADO DAS PUBLICAÇÕES

quantidadePortariasPublicadas = len(listaPortariasPublicadas)
quantidadePortariasNaoPublicadas = len(listaPortariasNaoPublicadas)
quantidadePortariasSemResultado = len(listaPortariasSemResultado)

print("------------------")
print()
print("PUBLICAÇÕES CONCLUÍDAS!")

if (quantidadePortariasPublicadas > 0):
    print()
    print("Quantidade de portarias publicadas: " +
          str(quantidadePortariasPublicadas))
    for portaria in listaPortariasPublicadas:
        print(portaria)

if (quantidadePortariasNaoPublicadas > 0):
    print()
    print("Quantidade de portarias não publicadas: " +
          str(quantidadePortariasNaoPublicadas))
    for portaria in listaPortariasNaoPublicadas:
        print(portaria)

if (quantidadePortariasSemResultado > 0):
    print()
    print("Quantidade de portarias sem resultado identificado: " +
          str(quantidadePortariasNaoPublicadas))
    for portaria in quantidadePortariasSemResultado:
        print(portaria)
    print('IMPORTANTE: Verifique se as portarias sem resultado foram cadastradas para publicação no SIGEPE')
