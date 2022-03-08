class Utilidades:

    import datetime
    from datetime import timedelta

    today = datetime.date.today() #Hoje no formato ANSI AAAA-MM-DD
    tomorrow = today + timedelta(1) #Amanhã no formato ANSI AAAA-MM-DD

    def ajustarData(data, separador):
        dataArray = str(data).split('-')
        dataAjustada = dataArray[2] + separador + dataArray[1] + separador + dataArray[0]
        data = str(dataAjustada)
        return data


    def limparQuebrasDeLinha(string):
        string = string.replace("\n", "") # Apagar quebras de linha
        return string