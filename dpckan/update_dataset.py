import click
from ckanapi import RemoteCKAN
from dpckan.functions import (load_complete_datapackage, dataset_update, update_datapackage_json_resource)
                              
def update(ckan_host, ckan_key, datapackage, metadata):
  """
  Função responsável pela atualização de um conjunto de dados na instância CKAN desejada.

  Parâmetros:

  ----------

  ckan_host: string

    host ou ambiente da instância CKAN para a qual se deseja atualizar conjunto de dados.
    Exemplo: https://demo.ckan.org/

  ckan_key: string

    Chave CKAN do usuário e ambiente para a qual se deseja atualizar conjunto de dados.

  datapackage: string

    Caminho local para arquivo datapackage.json.

  Retorna:

  -------

  Conjunto de dados atualizado no ambiente desejado.
  """
  package = load_complete_datapackage(datapackage)

  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)

  # update_datapackage_json_resource(ckan_instance, package)
  dataset_update(ckan_instance, package, metadata)


@click.command(name='update')
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: https://demo.ckan.org/")
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
@click.option('--datapackage', '-dp', required=True, default='datapackage.json',
              help="Caminho para arquivo datapackage.json")
@click.option('--metadata', '-m', is_flag=False, help="Indica se os recursos publicados terão metadados carregados no datastore")
def update_cli(ckan_host, ckan_key, datapackage, metadata):
  """
  Função CLI responsável pela atualização de um conjunto de dados na instância CKAN desejada.

  Por padrão, função buscará host e key da instância CKAN nas variáveis de ambiente CKAN_HOST e CKAN_KEY cadastradas na máquina ou
  em arquivo .env na raiz do dataset.

  Parâmetros:

  ----------

  ckan_host: string (não obrigatório caso variável CKAN_HOST esteja cadastrada na máquina ou em arquivo .env)

    host ou ambiente da instância CKAN para a qual se deseja atualizar conjunto de dados.
    Exemplo: https://demo.ckan.org/

  ckan_key: string (não obrigatório caso variável CKAN_KEY esteja cadastrada na máquina ou em arquivo .env)

    Chave CKAN do usuário e ambiente para a qual se deseja atualizar conjunto de dados.

  atapackage: string (não obrigatório caso comando seja executado no mesmo diretório do arquivo datapackage.json)

    Caminho local para arquivo datapackage.json.

  Retorna:

  -------

  Conjunto de dados atualizado no ambiente desejado.
  """
  update(ckan_host, ckan_key, datapackage, metadata)

