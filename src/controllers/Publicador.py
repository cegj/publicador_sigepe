from tkinter import *
import appConfig
from controllers import Variaveis as v
from controllers import UserConfig as uc
from striprtf.striprtf import rtf_to_text
from tkinter import messagebox
import os
from threading import Thread
import time

class Publicador:
  def __init__(self, publicacao):
    self.publicacao = publicacao
    self.files = publicacao.files
    self.config = v.Variaveis.atribuirValorVariaveis(self.publicacao.config)
    self.delimitadores = v.Variaveis.atribuirValorVariaveis(uc.UserConfig.obterDelimitadoresSalvos())
    self.pospublicacao = v.Variaveis.atribuirValorVariaveis(uc.UserConfig.obterConfigPosPublicacaoSalvos())
    t = Thread(target=self.publicar)
    t.start()

  def publicar(self):
    for file in self.files:
      completeFiletext = self.obterTextoDocumento(file)
      filetext = self.removerPrimeiraLinha(completeFiletext)
      self.publicacao.insertFileText(filetext)
      time.sleep(2)

  def obterTextoDocumento(self, file):
    try:
      rtfdocument = file.read()
      text = rtf_to_text(rtfdocument).strip()
      return text
    except Exception as e:
      messagebox.showerror("Erro ao carregar conteúdo do documento", e)
      document.close()

  def obterDoTexto(self, delimiterkey, filetext):
    try:
      a = filetext.split(self.delimitadores[f"{delimiterkey}"][0], 1)
      b = a[1].split(self.delimitadores[f"{delimiterkey}"][1], 1)
      data = b[0]
      return data
    except Exception as e:
      messagebox.showerror("Erro ao obter informação do documento", f"Informação: {delimiterkey}. Erro: {e}")

  def removerPrimeiraLinha(self, filetext):
    try:  
      result = filetext.split("\n",2)[2]
      return result
    except Exception as e:
      messagebox.showerror("Erro ao remover primeira linha do conteúdo do documento", e)
