import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
from dpckan.functions import separador, buscaListaDadosAbertos,buscaDataSet,criarArquivo,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta
from dpckan.updateResource import resource

def criarArquivo2(authorization,package_id,caminhoCompleto,separador=separador):
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
  format = caminhoCompleto.split(separador)[-1]
  caminhoCompletoJson = caminhoCompleto.split(format)[0] + "datapackage" + '.json'
  formato = format.split('.')[1]
  nome = format
  #alterar os parametros passando somente id
  pprint.pprint("Criacao de arquivo inicializada")
  if(caminhoCompleto.find("http") > 0):
      saida = requests.post('https://homologa.cge.mg.gov.br/api/action/resource_create',
            data={"package_id":package_id,"name" : format,"url":caminhoCompleto},
            #data=dataset_dictAtual,
            headers={"Authorization": authorization})
  else:
      files = {'upload': (caminhoCompleto.split(separador)[-1], open(caminhoCompleto, 'rb'), 'text/' + formato)}
      saida = requests.post('https://homologa.cge.mg.gov.br/api/action/resource_create',
            data={"package_id":package_id,"name" : format},
            #data=dataset_dictAtual,
            headers={"Authorization": authorization},
            files = files)
  pprint.pprint("Criacao de arquivo finalizada")

  resources = buscaDataSet(package_id,authorization)
  for d in resources:
      resource_id = d['id']
      name = str(d['name'])
      if(not name.find(".json") > 0 and name == nome):
          pprint.pprint("Atualizacao de dicionario de dados inicializada: " + name)
          atualizaDicionario(caminhoCompletoJson,resource_id,nome,authorization,separador)
          pprint.pprint("Atualizacao de dicionario de dados finalizada: " + name)

  time.sleep(10)

#criarArquivo2('local-onde-havia-chave-acesso', 'remuneracao4', local-onde-havia-caminho-maquina ,separador)
# if __name__ == '__main__':
#     criarArquivo2(sys.argv[1], sys.argv[2], sys.argv[3], separador)
# print(criarArquivo2.__doc__)
