import ipdb
import os
import click
import hashlib
import json
from urllib.request import urlopen
from frictionless_ckan_mapper import frictionless_to_ckan as f2c
from ckanapi import RemoteCKAN
from frictionless import Package

def datapackage_path():
  """
    Return the exact path to datapackage.json file. It must to be in the root directory
  """
  return 'datapackage.json'

def resource_create(ckan_instance, package_id, resource):
  
  click.echo(f"Criando recurso: {resource.name}")
  payload = {"package_id":package_id,
               "name": resource.title,
               "description": resource.description,
               "url": resource.path}
  if(resource.path.startswith('http')):
    result = ckan_instance.call_action('resource_create', payload)
  else:
    upload_files = {'upload': open(os.path.join(resource.basepath, resource.path), 'rb')}
    result = ckan_instance.call_action('resource_create', payload, files=upload_files)
  return result

def load_complete_datapackage(source):
  datapackage = Package(source)
  for resource_name in datapackage.resource_names:
    datapackage.get_resource(resource_name).dialect.expand()
    datapackage.get_resource(resource_name).schema.expand()
  return datapackage

def dataset_create(ckan_instance, package):
  dataset = frictionless_to_ckan(package)
  ckan_instance.call_action('package_create', dataset)
  clean_datapackage_with_ckan_ids(ckan_instance, package)
  for resource_name in package.resource_names:
    resource_path = package.get_resource(resource_name)['path']
    resource_ckan = resource_create(ckan_instance,
                                    package.name,
                                    package.get_resource(resource_name))
    resource_update_datastore_metadata(ckan_instance,
                              resource_ckan['id'],
                              package.get_resource(resource_name)
                              )
    resource_index = package.resource_names.index(resource_name)
    update_datapackage_with_ckan_ids(ckan_instance, package, resource_index, resource_path, resource_name, resource_ckan['id'])
  create_datapackage_json_resource(ckan_instance, package)

def update_datapackage_with_ckan_ids(ckan_instance, package, resource_index, resource_path, resource_name, resource_id):
  # ipdb.set_trace(context=10)
  dp = ''
  if package.basepath == '':
    dp = Package("datapackage.json")
  else:
    dp = Package(f"{package.basepath}/datapackage.json")
  if 'ckan_hosts' not in dp:
    dp['ckan_hosts'] = {}
    dp['ckan_hosts'][ckan_instance.address] = {}
    dp['ckan_hosts'][ckan_instance.address][f'{resource_index} - {resource_name} - {resource_path}'] = resource_id
  else:
    if ckan_instance.address not in dp['ckan_hosts']:
      dp['ckan_hosts'][ckan_instance.address] = {}
      dp['ckan_hosts'][ckan_instance.address][f'{resource_index} - {resource_name} - {resource_path}'] = resource_id
    else:
      dp['ckan_hosts'][ckan_instance.address][f'{resource_index} - {resource_name} - {resource_path}'] = resource_id
  if package.basepath == '':
    dp.to_json("datapackage.json")
  else:
    dp.to_json(f"{package.basepath}/datapackage.json")

def clean_datapackage_with_ckan_ids(ckan_instance, package):
  dp = ''
  if package.basepath == '':
    dp = Package("datapackage.json")
  else:
    dp = Package(f"{package.basepath}/datapackage.json")
  if 'ckan_hosts' in dp:
    dp.pop('ckan_hosts')
    if package.basepath == '':
      dp.to_json("datapackage.json")
    else:
      dp.to_json(f"{package.basepath}/datapackage.json")

def resource_update_datastore_metadata(ckan_instance, resource_id, resource):
  if resource.schema.fields == []:
    pass
  else:
    dataset_fields = {}
    resource_id = { "resource_id" : resource_id }
    dataset_fields.update(resource_id)
    force = { "force" : "True" }
    dataset_fields.update(force)
    fields = []
    for field in resource.schema.fields:
      meta_info = {"label": field.get("title", ""), "notes" : field.get("description", "") , "type_override" : 'text' }
      field = { "type" : 'text', "id" : field["name"] , "info" : meta_info }
      fields.append(field)
    dataset_fields.update({ "fields" : fields})
    ckan_instance.call_action('datastore_create', dataset_fields)

def delete_dataset(ckan_instance, dataset_name):
  ckan_instance.action.package_delete(id = dataset_name)

def is_dataset_published(ckan_instance, datapackage):
  try: 
    result = ckan_instance.action.package_show(id = datapackage.name)
  except Exception:
    return False

  if(result['state'] == 'deleted'):
    return False

  return True

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
                                       files={'upload': open(os.path.join(resource.basepath, resource.path), 'rb')})
  return result



