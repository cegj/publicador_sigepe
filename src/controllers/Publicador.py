from tkinter import *
import appConfig
from controllers import Variaveis as v
from controllers import UserConfig as uc
from striprtf.striprtf import rtf_to_text
from tkinter import messagebox
import os
from threading import Thread
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
from controllers.publicador.campos import Correlacao as c
from controllers.publicador.campos import Interessado as i
from controllers.publicador import Pospublicacao as pp
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
      self.publicacao.insertOnPendingFiles(os.path.basename(file.name))

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
      correlacao = self.verificarCorrelacao(file)   
      file.close()

      log = {"log": f"Iniciando publicação do documento {filename}", "type": "em"}
      self.handleResult(log)

      numeroDocumento = self.obterDoTexto("numero_documento", completeFiletext)
      if (numeroDocumento != ""):
        log = {"log": f"Número do documento identificado", "type": "n"}
        self.handleResult(log, numeroDocumento)
      else:
        log = {"log": f"Não foi localizado um número no texto do documento", "type": "a"}
        self.handleResult(log)

      matriculaSiape = self.obterDoTexto("matricula_siape", completeFiletext)
      if (matriculaSiape != ""):
        log = {"log": f"Matrícula SIAPE identificada: {matriculaSiape}", "type": "n"}
        self.handleResult(log, numeroDocumento)
      else:
        log = {"log": f"Não foi localizada uma matrícula SIAPE no texto do documento", "type": "a"}
        self.handleResult(log, numeroDocumento)

      if(self.config["tipo_tema_assunto"] == "Buscar no conteúdo do documento"):
        autoTemaResult = t.Tema.buscar(filetext)
        self.handleResult(autoTemaResult, numeroDocumento)
        if not self.checkResult(autoTemaResult): continue
        self.config["valores_sigepe"]["tema"] = autoTemaResult["return"]
        autoAssuntoResult = a.Assunto.buscar(filetext)
        self.handleResult(autoAssuntoResult, numeroDocumento)
        if not self.checkResult(autoAssuntoResult): continue
        self.config["valores_sigepe"]["assunto"] = autoAssuntoResult["return"]

      if (correlacao[0]):
        log = {"log": f"Foram localizados dados de correlação para o documento ({correlacao[1]['acao']} documento {correlacao[1]['numero']} publicado em {correlacao[1]['ano']})", "type": "em"}
        self.handleResult(log, numeroDocumento)

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

      assuntoResult = a.Assunto.preencher(self.config["valores_sigepe"]["assunto"])
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

      log = {"log": f"Selecionando órgão elaborador...", "type": "n"}
      self.handleResult(log, numeroDocumento)
      orgaoElaboradorResult = oe.OrgaoElaborador.preencher(
        self.config["valores_sigepe"]["orgao"],
        self.config["valores_sigepe"]["upag"],
        self.config["valores_sigepe"]["uorg"],
        self.config["valores_sigepe"]["responsavel_assinatura"],
        self.config["valores_sigepe"]["cargo_responsavel"]
      )
      self.handleResult(orgaoElaboradorResult, numeroDocumento)
      if not self.checkResult(orgaoElaboradorResult): continue

      if (correlacao[0]):
        log = {"log": f"Selecionando ato correlacionado...", "type": "n"}
        self.handleResult(log, numeroDocumento)
        correlacaoResult = c.Correlacao.preencher(correlacao[1])
        self.handleResult(correlacaoResult, numeroDocumento)
        c.Correlacao.apagarArquivo(file)
        if not self.checkResult(correlacaoResult): continue

      if (matriculaSiape != ""):
        log = {"log": f"Selecionando interessado...", "type": "n"}
        self.handleResult(log, numeroDocumento)
        interessadoResult = i.Interessado.preencher(matriculaSiape)
        self.handleResult(interessadoResult, numeroDocumento)
        if not self.checkResult(interessadoResult): continue
      else:
        log = {"log": f"Não foi selecionado um interessado, uma vez que não foi localizada a matrícula SIAPE no conteúdo do documento", "type": "a"}
        self.handleResult(log, numeroDocumento)

      publicacaoResult = self.enviarParaPublicacao(numeroDocumento, filename)
      self.handleResult(publicacaoResult, numeroDocumento)
      if not self.checkResult(publicacaoResult): continue

      self.currentFile = None
      self.publicacao.insertFileText("")
    
    log = {"log": f"Publicação concluída!", "type": "em"}
    self.handleResult(log)
    self.publicacao.showBtns()
    self.publicacao.showConcludeMessage()

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

  def verificarCorrelacao(self, file):
    try:
      path = os.path.dirname(file.name)
      filename = os.path.basename(file.name).split('.', 1)[0]
      corrFilename = str(filename + '.txt')
      corrPath = os.path.join(path, corrFilename)
      corrFile = open(corrPath, 'r', encoding="utf-8")
      contentArr = corrFile.read().replace('\n', '').strip().split('#')
      del contentArr[0]
      corrFile.close()
      contentObj = {}
      for value in contentArr:
        keyValue = value.split("=")
        contentObj[keyValue[0].lower()] = keyValue[1]
      return [True, contentObj]
    except Exception as e:
      return [False, e]

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

      if (self.config["acao"].lower() == "enviar para assinatura / publicação"):
        if(self.config["valores_sigepe"]["tipo_assinatura"].lower() == "digital"): xpath = xpaths["publicacao"]["enviarParaAssinaturaBotao"]
        elif(self.config["valores_sigepe"]["tipo_assinatura"].lower() == "manual"): xpath = xpaths["publicacao"]["enviarParaPublicacaoBotao"]
      elif (self.config["acao"].lower() == "enviar para análise"): xpath = xpaths["publicacao"]["enviarParaAnaliseBotao"]
      elif (self.config["acao"].lower() == "gravar rascunho"): xpath = xpaths["publicacao"]["gravarRascunhoBotao"]

      self.publicacao.insertLog(f"Executando a ação {self.config['acao'].lower()}", "n", numeroDocumento)

      sigepe_botaoAcao = wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpath)))
      sigepe_botaoAcao.click()
      wfl.waitForLoading()

      if (cebx.checkExistsByXpath(xpaths["publicacao"]["mensagemErroPublicacao"])):
        self.resultados["erro"].append(filename)
        mensagemErro = wait["regular"].until(EC.presence_of_element_located(
          (By.XPATH, xpaths["publicacao"]["mensagemErroPublicacao"])))
        raise Exception(f"Falha ao cadastrar documento: {mensagemErro.text}")
      
      if (cebx.checkExistsByXpath(xpaths["publicacao"]["mensagemSucessoPublicacao"])):
        self.resultados["sucesso"].append(filename)
        mensagemSucesso = wait["regular"].until(EC.presence_of_element_located(
          (By.XPATH, xpaths["publicacao"]["mensagemSucessoPublicacao"])))
        return {"log": f"Sucesso: {mensagemSucesso.text}", "type": "s", "isFinalResult": True}

    except Exception as e:
      return {"log": f"Falha: {e}", "type": "e", "e": e, "isFinalResult": True}

  def checkResult(self, result):
    if (result["type"] == "e"):
      return False
    else:
      return True

  def handleResult(self, result, docnumber = ""):
    if (self.currentFile): currentFileName = os.path.basename(self.currentFile.name)
    else: currentFileName = ""

    if (result["type"] == 's'):
      self.publicacao.moveToSuccessFiles(currentFileName)
    elif (result["type"] == 'e'):
      self.publicacao.moveToFailFiles(currentFileName)

    self.publicacao.insertLog(result["log"], result["type"], docnumber)

    if (result["type"] != 'n'):
      self.publicacao.insertResult(currentFileName, result["log"], result["type"], docnumber)

      if (result["type"] == 's'):
        newFilename = None
        if (self.pospublicacao["adicionar_ao_nome_arquivo"] != ""):
          renameResult = pp.Pospublicacao.renomearArquivo(self.currentFile, self.pospublicacao["adicionar_ao_nome_arquivo"])
          if (renameResult[0] == True):
            newFilename = renameResult[1]
            self.publicacao.insertLog(f"Arquivo renomeado para {renameResult[1]}", 'n', docnumber)
          else:
            log = {"log": f"Não foi possível renomear o arquivo. Erro: {renameResult[1]}", "type": "a"}
            self.publicacao.insertLog(log["log"], log["type"], docnumber)
            self.publicacao.insertResult(currentFileName, log["log"], log["type"], docnumber)
        if (self.pospublicacao["copiar_ou_mover"] == "Mover para..." or self.pospublicacao["copiar_ou_mover"] == "Copiar para..."):
          actionResult = pp.Pospublicacao.copiarMoverArquivo(self.currentFile, self.pospublicacao["copiar_ou_mover"], self.pospublicacao["destino"], newFilename)
          if (actionResult[0] == True):
            verb = "copiado" if "copiar" in self.pospublicacao["copiar_ou_mover"].lower() else "movido"
            self.publicacao.insertLog(f"Arquivo {verb} para {actionResult[1]}", 'n', docnumber)
          else:
            verb = "copiar" if "copiar" in self.pospublicacao["copiar_ou_mover"].lower() else "mover"
            log = {"log": f"Não foi possível {verb} o arquivo. Erro: {actionResult[1]}", "type": "a"}
            self.publicacao.insertLog(log["log"], log["type"], docnumber)
            self.publicacao.insertResult(currentFileName, log["log"], log["type"], docnumber)        