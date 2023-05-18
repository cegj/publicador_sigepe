import json
from tkinter import messagebox

class AppConfig:
  @staticmethod
  def obterXpaths():
    try:
      json_file = open('config/app/xpaths.json', 'r', encoding="utf-8")
      content = json.load(json_file)
      return content
    except Exception as e:
        messagebox.showerror("Erro ao carregar identificadores dos elementos do Sigepe (xpaths)", e)
    finally:
      json_file.close()

  @staticmethod
  def obterUrls():
    try:
      json_file = open('config/app/urls.json', 'r', encoding="utf-8")
      content = json.load(json_file)
      return content
    except Exception as e:
        messagebox.showerror("Erro ao carregar endereços das páginas do Sigepe (URLs)", e)
    finally:
      json_file.close()

  @staticmethod
  def obterWebdriverSettings():
    try:
      json_file = open('config/app/webdriversettings.json', 'r', encoding="utf-8")
      content = json.load(json_file)
      return content
    except Exception as e:
        messagebox.showerror("Erro ao carregar endereços das páginas do Sigepe (URLs)", e)
    finally:
      json_file.close()

  nome = "Publicador Sigepe"
  versao = "v1.1.1"
  fontes = {
    "titulo": ("Segoe UI", "13", "bold"),
    "normal": ("Segoe UI", "12"), "botao": ("Segoe UI", "10"),
    "log": ("Calibri", "11"),
    "botao": ("Segoe UI", "10")
  }
  pad = {"x": 20, "y": 20}
  xpaths = obterXpaths.__func__()
  urls = obterUrls.__func__()
  webdriverSettings = obterWebdriverSettings.__func__()
  