def create_datapackage_json_resource(ckan_instance, datapackage):
  click.echo("Criando datapackage.json")
  resource_ckan = ckan_instance.action.resource_create(package_id = datapackage.name,
                                       name = 'datapackage.json',
                                       upload = open(os.path.join(datapackage.basepath, 'datapackage.json'), 'rb'))
  datapackage_position = len(datapackage['ckan_hosts'][ckan_instance.address])
  update_datapackage_with_ckan_ids(ckan_instance, datapackage, datapackage_position, 'datapackage.json', 'datapackage', resource_ckan['id'])
  update_datapackage_json_resource(ckan_instance, datapackage)

def update_datapackage_json_resource(ckan_instance, datapackage):
  click.echo(f"Atualizando datapackage.json")
  ckan_dataset = ckan_instance.action.package_show(id = datapackage.name)
  for resource in ckan_dataset['resources']:
    if os.path.basename(resource['url']) == "datapackage.json":
      resource_id = resource['id']
  ckan_instance.action.resource_update(id = resource_id,
                                       upload = open(os.path.join(datapackage.basepath, 'datapackage.json'), 'rb'))

def dataset_update(ckan_instance, datapackage):
  click.echo(f"Atualizando conjunto de dados: {datapackage.name}")
  # Find ckan host url
  ckan_host = ckan_instance.address
  # Find datapackage.json id for ckan instance in local datapackage.json file
  datapackage_id = ''
  for key in datapackage['ckan_hosts'][ckan_host].keys():
    if key.split(' - ')[-1] == 'datapackage.json':
      datapackage_id = datapackage['ckan_hosts'][ckan_host][key]
  # Search datapackage.json resource in ckan instance using datapackage_id
  ckan_datapackage_resource = ckan_instance.action.resource_show(id = datapackage_id)
  # Load ckan_datapackage_resource as json
  dataset = load_complete_datapackage(json.loads(urlopen(ckan_datapackage_resource['url']).read()))
  dataset_diff(ckan_instance, ckan_host, datapackage, dataset)

def dataset_diff(ckan_instance, ckan_host, datapackage, dataset):
  # Remote datapackage.json paths: keys
  datapackage_remote_resource_paths = dataset['ckan_hosts']
  # Local datapackage.json paths: keys
  datapackage_local_resource_paths = datapackage['ckan_hosts']
  # Compare paths in datapackage.json remote with local
  for path in datapackage_remote_resource_paths[ckan_host].keys():
    # ipdb.set_trace(context=10)
    if path in datapackage_local_resource_paths[ckan_host].keys():
      # If path and id are the same use diff to compare them
      if datapackage_remote_resource_paths[ckan_host][path] == datapackage_local_resource_paths[ckan_host][path]:
        if resouce_index_name_path(path, datapackage):
          print(f'Caminho e chave iguais para {path}. Comparar dados e metadados')
          print(resource_hash(datapackage, path.split(' - ')[1]))
          print(resource_hash(dataset, path.split(' - ')[1]))
          print(resource_hash_2(path.split(' - ')[2]))
          print(resource_url_hash(ckan_instance, datapackage_remote_resource_paths[ckan_host][path]))
        else:
          print('problema no index, name, path')
      else:
        # path are the same but id is different something must be wrong, suggest confering process
        print(f'{path} com ids diferentes, conferir')
    else:
      # Is path doesn't exist in local datapackage.json suggest delete resource from remote
      print(f'{path} não existe no arquivo datapackage.json local, utilize `dpckan resource delete` para excluir recurso na instância {ckan_host}')
  # Compare paths in datapackage.json local with remote
  for path in datapackage_local_resource_paths[ckan_host].keys():
    # If local path doesn't exist in remote instance sugest creation
    if path not in datapackage_remote_resource_paths[ckan_host].keys():
      print(f'{path} não existe na instância {ckan_host}. utilize `dpckan resource create` para cria-lo')

def resouce_index_name_path(path, datapackage):
  if path.split(' - ')[-1] != 'datapackage.json':
    resource_index = int(path.split(' - ')[0])
    resouce_name = path.split(' - ')[1]
    resouce_path = path.split(' - ')[2]
    return datapackage['resources'][resource_index]['name'] == resouce_name and datapackage['resources'][resource_index]['path'] == resouce_path
  else:
    return True

def resource_hash(package, resouce_name):
  if resouce_name != 'datapackage':
    resource = package.get_resource(resouce_name)
    resource.infer(stats=True)
    return resource['stats']['hash']


def resource_hash_2(resource_path):
  md5_hash = hashlib.md5()
  resource_content = open(resource_path, "rb").read()
  md5_hash.update(resource_content)
  resource_hash = md5_hash.hexdigest()
  return resource_hash

