import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
import codecs
from functions import buscaListaDadosAbertos,buscaDataSet,criarArquivo,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta,atualizaDicionario,lerCaminhoRelativo, separador

def publish(caminho,authorizaton,separador=separador):
  """
  Summary line.

  Extended description of function.

  Parameters
  ----------
  arg1 : int
      Description of arg1
  arg2 : str
      Description of arg2

  Returns
  -------
  int
      Description of return value

  """
  #try:
  #separador = os.path.sep
  caminhoCompleto = caminho + separador + "datapackage" + '.json'
  if(os.path.isfile(caminhoCompleto)):
      comandoDelete = r'del /f filename'
      so = "WINDOWS"
      caminhoRelativo = caminho + separador + lerCaminhoRelativo(caminhoCompleto);
      privado = True
      autor = 'Usuario teste'
      tags = [{"name": "my_tag"}, {"name": "my-other-tag"}]
      if ((caminhoRelativo.find('http')) or (len(os.listdir(caminhoRelativo)) > 0)):
         #try:
         #nomePasta = arquivos[0]
         nameDataPackage = caminho.split(separador)[-1]
         pprint.pprint("Criacao de DataSet inicializada: " + nameDataPackage)
         importaDataSet(authorizaton,"",caminho,"csv",privado,autor,type,tags,separador,"",comandoDelete,so)
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
