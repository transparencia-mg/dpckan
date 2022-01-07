import os
import click
from ckanapi import RemoteCKAN
from dpckan.functions import (download_resource_from_ckan)

def get_dataset(ckan_host, dataset_id):
  """
  Função responsável por realizar o download de um conjunto de dados publicado na instância CKAN informada.

  Parâmetros:

  -------

  ckan_host: string

    host ou ambiente da instância CKAN para a qual se deseja buscar o conjunto de dados.
    Exemplo: https://demo.ckan.org/

  dataset_id: string

    Nome do conjunto de dados na instância CKAN informada.

  Retorna:

  -------

  Download do conjunto de dados desejado.
  """
  ckan_instance = RemoteCKAN(ckan_host)
  dataset_information = ckan_instance.action.package_show(id = dataset_id)
  if not os.path.exists('data'):
    os.makedirs('data')
  for resource in dataset_information["resources"]:
    import ipdb; ipdb.set_trace(context=10)
    resource_url = resource["url"]
    resource_content = download_resource_from_ckan(resource_url)
    if resource["name"] == 'datapackage.json':
      open('datapackage.json', 'w', encoding='utf-8').write(resource_content.content)
    else:
      file_name = resource_url.split('/')[-1]
      open(f'data/{file_name}', 'wb', encoding='utf-8').write(resource_content.content)

@click.command(name='get')
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: https://demo.ckan.org/")  # -H para respeitar convenção de -h ser help
@click.option('--dataset-id', '-id', required=True,
              help="Nome do conjunto de dados na instância CKAN informada")
def get_dataset_cli(ckan_host, dataset_id):
  """
  Função CLI responsável por realizar o download de um conjunto de dados publicado na instância CKAN informada.

  Por padrão, função buscará host da instância CKAN na variável de ambiente CKAN_HOST cadastrada na máquina ou
  em arquivo .env na raiz do dataset.

  Parâmetros:

  -------

  ckan_host: string

    host ou ambiente da instância CKAN para a qual se deseja buscar o conjunto de dados.
    Exemplo: https://demo.ckan.org/

  dataset_id: string

    Nome do conjunto de dados na instância CKAN informada.

  Retorna:

  -------

  Download do conjunto de dados desejado.
  """
  get_dataset(ckan_host, dataset_id)
