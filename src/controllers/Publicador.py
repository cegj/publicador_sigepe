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
from controllers.publicador.campos import EdicaoBoletim as eb
from controllers.publicador.campos import TipoAssinatura as ta
from controllers.publicador.campos import TipoNumero as tn
from controllers.publicador.campos import Tema as t
from controllers.publicador.campos import Assunto as a
from controllers.publicador.campos import Numero as n
from controllers.publicador.campos import DataAssinatura as da
from controllers.publicador.campos import DataPublicacao as dp
from controllers.publicador.campos import Especie as e
from controllers.publicador.campos import ConteudoDocumento as cd
from controllers.publicador.campos import OrgaoElaborador as oe
from controllers.publicador.campos import Interessado as i
from controllers.publicador import Pospublicacao as pp
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
    self.currentFile = None
    t = Thread(target=self.publicar)
    t.start()

  def publicar(self):
    for file in self.files:
      self.currentFile = file
      gt.goTo("https://bgp.sigepe.gov.br/sigepe-bgp-web-intranet/pages/publicacao/cadastrar.jsf")

      if (file.closed): file.open()
      filename = os.path.basename(file.name)
      completeFiletext = self.obterTextoDocumento(file)
      textBeforeRemoveTerms = self.removerPrimeiraLinha(completeFiletext)
      filetext = self.removerTermosConteudo(textBeforeRemoveTerms)
      filetext = Publicador.stripText(filetext)
      self.publicacao.insertFileText(filetext)
      file.close()

      self.publicacao.insertLog(f"Iniciando publicação do documento {filename}", "a")
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
      if not self.checkResult(edicaoBoletimResult): continue

      tipoAssinaturaResult = ta.TipoAssinatura.preencher(self.config["valores_sigepe"]["tipo_assinatura"])
      self.handleResult(tipoAssinaturaResult, numeroDocumento)
      if not self.checkResult(tipoAssinaturaResult): continue

      tipoNumeroResult = tn.TipoNumero.preencher(self.config["valores_sigepe"]["tipo_preenchimento"])
      self.handleResult(tipoNumeroResult, numeroDocumento)
      if not self.checkResult(tipoNumeroResult): continue

      temaResult = t.Tema.preencher(self.config["valores_sigepe"]["tema"])
      self.handleResult(temaResult, numeroDocumento)
      if not self.checkResult(temaResult): continue

      assuntoResult = a.Assunto.preencher()
      self.handleResult(assuntoResult, numeroDocumento)
      if not self.checkResult(assuntoResult): continue

      if (self.config["valores_sigepe"]["tipo_preenchimento"] == "Manual"):
        numeroResult = n.Numero.preencher(numeroDocumento)
        self.handleResult(numeroResult, numeroDocumento)
        if not self.checkResult(numeroResult): continue

      if (self.config["valores_sigepe"]["tipo_preenchimento"] == "Manual"):
        dataAssinaturaResult = da.DataAssinatura.preencher(self.config["valores_sigepe"]["data_assinatura"])
        self.handleResult(dataAssinaturaResult, numeroDocumento)
        if not self.checkResult(dataAssinaturaResult): continue

      if (self.config["valores_sigepe"]["edicao_bgp"] == "Normal"):
        dataPublicacaoResult = dp.DataPublicacao.preencher(self.config["valores_sigepe"]["data_publicacao"])
        self.handleResult(dataPublicacaoResult, numeroDocumento)
        if not self.checkResult(dataPublicacaoResult): continue

      especieResult = e.Especie.preencher(self.config["valores_sigepe"]["especie"])
      self.handleResult(especieResult, numeroDocumento)
      if not self.checkResult(especieResult): continue

      textoDocumentoResult = cd.ConteudoDocumento.preencher(filetext)
      self.handleResult(textoDocumentoResult, numeroDocumento)
      if not self.checkResult(textoDocumentoResult): continue

      self.publicacao.insertLog("Selecionando órgão elaborador...", "n", numeroDocumento)
      orgaoElaboradorResult = oe.OrgaoElaborador.preencher(
        self.config["valores_sigepe"]["orgao"],
        self.config["valores_sigepe"]["upag"],
        self.config["valores_sigepe"]["uorg"],
        self.config["valores_sigepe"]["responsavel_assinatura"],
        self.config["valores_sigepe"]["cargo_responsavel"]
      )
      self.handleResult(orgaoElaboradorResult, numeroDocumento)
      if not self.checkResult(orgaoElaboradorResult): continue

      self.publicacao.insertLog("Selecionando interessado...", "n", numeroDocumento)
      interessadoResult = i.Interessado.preencher(matriculaSiape)
      self.handleResult(interessadoResult, numeroDocumento)
      if not self.checkResult(interessadoResult): continue

      publicacaoResult = self.enviarParaPublicacao(numeroDocumento, filename)
      self.handleResult(publicacaoResult, numeroDocumento)
      if not self.checkResult(publicacaoResult): continue

      self.currentFile = None
    
    self.publicacao.insertLog("PUBLICAÇÃO ENCERRADA!", "n")

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
        return {"log": f"Sucesso: {mensagemSucesso.text}", "type": "s", "isFinalResult": True}

    except Exception as e:
      return {"log": f"Falha ao publicar: {e}", "type": "e", "e": e, "isFinalResult": True}

  def checkResult(self, result):
    if (result["type"] == "e"):
      return False
    else:
      return True

  def handleResult(self, result, docnumber = ""):
    currentFileName = os.path.basename(self.currentFile.name)
    if (result["type"] == 's'):
      self.resultados["sucesso"].append(currentFileName)
    elif (result["type"] == 'e'):
      self.resultados["erro"].append(currentFileName)

    self.publicacao.insertLog(result["log"], result["type"], docnumber)

    if (not ("isFinalResult" in result) and result["type"] == 'e'):
      self.publicacao.insertResult(currentFileName, result["log"], result["type"], docnumber)

    if (("isFinalResult" in result) and result["isFinalResult"] == True):
      self.publicacao.insertResult(currentFileName, result["log"], result["type"], docnumber)

      if (result["type"] == 's'):
        newFilename = None
        if (self.pospublicacao["adicionar_ao_nome_arquivo"] != ""):
          renameResult = pp.Pospublicacao.renomearArquivo(self.currentFile, self.pospublicacao["adicionar_ao_nome_arquivo"])
          if (renameResult[0] == True):
            self.publicacao.insertLog(f"Arquivo renomeado para {renameResult[1]}", 'n', docnumber)
          else:
            self.publicacao.insertLog(f"Não foi possível renomear o arquivo. Erro: {renameResult[1]}", 'e', docnumber)
        if (self.pospublicacao["copiar_ou_mover"] == "Mover para..." or self.pospublicacao["copiar_ou_mover"] == "Copiar para..."):
          actionResult = pp.Pospublicacao.copiarMoverArquivo(self.currentFile, self.pospublicacao["copiar_ou_mover"], self.pospublicacao["destino"], newFilename)
          if (actionResult[0] == True):
            verb = "copiado" if "copiar" in self.pospublicacao["copiar_ou_mover"].lower() else "movido"
            self.publicacao.insertLog(f"Arquivo {verb} para {actionResult[1]}", 'n', docnumber)
          else:
            verb = "copiar" if "copiar" in self.pospublicacao["copiar_ou_mover"].lower() else "mover"
            self.publicacao.insertLog(f"Não foi possível {verb} o arquivo. Erro: {actionResult[1]}", 'e', docnumber)


    