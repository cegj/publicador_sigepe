from models import AppConfig as ac
from tkinter import messagebox
import urllib.request, json 
import webbrowser
import os

class CheckUpdates():
  @staticmethod
  def checkRelease():
    currentVersion = ac.AppConfig.versao
    try:
      urls = ac.AppConfig.urls
      with urllib.request.urlopen(urls['lastRelease']) as url:
        lastRelease = json.load(url)
        if (currentVersion != lastRelease["version"]):
          answer = messagebox.askyesno("Nova versão disponível", f"Existe uma nova versão do Publicador Sigepe disponível ({lastRelease['version']}). Deseja baixar o instalador desta nova versão?")
          if (answer == True):
            webbrowser.open_new_tab(lastRelease["url"])
            messagebox.showinfo("Sucesso", "O instalador da nova versão do Publicador Sigepe está sendo baixado pelo seu navegador. Após a conclusão, execute o instalador para substituir a versão atual pela nova.\n\nAo instalar uma nova versão, suas configurações de usuário serão perdidas. Para mais informações sobre como fazer uma cópia das suas configurações na versão atual e importar na nova versão, consulte a Ajuda (em Configurações).")
    except Exception as e:
      messagebox.showerror("Ocorreu um erro ao verificar se há novas versões", e)      

  def checkXpaths():
    currentVersion = ac.AppConfig.xpaths["version"]
    try:
      urls = ac.AppConfig.urls
      with urllib.request.urlopen(f"{urls['configRepo']}/app/xpaths.json") as url:
        remoteXpaths = json.load(url)
        if (remoteXpaths["version"] > currentVersion):
          dest = os.path.normpath(os.path.join(os.path.expanduser('~'), f"AppData/Local/Programs/Publicador Sigepe/config/app/xpaths.json"))
          string = json.dumps(remoteXpaths, ensure_ascii=False, indent=4, separators=(',',':'))
          jsonFile = open(dest, "w", encoding="utf-8")
          jsonFile.write(string)
          jsonFile.close()
          answer = messagebox.showinfo("Atualização realizada", f"Uma atualização dos identificadores de elementos do Sigepe foi realizada automaticamente.")
    except Exception as e:
      messagebox.showerror("Erro em atualização de identificadores do Sigepe", e)      

  def checkUrls():
    currentVersion = ac.AppConfig.urls["version"]
    try:
      urls = ac.AppConfig.urls
      with urllib.request.urlopen(f"{urls['configRepo']}/app/urls.json") as url:
        remoteUrls = json.load(url)
        if (remoteUrls["version"] > currentVersion):
          dest = os.path.normpath(os.path.join(os.path.expanduser('~'), f"AppData/Local/Programs/Publicador Sigepe/config/app/urls.json"))
          string = json.dumps(remoteUrls, ensure_ascii=False, indent=4, separators=(',',':'))
          jsonFile = open(dest, "w", encoding="utf-8")
          jsonFile.write(string)
          jsonFile.close()
          answer = messagebox.showinfo("Atualização realizada", f"Uma atualização de URLs foi realizada automaticamente.")
    except Exception as e:
      messagebox.showerror("Erro em atualização de URLs", e)     

  def checkErrors():
    currentVersion = ac.AppConfig.errors["version"]
    try:
      urls = ac.AppConfig.urls
      with urllib.request.urlopen(f"{urls['configRepo']}/app/errors.json") as url:
        remoteErrors = json.load(url)
        if (remoteErrors["version"] > currentVersion):
          dest = os.path.normpath(os.path.join(os.path.expanduser('~'), f"AppData/Local/Programs/Publicador Sigepe/config/app/errors.json"))
          string = json.dumps(remoteErrors, ensure_ascii=False, indent=4, separators=(',',':'))
          jsonFile = open(dest, "w", encoding="utf-8")
          jsonFile.write(string)
          jsonFile.close()
          answer = messagebox.showinfo("Atualização realizada", f"Uma atualização de lista de erros foi realizada automaticamente.")
    except Exception as e:
      messagebox.showerror("Erro em atualização de lista de erros", e)

  def checkWebdriverSettings():
    currentVersion = ac.AppConfig.webdriverSettings["version"]
    try:
      urls = ac.AppConfig.urls
      with urllib.request.urlopen(f"{urls['configRepo']}/app/webdriversettings.json") as url:
        remoteWebdriverSettings = json.load(url)
        if (remoteWebdriverSettings["version"] > currentVersion):
          dest = os.path.normpath(os.path.join(os.path.expanduser('~'), f"AppData/Local/Programs/Publicador Sigepe/config/app/webdriversettings.json"))
          string = json.dumps(remoteWebdriverSettings, ensure_ascii=False, indent=4, separators=(',',':'))
          jsonFile = open(dest, "w", encoding="utf-8")
          jsonFile.write(string)
          jsonFile.close()
          answer = messagebox.showinfo("Atualização realizada", f"Uma atualização de configurações do navegador foi realizada automaticamente.")
    except Exception as e:
      messagebox.showerror("Erro em atualização de configurações do navegador", e)          