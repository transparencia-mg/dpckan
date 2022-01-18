import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_resource_validations
from dpckan.functions import (load_complete_datapackage, 
                              update_datapackage_json_resource, 
                              resource_create,
                              resource_update_datastore_metadata,
                              dataset_update,
                              update_datapackage_with_ckan_ids)

def create_resource(ckan_host, ckan_key, datapackage, resource_name, stop):
  """
  Função responsável pela publicação de um recurso em conjunto de dados já existente na instância CKAN desejada.

  Parâmetros:

  ----------

  ckan_host: string

    host ou ambiente da instância CKAN para a qual se deseja publicar conjunto de dados.
    Exemplo: https://demo.ckan.org/

  ckan_key: string

    Chave CKAN do usuário e ambiente para a qual se deseja publicar conjunto de dados.

  datapackage: string

    Caminho local para arquivo datapackage.json.

  resource_name: string

    Nome do recurso que será criado (presente no arquivo datapackage.json).

  Retorna

  -------

  Recurso criado em um conjunto de dados previamente publicado no ambiente desejado.
  """
  package = load_complete_datapackage(datapackage)
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  run_resource_validations(ckan_instance, package, stop)
  # Create new resource
  resource_ckan = resource_create(ckan_instance,
                                  package.name,
                                  package.get_resource(resource_name))
  resource_update_datastore_metadata(ckan_instance,
                            resource_ckan['id'],
                            package.get_resource(resource_name))
  # Update datapackage
  # Show package to find datapackage.json resource id
  ckan_datapackage_resources = ckan_instance.action.package_show(id=package.name)["resources"]
  # Filtering datackage id - https://stackoverflow.com/a/48192370/11755155
  datapackage_resource_id = [i["id"] for i in ckan_datapackage_resources if i["name"] == "datapackage.json"][0]
  # Update datapackage localy
  update_datapackage_with_ckan_ids(ckan_instance, package, resource_name, resource_ckan['id'])
  # Update datapackage remotly
  update_datapackage_json_resource(ckan_instance, package, datapackage_resource_id)

@click.command()
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: https://demo.ckan.org/")  # -H para respeitar convenção de -h ser help
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
@click.option('--datapackage', '-dp', required=True, default='datapackage.json',
              help="Caminho para arquivo datapackage.json")
@click.option('--resource-name', '-rn', required=True)
@click.option('--stop', '-s', is_flag=True, help="Parar execução caso validação frictionless retorne algum erro")
def create_resource_cli(ckan_host, ckan_key, datapackage, resource_name, stop):
  """
  Função CLI responsável pela publicação de um recurso em conjunto de dados já existente na instância CKAN desejada.

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

  resource_name: string

    Nome do recurso que será criado (presente no arquivo datapackage.json).

  Retorna:

  -------

  Recurso criado em um conjunto de dados previamente publicado no ambiente desejado.
  """
  create_resource(ckan_host, ckan_key, datapackage, resource_name, stop)

