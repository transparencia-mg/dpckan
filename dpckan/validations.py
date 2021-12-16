import json
import sys
import click
from dpckan.functions import is_dataset_published
from frictionless import validate

def run_dataset_validations(ckan_instance, package, stop):
  """
    Run validations before dataset publication
  """
  is_host_valid(ckan_instance)
  is_dataset_published_check(ckan_instance, package)
  is_datapackage_valid(package)
  is_owner_org_valid(ckan_instance, package)


def run_resource_validations(ckan_instance, package, stop):
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
    print(f'CKAN Host {ckan_instance.address} inexistente.')
    sys.exit(1)

def is_dataset_published_check(ckan_instance, package):
  if is_dataset_published(ckan_instance, package):
    click.echo(f'Dataset {package.name} já publicado acesse {ckan_instance.address}/dataset/{package.name}')
    sys.exit(1)

def is_owner_org_valid(ckan_instance, package):
  result = ckan_instance.action.organization_list(id = package.name)
  if package['owner_org'] not in result:
    click.echo(f"Propriedade `owner_org` {package['owner_org']} não existente na instância CKAN {ckan_instance.address}")
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

