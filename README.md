# Data package manager para CKAN (dpckan)

O `dpckan` é um pacote Python, acessível via interface [CLI](https://pt.wikipedia.org/wiki/Interface_de_linha_de_comandos), utilizado para criação e atualização de conjuntos de dados e recursos (documentados de acordo com o padrão de metadados [Frictionless Data](https://frictionlessdata.io/)) em uma instância do [CKAN](https://ckan.org/).

Curiosidades: Consulte a comparação do dpckan com alguns [projetos relacionados](RELATED_PROJECTS.md).

[Documentação complementar](https://dpckan.readthedocs.io/en/latest/)

## Instalação

O `dpckan` está disponível no Python Package Index - [PyPI](https://pypi.org/project/dpckan/) e pode ser instalado utilizando-se o comando abaixo:

```bash
# Antes de executar o comando abaixo lembre-se que ambiente Python deverá estar ativo
$ pip install dpckan
```

## Configuração de Variáveis de ambiente

Todos os comandos exigem a indicação de uma instância CKAN (ex: https://demo.ckan.org/) e de uma chave válida para autenticação na referida instância. Esta indicação deverá ser realizada através do cadastro de variáveis de ambiente. Para invocação CLI de qualquer comando sem a necessidade de indicar explicitamente estas variáveis recomenda-se utilização dos nomes `CKAN_HOST` e `CKAN_KEY` para cadastro de instância e chave respectivamente. Caso outros nomes sejam utilizados, necessário indicar explicitamente durante a chamada da função desejada, utilizando-se as flags "--ckan-host" e "--ckan-key", conforme demostrado abaixo e ou de maneira mais detalhada na sessão [Uso](#uso).


```
# CKAN_HOST=https://demo.ckan.org/
# CKAN_KEY=CC850181-6ZS9-4f4C-bf3f-fb4db7ce09f90 (Chave CKAN meramente ilustrativa)
# Utilização sem necessidade de indicar explicitamente variáveis
```
```bash
$ dpckan dataset create
````
```
# CKAN_HOST_PRODUCAO=https://demo.ckan.org/
# CKAN_KEY_PRODUCAO=CC850181-6ZS9-4f4C-bf3f-fb4db7ce09f90 (Chave CKAN meramente ilustrativa)
# Utilização indicando explicitamente variáveis, através flags --ckan-host e --ckan-key
```
```bash
$ dpckan dataset create --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO

```

O cadastro das variáveis de ambiente `CKAN_HOST` e `CKAN_KEY`, necessárias para invocação de cada comando, deverá ser realizada conforme sistema operacional do usuário. Abaixo links de referência para tal:

  * [Windows](https://professor-falken.com/pt/windows/como-configurar-la-ruta-y-las-variables-de-entorno-en-windows-10/)
  * [Linux](https://ricardo-reis.medium.com/vari%C3%A1veis-de-ambiente-no-linux-debian-f677d6ca94c)
  * [Mac](https://support.apple.com/pt-br/guide/terminal/apd382cc5fa-4f58-4449-b20a-41c53c006f8f/mac)


Alternativamente, o cadastro destas variáveis de ambiente poderá ser realizado em arquivo ".env", na raiz do conjunto de dados, sendo necessário a inclusão deste ".env" em arquivo ".gitignore", evitando assim a sincronização e consequente publicização destas chaves em repositórios online como [github](https://github.com/), conforme demostrado abaixo:


```
# SOMENTE UTILIZE A OPÇÃO SUGERIDA ABAIXO SE POSSUIR FAMILIARIDADE COM O ASSUNTO, EVITANDO ASSIM PROBLEMAS COM ACESSO DE TERCEIROS NÃO AUTORIZADOS EM SUA INSTÂNCIA CKAN
# CUIDADO: SOMENTE EXECUTE OS COMANDOS ABAIXO SE OS ARQUIVO ".env" e ".gitignore" NÃO EXISTIREM NA RAIZ DO CONJUNTO DE DADOS
# CUIDADO: CASO COMANDOS ABAIXO SEJAM EXECUTADOS COM ".env" e ".gitignore" EXISTENTES TODO CONTEÚDO DOS MESMOS SERÁ APAGADO
# CUIDADO: SOMENTE EXECUTE OS COMANDOS ABAIXO SE TIVER CERTEZA E CONHECIMENTO DO QUE SERÁ FEITO
```
```
# Crie arquivo ".env" com estrutura para receber chaves CKAN_HOST e CKAN_KEY
# Após a criação, abra o arquivo e inclua os valores para cada variável
```
```bash
$ echo "CKAN_HOST=''\nCKAN_KEY=''" > .env
```
```
# Crie arquivo ".gitignore" com configuração para excluir arquivo ".env" do controle de versão git
```
```bash
$ echo ".env" > .gitignore
```
```
# Confira se configuração foi realizada com sucesso
# Comando abaixo deverá mostrar apenas criação/modificação de arquivo ".gitignore", não sendo apresentado nada para arquivo ".env"
```
```bash
$ git status
```

## Uso

**AVISO: VERIFIQUE AS VARIÁVEIS DE AMBIENTE E O CAMINHO DOS ARQUIVOS ANTES DE EXECUTAR CADA COMANDO. NÃO COPIE E COLE O CÓDIGO CEGAMENTE!**

### Acessando documentação do dpckan via terminal

```
# Informações gerais sobre o pacote e seus comandos
# Utilização das flags --help ou -h retornará o mesmo resultado
```
```bash
$ dpckan
```
```
# Informações sobre comandos dataset e resource
# Utilização das flags --help ou -h retornará o mesmo resultado
```
```bash
$ dpckan dataset
$ dpckan resource
```
```
# Informações sobre subcomandos dataset
# Utilização da flag -h retornará o mesmo resultado
```
```bash
$ dpckan dataset create --help
$ dpckan dataset update --help
```
```
# Informações sobre subcomandos resource
# Utilização da flag -h retornará o mesmo resultado
```
```bash
$ dpckan resource create --help
$ dpckan resource update --help
```

### Interrompendo execução em caso de erros de validação frictionless

Durante a execução dos comandos dpckan a biblioteca `frictionless` será utilizada para [validação](https://framework.frictionlessdata.io/docs/guides/validation-guide) local do conjunto de dados via `frictionless validate`. Erros durante esta validação serão informados ao usuário mas somente interromperão a execução se a flag `--stop` for passada como parâmetro, conforme demonstrado abaixo:

```bash
$ dpckan dataset create --stop
```

### Criando e atualizando com um conjunto de dados via terminal

- Para criar um conjunto de dados, execute o comando no diretório aonde o arquivo datapackage.json se encontra:

```bash
$ dpckan dataset create
```

- E para atualizar o conjunto de dados, execute o comando no diretório aonde o arquivo datapackage.json se encontra:

```bash
$ dpckan dataset update
```



### Criando e atualizando recursos via terminal

- Para criar um recurso, execute o seguinte comando no diretório aonde o arquivo datapackage.json se encontra. Não se esqueça de modificar o último argumento com o nome do recurso presente no arquivo datapackage.json que será criado

```bash
$ dpckan resource create --resource-name nome-recurso
```
```
# Utilização alias -rn para flag --resource-name
```
```bash
$ dpckan resource create -rn nome-recurso
```


- Para atualizar um recurso, execute o seguinte comando no diretório aonde o arquivo datapackage.json se encontra. Não se esqueça de modificar os últimos argumentos com o nome e id do recurso presente no arquivo datapackage.json que será atualizado

```
# Utilização flags --resource-name e --resource-id
```
```bash
$ dpckan resource update --resource-name nome-recurso --resource-id id-recurso
```
```
# Utilização alias -rn e -id para flags --resource-name e --resource-id respectivamente
```
```bash
$ dpckan resource update -rn nome-recurso -id id-recurso
```

### Usando as flags

- É possível atualizar um conjunto de dados ou recurso fora do diretório onde o arquivo datapackage.json se encontra utilizando a flag `--datapackage` ou `-dp` como abaixo:

```
# Utilização flag --datapackage
```
```bash
$ dpckan resource update --datapackage local/path/para/datapackage.json --resource-name nome-recurso --resource-id id-recurso
```
```
# Utilização alias -dp, -rn e -id para flags --datapackage,--resource-name e --resource-id respectivamente
```
```bash
$ dpckan resource update -dp local/path/para/datapackage.json -rn nome-recurso -id id-recurso
```
- Podemos usar as flags `-H` para o `CKAN_HOST`, `-k` para o `CKAN_KEY`, `-rn` para o `--resource_name` e `-id` para o `--resource_id`, por exemplo:

```
# Utilização flags --ckan-host, --ckan-key, --resource-name e --resource-id
```
```bash
$ dpckan resource update --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO --resource-name nome-recurso --resource-id id-recurso
```
```
# Utilização alias -H, -k, -rn e -id para flags --ckan-host, --ckan-key, --resource-name e --resource-id respectivamente
```
```bash
$ dpckan resource update -H $CKAN_HOST_PRODUCAO -k $CKAN_KEY_PRODUCAO -rn nome-recurso -id id-rescurso
```

Para mais exemplos, consulte a [documentação](https://dpckan.readthedocs.io/en/latest/)


### Check diff before updating a dataset

#### CLI

Running the `diff` command

```bash
dpckan dataset diff --datapackage some-path/datapackage.json 
Differences detected:
 - On field title
   - CKAN value A vowel letters dataset for tests CHANGED
   - DataPackage value A vowel letters dataset for tests
Equal fields: version, url, license_id, owner_org, tags, notes

```

#### Via Python code

Using the python `diff_dataset` function

```python
import os
from dpckan.diff_dataset import diff_dataset

CKAN_HOST = os.environ.get('CKAN_HOST')
CKAN_KEY = os.environ.get('CKAN_KEY')
datapackage_path = 'local/path/para/datapackage.json'

# A chamada de funções via código Python exige passagem de todos os argumentos
diffs, oks = diff_dataset(
  ckan_host=CKAN_HOST,
  ckan_key=CKAN_KEY,
  datapackage=datapackage_path
)

diffs
[{'field_name': 'title', 'ckan_value': 'A vowel letters dataset for tests CHANGED', 'datapackage_value': 'A vowel letters dataset for tests'}]

oks
['version', 'url', 'license_id', 'owner_org', 'tags', 'notes']

```


### Check diff for resources

#### CLI

Running the `diff` command for a resource

```bash
dpckan resource diff --datapackage some-path/datapackage.json --resource-name="This is the actual data"
Differences detected:
 - On field format
   - CKAN value: CSV
   - DataPackage value: csv
Equal fields: description
```

#### Via Python code

Using the python `diff_dataset` function

```python
import os
from dpckan.diff_resource import diff_resource

CKAN_HOST = os.environ.get('CKAN_HOST')
CKAN_KEY = os.environ.get('CKAN_KEY')
datapackage_path = 'local/path/para/datapackage.json'
datapackage_path = 'dpckan/tests/data-samples/datapackage-example/datapackage.json'
resource_name = 'This is the actual data'

# A chamada de funções via código Python exige passagem de todos os argumentos
diffs, oks = diff_resource(
  ckan_host=CKAN_HOST,
  ckan_key=CKAN_KEY,
  datapackage=datapackage_path,
  resource_name=resource_name
)

diffs
[{'field_name': 'format', 'ckan_value': 'CSV', 'datapackage_value': 'csv'}]

oks
['description']
```

## Desenvolvimento

### Contribuir para o projeto

- Prerequisitos:
    - Python 3.9 ou superior

- [Documentação de referência mostrando procedimentos necessários para contribuição em um projeto open source](https://www.dataschool.io/how-to-contribute-on-github/)

- Passos básicos:
    - Crie um fork do repositório do projeto
    - Clone o repositório criado em sua conta após o fork
    - Navegue até o repositório clonado em sua máquina
    - Crie e ative um ambiente virtual Python para utilizar o projeto

- Crie um branch para realizar as modificações necessárias
- Realize o push da branch criada
- Abra um PR explicando os motivos da mudança e como esta auxiliará no desenvolvimento do projeto

### Atualizar versão

Conforme relatado no [issue 6](https://github.com/dados-mg/dpkgckanmg/issues/6), atualização de versões no [Pypi](https://pypi.org/) deve seguir [estes os passos](https://github.com/dados-mg/dpckan/issues/6#issuecomment-851678297)

## Licença

O **dpckan** é licenciado sob a licença MIT.
Veja o arquivo [`LICENSE.md`](LICENSE.md) para mais detalhes.
