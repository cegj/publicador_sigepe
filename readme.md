# Publicador Sigepe

Criado por [mim](https://github.com/cegj), com **Python**.

Publicador Sigepe é um software para publicação *em lote* de documentos (portarias e outros) no Sistema de Gestão de Pessoas do Governo Federal (Sigepe).

[⬇️ Faça o download da versão mais recente clicando aqui](https://github.com/cegj/publicador_sigepe/releases)

## Stack

- Python;
- Selenium.

## Recursos

- Publicação múltiplos documentos em lote no Sigepe via módulo Publicação;
- Definição do tema e assunto dos documentos com base no seu conteúdo (ou por seleção manual);
- Detecção de número do documento e matrícula SIAPE do interessado no conteúdo de cada documento;
- Copiar, mover e/ou renomear os arquivos após a publicação;
- Remover determinados termos (definidos pelo usuário) do conteúdo do documento antes de publicá-lo;
- Utilização de variáveis para representar datas (hoje, próximo dia útil, mês, ano etc.) nos dados da publicação;
- Tela de publicação com fila de arquivos e logs para acompanhar o passo-a-passo da publicação de cada documento.

### Planejado

1. Oferecer opção de salvar documento como PDF após a publicação;

### Limitações

1. Somente são publicados arquivos no formato **RTF (Rich Text Format)** — outros formatos, como .docx, .odt ou .txt não são suportados;
2. O conteúdo é publicado sem formatação (ou seja, negritos, itálicos e demais formatações são ignorados);
3. Atualmente disponível somente para 🪟 Windows;
4. Necessita que o Google Chrome esteja instalado e atualizado.

## Imagens
Tela de entrada (login)
<img src="https://i.imgur.com/7JpOy65.png" title="Entrada (login)" />

Tela principal (definições da publicação)
<img src="https://i.imgur.com/Lvh8sN0.png" title="Tela principal (definições da publicação)" />

Tela de publicação
<img src="https://i.imgur.com/K0fBfzq.png" title="Tela de publicação em lote" />

Tela de publicação em execução (exemplo)
<img src="https://i.imgur.com/7nM8uQL.gif" title="Publicação em execução (exemplo)" />

## Documentação de ajuda

Em breve.

## Requisitos prévios

Para utilizar o Publicador Sigepe, é necessário:
-  Ter o [Google Chrome (download aqui)](https://www.google.com/intl/pt-BR/chrome/) instalado em seu computador na versão mais recente.
-  Ter uma conta no Sigepe com uma habilitação que tenha acesso ao Módulo Publicação.

## Instalação

1. [⬇️ Faça o download da versão mais recente do Publicador Sigepe clicando aqui](https://github.com/cegj/publicador_sigepe/releases)

2. Execute o instalador *(setup_publicador-sigepe.exe)*

## Aviso

⚠️ É necessário inserir seus dados de acesso ao Sigepe (CPF e senha) para utilizar o Publicador Sigepe, uma vez que o software precisa acessar a sua conta para realizar as publicações. **Estes dados não são armazenados (nem mesmo no seu computador), não são enviados para terceiros ou nem utilizados para qualquer outra finalidade.** O código-fonte do Publicador Sigepe é aberto e pode ser auditado por qualquer pessoa.