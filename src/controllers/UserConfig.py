import json
import shutil
import tempfile
from tkinter import messagebox

class UserConfig:
  def __init__(self):
    pass

  @staticmethod
  def obterConfiguracoesSalvas():
    try:
      user_config_file = open('config/userconfig.json', 'r', encoding="utf-8")
      userConfig = json.load(user_config_file)
      return userConfig
    except Exception as e:
        messagebox.showerror("Erro ao carregar configurações do usuário", e)
    finally:
      user_config_file.close()
  
  @staticmethod
  def salvarConfiguracoes(newUserConfig):
    try:
      user_config_file = open('config/userconfig.json', 'w', encoding="utf-8")
      json.dump(newUserConfig, user_config_file, ensure_ascii=False, indent=4, separators=(',',':'))
      messagebox.showinfo("Sucesso", "Configurações salvas com sucesso")
    except Exception as e:
        messagebox.showerror("Erro ao salvar configurações do usuário", e)
    finally:
      user_config_file.close()

  @staticmethod
  def obterDelimitadoresSalvos():
    try:
      delimiters_file = open('config/delimiters.json', 'r', encoding="utf-8")
      delimiters = json.load(delimiters_file)
      return delimiters
    except Exception as e:
        messagebox.showerror("Erro ao carregar delimitadores", e)
    finally:
      delimiters_file.close()
  
  @staticmethod
  def salvarDelimitadores(newDelimiters):
    try:
      delimiters_file = open('config/delimiters.json', 'w', encoding="utf-8")
      json.dump(newDelimiters, delimiters_file, ensure_ascii=False, indent=4, separators=(',',':'))
      messagebox.showinfo("Sucesso", "Configurações salvas com sucesso")
    except Exception as e:
        messagebox.showerror("Erro ao salvar delimitadores", e)
    finally:
      delimiters_file.close()