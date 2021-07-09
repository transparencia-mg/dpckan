import urllib
import json
import pprint
import os
import requests
import json
import sys
import shutil
import time
import json
import importlib
import time
import click
from urllib.parse import quote
from frictionless_ckan_mapper import ckan_to_frictionless as c2f
from frictionless_ckan_mapper import frictionless_to_ckan as f2c
from ckanapi import RemoteCKAN
from frictionless import Package
import ipdb

# Excluir quando todas as funções estiverem refatoradas
# Código contará apenas com varável os_slash, definido abaixo
separador = os.path.sep

# Helps functions identify which slash user operating system uses
os_slash = os.path.sep

def datapackage_path():
  """
    Return the exact path to datapackage.json file. It must to be in the root directory
  """
  return f'.{os_slash}datapackage.json'

def buscaListaDadosAbertos(authorizaton):
    request = urllib2.Request('https://homologa.cge.mg.gov.br/api/3/action/package_list')
    #request.add_header('Authorization', authorizaton)
    response_dict = json.loads(urllib2.urlopen(request, '{}').read())
    return response_dict['result']

def buscaDataSet(url,id,authorization):
        parametros = {
            'id': id
        }


        headers = {
    'Authorization': authorization
    }

        data_string = quote(json.dumps(parametros))
        request = urllib.request.Request(f'{url}/api/3/action/package_show', data=data_string.encode('utf-8'), headers=headers)
        #request.add_header('Authorization', authorization)
        response_dict = json.loads(urllib.request.urlopen(request).read())
        #for i in range(len(response_dict['result']['resources']))
        if(response_dict['success'] == True and response_dict["result"]["resources"] != []):
            return response_dict['result']['resources']
        else:
            return response_dict['result']['id']

def buscaPastaArquivos(diretorio,separador):
    os.chdir(diretorio)
    listArquivos = []
    all_subdirs = [d for d in os.listdir(diretorio) if os.path.isdir(d)]
    #all_subdirs.remove('.cache')
    #pprint.pprint(all_subdirs)
    for dirs in all_subdirs:
        dir = os.path.join(diretorio, dirs)
        os.chdir(dir)
        current = os.getcwd()
        new = str(current).split(separador)[-1]
        listArquivos.append(new)
    return listArquivos

def buscaArquivos(diretorio,separador,isJson):
    #pprint.pprint(diretorio)
    os.listdir(diretorio)
    #pprint.pprint(os.listdir(diretorio))
    listArquivos = []
    all_subdirs = os.listdir(diretorio)#[d for d in os.listdir(diretorio) if os.path.isdir(d)]
    #all_subdirs.remove('.cache')
    for dirs in all_subdirs:
        #dir = os.path.join(diretorio, dirs)
        #os.chdir(dir)
        #current = os.getcwd()
        new = str(dirs)#.split(separador)[-1]

        if(not isJson and (new.find(".xls") > 0 or new.find(".csv") > 0)):
            listArquivos.append(new)
        elif(isJson and new.find(".json") > 0):
            listArquivos.append(new)

    #pprint.pprint(listArquivos)
    return listArquivos

def removePastaArquivos(diretorio,separador,comando,so,arquivo):
        os.chdir(diretorio)
        listArquivos = []
        #all_subdirs = [d for d in os.listdir(diretorio) if os.path.isdir(d)]
        #all_subdirs.remove('.cache')
        #pprint.pprint(os.path.isdir(diretorio))
        #for dirs in all_subdirs:
            #dir = os.path.join(diretorio, dirs)
        if os.path.isdir(diretorio):
            if(so == "WINDOWS"):
                arquivoDel = diretorio + separador + arquivo
                if(os.path.exists(arquivoDel)):
                    os.system(comando.replace('filename',arquivoDel))
                #time.sleep(20)
                #shutil.rmtree(diretorio)
            else:
                arquivoDel = diretorio + separador + arquivo
                comandoCompleto = comando + arquivoDel
                os.system(comandoCompleto)

