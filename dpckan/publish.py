import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
import codecs
import click
from dpckan.functions import separador,buscaListaDadosAbertos,buscaDataSet,criarArquivo,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta,atualizaDicionario,lerCaminhoRelativo, delete_dataset
from dpckan.functions import os_slash,datapackage_path
from dpckan.validations import run_validations

@click.command()
@click.option('--host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: http://dados.mg.gov.br ou https://dados.mg.gov.br")  # -H para respeitar convenção de -h ser help
@click.option('--key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
def publish(host, key):
  """
  Função responsável pela publicação/atualização de um conjunto de dados no ambiente (host) desejado.

  Por padrão, função buscará host e key da instância CKAN para qual e deseja publicar/atualizar dataset
  nas variáveis de ambiente CKAN_HOST e CKAN_KEY cadastradas na máquina ou até mesmo em arquivo .env na raiz do dataset.

  Parameters
  ----------
  host: string (não obrigatório para variáveis cadastradas ou na máquina ou em arquivos .env)
    host ou ambiente da instância CKAN para a qual se deseja publicar/atualizar dataset
  key: string (não obrigatório para variáveis cadastradas ou na máquina ou em arquivos .env)
    Chave CKAN do usuário e ambiente para a qual se deseja publicar/atualizar dataset

  Returns
  -------
  string
      Conjunto publicado/atualizado no ambiente desejado
  """
  click.echo("----Iniciando publicação/atualização datasest----")
  click.echo(f"----Publicação/atualização datasest em {host}----")
  run_validations()
  os_forward_slash_publish = separador
  package_path = "."
  path_datapackage = datapackage_path()
  dataset_dict = lerDadosJsonMapeado(host,path_datapackage,key,'false','null')
  # Deleting dataset if it exists
  delete_dataset(host, key, json.loads(dataset_dict)['name'])
  if(os.path.isfile(path_datapackage)):
      comandoDelete = r'del /f filename'
      so = "WINDOWS"
      caminhoRelativo = package_path + os_forward_slash_publish + lerCaminhoRelativo(path_datapackage);
      privado = True
      autor = 'Usuario teste'
      tags = [{"name": "my_tag"}, {"name": "my-other-tag"}]
      if ((caminhoRelativo.find('http')) or (len(os.listdir(caminhoRelativo)) > 0)):
         nameDataPackage = package_path.split(os_forward_slash_publish)[-1]
         pprint.pprint("Criacao de DataSet inicializada: " + nameDataPackage)
         importaDataSet(key,"",package_path,"csv",privado,autor,type,tags,os_forward_slash_publish,"",comandoDelete,so,host)
         pprint.pprint("Criacao de DataSet finalizada: " + nameDataPackage)
         pprint.pprint("***********************************************************")

