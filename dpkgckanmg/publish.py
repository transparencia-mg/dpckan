import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
import codecs
from functions import buscaListaDadosAbertos,buscaDataSet,criarArquivo,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta,atualizaDicionario,lerCaminhoRelativo, publish, separador

if __name__ == '__main__':
  publish(sys.argv[1], sys.argv[2])
#publish(local-onde-havia-caminho-maquina,'local-onde-havia-chave-acesso',separador)
#atualizaDicionario(local-onde-havia-caminho-maquina,'local-onde-havia-chave-acesso','local-onde-havia-caminho-maquina','/')
