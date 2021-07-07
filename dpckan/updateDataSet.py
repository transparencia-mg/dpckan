import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
from dpckan.functions import (buscaListaDadosAbertos, buscaDataSet,
                              buscaPastaArquivos, removePastaArquivos,
                              frictionless_to_ckan_dictionary, buscaArquivos, atualizaMeta)

def dataSet(authorizaton,caminhoCompleto,id):
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
  pprint.pprint("Atualizacao de dataset iniciada")
  #arquivosData = buscaArquivos(caminhoCompleto + separador +
  #"data",separador)
  caminhoCompletoJson = caminhoCompleto

  #pprint.pprint(caminhoCompletoJson)
      #caminhoCompletoJson = local-onde-havia-caminho-maquina
  if(os.path.isfile(caminhoCompletoJson)):
      dataset_dict = frictionless_to_ckan_dictionary(caminhoCompletoJson,authorizaton,'true',id)
      #pprint.pprint(dataset_dict)
  else:
      raise Exception("Diretorio nao encontrado")

  # Use the json module to dump the dictionary to a string for posting.
  data_string = quote(dataset_dict)

  headers = {
  'Authorization': authorizaton
  }

  # We'll use the package_create function to create a new dataset.
  request = urllib.request.Request('https://homologa.cge.mg.gov.br/api/action/package_update',data=data_string.encode('utf-8'),headers=headers)

  # Creating a dataset requires an authorization header.
  # Replace *** with your API key, from your user account on the CKAN site
  # that you're creating the dataset on.
  #request.add_header('Authorization', authorizaton)

  # Make the HTTP request.
  response = urllib.request.urlopen(request)
  assert response.code == 200

  # Use the json module to load CKAN's response into a dictionary.
  response_dict = json.loads(response.read())
  assert response_dict['success'] is True

  # package_create returns the created package as its result.
  update_package = response_dict['result']
  pprint.pprint("Atualizacao de dataset finalizada")

