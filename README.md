# Data package manager para CKAN (dpckan)

[![Coverage](https://img.shields.io/codecov/c/github/transparencia-mg/dpckan/dev)](https://codecov.io/gh/transparencia-mg/dpckan)

O `dpckan` é um pacote Python, acessível via interface [CLI](https://pt.wikipedia.org/wiki/Interface_de_linha_de_comandos), utilizado para criação e atualização de conjuntos de dados e recursos (documentados de acordo com o padrão de metadados [Frictionless Data](https://frictionlessdata.io/)) em uma instância do [CKAN](https://ckan.org/).

## Linha cronológica de ações para uso do dpckan

configurar variável de ambiente ==> criar e ligar venv ==> instalar pacote ==> criar/atualizar conjunto ==> criar/atualizar recurso

## Funções/comandos

1. Criar conjunto/dataset: ````$ dpckan dataset create````

2. Atualizar conjunto/dataset: ````$ dpckan dataset update````

3. Criar recurso/arquivo: ````$ dpckan resource <resource-name> create````

4. Atualizar recurso/arquivo: ````$ dpckan resource <resource-name> <resource-id> update````

Curiosidades: Consulte a comparação do dpckan com alguns [projetos relacionados](RELATED_PROJECTS.md).

[Documentação complementar](https://dpckan.readthedocs.io/en/latest/)

## Instalação

O `dpckan` está disponível no Python Package Index - [PyPI](https://pypi.org/project/dpckan/) e pode ser instalado utilizando-se o comando abaixo:

```bash
# Antes de executar o comando abaixo lembre-se que ambiente Python deverá estar ativo
$ pip install dpckan
```

## Uso

- Antes de executar cada comando verifique:
    - Se as variáveis de ambiente estão definidas corretamente - veja como [aqui](https://github.com/transparencia-mg/dpckan/blob/dev/VARIAVEIS_AMBIENTE.md);
    - O local onde os comandos serão executados, pois a execução no mesmo diretório do arquivo datapackage.json simplificará o trabalho;
    - Não copie e cole os comandos sugeridos abaixo cegamente, indicações entre "<>" sevirão para ilustrar variáveis a serem adequadas para a realidade do usuário.




### Acessando documentação do dpckan via terminal

```bash
# Informações gerais sobre o pacote e seus comandos
$ dpckan --help

# Informações sobre comandos dataset e resource
$ dpckan dataset --help
$ dpckan resource --help

# Informações sobre sub-comandos dataset
$ dpckan dataset create --help
$ dpckan dataset update --help

# Informações sobre sub-comandos resource
$ dpckan resource create --help
$ dpckan resource update --help
```

### Interrompendo execução em caso de erros de validação frictionless

Durante a execução dos comandos dpckan a biblioteca `frictionless` será utilizada para [validação](https://framework.frictionlessdata.io/docs/guides/validation-guide) local do conjunto de dados via `frictionless validate`. Erros durante esta validação serão informados ao usuário mas somente interromperão a execução se a flag `--stop` for passada como parâmetro, conforme demonstrado abaixo:

```bash
$ dpckan dataset create --stop
```
### Baixando conjuntos de dados publicados em instância CKAN

- Para baixar um conjunto de dados publicado em alguma instância do CKAN utilize o comando abaixo:

```bash
$ dpckan dataset get --dataset-id dataset-link
```

### Criando e atualizando um conjunto de dados via terminal

Para criar um conjunto de dados, execute o comando no diretório aonde o arquivo datapackage.json se encontra:

```bash
$ dpckan dataset create
```

E para atualizar o conjunto de dados, execute o comando no diretório aonde o arquivo datapackage.json se encontra:

```bash
$ dpckan dataset update
```

CUIDADO: A atualização de conjunto de dados presupõe:

* Criação do conjunto de dados via comando `dpckan dataset create`;
* Criação de recursos via comando `dpckan resource create`; e
* Igualdade entre o número e nome dos recursos locais e da instância CKAN.

### Criando e atualizando recursos via terminal

CUIDADO: Recursos com nomes iguais além de desrespeitar a [especificação frictionless](https://specs.frictionlessdata.io/data-resource/#metadata-properties) confundem o usuário.

Para criar um recurso, execute o seguinte comando no diretório aonde o arquivo datapackage.json se encontra.

```bash
$ dpckan resource create --resource-name <nome-recurso>
```

Para atualizar um recurso, execute o seguinte comando no diretório aonde o arquivo datapackage.json se encontra.

```bash
$ dpckan resource update --resource-name <nome-recurso> --resource-id <id-recurso>
```

## Contribuições

Pré-requisitos: Python 3.9 ou superior

[Documentação de referência mostrando procedimentos necessários para contribuição em um projeto open source](https://www.dataschool.io/how-to-contribute-on-github/)

- Passos básicos:
    - Crie um fork do repositório do projeto;
    - Clone o repositório criado em seu github após o fork;
    - Navegue até o repositório clonado em sua máquina;
    - Crie e ative um ambiente virtual Python para utilizar o projeto;
    - Crie um branch para realizar as modificações necessárias;
    - Realize o push da branch criada; e
    - Abra um PR explicando os motivos da mudança e como esta auxiliará no desenvolvimento do projeto.

### Atualizar versão

Conforme relatado no [issue 6](https://github.com/dados-mg/dpkgckanmg/issues/6), atualização de versões no [Pypi](https://pypi.org/) deve seguir [estes os passos](https://github.com/dados-mg/dpckan/issues/6#issuecomment-851678297)

## Licença

O **dpckan** é licenciado sob a licença MIT.
Veja o arquivo [`LICENSE.md`](LICENSE.md) para mais detalhes.
