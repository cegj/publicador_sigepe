from tkinter import *
from controllers import Variaveis as v
from models import UserConfig as uc
from models import AppConfig as ac
from striprtf.striprtf import rtf_to_text
from tkinter import messagebox
import os
from urllib.parse import urlparse, parse_qs
from threading import Thread
from controllers.publicador.campos import EdicaoBoletim as eb
from controllers.publicador.campos import TipoAssinatura as ta
from controllers.publicador.campos import TipoNumero as tn
from controllers.publicador.campos import Tema as t
from controllers.publicador.campos import Assunto as a
from controllers.publicador.campos import Numero as n
from controllers.publicador.campos import DataAssinatura as da
from controllers.publicador.campos import DataPublicacao as dp
from controllers.publicador.campos import Especie as es
from controllers.publicador.campos import ConteudoDocumento as cd
from controllers.publicador.campos import OrgaoElaborador as oe
from controllers.publicador.campos import Correlacao as c
from controllers.publicador.campos import Interessado as i
from controllers.publicador import Pospublicacao as pp
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from controllers import Webdriver as wd
import re
from helpers import checkDateIsHoliday as cdih
from helpers import getNextWorkDay as gnwd

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
    try:
      for file in self.files:
        self.publicacao.insertOnPendingFiles(os.path.basename(file.name))

      tipoNumero = self.config["valores_sigepe"]["tipo_preenchimento"]
      if (tipoNumero.lower() == "sem número"):
        answer = messagebox.askyesno("Aviso", "Você selecionou o Tipo de Número como 'Sem número'. Neste caso, todos os documentos da lista serão publicados sem um número do ato. Deseja continuar?")
        if (answer == False): self.publicacao.handleFecharJanela()

      if (tipoNumero.lower() == "automático"):
        answer = messagebox.askyesno("Aviso", "Você selecionou o Tipo de Número como 'Automático'. Neste caso, a numeração dos documentos será definida automaticamente pelo Sigepe ao publicar. Deseja continuar?")
        if (answer == False): self.publicacao.handleFecharJanela()

      holiday = cdih.checkDateIsHoliday(self.config["valores_sigepe"]["data_publicacao"])

      if (holiday):
        nextWorkDay = gnwd.getNextWorkDay(self.config["valores_sigepe"]["data_publicacao"], "/")
        answer = messagebox.askyesno("Aviso", f"A data de publicação escolhida ({self.config['valores_sigepe']['data_publicacao']}) é feriado nacional de {holiday}. Deseja alterar para o próximo dia útil ({nextWorkDay})?")
        if (answer == True):
          self.config["valores_sigepe"]["data_publicacao"] = nextWorkDay
    except Exception as e:
      messagebox.showerror("Erro ao iniciar publicação", {e})

    for file in self.files:
      try:
        self.currentFile = file
        wd.Webdriver.go(ac.AppConfig.urls["cadastrarAtoPublicacao"])

        if (file.closed): file = open(file.name)
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

        if (tipoNumero.lower() == "manual"):
          numeroDocumentoResult = self.obterDoTexto("numero_documento", "Número do documento", completeFiletext)
          numeroDocumento = numeroDocumentoResult["result"]
          self.handleResult(numeroDocumentoResult, numeroDocumento)
        else:
          numeroDocumento = ""

        matriculaSiapeResult = self.obterDoTexto("matricula_siape", "Matrícula SIAPE", completeFiletext)
        matriculaSiape = matriculaSiapeResult["result"]
        self.handleResult(matriculaSiapeResult, numeroDocumento)

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

        if (self.config["valores_sigepe"]["tipo_preenchimento"].lower() == "manual"):
          numeroResult = n.Numero.preencher(numeroDocumento)
          self.handleResult(numeroResult, numeroDocumento)
          if not self.checkResult(numeroResult): continue
        else:
          log = {"log": f"Número do ato não preenchido: o tipo de número é '{self.config['valores_sigepe']['tipo_preenchimento'].lower()}'", "type": "n"}
          self.handleResult(log, numeroDocumento)

        if (self.config["valores_sigepe"]["tipo_assinatura"].lower() == "manual"):
          dataAssinaturaResult = da.DataAssinatura.preencher(self.config["valores_sigepe"]["data_assinatura"])
          self.handleResult(dataAssinaturaResult, numeroDocumento)
          if not self.checkResult(dataAssinaturaResult): continue
        else:
          log = {"log": f"Data de assinatura não preenchida: o tipo de assinatura é '{self.config['valores_sigepe']['tipo_assinatura'].lower()}'", "type": "n"}
          self.handleResult(log, numeroDocumento)

        if (self.config["valores_sigepe"]["edicao_bgp"].lower() == "normal"):
          dataPublicacaoResult = dp.DataPublicacao.preencher(self.config["valores_sigepe"]["data_publicacao"])
          self.handleResult(dataPublicacaoResult, numeroDocumento)
          if not self.checkResult(dataPublicacaoResult): continue
        else:
          log = {"log": f"Data de publicação preenchido automaticamente: a edição do boletim selecionada é '{self.config['valores_sigepe']['edicao_bgp'].lower()}'", "type": "n"}
          self.handleResult(log, numeroDocumento)

        especieResult = es.Especie.preencher(self.config["valores_sigepe"]["especie"])
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
      except Exception as e:
        log = {"log": f"ERRO: {e}", "type": "e"}
        self.handleResult(log)
        if not self.checkResult(log): continue
    
    try:
      self.currentFile = None
      self.publicacao.insertFileText("")
      log = {"log": f"Fila de arquivos concluída!", "type": "em"}
      self.handleResult(log)
      self.publicacao.showBtns()
      self.publicacao.showConcludeMessage()
    except Exception as e:
      log = {"log": f"ERRO: {e}", "type": "e"}
      self.handleResult(log)
      messagebox.showerror("Erro ao encerrar fila", {e})

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

  def obterDoTexto(self, delimiterkey, description, filetext):
    try:
      firstDelimiter = self.delimitadores[f"{delimiterkey}"][0]
      secondDelimiter = self.delimitadores[f"{delimiterkey}"][1]
      if (firstDelimiter == "" or secondDelimiter == ""): raise Exception("um ou mais delimitadores estão vazios.")
      a = filetext.split(firstDelimiter, 1)
      b = a[1].split(secondDelimiter, 1)
      data = b[0]
      if (data == ""): return {"log": f"A busca por {description.lower()} entre os termos '{firstDelimiter}' e '{secondDelimiter}' no conteúdo retornou um valor vazio", "type": "a", "result": data}
      else: return {"log": f"{description} identificado(a) no conteúdo: {data}", "type": "n", "result": data}
    except IndexError as e:
      return {"log": f"Não foi possível identificar {description.lower()} no conteúdo: os delimitadores '{firstDelimiter}' e/ou '{secondDelimiter}' não foram localizados.", "type": "a", "result": ""}
    except Exception as e:
      return {"log": f"Não foi possível identificar {description.lower()} no conteúdo: {e}", "type": "a", "result": ""}

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
        if(self.config["valores_sigepe"]["tipo_assinatura"].lower() == "digital"): xpath = ac.AppConfig.xpaths["publicacao"]["enviarParaAssinaturaBotao"]
        elif(self.config["valores_sigepe"]["tipo_assinatura"].lower() == "manual"): xpath = ac.AppConfig.xpaths["publicacao"]["enviarParaPublicacaoBotao"]
      elif (self.config["acao"].lower() == "enviar para análise"): xpath = ac.AppConfig.xpaths["publicacao"]["enviarParaAnaliseBotao"]
      elif (self.config["acao"].lower() == "gravar rascunho"): xpath = ac.AppConfig.xpaths["publicacao"]["gravarRascunhoBotao"]

      self.publicacao.insertLog(f"Executando a ação {self.config['acao'].lower()}", "n", numeroDocumento)

      sigepe_botaoAcao = wd.Webdriver.wait["regular"].until(EC.element_to_be_clickable(
        (By.XPATH, xpath)))
      sigepe_botaoAcao.click()
      wd.Webdriver.waitLoadingModal()

      checkLoadErrors = wd.Webdriver.checkErrorsLoadedPage() 
      if(not checkLoadErrors[0]):
        raise Exception(f"Erro no Sigepe: {checkLoadErrors[1]}")

      if (wd.Webdriver.checkExistsByXpath(ac.AppConfig.xpaths["publicacao"]["mensagemErroPublicacao"])):
        self.resultados["erro"].append(filename)
        mensagemErro = wd.Webdriver.wait["regular"].until(EC.presence_of_element_located(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["mensagemErroPublicacao"])))
        raise Exception(f"Falha ao cadastrar documento: {mensagemErro.text}")
      
      if (wd.Webdriver.checkExistsByXpath(ac.AppConfig.xpaths["publicacao"]["mensagemSucessoPublicacao"])):
        self.resultados["sucesso"].append(filename)
        mensagemSucesso = wd.Webdriver.wait["regular"].until(EC.presence_of_element_located(
          (By.XPATH, ac.AppConfig.xpaths["publicacao"]["mensagemSucessoPublicacao"])))
        return {"log": f"Sucesso: {mensagemSucesso.text}", "type": "s", "isFinalResult": True}
      else:
        try:
          urlParams = parse_qs(urlparse(wd.Webdriver.nav.current_url).query)
          mensagemSucesso = urlParams["mensagem"][0]
          return {"log": f"Sucesso: {mensagemSucesso}", "type": "s", "isFinalResult": True}
        except Exception as e:
          raise Exception(f"Falha ao identificar resultado: {e}. VERIFIQUE SE O CADASTRO DO DOCUMENTO FOI REALIZADO NO SIGEPE.")

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

      if (result["type"] == 'e'):
        log = "A publicação do arquivo foi interrompida devido ao erro acima"
        self.publicacao.insertLog(log, result["type"], docnumber)
        self.publicacao.insertResult(currentFileName, log, 'e', docnumber)

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