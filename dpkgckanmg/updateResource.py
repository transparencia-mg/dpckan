import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
# lembrar que ao chamar from functions import... erro para encontrar "functions" ao chamar a função utilizando "from dpkgckanmg.publish import publish"
# ao utilizar o método abaixo erro para encontrar "dpkgckanmg" ao chamar a função no final deste arquivo
from dpkgckanmg.functions import separador, buscaListaDadosAbertos,buscaDataSet,criarArquivo,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta

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

#resource(local-onde-havia-caminho-maquina,'local-onde-havia-chave-acesso', 'local-onde-havia-chave-acesso', separador)
# if __name__ == '__main__':
#     resource(sys.argv[1], sys.argv[2], sys.argv[3], separador)
# print(resource.__doc__)
