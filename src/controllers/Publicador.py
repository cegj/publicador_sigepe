from tkinter import *
import appConfig
from controllers import Variaveis as v
from controllers import UserConfig as uc
from striprtf.striprtf import rtf_to_text
from tkinter import messagebox
import os
from threading import Thread
import time
from helpers import goTo as gt
from controllers.publicador import EdicaoBoletim as eb
from controllers.publicador import TipoAssinatura as ta
from controllers.publicador import TipoNumero as tn
from controllers.publicador import Tema as t
from controllers.publicador import Assunto as a
from controllers.publicador import Numero as n
from controllers.publicador import DataAssinatura as da
from controllers.publicador import DataPublicacao as dp
from controllers.publicador import Especie as e
from controllers.publicador import ConteudoDocumento as cd
from controllers.publicador import OrgaoElaborador as oe

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
      gt.goTo("https://bgp.sigepe.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")

      completeFiletext = self.obterTextoDocumento(file)
      filetext = self.removerPrimeiraLinha(completeFiletext)
      self.publicacao.insertFileText(filetext)

      self.publicacao.insertLog("Iniciando publicação de documento", "a")
      numeroDocumento = self.obterDoTexto("numero_documento", completeFiletext)
      if (numeroDocumento != ""):
        self.publicacao.insertLog("Número do documento identificado", "", numeroDocumento)
      else:
        self.publicacao.insertLog("Não foi localizado um número no texto do documento", "a", numeroDocumento)
      matriculaSiape = self.obterDoTexto("matricula_siape", completeFiletext)
      if (matriculaSiape != ""):
        self.publicacao.insertLog(f"Matrícula SIAPE identificada: {matriculaSiape}", "n", numeroDocumento)
      else:
        self.publicacao.insertLog("Não foi localizada uma matrícula SIAPE no texto do documento", "a")

      edicaoBoletimResult = eb.EdicaoBoletim.preencher(self.config["valores_sigepe"]["edicao_bgp"])
      self.sendLogToInterface(edicaoBoletimResult, numeroDocumento)

      tipoAssinaturaResult = ta.TipoAssinatura.preencher(self.config["valores_sigepe"]["tipo_assinatura"])
      self.sendLogToInterface(tipoAssinaturaResult, numeroDocumento)

      tipoNumeroResult = tn.TipoNumero.preencher(self.config["valores_sigepe"]["tipo_preenchimento"])
      self.sendLogToInterface(tipoNumeroResult, numeroDocumento)

      temaResult = t.Tema.preencher(self.config["valores_sigepe"]["tema"])
      self.sendLogToInterface(temaResult, numeroDocumento)

      assuntoResult = a.Assunto.preencher()
      self.sendLogToInterface(assuntoResult, numeroDocumento)

      if (self.config["valores_sigepe"]["tipo_preenchimento"] == "Manual"):
        numeroResult = n.Numero.preencher(numeroDocumento)
        self.sendLogToInterface(numeroResult, numeroDocumento)
      else:
        pass

      if (self.config["valores_sigepe"]["tipo_preenchimento"] == "Manual"):
        dataAssinaturaResult = da.DataAssinatura.preencher(self.config["valores_sigepe"]["data_assinatura"])
        self.sendLogToInterface(dataAssinaturaResult, numeroDocumento)
      else:
        pass

      if (self.config["valores_sigepe"]["edicao_bgp"] == "Normal"):
        dataPublicacaoResult = dp.DataPublicacao.preencher(self.config["valores_sigepe"]["data_assinatura"])
        self.sendLogToInterface(dataPublicacaoResult, numeroDocumento)
      else:
        pass

      especieResult = e.Especie.preencher(self.config["valores_sigepe"]["especie"])
      self.sendLogToInterface(especieResult, numeroDocumento)

      textoDocumentoResult = cd.ConteudoDocumento.preencher(filetext)
      self.sendLogToInterface(textoDocumentoResult, numeroDocumento)

      orgaoElaboradorResult = oe.OrgaoElaborador.preencher(
        self.config["valores_sigepe"]["upag"],
        self.config["valores_sigepe"]["uorg"],
        self.config["valores_sigepe"]["responsavel_assinatura"],
        self.config["valores_sigepe"]["cargo_responsavel"]
      )
      self.sendLogToInterface(orgaoElaboradorResult, numeroDocumento)

      time.sleep(10)

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

  def sendLogToInterface(self, result, docnumber = ""):
    self.publicacao.insertLog(result["log"], result["type"], docnumber)