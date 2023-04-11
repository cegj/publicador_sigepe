def dateToBrFormat(data, separador):
    dataArray = str(data).split('-')
    dataAjustada = dataArray[2] + separador + \
        dataArray[1] + separador + dataArray[0]
    return str(dataAjustada)
