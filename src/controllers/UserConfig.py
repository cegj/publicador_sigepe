import json
from tkinter import messagebox

class UserConfig:
  def __init__(self):
    pass

  @staticmethod
  def obterConfiguracoesSalvas():
    try:
      json_file = open('config/userconfig.json', 'r', encoding="utf-8")
      userConfig = json.load(json_file)
      return userConfig
    except Exception as e:
        messagebox.showerror("Erro ao carregar configurações do usuário", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarConfiguracoes(newUserConfig):
    try:
      json_file = open('config/userconfig.json', 'w', encoding="utf-8")
      json.dump(newUserConfig, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
      messagebox.showinfo("Sucesso", "Configurações salvas com sucesso")
    except Exception as e:
        messagebox.showerror("Erro ao salvar configurações do usuário", e)
    finally:
      json_file.close()

  @staticmethod
  def obterDelimitadoresSalvos():
    try:
      json_file = open('config/delimiters.json', 'r', encoding="utf-8")
      delimiters = json.load(json_file)
      return delimiters
    except Exception as e:
        messagebox.showerror("Erro ao carregar delimitadores", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarDelimitadores(newDelimiters):
    try:
      json_file = open('config/delimiters.json', 'w', encoding="utf-8")
      json.dump(newDelimiters, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
    except Exception as e:
        messagebox.showerror("Erro ao salvar delimitadores", e)
    finally:
      json_file.close()

  @staticmethod
  def obterConfigPosPublicacaoSalvos():
    try:
      json_file = open('config/afterpublishingconfig.json', 'r', encoding="utf-8")
      afterPublishingConfig = json.load(json_file)
      return afterPublishingConfig
    except Exception as e:
        messagebox.showerror("Erro ao carregar configurações de  pós-publicação", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarConfigPosPublicacao(newConfig):
    try:
      json_file = open('config/afterpublishingconfig.json', 'w', encoding="utf-8")
      json.dump(newConfig, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
    except Exception as e:
        messagebox.showerror("Erro ao salvar configurações de pós-publicação", e)
    finally:
      json_file.close()

  @staticmethod
  def obterTermosConteudoRemover():
    try:
      json_file = open('config/removefromcontent.json', 'r', encoding="utf-8")
      afterPublishingConfig = json.load(json_file)
      return afterPublishingConfig
    except Exception as e:
        messagebox.showerror("Erro ao carregar termos para remoção do conteúdo", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarTermosConteudoRemover(newConfig):
    try:
      json_file = open('config/removefromcontent.json', 'w', encoding="utf-8")
      json.dump(newConfig, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
    except Exception as e:
        messagebox.showerror("Erro ao salvar termos para remoção do conteúdo", e)
    finally:
      json_file.close()

  @staticmethod
  def obterAutoTemasAssuntos():
    try:
      json_file = open('config/autotheme.json', 'r', encoding="utf-8")
      afterPublishingConfig = json.load(json_file)
      return afterPublishingConfig
    except Exception as e:
        messagebox.showerror("Erro ao carregar termos para remoção do conteúdo", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarAutoTemasAssuntos(newConfig):
    try:
      json_file = open('config/autotheme.json', 'w', encoding="utf-8")
      json.dump(newConfig, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
    except Exception as e:
        messagebox.showerror("Erro ao salvar termos para remoção do conteúdo", e)
    finally:
      json_file.close()