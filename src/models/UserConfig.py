import json
from tkinter import messagebox

class UserConfig:
  def __init__(self):
    pass

  @staticmethod
  def obterConfiguracoesSalvas():
    try:
      json_file = open('config/user/userconfig.json', 'r', encoding="utf-8")
      userConfig = json.load(json_file)
      return userConfig
    except Exception as e:
        messagebox.showerror("Erro ao carregar configurações do usuário", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarConfiguracoes(newUserConfig):
    try:
      json_file = open('config/user/userconfig.json', 'w', encoding="utf-8")
      json.dump(newUserConfig, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
      messagebox.showinfo("Sucesso", "Dados salvos com sucesso")
    except Exception as e:
        messagebox.showerror("Erro ao salvar configurações do usuário", e)
    finally:
      json_file.close()

  @staticmethod
  def obterDelimitadoresSalvos():
    try:
      json_file = open('config/user/delimiters.json', 'r', encoding="utf-8")
      delimiters = json.load(json_file)
      return delimiters
    except Exception as e:
        messagebox.showerror("Erro ao carregar delimitadores", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarDelimitadores(newDelimiters):
    try:
      json_file = open('config/user/delimiters.json', 'w', encoding="utf-8")
      json.dump(newDelimiters, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
    except Exception as e:
        messagebox.showerror("Erro ao salvar delimitadores", e)
    finally:
      json_file.close()

  @staticmethod
  def obterConfigPosPublicacaoSalvos():
    try:
      json_file = open('config/user/afterpublishingconfig.json', 'r', encoding="utf-8")
      afterPublishingConfig = json.load(json_file)
      return afterPublishingConfig
    except Exception as e:
        messagebox.showerror("Erro ao carregar configurações de  pós-publicação", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarConfigPosPublicacao(newConfig):
    try:
      json_file = open('config/user/afterpublishingconfig.json', 'w', encoding="utf-8")
      json.dump(newConfig, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
    except Exception as e:
        messagebox.showerror("Erro ao salvar configurações de pós-publicação", e)
    finally:
      json_file.close()

  @staticmethod
  def obterTermosConteudoRemover():
    try:
      json_file = open('config/user/removefromcontent.json', 'r', encoding="utf-8")
      afterPublishingConfig = json.load(json_file)
      return afterPublishingConfig
    except Exception as e:
        messagebox.showerror("Erro ao carregar termos para remoção do conteúdo", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarTermosConteudoRemover(newConfig):
    try:
      json_file = open('config/user/removefromcontent.json', 'w', encoding="utf-8")
      json.dump(newConfig, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
    except Exception as e:
        messagebox.showerror("Erro ao salvar termos para remoção do conteúdo", e)
    finally:
      json_file.close()

  @staticmethod
  def obterAutoTemasAssuntos():
    try:
      json_file = open('config/user/autotheme.json', 'r', encoding="utf-8")
      afterPublishingConfig = json.load(json_file)
      return afterPublishingConfig
    except Exception as e:
        messagebox.showerror("Erro ao carregar termos para remoção do conteúdo", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarAutoTemasAssuntos(newConfig):
    try:
      json_file = open('config/user/autotheme.json', 'w', encoding="utf-8")
      json.dump(newConfig, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
    except Exception as e:
        messagebox.showerror("Erro ao salvar termos para remoção do conteúdo", e)
    finally:
      json_file.close()

  @staticmethod
  def obterNavegador():
    try:
      json_file = open('config/user/browser.json', 'r', encoding="utf-8")
      browser = json.load(json_file)
      return browser["browser"]
    except Exception as e:
        messagebox.showerror("Erro ao identificar navegador escolhido pelo usuário", e)
    finally:
      json_file.close()
  
  @staticmethod
  def salvarNavegador(newConfig):
    try:
      json_file = open('config/user/browser.json', 'w', encoding="utf-8")
      json.dump(newConfig, json_file, ensure_ascii=False, indent=4, separators=(',',':'))
    except Exception as e:
        messagebox.showerror("Erro ao salvar navegador escolhido pelo usuário", e)
    finally:
      json_file.close()