def resource_url_hash(ckan_instance, resource_id):
  md5_hash = hashlib.md5()
  ckan_datapackage_resource = ckan_instance.action.resource_show(id = resource_id)
  # ipdb.set_trace(context=10)
  resouce_content = urlopen(ckan_datapackage_resource['url']).read()
  md5_hash.update(resouce_content)
  resource_hash = md5_hash.hexdigest()
  return resource_hash

def frictionless_to_ckan(datapackage):
  dataset = f2c.package(datapackage)
  dataset.pop('resources') # Withdraw resources from dataset dictionary to avoid dataset creation with them
  README_path = os.path.join(datapackage.basepath, 'README.md')
  CONTRIBUTING_path = os.path.join(datapackage.basepath, 'CONTRIBUTING.md')
  CHANGELOG_path = os.path.join(datapackage.basepath, 'CHANGELOG.md')
  if "notes" not in dataset.keys():
    dataset["notes"] = ""
  if os.path.isfile(README_path):
    dataset["notes"] = f"{dataset['notes']}\n{open(README_path).read()}"
  if os.path.isfile(CONTRIBUTING_path):
    dataset["notes"] = f"{dataset['notes']}\n{open(CONTRIBUTING_path).read()}"
  if os.path.isfile(CHANGELOG_path):
    dataset["notes"] = f"{dataset['notes']}\n{open(CHANGELOG_path).read()}"
  if 'id' in dataset.keys():
    dataset.update({ "id" : datapackage.name})
  return dataset

def resource_diff(ckan_instance, datapackage, resource_name):
  dp_dataset = f2c.package(datapackage)
  ckan_dataset = ckan_instance.action.package_show(id=datapackage.name)

  # to return results
  diffs = []
  oks = []

  for res in dp_dataset.get('resources', []):
    if res['title'] == resource_name:
      dp_resource = res
      break
  else:
    dp_resource = None

  # it's not easy to detect which is the right resource, because we use the title as name
  for res in ckan_dataset.get('resources', []):
    if res['name'] == resource_name:
      ckan_resource = res
      break
  else:
    ckan_resource = None

  if ckan_resource is None or dp_resource is None:
    if ckan_resource is None:
      diffs.append({'field_name': 'ALL', 'error': 'Resource not found in CKAN'})
    if dp_resource is None:
      diffs.append({'field_name': 'ALL', 'error': 'Resource not found in DataPackage'})
    return diffs, []

  fields = ["format", "description"]
  # TODO use hash functions for the resource file

  for field in fields:
    if dp_resource.get(field) == ckan_resource.get(field):
      oks.append(field)
    else:
      diffs.append(
        {
          'field_name': field,
          'ckan_value': ckan_resource.get(field),
          'datapackage_value': dp_resource.get(field)
        }
      )

  return diffs, oks


# def dataset_diff(ckan_instance, datapackage):
#   dp_dataset = frictionless_to_ckan(datapackage)
#   ckan_dataset = ckan_instance.action.package_show(id = datapackage.name)

#   diffs = []
#   oks = []
#   # TODO, add more
#   fields = ["title", "version", "url", "license_id"]

#   for field in fields:
#     if dp_dataset.get(field) == ckan_dataset.get(field):
#       oks.append(field)
#     else:
#       diffs.append(
#         {
#           'field_name': field,
#           'ckan_value': ckan_dataset.get(field),
#           'datapackage_value': dp_dataset.get(field)
#         }
#       )

#   # check org (dataset use ID, datapackage uses name)
#   if dp_dataset['owner_org'] == ckan_dataset['organization']['name']:
#     oks.append('owner_org')
#   else:
#     diffs.append(
#         {
#           'field_name': 'owner_org',
#           'ckan_value': ckan_dataset['organization']['name'],
#           'datapackage_value': dp_dataset['owner_org']
#         }
#       )

#   # Analyze tags
#   dp_tags = sorted([t['name'] for t in dp_dataset['tags']])
#   ckan_tags = sorted([t['name'] for t in ckan_dataset['tags']])
#   if dp_tags == ckan_tags:
#     oks.append('tags')
#   else:
#     diffs.append(
#         {
#           'field_name': 'tags',
#           'ckan_value': ckan_tags,
#           'datapackage_value': dp_tags
#         }
#       )

#   # Analyze notes
#   dp_notes = dp_dataset['notes'].replace('\n', '')
#   ckan_notes = ckan_dataset['notes'].replace('\n', '')
#   if dp_tags == ckan_tags:
#     oks.append('notes')
#   else:
#     diffs.append(
#         {
#           'field_name': 'notes',
#           'ckan_value': ckan_tags,
#           'datapackage_value': dp_tags
#         }
#       )

#   return diffs, oks
