import json
import sys
import click
from frictionless import validate
from dpckan.functions import (
                              is_dataset_published,
                              dataset_path,
                              )

def run_dataset_validations(ckan_instance, package):
  """
    Run validations before dataset publication
  """
  is_host_valid(ckan_instance)
  is_dataset_published_check(ckan_instance, package)
  is_datapackage_valid(package)
  is_owner_org_valid(ckan_instance, package)


def run_resource_validations(ckan_instance, package):
  """
    Run validations before dataset publication
  """
  is_host_valid(ckan_instance)
  is_datapackage_valid(package)
  is_owner_org_valid(ckan_instance, package)

def is_host_valid(ckan_instance):
  demo = ckan_instance
  try:
    ckan_exist = demo.action.site_read()
  except:
    print(f'Host {ckan_instance.address} not exist')
    sys.exit(1)

def is_dataset_published_check(ckan_instance, package):
  dataset = dataset_path(ckan_instance.address, package)
  if is_dataset_published(ckan_instance, package.name):
    click.echo(f'Dataset {dataset} already published')
    sys.exit(1)

def is_owner_org_valid(ckan_instance, package):
  dataset = dataset_path(ckan_instance.address, package)
  result = ckan_instance.action.organization_list(id = package.name)
  if package['owner_org'] not in result:
    click.echo(f"{package['owner_org']} not exist in {dataset}")
    sys.exit(1)

def is_datapackage_valid(package):
  """
  Verifica a existência da chave "datapackage_resource_id" no arquivo datapackage.json para o ambiente desejado (homologação ou produção)
  Existência da chave "datapackage_resource_id" significa que pacote já foi publicado no ambiente desejado
  Arquivo datapackage.json deve estar na raiz do dataset
  Trata erro para:
   - datapackage.json inexistente
   - algum erro de sintaxe no arquivo datapackage.json, ou até mesmo arquivo existente mas em branco

  Parameters
  ----------
    env
    homologacao: homologa.cge.mg.gov.br/
    producao: dados.mg.gov.br/


  Returns
  -------
  string
    valor correspondente a chave "datapackage_resource_id" do ambiente solicitado, quando a mesma existir
  None
    quando a chave não existir
  """
  if f"name" in package.keys():
    pass
  else:
    click.echo("Arquivo datapackage.json sem a propriedade `name` obrigatória")
    sys.exit(1)
  if f"resources" in package.keys():
    pass
  else:
    click.echo("Arquivo datapackage.json sem a propriedade `resources` obrigatória")
    sys.exit(1)
  if f"owner_org" in package.keys():
    pass
  else:
    click.echo("Arquivo datapackage.json sem a propriedade `owner_org` obrigatória")
    sys.exit(1)

