from models import AppConfig as ac
from tkinter import messagebox
import urllib.request, json 
import webbrowser

class CheckUpdates():
  @staticmethod
  def checkRelease():
    currentVersion = ac.AppConfig.versao
    try:
      json_file = open('config/app/urls.json', 'r', encoding="utf-8")
      urls = json.load(json_file)
      json_file.close()
      with urllib.request.urlopen(urls['lastRelease']) as url:
        lastRelease = json.load(url)
        if (currentVersion != lastRelease["version"]):
          answer = messagebox.askyesno("Nova versão disponível", f"Existe uma nova versão do Publicador Sigepe disponível ({lastRelease['version']}). Deseja baixar o instalador desta nova versão?")
          if (answer == True):
            webbrowser.open_new_tab(lastRelease["url"])
            messagebox.showinfo("Sucesso", "O instalador da nova versão do Publicador Sigepe está sendo baixado pelo seu navegador. Após a conclusão, execute o instalador para substituir a versão atual pela nova.\n\nAo instalar uma nova versão, suas configurações de usuário serão perdidas. Para mais informações sobre como fazer uma cópia das suas configurações na versão atual e importar na nova versão, consulte a Ajuda (em Configurações).")
    except Exception as e:
      messagebox.showerror("Ocorreu um erro ao buscar atualizações", e)      
