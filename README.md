# Data package manager para CKAN (dpckan)

O `dpckan` é um pacote Python, acessível via interface [CLI](https://pt.wikipedia.org/wiki/Interface_de_linha_de_comandos), utilizado para criação e atualização de conjuntos de dados e recursos (documentados de acordo com o padrão de metadados [Frictionless Data](https://frictionlessdata.io/)) em uma instância do [CKAN](https://ckan.org/).

[Documentação complementar](https://dpckan.readthedocs.io/en/latest/)

## Instalação

O `dpckan` está disponível no Python Package Index - [PyPI](https://pypi.org/project/dpckan/) e pode ser instalado utilizando-se o comando abaixo:

```bash
# Antes de executar o comando abaixo lembre-se que ambiente Python deverá estar ativo
$ pip install dpckan
```

## Configuração de Variáveis de ambiente

Todos os comandos exigem a indicação de uma instância CKAN (ex: https://demo.ckan.org/) e de uma chave válida para autenticação na referida instância. Esta indicação deverá ser realizada através do cadastro de variáveis de ambiente. Para invocação CLI de qualquer comando sem a necessidade de indicar explicitamente estas variáveis recomenda-se utilização dos nomes `CKAN_HOST` e `CKAN_KEY` para cadastro de instância e chave respectivamente. Caso outros nomes sejam utilizados, necessário indicar explicitamente durante a chamada da função desejada, utilizando-se as flags "--ckan-host" e "--ckan-key", conforme demostrado abaixo e ou de maneira mais detalhada na sessão [Uso](#uso).


```bash
# CKAN_HOST=https://demo.ckan.org/
# CKAN_KEY=CC850181-6ZS9-4f4C-bf3f-fb4db7ce09f90 (Chave CKAN meramente ilustrativa)
# Utilização sem necessidade de indicar explicitamente variáveis
$ dpckan dataset create

# CKAN_HOST_PRODUCAO=https://demo.ckan.org/
# CKAN_KEY_PRODUCAO=CC850181-6ZS9-4f4C-bf3f-fb4db7ce09f90 (Chave CKAN meramente ilustrativa)
# Utilização indicando explicitamente variáveis, através flags --ckan-host e --ckan-key
$ dpckan dataset create --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO

```

O cadastro das variáveis de ambiente `CKAN_HOST` e `CKAN_KEY`, necessárias para invocação de cada comando, deverá ser realizada conforme sistema operacional do usuário. Abaixo links de referência para tal:

  * [Windows](https://professor-falken.com/pt/windows/como-configurar-la-ruta-y-las-variables-de-entorno-en-windows-10/);
  * [Linux](https://ricardo-reis.medium.com/vari%C3%A1veis-de-ambiente-no-linux-debian-f677d6ca94c); e
  * [Mac](https://support.apple.com/pt-br/guide/terminal/apd382cc5fa-4f58-4449-b20a-41c53c006f8f/mac).


**CUIDADO: SOMENTE UTILIZE A OPÇÃO SUGERIDA ABAIXO SE POSSUIR CONHECIMENTO TÉCNICO E FAMILIARIDADE COM O ASSUNTO, EVITANDO ASSIM PROBLEMAS COM ACESSO DE TERCEIROS NÃO AUTORIZADOS EM SUA INSTÂNCIA CKAN**

Alternativamente, o cadastro destas variáveis de ambiente poderá ser realizado em arquivo ".env", na raiz do conjunto de dados, sendo necessário a inclusão deste ".env" em arquivo ".gitignore", evitando assim a sincronização e consequente publicização destas chaves em repositórios online como [github](https://github.com/), conforme demostrado abaixo:


```bash
# CUIDADO: SOMENTE EXECUTE OS COMANDOS ABAIXO SE OS ARQUIVO ".env" e ".gitignore" NÃO EXISTIREM NA RAIZ DO CONJUNTO DE DADOS
# CUIDADO: CASO COMANDOS ABAIXO SEJAM EXECUTADOS COM ".env" e ".gitignore" EXISTENTES TODO CONTEÚDO DOS MESMOS SERÁ APAGADO
# CUIDADO: SOMENTE EXECUTE OS COMANDOS ABAIXO SE TIVER CERTEZA E CONHECIMENTO DO QUE SERÁ FEITO

# Crie arquivo ".env" com estrutura para receber chaves CKAN_HOST e CKAN_KEY
# Após a criação, abra o arquivo e inclua os valores para cada variável
$ echo "CKAN_HOST=''\nCKAN_KEY=''" > .env

# Crie arquivo ".gitignore" com configuração para excluir arquivo ".env" do controle de versão git
$ echo ".env" > .gitignore

# Confira se configuração foi realizada com sucesso
# Comando abaixo deverá mostrar apenas criação/modificação de arquivo ".gitignore", não sendo apresentado nada para arquivo ".env"
$ git status
```

## Uso

### Acessando documentação dpckan via terminal

```bash
# Informações gerais sobre o pacote e seus comandos
# Utilização das flags --help ou -h retornará o mesmo resultado
$ dpckan

# Informações sobre comandos dataset e resource
# Utilização das flags --help ou -h retornará o mesmo resultado
$ dpckan dataset
$ dpckan resource

# Informações sobre subcomandos dataset
# Utilização da flag -h retornará o mesmo resultado
$ dpckan dataset create --help
$ dpckan dataset update --help

# Informações sobre subcomandos resource
# Utilização da flag -h retornará o mesmo resultado
$ dpckan resource create --help
$ dpckan resource update --help
```

### Criação de conjunto de dados via terminal

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra:

```bash
$ dpckan dataset create
```

- Executar o comando fora do diretório aonde o arquivo datapackage.json se encontra (não copie e cole o comando abaixo cegamente, modifique o último argumento com o caminho local para arquivo datapackage.json):

```bash
# Utilização flag --datapackage
$ dpckan dataset create --datapackage local/path/para/datapackage.json

# Utilização alias -dp para flag --datapackage
$ dpckan dataset create -dp local/path/para/datapackage.json
```

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra e variáveis de ambiente com nomenclatura diferente de `CKAN_HOST` e `CKAN_KEY` (não copie e cole o comando abaixo cegamente, modifique o nome das variáveis de ambiente para a sua realidade):

```bash
# Utilização flag --ckan-host e --ckan-key
$ dpckan dataset create --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO

# Utilização alias -H e -k para flags --ckan-host e --ckan-key respectivamente
$ dpckan dataset create -H $CKAN_HOST_PRODUCAO -k $CKAN_KEY_PRODUCAO
```

### Criação de conjunto de dados via código Python

- Criar um arquivo .py com a seguinte estrutura (não copie e cole o comando abaixo cegamente, modifique o nome das variáveis de ambiente e  o caminho para o arquivo datapackage.json de acordo com a sua realidade):

```python
import os
from dpckan import create_dataset

CKAN_HOST = os.environ.get('CKAN_HOST')
CKAN_KEY = os.environ.get('CKAN_KEY')
datapackage_path = 'local/path/para/datapackage.json'

# A chamada de funções via código Python exige passagem de todos os argumentos
create_dataset.create(ckan_host=CKAN_HOST,
                      ckan_key=CKAN_KEY,
                      datapackage=datapackage_path)
```

### Atualização de conjunto de dados via terminal

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra:

```bash
$ dpckan dataset update
```

- Executar o comando fora do diretório aonde o arquivo datapackage.json se encontra (não copie e cole o comando abaixo cegamente, modifique o último argumento com o caminho local para arquivo datapackage.json):

```bash
# Utilização flag --datapackage
$ dpckan dataset update --datapackage local/path/para/datapackage.json

# Utilização alias -dp para flag --datapackage
$ dpckan dataset update -dp local/path/para/datapackage.json
```

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra e variáveis de ambiente com nomenclatura diferente de `CKAN_HOST` e `CKAN_KEY` (não copie e cole o comando abaixo cegamente, modifique o nome das variáveis de ambiente para a sua realidade):

```bash
# Utilização flag --ckan-host e --ckan-key
$ dpckan dataset update --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO

# Utilização alias -H e -k para flags --ckan-host e --ckan-key respectivamente
$ dpckan dataset update -H $CKAN_HOST_PRODUCAO -k $CKAN_KEY_PRODUCAO
```

### Atualização de conjunto de dados via código Python

- Criar um arquivo .py com a seguinte estrutura (não copie e cole o comando abaixo cegamente, modifique o nome das variáveis de ambiente e  o caminho para o arquivo datapackage.json de acordo com a sua realidade):

```python
import os
from dpckan import update_dataset

CKAN_HOST = os.environ.get('CKAN_HOST')
CKAN_KEY = os.environ.get('CKAN_KEY')
datapackage_path = 'local/path/para/datapackage.json'

# A chamada de funções via código Python exige passagem de todos os argumentos
update_dataset.update(ckan_host=CKAN_HOST,
                      ckan_key=CKAN_KEY,
                      datapackage=datapackage_path)
```

### Criação de recurso via terminal

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra (não copie e cole o comando abaixo cegamente, modifique o último argumento com o nome do recurso presente no arquivo datapackage.json que será criado):

```bash
$ dpckan resource create --resource-name nome-recurso

# Utilização alias -rn para flag --resource-name
$ dpckan resource create -rn nome-recurso
```

- Executar o comando fora do diretório aonde o arquivo datapackage.json se encontra (não copie e cole o comando abaixo cegamente, modifique o caminho local para arquivo datapackage.json e o nome do recurso para a sua realidade):

```bash
# Utilização flags --datapackage e --resource-name
$ dpckan resource create --datapackage local/path/para/datapackage.json --resource-name nome-recurso

# Utilização alias -dp e -rn para flags --datapackage e --resource-name respectivamente
$ dpckan resource create -dp local/path/para/datapackage.json -rn nome-recurso
```

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra e variáveis de ambiente com nomenclatura diferente de `CKAN_HOST` e `CKAN_KEY` (não copie e cole o comando abaixo cegamente, modifique o nome do recurso e o nome das variáveis de ambiente para a sua realidade):

```bash
# Utilização flags --resource-name, --ckan-host e --ckan-key
$ dpckan resource create --resource-name nome-recurso --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO

# Utilização alias -rn, -H e -k para flags --resource-name, --ckan-host e --ckan-key respectivamente
$ dpckan resource create -rn nome-recurso -H $CKAN_HOST_PRODUCAO -k $CKAN_KEY_PRODUCAO
```

### Criação de recurso via código Python

- Criar um arquivo .py com a seguinte estrutura (não copie e cole o comando abaixo cegamente, modifique o nome das variáveis de ambiente, o caminho para o arquivo datapackage.json e o nome do recurso a ser criado de acordo com a sua realidade):

```python
import os
from dpckan import create_resource

CKAN_HOST = os.environ.get('CKAN_HOST')
CKAN_KEY = os.environ.get('CKAN_KEY')
datapackage_path = 'local/path/para/datapackage.json'
resource_name = 'nome-recurso'

# A chamada de funções via código Python exige passagem de todos os argumentos
create_resource.create_resource(ckan_host=CKAN_HOST,
                      ckan_key=CKAN_KEY,
                      datapackage=datapackage_path,
                      resource_name=resource_name)
```

### Atualização de recurso via terminal

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra (não copie e cole o comando abaixo cegamente, modifique os últimos argumentos com o nome e id do recurso presente no arquivo datapackage.json que será atualizado):

```bash
# Utilização flags --resource-name e --resource-id
$ dpckan resource update --resource-name nome-recurso --resource-id id-recurso

# Utilização alias -rn e -id para flags --resource-name e --resource-id respectivamente
$ dpckan resource update -rn nome-recurso -id id-recurso
```

- Executar o comando fora do diretório aonde o arquivo datapackage.json se encontra (não copie e cole o comando abaixo cegamente, modifique o caminho local para arquivo datapackage.json, o nome e id do recurso para a sua realidade):

```bash
# Utilização flag --datapackage
$ dpckan resource update --datapackage local/path/para/datapackage.json --resource-name nome-recurso --resource-id id-recurso

# Utilização alias -dp, -rn e -id para flags --datapackage,--resource-name e --resource-id respectivamente
$ dpckan resource update -dp local/path/para/datapackage.json -rn nome-recurso -id id-recurso
```

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra e variáveis de ambiente com nomenclatura diferente de `CKAN_HOST` e `CKAN_KEY` (não copie e cole o comando abaixo cegamente, modifique o nome das variáveis de ambiente, o nome e id do recurso para a sua realidade):

```bash
# Utilização flags --ckan-host, --ckan-key, --resource-name e --resource-id
$ dpckan resource update --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO --resource-name nome-recurso --resource-id id-recurso

# Utilização alias -H, -k, -rn e -id para flags --ckan-host, --ckan-key, --resource-name e --resource-id respectivamente
$ dpckan resource update -H $CKAN_HOST_PRODUCAO -k $CKAN_KEY_PRODUCAO -rn nome-recurso -id id-rescurso
```

### Criação de recurso via código Python

- Criar um arquivo .py com a seguinte estrutura (não copie e cole o comando abaixo cegamente, modifique o nome das variáveis de ambiente, o caminho para o arquivo datapackage.json, o nome e id do recurso a ser atualizado de acordo com a sua realidade):

```python
import os
from dpckan import update_resource

CKAN_HOST = os.environ.get('CKAN_HOST')
CKAN_KEY = os.environ.get('CKAN_KEY')
datapackage_path = 'local/path/para/datapackage.json'
resource_name = 'nome-recurso'
resource_id = 'id-resource'

# A chamada de funções via código Python exige passagem de todos os argumentos
update_resource.update_resource(ckan_host=CKAN_HOST,
                      ckan_key=CKAN_KEY,
                      datapackage=datapackage_path,
                      resource_name=resource_name,
                      resource_id=resource_id)
```

## Desenvolvimento

### Contribuir para o projeto

- Prerequisitos:
    - Python 3.9 ou superior

- [Documentação de referência mostrando procedimentos necessários para contribuiação em um projeto open source](https://www.dataschool.io/how-to-contribute-on-github/)

- Passos básicos:
    - Fork o repositório do projeto;
    - Clone o repositório criado em sua conta após o fork;
    - Navegue até o repositório clonado em sua máquina;
    - Crie e ative ambiente python para utilizar o projeto, conforme sugerido abaixo (procedimentos poderão ser diferentes conforme sistema operacional):

```
# Linux
$ python3.9 -m venv venv
$ source venv/bin/activate
(venv) ➜ pip install -r requirements.txt
# Desativar o ambiente
(venv) ➜ deactivate

# Windows
$ python -m venv venv
$ source venv/Script/activate
(venv) ➜ pip install -r requirements.txt
# Desativar o ambiente
(venv) ➜ deactivate
```

  - Crie um branch para realizar as modificações necessárias;
  - Realize o push da branch criada; e
  - Abra um PR explicando os motivos da mudança e como esta auxiliará no desenvolvimento do projeto.

### Atualizar versão

Conforme relatado no [issue 6](https://github.com/dados-mg/dpkgckanmg/issues/6), atualização de versões no [Pypi](https://pypi.org/) deve seguir [estes os passos](https://github.com/dados-mg/dpckan/issues/6#issuecomment-851678297):
