# Data package manager para CKAN (dpckan)

O `dpckan` é um pacote python, acessível via interface CLI, utilizado para catalogação inicial e atualização de conjuntos de dados documentados de acordo com o padrão de metadados [Frictionless Data](https://frictionlessdata.io/) (ie. pacotes de dados) em uma instância do [CKAN](https://ckan.org/).

## Instalação e configuração

O `dpckan` está disponível no Python Package Index - [PyPI](https://pypi.org/project/dpckan/) e pode ser instalado utilizando-se o comando abaixo:

```bash
# Antes de executar o comando abaixo lembre-se que ambiente python deverá estar ativo
$ pip install dpckan
```

Todos os comandos exigem a indicação de uma instância CKAN (ex: https://demo.ckan.org/) e de uma chave válida para autenticação na referida instância. Essas configurações podem ser informadas como argumento na invocação de cada comando ou com as variáveis de ambientes `CKAN_HOST` e `CKAN_KEY` para instância e chave respectivamente.

O cadastro das variáveis de ambiente `CKAN_HOST` e `CKAN_KEY`, necessárias para invocação de cada comando, deverá ser realizada conforme sistema operacional do usuário, podendo ser utilizado como referência links como [este para windows](https://professor-falken.com/pt/windows/como-configurar-la-ruta-y-las-variables-de-entorno-en-windows-10/), [este para linux](https://ricardo-reis.medium.com/vari%C3%A1veis-de-ambiente-no-linux-debian-f677d6ca94c) ou [este para mac](https://support.apple.com/pt-br/guide/terminal/apd382cc5fa-4f58-4449-b20a-41c53c006f8f/mac).


**CUIDADO: SOMENTE UTILIZE A OPÇÃO SUGERIDA ABAIXO SE POSSUIR CONHECIMENTO TÉCNICO E FAMILIARIDADE COM O ASSUNTO, EVITANDO ASSIM PROBLEMAS COM ACESSO DE TERCEIROS NÃO AUTORIZADOS EM SUA INSTÂNCIA CKAN**

Alternativamente, o cadastro destas variáveis poderá ser realizado em arquivo .env, na raiz do conjunto de dados, sendo necessário a inclusão do novo arquivo .env em arquivo .gitignore, evitando assim a sincronização e consequente publicização destas chaves em repositórios online como [github](https://github.com/), conforme demostrado abaixo:


```bash
# CUIDADO: SOMENTE EXECUTE OS COMANDOS ABAIXO SE OS ARQUIVO .env e .gitignore NÃO EXISTIREM NA RAIZ DO CONJUNTO DE DADOS
# CUIDADO: CASO COMANDOS ABAIXO SEJAM EXECUTADOS COM .env e .gitignore EXISTENTES TODO CONTEÚDO DOS MESMOS SERÁ APAGADO
# CUIDADO: SOMENTE EXECUTE OS COMANDOS ABAIXO SE TIVER CERTEZA E CONHECIMENTO DO QUE SERÁ FEITO

# Crie arquivo .env com estrutura para receber chaves CKAN_HOST e CKAN_KEY
# Após a criação, abra o arquivo e inclua os valores para cada variável
$ echo "CKAN_HOST=''\nCKAN_KEY=''" > .env

# Crie arquivo .gitignore com configuração para excluir arquivo .env do controle de versão git
$ echo ".env" > .gitignore

# Confira se configuração foi realizada com sucesso
# Comando abaixo deverá mostrar apenas criação/modificação de arquivo .gitignore, não sendo apresentado nada para arquivo .env
$ git status
```

Recomendamos fortemente a utilização da primeira opção sugerida acima, via cadastro de variáveis de ambiente, por considerarmos a facilidade de erro da segunda e consequente publicização das chaves CKAN em repositórios online.

## Uso

### Acessando documentação dpckan via terminal

```bash
# Informações gerais sobre o pacote e seus comandos
# Utilização da flag --help retornará o mesmo resultado
$ dpckan

# Informações sobre comandos dataset e resource
# Utilização da flag --help retornará o mesmo resultado
$ dpckan dataset
$ dpckan resource

# Informações sobre subcomandos dataset
$ dpckan dataset create --help
$ dpckan dataset update --help

# Informações sobre subcomandos resource
$ dpckan resource create --help
$ dpckan resource update --help
```

### Criação de conjunto de dados via terminal

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra:

```bash
$ dpckan dataset create
```

- Executar o comando fora do diretório aonde o arquivo datapackage.json se encontra. Não copie e cole o comando abaixo cegamente, modifique o último argumento com o caminho local para arquivo datapackage.json

```bash
# Utilização flag --datapackage
$ dpckan dataset create --datapackage local/path/para/datapackage.json

# Utilização alias -dp para flag --datapackage
$ dpckan dataset create -dp local/path/para/datapackage.json
```

- Executar o comando no diretório aonde o arquivo datapackage.json se encontra utilizando variáveis de ambiente com nomenclatura diferente de `CKAN_HOST` e `CKAN_KEY`. Não copie e cole o comando abaixo cegamente, modifique o nome das variáveis de ambiente para a sua realidade.

```bash
# Utilização flag --ckan-host e --ckan-key
$ dpckan dataset create --ckan-host $CKAN_HOST_PRODUCAO --ckan-key $CKAN_KEY_PRODUCAO

# Utilização alias -H e -K para flags --ckan-host e --ckan-key respectivamente
$ dpckan dataset create -H $CKAN_HOST_PRODUCAO -k $CKAN_KEY_PRODUCAO
```

### Atualização de conjunto de dados via terminal

### Criação de recursos via terminal

### Atualização de recursos via terminal

## Desenvolvimento