def resource_create(ckan_host, ckan_key, package_id, resource):
  if(resource.path.startswith('http')):
    
    payload = quote(json.dumps({"package_id": package_id,
                               "name" : resource.title,
                               "url": resource.path})).encode('utf-8')

    request = urllib.request.Request(f'{ckan_host}/api/action/resource_create',
                                     data = payload,
                                     headers={"Authorization": ckan_key})
    
    response = urllib.request.urlopen(request)
    
    result = json.loads(response.read().decode('utf-8'))['result']
  else:
    payload = {"package_id":package_id,
                                "name": resource.title,
                                "description": resource.description}
    upload_files = {'upload': (resource.path, open(resource.path, 'rb'), 'text/' + resource.format)}
    response = requests.post(f'{ckan_host}/api/action/resource_create',
                          data = payload,
                          headers = {"Authorization": ckan_key},
                          files = upload_files) # https://stackoverflow.com/questions/12385179/how-to-send-a-multipart-form-data-with-requests-in-python
    result = response.json()['result']
  return result

def load_complete_datapackage(source):
  datapackage = Package(source)
  for resource_name in datapackage.resource_names:
    datapackage.get_resource(resource_name).dialect.expand()
    datapackage.get_resource(resource_name).schema.expand()
  return datapackage

def lerCaminhoRelativo(diretorio):
    separador = os.path.sep
    with open(diretorio,'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
        for m in data.keys():
            if(m == 'resources'):
               for t in data[m]:
                   existe = 0
                   if(t['path'].find('http://') > 0):
                       existe = 1
                   if(t['path'].find('https://') > 0):
                       existe = 1

                   if(existe):
                     path = t['path'].replace(r'/',separador)
                     path = path.replace('\\',separador)
                     caminho = path.split(separador)[-1]
                     return path.split(separador)[0]
                   else:
                     return t['path']

def frictionless_to_ckan_dictionary(diretorio):
  listaParametros = ["license_title", "maintainer", "relationships_as_object",
                     "private", "maintainer_email", "num_tags", "id", "metadata_created",
                     "metadata_modified", "author_email", "state", "version", "creator_user_id",
                     "type", "num_resources", "groups", "license_id", "relationships_as_subject", "isopen",
                     "url", "owner_org", "extras", "title", "revision_id", "update"]
  with open(diretorio,'r', encoding="utf-8") as json_file:
    data = json.load(json_file)
    tagsJson = {}
    tagsJson['tags'] = []
    tagsDicionario = {}
    tagsDicionario['fields'] = []
    dataset_dict = {}
    for m in data.keys():
      if(str(m) == 'keywords'):
        for t in data[m]:
          tagsJson['tags'].append({'name': t})
        y = { 'tags' : tagsJson['tags'] }
        dataset_dict.update(y)
      elif(str(m) == 'fields'):
        for t in data[m]:
            tagsDicionario['fields'].append({'id': t})
        y = { 'fields' : tagsDicionario['fields'] }
        dataset_dict.update(y)
      elif ((str(m) == 'resources')):
        y = { str(m) : str(data[m]) }
      elif (str(m) == 'name'):
        y = { str(m) : str(data[m]) }
        dataset_dict.update(y)
      elif (str(m) == 'description'):
        y = { 'notes' : str(data[m]) }
        dataset_dict.update(y)
      elif (str(m) == 'homepage'):
        y = { 'url' : str(data[m]) }
        dataset_dict.update(y)
      elif (str(m) == 'package_id'):
        id = str(data[m])
        y = { 'id' : id }
        dataset_dict.update(y)
      elif (str(m) == 'update'):
        isUpdate = 'true'
      elif (str(m) == 'contributors'):
        for c in data[m]:
          if(c['title']):
              y = { "author" : c["title"] }
              dataset_dict.update(y)
          if(c['role'] == "publisher"):
            y = { "owner_org" : c["organization"] }
            dataset_dict.update(y)
      else:
        if(str(m) in listaParametros):
          y = { str(m) : str(data[m]) }
          dataset_dict.update(y)
    dataset_dict = json.dumps(dataset_dict)
    return dataset_dict

def dataset_create(ckan_host, ckan_key):
  try:
    datapackage_path = f'.{os_slash}datapackage.json'
    package = load_complete_datapackage(datapackage_path)
    dataset = f2c.package(package)
    dataset.pop('resources') # Withdraw resources from dataset dictionary to avoid dataset creation with them
    if "notes" not in dataset.keys():
      dataset["notes"] = ""
    if os.path.isfile('README.md'): # Put dataset description and readme together to show a better description on dataset's page
      dataset["notes"] = f"{dataset['notes']}\n{open('README.md').read()}"
    if os.path.isfile('CHANGELOG.md'): # Put dataset description and changelog together to show a better description on dataset's page
      dataset["notes"] = f"{dataset['notes']}\n{open('CHANGELOG.md').read()}"
    dataset_name = package.name
    headers = {
      'Authorization': ckan_key
    }

    request = urllib.request.Request(f'{ckan_host}/api/action/package_create',
                                     data=quote(json.dumps(dataset)).encode('utf-8'),
                                     headers=headers)
    response = urllib.request.urlopen(request)
    assert response.code == 200

    response_dict = json.loads(response.read())
    assert response_dict['success'] is True

    created_package = response_dict['result']
    if(created_package['id']):
      id = str(created_package['id']).replace('u','')

    try:
      create_datapackage_json_resource(ckan_host, ckan_key, id)
    except Exception:
      delete_dataset(ckan_host, ckan_key, dataset_name)
      print(f"Erro durante atualização do datapackage.json")
      sys.exit(1)

    for resource_name in package.resource_names:
      try:
        click.echo(f"Criando recurso: {resource_name}")
        resource_ckan = resource_create(ckan_host,
                                        ckan_key,
                                        id,
                                        package.get_resource(resource_name))
        resources_metadata_create(ckan_host,
                                  ckan_key,
                                  resource_ckan['id'],
                                  package.get_resource(resource_name)
                                  )
      except Exception:
        delete_dataset(ckan_host, ckan_key, dataset_name)
        print(f"Erro durante atualização do recurso: {resource_name}")
        sys.exit(1)
      except urllib.error.HTTPError as e:
        delete_dataset(ckan_host, ckan_key, dataset_name)
        print(e.read().decode())
        sys.exit(1)

  except Exception:
    delete_dataset(ckan_host, ckan_key, dataset_name)
    print(f"Não foi possível criar o dataset {dataset_name}")
    sys.exit(1)

def comparaDataSet(dataset_dict,resources):
    dataset_dictNovo = {}

    for m in resources.keys():
        if(dataset_dict.has_key(m) and (str(resources[m]) != str(dataset_dict[m]))):
            y = { str(m) : str(dataset_dict[m]) }
            resources[m] = str(dataset_dict[m])
            dataset_dictNovo.update(y)

    return resources

def atualizaMeta():
    dataset_dict = {
    'title': "teste",
    'name':  "teste4554",
    'notes': "nota",
    'private': 'false',
    'author': "fulano de tal",
    'type': "text/csv",
    'tags': [{"name": "my_tag"}, {"name": "my-other-tag"}],
    'owner_org': 'controladoria-geral-do-estado',
    'id': 'local-onde-havia-chave-acesso'
    }

    data_string = quote(json.dumps(dataset_dict))

    headers = {
    'Authorization': authorization
    }

    # We'll use the package_create function to create a new dataset.
    request = urllib.request.Request('https://homologa.cge.mg.gov.br/api/action/package_update', data=data_string.encode('utf-8'), headers=headers)

    # Creating a dataset requires an authorization header.
    # Replace *** with your API key, from your user account on the CKAN site
    # that you're creating the dataset on.
    #request.add_header('Authorization',
    #'local-onde-havia-chave-acesso')

    # Make the HTTP request.
    response = urllib.request.urlopen(request)
    assert response.code == 200

    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read())
    assert response_dict['success'] is True

    # package_create returns the created package as its result.
    created_package = response_dict['result']

    return created_package

