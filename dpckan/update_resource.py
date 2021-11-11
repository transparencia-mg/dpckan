import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_resource_validations
from dpckan.functions import (load_complete_datapackage, 
                              update_datapackage_json_resource, 
                              resource_update,
                              resource_update_datastore_metadata,
                              dataset_update)

def update_resource(ckan_host, ckan_key, datapackage, resource_id, resource_name, stop):
  """
  Função responsável pela atualização de um recurso em conjunto de dados já existente na instância CKAN desejada.

  Parâmetros:

  ----------

  ckan_host: string

    host ou ambiente da instância CKAN para a qual se deseja atualizar conjunto de dados.
    Exemplo: https://demo.ckan.org/

  ckan_key: string

    Chave CKAN do usuário e ambiente para a qual se deseja atualizar conjunto de dados.

  datapackage: string

    Caminho local para arquivo datapackage.json.

  resource_id: string

    Id do recurso a ser atualizado na instância CKAN desejada. Ultima parte da url do recurso no CKAN.

  resource_name: string

    Nome do recurso que será atualizado. Propriedade `name` do resource dentro do arquivo datapackage.json.

  Retorna:

  -------

  Recurso atualizado em um conjunto de dados previamente publicado no ambiente desejado.
  """
  package = load_complete_datapackage(datapackage)
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  run_resource_validations(ckan_instance, package, stop)
  # Show package to find datapackage.json resource id
  # Update datapakcage.json resource
  update_datapackage_json_resource(ckan_instance, package)
  # dataset_update(ckan_instance, package)
  resource_update(ckan_instance,
                  resource_id,
                  package.get_resource(resource_name))
  resource_update_datastore_metadata(ckan_instance,
                            resource_id,
                            package.get_resource(resource_name))


@click.command()
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: http://dados.mg.gov.br ou https://dados.mg.gov.br")  # -H para respeitar convenção de -h ser help
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
@click.option('--datapackage', '-dp', required=True, default='datapackage.json',
              help="Caminho para arquivo datapackage.json")
@click.option('--resource-id', '-id', required=True,
              help="Id do recurso a ser atualizado na instância CKAN desejada. Ultima parte da url do recurso no CKAN")
@click.option('--resource-name', '-rn', required=True,
              help="Nome do recurso que será atualizado. Propriedade `name` do resource dentro do arquivo datapackage.json")
@click.option('--stop', '-s', is_flag=True, help="Parar execução caso validação frictionless retorne algum erro")
def update_resource_cli(ckan_host, ckan_key, datapackage, resource_id, resource_name, stop):
  """
  Função CLI responsável pela atualização de um recurso em conjunto de dados já existente na instância CKAN desejada.

  Por padrão, função buscará host e key da instância CKAN nas variáveis de ambiente CKAN_HOST e CKAN_KEY cadastradas na máquina ou
  em arquivo .env na raiz do dataset.

  Parâmetros:

  ----------

  ckan_host: string (não obrigatório caso variável CKAN_HOST esteja cadastrada na máquina ou em arquivo .env)

    host ou ambiente da instância CKAN para a qual se deseja publicar conjunto de dados.
    Exemplo: https://demo.ckan.org/

  ckan_key: string (não obrigatório caso variável CKAN_KEY esteja cadastrada na máquina ou em arquivo .env)

    Chave CKAN do usuário e ambiente para a qual se deseja publicar conjunto de dados.

  datapackage: string (não obrigatório caso comando seja executado no mesmo diretório do arquivo datapackage.json)

    Caminho local para arquivo datapackage.json.

  resource_id: string

    Id do recurso a ser atualizado na instância CKAN desejada. Ultima parte da url do recurso no CKAN.

  resource_name: string

    Nome do recurso que será atualizado. Propriedade `name` do resource dentro do arquivo datapackage.json.

  Retorna:

  -------

  Recurso atualizado em um conjunto de dados previamente publicado no ambiente desejado.
  """
  update_resource(ckan_host, ckan_key, datapackage, resource_id, resource_name, stop)
