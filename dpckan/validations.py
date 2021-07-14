import json
import sys
import click
from ckanapi import RemoteCKAN

def run_validations(host, key, datapackage):
  """
    Run validations before dataset publication
  """
  is_datapackage_present(datapackage)
  is_host_valid(host)

def is_host_valid(host):
  demo = RemoteCKAN(host)
  try:
    ckan_exist = demo.action.site_read()
  except:
    sys.exit(1)

def is_datapackage_present(datapackage):
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
  if f"name" in datapackage.keys():
    pass
  else:
    click.echo("----Arquivo datapackage.json sem a chave 'name' obrigatória----")
    sys.exit(1)
  if f"resources" in datapackage.keys():
    pass
  else:
    click.echo("----Arquivo datapackage.json sem a chave 'resources' obrigatória----")
    sys.exit(1)

