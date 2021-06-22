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
from dpckan.functions import separador,buscaListaDadosAbertos,buscaDataSet,criarArquivo,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta,atualizaDicionario,lerCaminhoRelativo

@click.command()
@click.option('--env',
              '-e',
              help='''
                Flag que completará as variáveis de ambiente CKAN_HOST e CKAN_KEY.
                Exemplo --env HOMOLOGA para CKAN_HOST_HOMOLOGA e CKAN_KEY_HOMOLOGA
              ''')
def publish(package_path, ckan_key, environment='homologa'):
  """
  Função responsável pela publicação de um conjunto de dados no ambiente desejado.

  Por padrão, função buscará Host e Key da instância CKAN para qual e deseja publicar/atualizar dataset
  nas variáveis de ambiente CKAN_HOST e CKAN_KEY. Caso usuário deseja cadastrar mais de uma instância,
  basta acrescentar uma "flag" ao final destes dois nomes, exemplo CKAN_HOST_HOMOLOGA e CKAN_KEY_HOMOLOGA

  Parameters
  ----------
  env: string (não obrigatório)
    Flag complementando as variáveis de ambiente padrão CKAN_HOST e CKAN_KEY

  Returns
  -------
  string
      Conjunto publicado no ambiente desejado e mensagem de sucesso:
      "Criacao de DataSet finalizada: <nome-do-conjunto>"
  """
  os_forward_slash_publish = separador
  caminhoCompleto = package_path + os_forward_slash_publish + "datapackage" + '.json'
  if(os.path.isfile(caminhoCompleto)):
      comandoDelete = r'del /f filename'
      so = "WINDOWS"
      caminhoRelativo = package_path + os_forward_slash_publish + lerCaminhoRelativo(caminhoCompleto);
      privado = True
      autor = 'Usuario teste'
      tags = [{"name": "my_tag"}, {"name": "my-other-tag"}]
      if ((caminhoRelativo.find('http')) or (len(os.listdir(caminhoRelativo)) > 0)):
         nameDataPackage = package_path.split(os_forward_slash_publish)[-1]
         pprint.pprint("Criacao de DataSet inicializada: " + nameDataPackage)
         importaDataSet(ckan_key,"",package_path,"csv",privado,autor,type,tags,os_forward_slash_publish,"",comandoDelete,so,environment)
         pprint.pprint("Criacao de DataSet finalizada: " + nameDataPackage)
         pprint.pprint("***********************************************************")

