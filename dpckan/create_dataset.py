import sys
import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_dataset_validations
from dpckan.functions import (delete_dataset, 
                              dataset_create,
                              is_dataset_published,
                              load_complete_datapackage)

def create(ckan_host, ckan_key, datapackage, stop, metadata):
  """
  Função responsável pela publicação de um conjunto de dados na instância CKAN desejada.

  Parâmetros:

  -------

  ckan_host: string

    host ou ambiente da instância CKAN para a qual se deseja publicar conjunto de dados.
    Exemplo: https://demo.ckan.org/

  ckan_key: string

    Chave CKAN do usuário e ambiente para a qual se deseja publicar conjunto de dados.

  datapackage: string

    Caminho local para arquivo datapackage.json.

  Retorna:

  -------

  Conjunto de dados publicado no ambiente desejado.
  """
  local_datapackage = load_complete_datapackage(datapackage)
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  run_dataset_validations(ckan_instance, local_datapackage, stop)
  try:
    dataset_create(ckan_instance, local_datapackage, metadata)
    print(f"Conjunto de dados {local_datapackage.name} publicado. Datapackage.json Atualizado com id dos recursos publicados.")
  except Exception:
    delete_dataset(ckan_instance, local_datapackage.name)
    print(f"Erro durante criação do conjunto de dados {local_datapackage.name}")
    sys.exit(1)

@click.command(name='create')
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: https://demo.ckan.org/")  # -H para respeitar convenção de -h ser help
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
@click.option('--datapackage', '-dp', required=True, default='datapackage.json',
              help="Caminho para arquivo datapackage.json")
@click.option('--stop', '-s', is_flag=True, help="Parar execução caso validação frictionless retorne algum erro")
@click.option('--metadata', '-m', is_flag=False, help="Indica se os recursos publicados terão metadados carregados no datastore")
def create_cli(ckan_host, ckan_key, datapackage, stop, metadata):
  """
  Função CLI responsável pela publicação de um conjunto de dados na instância CKAN desejada.

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

  Retorna:

  -------

  Conjunto de dados publicado no ambiente desejado.
  """
  create(ckan_host, ckan_key, datapackage, stop, metadata)
