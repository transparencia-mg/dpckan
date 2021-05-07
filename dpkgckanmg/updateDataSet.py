import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
from functions import buscaListaDadosAbertos,buscaDataSet,criarArquivo,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta,dataSet

#dataSet('local-onde-havia-chave-acesso',local-onde-havia-caminho-maquina,'local-onde-havia-chave-acesso')
if __name__ == '__main__':
    dataSet(sys.argv[1], sys.argv[2], sys.argv[3])
