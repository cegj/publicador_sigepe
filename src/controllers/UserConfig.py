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
        messagebox.showerror("Erro ao abrir configurações do usuário", e)
    finally:
      user_config_file.close()

    # with open('config/userconfig.json', 'r', encoding="utf-8") as user_config_file:
    #   userConfig = json.load(user_config_file)
    #   return userConfig
  
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


    # with open('config/userconfig.json', 'r', encoding="utf-8") as user_config_file: 
    #   with tempfile.NamedTemporaryFile('w', delete=False) as out:
    #     out = newUserConfig
    #     json.dump(user_config_file, out, ensure_ascii=False, indent=4, separators=(',',':'))
    #     shutil.move(out.name, 'config/userconfig2.json')