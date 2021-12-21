import os
import click
import hashlib
import json
from urllib.request import urlopen
from frictionless_ckan_mapper import frictionless_to_ckan as f2c
from ckanapi import RemoteCKAN
from frictionless import Package

def load_complete_datapackage(source):
  datapackage = Package(source)
  for resource_name in datapackage.resource_names:
    datapackage.get_resource(resource_name).dialect.expand()
    datapackage.get_resource(resource_name).schema.expand()
  return datapackage

def dataset_create(ckan_instance, datapackage, metadata):
  # In this context datapackage is frictionless package object from datapackage.json local file
  remote_datapackage = frictionless_to_ckan(datapackage)
  ckan_instance.call_action('package_create', remote_datapackage)
  clean_datapackage_with_ckan_ids(ckan_instance, datapackage)
  for resource_name in datapackage.resource_names:
    resource_ckan = resource_create(ckan_instance,
                                    datapackage.name,
                                    datapackage.get_resource(resource_name))
    if metadata == True:
      resource_update_datastore_metadata(ckan_instance,
                                resource_ckan['id'],
                                datapackage.get_resource(resource_name)
                                )
    update_datapackage_with_ckan_ids(ckan_instance, datapackage, resource_name, resource_ckan['id'])
  create_datapackage_json_resource(ckan_instance, datapackage)

def resource_create(ckan_instance, datapackage_id, resource):
  click.echo(f"Criando recurso: {resource.name}")
  payload = {"package_id":datapackage_id,
               "name": resource.title,
               "description": resource.description,
               "url": resource.path}
  if(resource.path.startswith('http')):
    result = ckan_instance.call_action('resource_create', payload)
  else:
    upload_files = {'upload': open(os.path.join(resource.basepath, resource.path), 'rb')}
    result = ckan_instance.call_action('resource_create', payload, files=upload_files)
  return result

def update_datapackage_with_ckan_ids(ckan_instance, datapackage, resource_name, resource_id):
  basepath = find_dataset_basepath(datapackage)
  dp = Package(f"{basepath}/datapackage.json")
  if 'ckan_hosts' not in dp:
    dp['ckan_hosts'] = {}
    dp['ckan_hosts'][ckan_instance.address] = {}
    dp['ckan_hosts'][ckan_instance.address][resource_name] = resource_id
  else:
    if ckan_instance.address not in dp['ckan_hosts']:
      dp['ckan_hosts'][ckan_instance.address] = {}
      dp['ckan_hosts'][ckan_instance.address][resource_name] = resource_id
    else:
      dp['ckan_hosts'][ckan_instance.address][resource_name] = resource_id
  dp.to_json(f"{basepath}/datapackage.json")

def clean_datapackage_with_ckan_ids(ckan_instance, package):
  basepath = find_dataset_basepath(package)
  package = Package(f'{basepath}/datapackage.json')
  if 'ckan_hosts' in package and ckan_instance.address in package['ckan_hosts']:
    package['ckan_hosts'].pop(ckan_instance.address)
    package.to_json(f'{basepath}/datapackage.json')

def find_dataset_basepath(datapackage):
  if datapackage.basepath == '':
    return '.'
  else:
    return datapackage.basepath

def resource_update_datastore_metadata(ckan_instance, resource_id, resource):
  click.echo(f"Atualizando metadado de recurso: {resource.name}")
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
  basepath = find_dataset_basepath(datapackage)
  expand_datapackage(datapackage, basepath)
  resource_ckan = ckan_instance.action.resource_create(package_id = datapackage.name,
                                       name = 'datapackage.json',
                                       upload = open(f"{basepath}/temp/extended_datapackage.json", 'rb'))
  update_datapackage_with_ckan_ids(ckan_instance, datapackage, 'datapackage.json', resource_ckan['id'])
  update_datapackage_json_resource(ckan_instance, datapackage, resource_ckan['id'])

def update_datapackage_json_resource(ckan_instance, datapackage, resource_id):
  click.echo(f"Atualizando datapackage.json")
  basepath = find_dataset_basepath(datapackage)
  updated_datapackage = load_complete_datapackage(f'{basepath}/datapackage.json')
  expand_datapackage(updated_datapackage, basepath)
  ckan_instance.action.resource_update(id = resource_id,
                                       upload = open(f"{basepath}/temp/extended_datapackage.json", 'rb'))
  os.system(f'rm -rf {basepath}/temp')

def expand_datapackage(datapackage, basepath):
  datapackage.to_json(f'{basepath}/temp/extended_datapackage.json')

def dataset_update(ckan_instance, datapackage, metadata):
  click.echo(f"Atualizando conjunto de dados: {datapackage.name}")
  # Find ckan host url
  ckan_host = ckan_instance.address
  # Find datapackage.json id for ckan instance in local datapackage.json file
  datapackage_id = datapackage['ckan_hosts'][ckan_instance.address]['datapackage.json']
  # Find datapackage resource in ckan instance
  ckan_datapackage_resource = ckan_instance.action.resource_show(id = datapackage_id)
  # Load ckan_datapackage_resource as json
  remote_datapackage = load_complete_datapackage(json.loads(urlopen(ckan_datapackage_resource['url']).read()))
  dataset_diff(ckan_instance, datapackage, remote_datapackage, metadata)

