# DPKG CKAN MG

## Descrição

Pacote Python criado pela [Diretoria de Transparência Ativa - DTA](https://www.cge.mg.gov.br/a-cge/quem-e-quem/subcontroladoria-de-transparencia-e-integridade) da [Controladoria Geral do Estado de Minas Gerais - CGE/MG](https://www.cge.mg.gov.br/) com intuito de automatizar a publicação/manutenção de conjunto de dados abertos no [Portal de Dados Abertos do Estado de Minas Gerais](https://dados.mg.gov.br/). Trabalho realizado seguindo padrões internacionais de documentação e utilização de conjuntos de dados abertos, tais como [Frictionless Data](https://frictionlessdata.io/) e ferramentas open source como [CKAN](https://ckan.org/).

Obs.: "#" Utlizados nas caixas de código abaixo são comentários e deverão ser observados atentamente antes da execução de qualquer comando

## Utilização

- Instalação

```
$ pip install dpkgckanmg
```

- Trabalhando com variáveis de ambiente

A utilizaçao deste pacote exige a utilizaçao de chaves CKAN, tanto do ambiente de [homologação](https://homologa.cge.mg.gov.br/) quanto de [produção](https://dados.mg.gov.br/). Para solicitar login de acesso mande um e-mail para dadosabertos@cge.mg.gov.br.


Sugerimos a criação de um arquivo .env na raiz do pacote (bem como o cadastro .gitignore do mesmo) para utilização destas chaves sem a sincronização das mesmas com o repositório online. O pacote "python-dotenv" necessário para carregamento das chaves cadastradas no arquivo .env, será instalado juntamente com o pacote. Sendo assim, sugerimos os seguintes passos para criaçao do arquivo .env:

```
# Criação arquivo .env com estrutura para receber chaves CKAN homologação e produção
# Após a criação, abra o arquivo e inclua as chaves em seus respectivos ambientes
$ echo "CKAN_HOMOLOGA=''\nCKAN_PORTAL=''" > .env

# Inclua ".env" na última linha do arquivo .gitignore existente na raiz do conjunto. Caso .gitignore não exista execute o comando abaixo:
# CUIDADO: Caso comando abaixo seja executado em um conjunto cujo .gitignore exista toda configuração preexistente no mesmo será apagada
$ echo ".env" > .gitignore
```


- Publicação de conjuntos (Arquivo Python ou terminal)
  - publish(package_path, ckan_key, environment):
    - package_path: caminho do arquivo datapackage.json
    - ckan_key: chave ckan do usuário no ambiente desejado
    - environment: escolher entre "homologa" e"portal" (homologa default)

```
# Publicação em ambiente de homologação - Executar na raiz do conjunto (local onde datapackage.json está armazenado)

import os
from dotenv import load_dotenv
load_dotenv()
from dpkgckanmg import publish
publish("./", os.getenv('CKAN_HOMOLOGA'), "homologa")


# Publicação em ambiente de produção - Executar na raiz do conjunto (local onde datapackage.json está armazenado)

import os
from dotenv import load_dotenv
load_dotenv()
from dpkgckanmg import publish
publish("./", os.getenv('CKAN_PORTAL'), "portal")
```

# Criar Recurso
from dpkgckanmg import criarArquivo2
criarArquivo2(1, 2, 3)

# Atualizar Data Set
from dpkgckanmg import dataSet
dataSet(1, 2, 3)

# Atualizar Recurso
from dpkgckanmg import resource
resource(1, 2, 3)


### 1,2 3 deveráo ser retirados do arquivo .doc (gabriel atualizará)
```

## Desenvolvimento

# Instalação

- Prerequisitos:
  - Python 3.9 ou superior

- [Documentação de referência mostrando procedimentos necessários para contribuiação em um projeto open source](https://www.dataschool.io/how-to-contribute-on-github/)
- Passos básicos:
  - Fork o repositório do projeto
  - Clone o repositório criado em sua conta após o fork
  - Navegue até o repositório clonado em sua máquina
  - Crie e ative ambiente python para utilizar o projeto. Os passos abaixo são sugestões, podendo outro método ser utilizado de acordo com a preferência do usuário:
```
$ python3.9 -m venv venv
$ source venv/bin/activate
(venv) ➜ pip install -r requirements.txt
# Desativar o ambiente
(venv) ➜ deactivate
```
  - Crie um branch e realize as modificações necessárias
  - Realize o push de suas modificações no branch criado
  - Abra um PR explicando os motivos que o levaram a realizar a modificar parte do código e em como esta modificação auxiliará no desenvolvimento do projeto

# Atualização de versão

Conforme relatado no [issue 6](https://github.com/dados-mg/dpkgckanmg/issues/6), atualização de versões no [Pypi](https://pypi.org/) deve seguir os passos:

- Visualização da última versão publicada no Pypi
- Atualização arquivo setup.py com uma versão superior à identificada no Pypi
- Commit diretamente na main da modificação
```
$ git add .
$ git commit -m "v<numero-versao>"
# Exemplo - $ git commit -m "v0.0.1.9013"
```
- Criação da tag e vinculação da mesma com o último commit
```
$ git tag v<numero-versao> HEAD
# Exemplo - $ git tag v0.0.1.9013 HEAD
```
- Push commit (diretamente main) e tag para repo online
```
$ git push origin main                # branch
$ git push origin v<numero-versao>    # tag
```
- Publicar nova versão
```
# Leitura do arquivo Makefile para relembrar
# Ativar ambiente python e publicação
$ source venv/bin/activate
(venv) ➜  dpkgckanmg git:(main) make update-package
```

- Consulta nova versão publicada
