import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
import codecs
# lembrar que ao chamar from functions import... erro para encontrar "functions" ao chamar a função utilizando "from dpkgckanmg.publish import publish"
# ao utilizar o método abaixo erro para encontrar "dpkgckanmg" ao chamar a função no final deste arquivo
from dpkgckanmg.functions import separador,buscaListaDadosAbertos,buscaDataSet,criarArquivo,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta,atualizaDicionario,lerCaminhoRelativo


def publish(package_path, ckan_key, environment='homologa'):
  """
  Função responsável pela publicação de um conjunto de dados.

  Parameters
  ----------
  package_path : string
    Caminho aonde o arquivo datapackage.json a ser publicado se encontra
  ckan_key : string
    ckan key do usuário no ambiente desejado
    Sugerimos a criação de arquivo .env (não rastreado via .gitignore) para armazenamento das chaves de seus respectivos ambientes
  environment: string
    usuário de deverá escolher entre:
      - homologa (para embiente de homologação - homologa.cge.mg.gov.br); e
      - portal (para embiente de produção - dados.mg.gov.br).
    Caso ambiente não seja informado publicação ocorrerá no ambiente de homologação
  Returns
  -------
  string
      Conjunto publicado no ambiente desejado e mensagem de sucesso:
      "Criacao de DataSet finalizada: <nome-do-conjunto>"
  """
  #try:
  #separador = os.path.sep
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
         #try:
         #nomePasta = arquivos[0]
         nameDataPackage = package_path.split(os_forward_slash_publish)[-1]
         pprint.pprint("Criacao de DataSet inicializada: " + nameDataPackage)
         importaDataSet(ckan_key,"",package_path,"csv",privado,autor,type,tags,os_forward_slash_publish,"",comandoDelete,so,environment)
         pprint.pprint("Criacao de DataSet finalizada: " + nameDataPackage)
         pprint.pprint("***********************************************************")
         #except Exception as e:
             #print("Erro ao importar: " + arquivos[0] + " ERROR:" + e)
  #except Exception as e:
      #print(e)

# if __name__ == '__main__':
#   publish(sys.argv[1], sys.argv[2])
#publish(local-onde-havia-caminho-maquina,'local-onde-havia-chave-acesso',separador)
#atualizaDicionario(local-onde-havia-caminho-maquina,'local-onde-havia-chave-acesso','local-onde-havia-caminho-maquina','/')
# print(publish.__doc__)
