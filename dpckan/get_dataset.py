import sys
import click
from ckanapi import RemoteCKAN
from dpckan.functions import (delete_dataset,
                              dataset_create,
                              is_dataset_published,
                              load_complete_datapackage)

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
