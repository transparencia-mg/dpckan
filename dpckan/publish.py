import urllib
import os
import requests
import json
import click
from dpckan.validations import run_validations
from dpckan.functions import (os_slash, datapackage_path, lerDadosJsonMapeado,
                              delete_dataset, lerCaminhoRelativo, importaDataSet)

@click.command()
@click.option('--host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: http://dados.mg.gov.br ou https://dados.mg.gov.br")  # -H para respeitar convenção de -h ser help
@click.option('--key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
def publish(host, key):
  """
  Função responsável pela publicação/atualização de um conjunto de dados no ambiente (host) desejado.

  Por padrão, função buscará host e key da instância CKAN para qual e deseja publicar/atualizar dataset
  nas variáveis de ambiente CKAN_HOST e CKAN_KEY cadastradas na máquina ou em arquivo .env na raiz do dataset.

  Parameters
  ----------
  host: string (não obrigatório caso variável CKAN_HOST esteja cadastrada na máquina ou em arquivo .env)
    host ou ambiente da instância CKAN para a qual se deseja publicar/atualizar dataset.
    Exemplo: http://dados.mg.gov.br ou https://dados.mg.gov.br
  key: string (não obrigatório caso variável CKAN_KEY esteja cadastrada na máquina ou em arquivo .env)
    Chave CKAN do usuário e ambiente para a qual se deseja publicar/atualizar dataset

  Returns
  -------
    Dataset publicado/atualizado no ambiente desejado
  """
  click.echo("----Iniciando publicação/atualização datasest----")
  click.echo(f"----Publicação/atualização datasest em {host}----")
  run_validations()
  path_datapackage = datapackage_path()
  dataset_dict = lerDadosJsonMapeado(host,path_datapackage,key,'false','null')
  # Deleting dataset if it exists
  delete_dataset(host, key, json.loads(dataset_dict)['name'])
  if(os.path.isfile(path_datapackage)):
      comandoDelete = r'del /f filename'
      so = "WINDOWS"
      caminhoRelativo = os_slash + lerCaminhoRelativo(path_datapackage);
      privado = True
      autor = 'Usuario teste'
      tags = [{"name": "my_tag"}, {"name": "my-other-tag"}]
      if ((caminhoRelativo.find('http')) or (len(os.listdir(caminhoRelativo)) > 0)):
         importaDataSet(key,"",".","csv",privado,autor,type,tags,os_slash,"",comandoDelete,so,host)
         click.echo('----Publicação/atualização datasest finalizada----')
