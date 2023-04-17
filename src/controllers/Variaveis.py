import json
from tkinter import messagebox
import datetime
from datetime import timedelta
from helpers import dateToBrFormat as dtbf
from copy import copy
import ast

class Variaveis:
  @staticmethod
  def obterValorVariaveis(config):
    variaveis = {}

    today = datetime.date.today()  # Hoje no formato ANSI AAAA-MM-DD
    tomorrow = today + timedelta(1)  # Amanhã no formato ANSI AAAA-MM-DD
    day = today.day
    month = today.month
    year = today.year

    variaveis["hoje."] = str(dtbf.dateToBrFormat(today, '.'))
    variaveis["hoje/"] = str(dtbf.dateToBrFormat(today, '/'))
    variaveis["hoje-"] = str(dtbf.dateToBrFormat(today, '-'))

    if (tomorrow.weekday() == 5):
        variaveis["proximo_dia_util."] = str(dtbf.dateToBrFormat(tomorrow + timedelta(2), '.'))
    elif (tomorrow.weekday() == 6):
        variaveis["proximo_dia_util."] = str(dtbf.dateToBrFormat(tomorrow + timedelta(1), '.'))
    else:
        variaveis["proximo_dia_util."] = str(dtbf.dateToBrFormat(tomorrow, '.'))

    if (tomorrow.weekday() == 5):
        variaveis["proximo_dia_util/"] = str(dtbf.dateToBrFormat(tomorrow + timedelta(2), '/'))
    elif (tomorrow.weekday() == 6):
        variaveis["proximo_dia_util/"] = str(dtbf.dateToBrFormat(tomorrow + timedelta(1), '/'))
    else:
        variaveis["proximo_dia_util/"] = str(dtbf.dateToBrFormat(tomorrow, '/'))

    if (tomorrow.weekday() == 5):
        variaveis["proximo_dia_util-"] = str(dtbf.dateToBrFormat(tomorrow + timedelta(2), '-'))
    elif (tomorrow.weekday() == 6):
        variaveis["proximo_dia_util-"] = str(dtbf.dateToBrFormat(tomorrow + timedelta(1), '-'))
    else:
        variaveis["proximo_dia_util-"] = str(dtbf.dateToBrFormat(tomorrow, '-'))

    # [hoje_dia] / [hoje_mes] / [hoje_ano]
    variaveis["hoje_dia"] = str(day)
    variaveis["hoje_mes"] = str(month)
    variaveis["hoje_ano"] = str(year)

    if day < 10:
      variaveis["hoje_dia0"] = '0' + str(day)
    else:
      variaveis["hoje_dia0"] = str(day)
    if month < 10:
      variaveis["hoje_mes0"] = '0' + str(month)
    else:
      variaveis["hoje_mes0"] = str(month)

    mesesExtenso = {
        "1": 'janeiro',
        "2": "fevereiro",
        "3": "marco",
        "4": "abril",
        "5": "maio",
        "6": "junho",
        "7": "julho",
        "8": "agosto",
        "9": "setembro",
        "10": "outubro",
        "11": "novembro",
        "12": "dezembro"
    }

    for key, value in mesesExtenso.items():
      if (key == str(month)):
          variaveis["hoje_mes_extenso"] = value
          break

    return variaveis
  
  @staticmethod
  def atribuirValorVariaveis(jsondata):
    try:
      variaveis = Variaveis.obterValorVariaveis(jsondata)
      jsonAsStr = json.dumps(jsondata, ensure_ascii=False)
      jsonAsStr = jsonAsStr.replace("[hoje.]", variaveis["hoje."])
      jsonAsStr = jsonAsStr.replace("[hoje/]", variaveis["hoje/"])
      jsonAsStr = jsonAsStr.replace("[hoje-]", variaveis["hoje-"])
      jsonAsStr = jsonAsStr.replace("[proximo_dia_util.]", variaveis["proximo_dia_util."])
      jsonAsStr = jsonAsStr.replace("[proximo_dia_util/]", variaveis["proximo_dia_util/"])
      jsonAsStr = jsonAsStr.replace("[proximo_dia_util-]", variaveis["proximo_dia_util-"])
      jsonAsStr = jsonAsStr.replace("[hoje_dia]", variaveis["hoje_dia"])
      jsonAsStr = jsonAsStr.replace("[hoje_dia0]", variaveis["hoje_dia0"])
      jsonAsStr = jsonAsStr.replace("[hoje_mes]", variaveis["hoje_mes"])
      jsonAsStr = jsonAsStr.replace("[hoje_mes0]", variaveis["hoje_mes0"])
      jsonAsStr = jsonAsStr.replace("[hoje_mes_extenso]", variaveis["hoje_mes_extenso"])
      jsonAsStr = jsonAsStr.replace("[hoje_ano]", variaveis["hoje_ano"])
      strAsJson = json.loads(jsonAsStr)
      return strAsJson
    except Exception as e:
      messagebox.showerror("Erro ao definir valor das variáveis", e)
      return jsondata






