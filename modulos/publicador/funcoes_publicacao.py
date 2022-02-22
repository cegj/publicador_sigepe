from modulos.config import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modulos.funcoes import obter_tema
from modulos.funcoes import aguardar_loading

# Inicia o processo de preenchimento e publicação das portarias


def preencher(textoPortaria, numPortaria, textoPortariaFormatado):

    print(numPortaria, '- Iniciando preenchimento da portaria...')

    print(textoPortariaFormatado[0])
    print(textoPortariaFormatado[1])

    aguardar_loading()

    # Tipo de assinatura (manual)

    from modulos.publicador.campos.tipo_assinatura import preencher_tipo_assinatura

    preencher_tipo_assinatura(numPortaria)

    ##Espécie (portaria)

    from modulos.publicador.campos.especie import preencher_especie

    preencher_especie(numPortaria)

    # Tipo de preenchimento do número

    from modulos.publicador.campos.tipo_numero import preencher_tipo_numero

    preencher_tipo_numero(numPortaria)

    # Tema

    from modulos.publicador.campos.tema import preencher_tema

    if (obter_tema(textoPortariaFormatado[1])):
        temaAssunto = obter_tema(textoPortariaFormatado[1])
    else:
        print('!!!TEMA NÃO IDENTIFICADO!!!')

    preencher_tema(temaAssunto, numPortaria)

    # Assunto

    from modulos.publicador.campos.assunto import preencher_assunto

    preencher_assunto(temaAssunto, numPortaria)
        
    # Número do ato

    from modulos.publicador.campos.numero_ato import preencher_numero_ato

    preencher_numero_ato(numPortaria)

    # Datas

    from modulos.publicador.campos.datas import preencher_data_assinatura, preencher_data_publicacao

    preencher_data_assinatura(numPortaria)
    preencher_data_publicacao(numPortaria)

    # Texto do ato/portaria (iframe)

    from modulos.publicador.campos.texto_ato import preencher_texto_ato

    preencher_texto_ato(textoPortariaFormatado, numPortaria)

    # Órgãos elaboradores

    from modulos.publicador.campos.orgao_elaborador import preencher_orgao_elaborador

    preencher_orgao_elaborador(numPortaria)

    # Interessado

    from modulos.publicador.campos.interessado import preencher_interessado

    preencher_interessado(textoPortaria, numPortaria)
