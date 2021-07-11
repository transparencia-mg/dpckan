import json
import os
import json
import sys
import click
from frictionless_ckan_mapper import frictionless_to_ckan as f2c
from ckanapi import RemoteCKAN
from frictionless import Package

def datapackage_path():
  """
    Return the exact path to datapackage.json file. It must to be in the root directory
  """
  return 'datapackage.json'

def resource_create(ckan_instance, package_id, resource):
  payload = {"package_id":package_id,
               "name": resource.title,
               "description": resource.description,
               "url": resource.path}
  if(resource.path.startswith('http')):
    result = ckan_instance.call_action('resource_create', payload)
  else:
    upload_files = {'upload': open(resource.path, 'rb')}
    result = ckan_instance.call_action('resource_create', payload, files=upload_files)
  return result

def load_complete_datapackage(source):
  datapackage = Package(source)
  for resource_name in datapackage.resource_names:
    datapackage.get_resource(resource_name).dialect.expand()
    datapackage.get_resource(resource_name).schema.expand()
  return datapackage

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

def dataset_create(ckan_instance):
  try:
    datapackage_path = 'datapackage.json'
    datapackage = load_complete_datapackage(datapackage_path)
    dataset = f2c.package(datapackage)
    dataset.pop('resources') # Withdraw resources from dataset dictionary to avoid dataset creation with them
    if "notes" not in dataset.keys():
      dataset["notes"] = ""
    if os.path.isfile('README.md'): # Put dataset description and readme together to show a better description on dataset's page
      dataset["notes"] = f"{dataset['notes']}\n{open('README.md').read()}"
    if os.path.isfile('CHANGELOG.md'): # Put dataset description and changelog together to show a better description on dataset's page
      dataset["notes"] = f"{dataset['notes']}\n{open('CHANGELOG.md').read()}"
    
    result = ckan_instance.call_action('package_create', dataset)

    try:
      create_datapackage_json_resource(ckan_instance, result['id'])
    except Exception:
      delete_dataset(ckan_instance, datapackage.name)
      print(f"Erro durante atualização do datapackage.json")
      sys.exit(1)

    for resource_name in datapackage.resource_names:
      try:
        click.echo(f"Criando recurso: {resource_name}")
        resource_ckan = resource_create(ckan_instance,
                                        datapackage.name,
                                        datapackage.get_resource(resource_name))
        resources_metadata_create(ckan_instance,
                                  resource_ckan['id'],
                                  datapackage.get_resource(resource_name)
                                  )
      except Exception:
        delete_dataset(ckan_instance, datapackage.name)
        print(f"Erro durante atualização do recurso: {resource_name}")
        sys.exit(1)

  except Exception:
    delete_dataset(ckan_instance, datapackage.name)
    print(f"Não foi possível criar o dataset {datapackage.name}")
    sys.exit(1)


def resources_metadata_create(ckan_instance, resource_id, resource):
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
  ckan_instance.call_action('datastore_create', dataset_fields)


def delete_dataset(ckan_instance, dataset_name):
  ckan_instance.action.package_delete(id = dataset_name)

def is_dataset_alread_published(host, dataset_name):
  demo = RemoteCKAN(host)
  if dataset_name in demo.action.package_list():
    return True
  else:
    return False

def resource_update(ckan_instance, resource_id, resource):

  click.echo(f"Atualizando recurso: {resource.name}")

  payload = {"id": resource_id,
             "name": resource.title,
             "description": resource.description,
             "url": resource.path}

  if(resource.path.startswith('http')):
    result = ckan_instance.call_action('resource_update', payload)
  else:
    result = ckan_instance.call_action('resource_update', payload, 
                                       files={'upload': open(resource.path, 'rb')})
  return result


def create_datapackage_json_resource(ckan_instance, package_id):

  click.echo("Criando datapackage.json")

  ckan_instance.action.resource_create(package_id = package_id,
                                       name = "datapackage.json",
                                       upload = open('datapackage.json', 'rb'))
  

def update_datapackage_json_resource(ckan_instance, package_id):
    
    click.echo(f"Atualizando datapackage.json")

    ckan_dataset = ckan_instance.action.package_show(id = package_id)
    
    for resource in ckan_dataset['resources']:
      if resource['name'] == "datapackage.json":
        resource_id = resource['id']

    ckan_instance.action.resource_update(id = resource_id,
                                         upload = open('datapackage.json', 'rb'))

