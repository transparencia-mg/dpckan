import sys
import click
from ckanapi import RemoteCKAN
from dpckan.functions import (
  load_complete_datapackage,
  is_dataset_published,
  resource_diff
)


def diff_resource(ckan_host, ckan_key, datapackage, resource_name):
  """
  Detect changes between datapackage an the created dataset. 

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

  A list of (non-expected) differences between the datapackage and the CKAN dataset

  """
  package = load_complete_datapackage(datapackage)

  ckan_instance = RemoteCKAN(ckan_host, apikey=ckan_key)
  if not is_dataset_published(ckan_instance, package):
    raise Exception('Conjunto de dados nao existente.')

  ckan_instance = RemoteCKAN(ckan_host, apikey=ckan_key)
  return resource_diff(ckan_instance, package, resource_name)


@click.command()
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: https://demo.ckan.org/")  # -H para respeitar convenção de -h ser help
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
@click.option('--datapackage', '-dp', required=True, default='datapackage.json')
@click.option('--resource-name', '-rn', required=True)
def diff_resource_cli(ckan_host, ckan_key, datapackage, resource_name):
  """
  Detect changes between datapackage resource an a CKAN resource. 

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

    Nome do recurso, presente no arquivo datapackage.json, que será atualizado.

  Retorna:

  -------

  A list of (non-expected) differences between the datapackage and the CKAN dataset
  """

  diffs, oks = diff_resource(ckan_host, ckan_key, datapackage, resource_name)
  if len(diffs) == 0:
    click.echo("There are no differences")
  else:
    click.echo("Differences detected:")
    for diff in diffs:
      click.echo(f" - On field {diff['field_name']}")
      if diff.get('ckan_value'):
        click.echo(f"   - CKAN value: {diff['ckan_value']}")
      if diff.get('datapackage_value'):
        click.echo(f"   - DataPackage value: {diff['datapackage_value']}")
      if diff.get('error'):
        click.echo(f"   - Error: {diff['error']}")
  if len(oks) == 0:
    click.echo("No equal field found")
  else:
    click.echo("Equal fields: {}".format(', '.join(oks)))
