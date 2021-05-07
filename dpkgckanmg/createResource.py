import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
from functions import separador, buscaListaDadosAbertos,buscaDataSet,criarArquivo,criarArquivo2,importaDataSet,buscaPastaArquivos,removePastaArquivos,lerDadosJsonMapeado,buscaArquivos,atualizaMeta,resource

#criarArquivo2('local-onde-havia-chave-acesso', 'remuneracao4', local-onde-havia-caminho-maquina ,separador)
if __name__ == '__main__':
    criarArquivo2(sys.argv[1], sys.argv[2], sys.argv[3], separador)