def dataset_diff(ckan_instance, datapackage, dataset, metadata):
  # Remote datapackage.json resources
  dataset_remote_resources = dataset['ckan_hosts'][ckan_instance.address]
  # Local datapackage.json resource
  datapackage_local_resources = datapackage['ckan_hosts'][ckan_instance.address]
  # Compare resources in datapackage.json remote with local
  for name in dataset_remote_resources.keys(): # Iterate through remote ckan_hosts property
    if name != 'datapackage.json':
      if name in datapackage_local_resources.keys() and name in datapackage.resource_names: # Is this name valid in local ckan_hosts?
        if name in datapackage.resource_names: # Is this name valid in local resources?
          local_data_hash = resource_hash(datapackage, name)
          remote_data_hash = resource_url_hash(ckan_instance, dataset_remote_resources[name])
          if local_data_hash != remote_data_hash:
            click.echo(f"Diferenças nos dados do recurso: {name}")
            resource_update(ckan_instance, datapackage_local_resources[name], datapackage.get_resource(name))
          if datapackage.get_resource(name) != dataset.get_resource(name) and metadata == True:
            click.echo(f"Diferenças nos metadados recurso: {name}")
            resource_update_datastore_metadata(ckan_instance, datapackage_local_resources[name], datapackage.get_resource(name))
            update_datapackage_json_resource(ckan_instance, datapackage, datapackage_local_resources['datapackage.json'])
            dataset_patch(ckan_instance, datapackage)
          if datapackage.get_resource(name) != dataset.get_resource(name):
            update_datapackage_json_resource(ckan_instance, datapackage, datapackage_local_resources['datapackage.json'])
            dataset_patch(ckan_instance, datapackage)
      else:
        print(f'Recurso {name} inexistente localmente, `dpckan resource delete` para excluí-lo da instância {ckan_instance.address}')
    if name == 'datapackage.json':
      local_data_hash = resource_hash(datapackage, name)
      remote_data_hash = resource_url_hash(ckan_instance, dataset_remote_resources[name])
      if local_data_hash != remote_data_hash:
        click.echo(f"Diferenças nos metadados do conjunto: {dataset.name}")
        update_datapackage_json_resource(ckan_instance, datapackage, datapackage_local_resources['datapackage.json'])
        dataset_patch(ckan_instance, datapackage)
  # Compare resources in datapackage.json local with remote
  for name in datapackage.resource_names:
    if name != 'datapackage.json':
      if name not in dataset.resource_names:
        print(f'Recurso {name} não existe na instância {ckan_instance.address}. utilize `dpckan resource create` para cria-lo')

def dataset_patch(ckan_instance, datapackage):
  ckan_datapackage = frictionless_to_ckan(datapackage)
  ckan_datapackage['id'] = datapackage.name
  ckan_instance.call_action('package_patch', ckan_datapackage)

def resource_hash(datapackage, name):
  resource_content = ''
  md5_hash = hashlib.md5()
  if name == 'datapackage.json':
    ckan_datapackage = frictionless_to_ckan(datapackage)
    resource_content = json.dumps(ckan_datapackage).encode('utf-8')
  else:
    basepath = find_dataset_basepath(datapackage)
    resource_path = datapackage.get_resource(name)['path']
    resource_content = open(f'{basepath}/{resource_path}', "rb").read()
  md5_hash.update(resource_content)
  resource_hash = md5_hash.hexdigest()
  return resource_hash

def resource_url_hash(ckan_instance, resource_id):
  resource_content = ''
  md5_hash = hashlib.md5()
  ckan_datapackage_resource = ckan_instance.action.resource_show(id = resource_id)
  if ckan_datapackage_resource['name'] == 'datapackage.json':
    # Buscar os metatados do dataset para retirar a key notes
    ckan_datapackage = ckan_instance.action.package_show(id=ckan_datapackage_resource['package_id'])
    # Buscar arquivo datapackage.json remoto para criar hash
    resource_content = urlopen(ckan_datapackage_resource['url']).read()
    resource_content = json.loads(resource_content.decode('utf-8'))
    resource_content = Package(resource_content)
    # Convert para metadados ckan para igualar à conversão do arquivo local
    # Esta conversão é importante para comparar modificações README, CHANGELOG e CONTRIBUTING
    resource_content = frictionless_to_ckan(resource_content)
    resource_content['notes'] = ckan_datapackage['notes']
    resource_content = json.dumps(resource_content).encode('utf-8')
  else:
    resource_content = urlopen(ckan_datapackage_resource['url']).read()
  md5_hash.update(resource_content)
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
    dataset["notes"] = ""
    dataset["notes"] += f"\n{open(README_path, encoding='utf-8').read()}"
  if os.path.isfile(CONTRIBUTING_path):
    dataset["notes"] += f"\n{open(CONTRIBUTING_path, encoding='utf-8').read()}"
  if os.path.isfile(CHANGELOG_path):
    dataset["notes"] += f"\n{open(CHANGELOG_path, encoding='utf-8').read()}"
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

# def resource_hash(package, resouce_name):
#   if resouce_name != 'datapackage.json':
#     resource = package.get_resource(resouce_name)
#     resource.infer(stats=True)
#     return resource['stats']['hash']
