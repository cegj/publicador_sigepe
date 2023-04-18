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
from helpers import checkExistsByXpath as cebx
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
from controllers.publicador import Interessado as i
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from Webdriver import wait
from appXpaths import xpaths
from helpers import waitForLoading as wfl
import re

class Publicador:
  def __init__(self, publicacao):
    self.publicacao = publicacao
    self.files = publicacao.files
    self.config = v.Variaveis.atribuirValorVariaveis(self.publicacao.config)
    self.delimitadores = v.Variaveis.atribuirValorVariaveis(uc.UserConfig.obterDelimitadoresSalvos())
    self.pospublicacao = v.Variaveis.atribuirValorVariaveis(uc.UserConfig.obterConfigPosPublicacaoSalvos())
    self.termosremover = v.Variaveis.atribuirValorVariaveis(uc.UserConfig.obterTermosConteudoRemover())
    self.resultados = {"sucesso": [], "erro": [], "indefinido": []}
    t = Thread(target=self.publicar)
    t.start()

  def publicar(self):
    for file in self.files:
      gt.goTo("https://bgp.sigepe.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")

      filename = os.path.basename(file.name)
      completeFiletext = self.obterTextoDocumento(file)
      textBeforeRemoveTerms = self.removerPrimeiraLinha(completeFiletext)
      filetext = self.removerTermosConteudo(textBeforeRemoveTerms)
      filetext = Publicador.stripText(filetext)
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
      self.handleResult(edicaoBoletimResult, numeroDocumento)

      tipoAssinaturaResult = ta.TipoAssinatura.preencher(self.config["valores_sigepe"]["tipo_assinatura"])
      self.handleResult(tipoAssinaturaResult, numeroDocumento)

      tipoNumeroResult = tn.TipoNumero.preencher(self.config["valores_sigepe"]["tipo_preenchimento"])
      self.handleResult(tipoNumeroResult, numeroDocumento)

      temaResult = t.Tema.preencher(self.config["valores_sigepe"]["tema"])
      self.handleResult(temaResult, numeroDocumento)

      assuntoResult = a.Assunto.preencher()
      self.handleResult(assuntoResult, numeroDocumento)

      if (self.config["valores_sigepe"]["tipo_preenchimento"] == "Manual"):
        numeroResult = n.Numero.preencher(numeroDocumento)
        self.handleResult(numeroResult, numeroDocumento)
      else:
        pass

      if (self.config["valores_sigepe"]["tipo_preenchimento"] == "Manual"):
        dataAssinaturaResult = da.DataAssinatura.preencher(self.config["valores_sigepe"]["data_assinatura"])
        self.handleResult(dataAssinaturaResult, numeroDocumento)
      else:
        pass

      if (self.config["valores_sigepe"]["edicao_bgp"] == "Normal"):
        dataPublicacaoResult = dp.DataPublicacao.preencher(self.config["valores_sigepe"]["data_publicacao"])
        self.handleResult(dataPublicacaoResult, numeroDocumento)
      else:
        pass

      especieResult = e.Especie.preencher(self.config["valores_sigepe"]["especie"])
      self.handleResult(especieResult, numeroDocumento)

      textoDocumentoResult = cd.ConteudoDocumento.preencher(filetext)
      self.handleResult(textoDocumentoResult, numeroDocumento)

      self.publicacao.insertLog("Selecionando órgão elaborador...", "n", numeroDocumento)
      orgaoElaboradorResult = oe.OrgaoElaborador.preencher(
        self.config["valores_sigepe"]["orgao"],
        self.config["valores_sigepe"]["upag"],
        self.config["valores_sigepe"]["uorg"],
        self.config["valores_sigepe"]["responsavel_assinatura"],
        self.config["valores_sigepe"]["cargo_responsavel"]
      )
      self.handleResult(orgaoElaboradorResult, numeroDocumento)

      self.publicacao.insertLog("Selecionando interessado...", "n", numeroDocumento)
      interessadoResult = i.Interessado.preencher(matriculaSiape)
      self.handleResult(interessadoResult, numeroDocumento)

      publicacaoResult = self.enviarParaPublicacao(numeroDocumento, filename)
      self.handleResult(publicacaoResult, numeroDocumento)

  def obterTextoDocumento(self, file):
    try:
      rtfdocument = file.read()
      text = rtf_to_text(rtfdocument)
      return text
    except Exception as e:
      messagebox.showerror("Erro ao carregar conteúdo do documento", e)
      document.close()

  @staticmethod
  def stripText(filetext):
    return filetext.strip()

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

  def removerTermosConteudo(self, filetext):
    try:
      terms = self.termosremover["termos"].split(";")
      for term in terms:
        term = term.strip()
        filetext = re.sub(term, '', filetext, flags=re.IGNORECASE)
      return filetext
    except Exception as e:
      messagebox.showerror("Erro ao remover termos do conteúdo", e)

  def enviarParaPublicacao(self, numeroDocumento, filename):
    try:
      self.publicacao.insertLog("Enviando documento para publicação...", "n", numeroDocumento)
      sigepe_botaoEnviarPublicacao = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpaths["publicacao"]["enviarParaPublicacaoBotao"])))
      sigepe_botaoEnviarPublicacao.click()
      wfl.waitForLoading()

      if (cebx.checkExistsByXpath(xpaths["publicacao"]["mensagemErroPublicacao"])):
        self.resultados["erro"].append(filename)
        mensagemErro = wait["regular"].until(EC.presence_of_element_located(
          (By.XPATH, xpaths["publicacao"]["mensagemErroPublicacao"])))
        raise Exception(f"Falha ao enviar documento para publicação: {mensagemErro.text}")
      
      if (cebx.checkExistsByXpath(xpaths["publicacao"]["mensagemSucessoPublicacao"])):
        self.resultados["sucesso"].append(filename)
        mensagemSucesso = wait["regular"].until(EC.presence_of_element_located(
          (By.XPATH, xpaths["publicacao"]["mensagemSucessoPublicacao"])))
        return {"log": f"Sucesso: {mensagemSucesso.text}", "type": "s", "isFinalResult": True, "filename": filename}

    except Exception as e:
      return {"log": f"Falha ao publicar: {e}", "type": "e", "e": e, "isFinalResult": True, "filename": filename}

  def handleResult(self, result, docnumber = ""):
    self.publicacao.insertLog(result["log"], result["type"], docnumber)
    if (("isFinalResult" in result) and result["isFinalResult"] == True):
      self.publicacao.insertResult(result["filename"], result["log"], result["type"], docnumber)
    