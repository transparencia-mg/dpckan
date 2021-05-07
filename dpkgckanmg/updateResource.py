import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
from functions import separador, buscaListaDadosAbertos,buscaDataSet,criarArquivo,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta,resource

#resource(local-onde-havia-caminho-maquina,'local-onde-havia-chave-acesso', 'local-onde-havia-chave-acesso', separador)
if __name__ == '__main__':
    resource(sys.argv[1], sys.argv[2], sys.argv[3], separador)