def updateMetaData(caminhoCompleto,separador,url,authorization):
    caminhoCompletoJson = caminhoCompleto + separador + 'datapackage.json'

    #pprint.pprint(caminhoCompletoJson)
        #caminhoCompletoJson = local-onde-havia-caminho-maquina
    if(os.path.isfile(caminhoCompletoJson)):
        dataset_dict = frictionless_to_ckan_dictionary(caminhoCompletoJson)
        #pprint.pprint(dataset_dict)
    else:
        #pprint.pprint(caminhoCompletoJson)
        # Put the details of the dataset we're going to create into a dict.
        dataset_dict = {
            'title': str(url).replace('_',' ').upper(),
            'name':  str(url),
            'notes': str(url).replace('_',' '),
            'private': privado,
            'author':autor,
            'type': type,
            'tags': [{"name": "my_tag"}, {"name": "my-other-tag"}],
            'owner_org': 'controladoria-geral-do-estado'
        }

    # Use the json module to dump the dictionary to a string for posting.
    data_string = quote(json.dumps(dataset_dict))


    headers = {
    'Authorization': authorization
    }

    # We'll use the package_create function to create a new dataset.
    request = urllib.request.Request('https://homologa.cge.mg.gov.br/api/action/package_update', data=data_string.encode('utf-8'), headers=headers)

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
    #pprint.pprint(response_dict['result'])

