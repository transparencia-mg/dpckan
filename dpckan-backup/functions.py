import os
from pathlib import Path
from dotenv import load_dotenv
import json
import codecs
import sys
import click

def is_datapackage_present(env):
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
    with codecs.open('datapackage.json','r', 'utf-8-sig') as json_file:
      datapackage_keys = json.load(json_file)
      if f"datapackage_resource_id_{env}" in datapackage_keys.keys():
        click.echo("----Iniciando atualização do Dataset----")
        return datapackage_keys[f"datapackage_resource_id_{env}"]
      else:
        click.echo("----Iniciando Publicação do Dataset----")
        return None
  except FileNotFoundError:
    click.echo("----Arquivo datapackage.json não encontrado na raiz do dataset----")
    sys.exit(1)
  except json.decoder.JSONDecodeError:
    click.echo("----Arquivo datapackage.json com algum problema de sintaxe ou em branco----")
    sys.exit(1)


def get_ckan_key(env):
  env_path = Path('.', '.env')
  load_dotenv(dotenv_path=env_path)
  if env == "homologacao":
    return os.getenv('CKAN_KEY_HOMOLOGACAO_ENV')
  elif env == "producao":
    return os.getenv('CKAN_KEY_PRODUCAO_ENV')
  else:
    print("Retornar um erro - não pode ser diferente de produção ou homologaçao")
