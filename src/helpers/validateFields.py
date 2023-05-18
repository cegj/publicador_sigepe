from tkinter import messagebox

#EDIÇÃO: obrigatório. se NORMAL, DATA PUBLICAÇÃO obrigatório; se EXTRAORDINÁRIA, DATA PUBLICAÇÃO ignorado.
#TIPO_ASSINATURA: obrigatório. se DIGITAL, DATA ASSINATURA ignorado; se MANUAL, DATA ASSINATURA obrigatório.
#ESPECIE: obrigatório
#TEMA: obrigatório (verificar tipo de preenchimento)
#ASSUNTO: obrigatório (verificar tipo de preenchimento)
#TIPO_NUMERO: obrigatório. se AUTOMÁTICO ou SEM NÚMERO, NÚMERO DO ATO ignorado; se MANUAL, NÚMERO DO ATO obrigatório. Obs.: número do ato não é campo, é obtido do conteúdo.
#ORGAO, UPAG, UORG: obrigatório
#RESPONSÁVEL ASSINATURA, CARGO: obrigatório

labels = {
  "edicao_bgp":"Edição do boletim",
  "tipo_assinatura":"Tipo de assinatura",
  "especie":"Espécie",
  "tema":"Tema",
  "assunto":"Assunto",
  "tipo_preenchimento":"Tipo de número",
  "data_assinatura":"Data de assinatura",
  "data_publicacao":"Data de publicação",
  "orgao":"Órgão",
  "upag":"UPAG",
  "uorg":"UORG",
  "responsavel_assinatura":"Responsável pela assinatura",
  "cargo_responsavel":"Cargo do responsável"
}

required = ["edicao_bgp", "tipo_assinatura", "especie", "tipo_preenchimento", "orgao", "upag", "uorg", "responsavel_assinatura", "cargo_responsavel"]

conditionallyRequired = [
  ["data_publicacao", "valores_sigepe//edicao_bgp", "Normal"],
  ["data_assinatura", "valores_sigepe//tipo_assinatura", "Manual"],
  ["tema", "tipo_tema_assunto", "Selecionar manualmente"],
  ["assunto", "tipo_tema_assunto", "Selecionar manualmente"]
]

def validateFields(userConfig):
  failed = []
  for key, value in userConfig["valores_sigepe"].items():
    for field in required:
      if (field == key and value == ""): failed.append(field)
    for field in conditionallyRequired:
      if (field[0] == key and value == ""):
        keys = field[1].split("//")
        if (len(keys) == 2):
          if(userConfig[keys[0]][keys[1]] == field[2]): failed.append(field[0])
        else:
          if (userConfig[keys[0]] == field[2]): failed.append(field[0])        

  if (len(failed) > 0):
    msg = "Os seguintes dados de publicação devem ser preenchidos:\n"
    for field in failed:
      msg += f"\n- {labels[field]}"
    messagebox.showerror("Campos obrigatórios não preenchidos", msg)
    return False
  return True

#   {
#     "habilitacao":{
#         "inicial":""
#     },
#     "tipo_tema_assunto":"",
#     "acao":"",
#     "valores_sigepe":{
#         "edicao_bgp":"",
#         "tipo_assinatura":"",
#         "especie":"",
#         "tema":"",
#         "assunto":"",
#         "tipo_preenchimento":"",
#         "data_assinatura":"",
#         "data_publicacao":"",
#         "orgao":"",
#         "upag":"",
#         "uorg":"",
#         "responsavel_assinatura":"",
#         "cargo_responsavel":""
#     }
# }