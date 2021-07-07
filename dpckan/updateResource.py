import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
from dpckan.functions import (separador, buscaListaDadosAbertos,
                              buscaDataSet, buscaPastaArquivos,
                              removePastaArquivos, buscaArquivos, atualizaMeta)

def resource(caminhoCompleto, id, authorizaton,separador=separador):
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
  #dataset_dictAtual = comparaDataSet(dataset_dict,resources)
  #pprint.pprint("caminhoatualizado: " + caminhoCompleto +
  #dataset_dictAtual["name"])
  formato = format.split('.')[1]
  files = {'upload': (caminhoCompleto.split(separador)[-1], open(caminhoCompleto, 'rb'), 'text/' + formato)}
  pprint.pprint("Atualizacao de arquivo inicializada")
  resultado = requests.post('https://homologa.cge.mg.gov.br/api/action/resource_update',
            data={"id":id},
            #data=dataset_dictAtual,
            headers={"Authorization": authorizaton},
            files = files)
  if(resultado.iter_lines.__self__.status_code == 500):
      pprint.pprint("Erro ao atualizar arquivo")
  elif(resultado.iter_lines.__self__.status_code == 403):
       pprint.pprint("Acesso negado. Verifique a autorizacao de acesso.")
  else:
      pprint.pprint("Atualizacao de arquivo finalizada")
