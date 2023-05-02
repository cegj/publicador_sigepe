from tkinter import *
from controllers import ObterDoSigepe as ods
import appConfig
from views import Habilitacao as h

class Habilitacao:
  def __init__(self, sessao, container):
    self.sessao = sessao
    self.container = container
    self.construirContainer()

  def construirContainer(self):
    self.subcontainer = Frame(self.container)
    self.subcontainer.pack(side=LEFT, padx=10)
    sigepe_habilitacaoBotao = ods.ObterDoSigepe.botaoHabilitacao()
    habilitacaoAtualLabel = Label(
      self.subcontainer,
      text=f"Habilitação atual: {sigepe_habilitacaoBotao.text}",
      anchor="w",
      font=appConfig.fontes["normal"])
    habilitacaoAtualLabel.pack(side=LEFT)
    self.sessao.userConfig["habilitacao"]["inicial"] = sigepe_habilitacaoBotao.text
    botaoAlterarHabilitacao = Button(
      self.subcontainer,
      text="Alterar habilitação",
      font=appConfig.fontes["botao"],
      width=20,
      command=self.abrirSeletorHabilitacao)
    botaoAlterarHabilitacao.pack(side=LEFT)

  def abrirSeletorHabilitacao(self):
    self.sessao.root.destroy()
    janelaHabilitacao = h.Habilitacao()

  