def resources_metadata_create(ckan_host, ckan_key, resource_id, resource):
  
  dataset_fields = {}
  resource_id = { "resource_id" : resource_id }
  dataset_fields.update(resource_id)
  force = { "force" : "True" }
  dataset_fields.update(force)
  fields = []
  for field in resource.schema.fields:
    meta_info = {"label": field["title"], "notes" : field["description"] , "type_override" : 'text' }
    field = { "type" : 'text', "id" : field["name"] , "info" : meta_info }
    fields.append(field)
  dataset_fields.update({ "fields" : fields})
  frictionless_package = json.dumps(c2f.dataset(dataset_fields)).encode('utf-8')

  try:
    request = urllib.request.Request(f'{ckan_host}/api/action/datastore_create',
                                    data=frictionless_package,
                                    headers={ 'Authorization': ckan_key })

    response = urllib.request.urlopen(request)
    assert response.code == 200
    response_dict = json.loads(response.read())
    assert response_dict['success'] is True

  except urllib.error.HTTPError as e:
    print(e.read().decode())
    sys.exit(1)

def delete_dataset(host, key, dataset_name):
  demo = RemoteCKAN(host, apikey=key)
  demo.action.package_delete(id=dataset_name)

def is_dataset_alread_published(host, dataset_name):
  demo = RemoteCKAN(host)
  if dataset_name in demo.action.package_list():
    return True
  else:
    return False

def resource_update(ckan_host, ckan_key, resource_id, resource_path):
  try:
    resource_name = resource_path.split(separador)[-1]
    click.echo(f"Atualizando recurso {resource_name}")
    resource_format = resource_name.split('.')[1]
    files = {'upload': (resource_name, open(resource_path, 'rb'), 'text/' + resource_format)}
    result = requests.post(f'{ckan_host}/api/action/resource_update',
              data={"id":resource_id},
              headers={"Authorization": ckan_key},
              files = files)
  except urllib.error.HTTPError as e:
    print(e.read().decode())
    sys.exit(1)


def create_datapackage_json_resource(ckan_host, ckan_key, package_id):

  click.echo("Criando datapackage.json")
      
  requests.post(f'{ckan_host}/api/action/resource_create',
                          data = {"package_id": package_id,
                                  "name": "datapackage.json"},
                          headers = {"Authorization": ckan_key},
                          files = {'upload': ('datapackage.json', open('datapackage.json', 'rb') , 'application/json')})
  

def update_datapackage_json_resource(ckan_host, ckan_key, package_id):
    
    click.echo(f"Atualizando datapackage.json")

    ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
    ckan_dataset = ckan_instance.action.package_show(id = package_id)
    
    for resource in ckan_dataset['resources']:
      if resource['name'] == "datapackage.json":
        resource_id = resource['id']

    requests.post(f'{ckan_host}/api/action/resource_update',
                  data={"id": resource_id},
                  headers={"Authorization": ckan_key},
                  files = {'upload': ('datapackage.json', open('datapackage.json', 'rb') , 'application/json')})
