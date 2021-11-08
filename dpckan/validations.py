import json
import sys
import click
from dpckan.functions import is_dataset_published
from frictionless import validate

def run_dataset_validations(ckan_instance, package):
  """
    Run validations before dataset publication
  """
  is_dataset_valid(package)
  is_datapackage_valid(package)
  is_host_valid(ckan_instance)
  is_dataset_published_check(ckan_instance, package)

def run_resource_validations(ckan_instance, package):
  """
    Run validations before dataset publication
  """
  is_dataset_valid(package)
  is_datapackage_valid(package)
  is_host_valid(ckan_instance)

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

def is_dataset_valid(package):
  report = validate(package)
  if report.valid == False:
    for error in report.errors:
      click.echo(error.message)
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
    click.echo("Arquivo datapackage.json sem a chave 'name' obrigatória")
    sys.exit(1)
  if f"resources" in package.keys():
    pass
  else:
    click.echo("Arquivo datapackage.json sem a chave 'resources' obrigatória")
    sys.exit(1)

