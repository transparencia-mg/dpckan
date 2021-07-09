import os
import json
import sys
import click
from ckanapi import RemoteCKAN

def run_validations(host, key):
  """
    Run validations before dataset publication
  """
  is_datapackage_present()
  is_host_valid(host)

def is_host_valid(host):
  demo = RemoteCKAN(host)
  try:
    ckan_exist = demo.action.site_read()
  except:
    sys.exit(1)

def is_datapackage_present():
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
  try:
    with open('datapackage.json','r', encoding="utf-8") as json_file:
      datapackage_keys = json.load(json_file)
      if f"name" in datapackage_keys.keys():
        pass
      else:
        click.echo("----Arquivo datapackage.json sem a chave 'name' obrigatória----")
        sys.exit(1)
      if f"resources" in datapackage_keys.keys():
        pass
      else:
        click.echo("----Arquivo datapackage.json sem a chave 'resources' obrigatória----")
        sys.exit(1)
  except FileNotFoundError:
    click.echo("----Arquivo datapackage.json não encontrado na raiz do dataset----")
    sys.exit(1)
  except json.decoder.JSONDecodeError:
    click.echo("----Arquivo datapackage.json com algum problema de sintaxe ou em branco----")
    sys.exit(1)
