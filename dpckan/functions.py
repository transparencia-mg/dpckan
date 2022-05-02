import sys
import os
import click
import hashlib
import json
from urllib.request import urlopen
from urllib import request
from frictionless_ckan_mapper import frictionless_to_ckan as f2c
from ckanapi import RemoteCKAN
from frictionless import Package
import shutil
import validators
import re

def load_complete_datapackage(source):
  datapackage = Package(source)
  for resource_name in datapackage.resource_names:
    datapackage.get_resource(resource_name).dialect.expand()
    datapackage.get_resource(resource_name).schema.expand()
  return datapackage

def dataset_create(ckan_instance, datapackage, datastore):
  # In this context datapackage is frictionless package object from datapackage.json local file
  remote_datapackage = frictionless_to_ckan(datapackage)
  click.echo(f"Criando conjunto: {datapackage.name}")
  ckan_instance.call_action('package_create', remote_datapackage)
  resources_ids = {}
  for resource_name in datapackage.resource_names:
    resource_ckan = resource_create(
                                    ckan_instance,
                                    datapackage.name,
                                    datapackage.get_resource(resource_name),
                                    datastore,
                                    )
    resources_ids[resource_name] = resource_ckan['id']
  ckan_datapackage_resource_id = create_datapackage_json_resource(ckan_instance, datapackage)
  resources_ids['datapackage.json'] = ckan_datapackage_resource_id
  datapackage['resources_ids'] = resources_ids
  dataset_patch_resources_ids(ckan_instance, datapackage)

def resource_create(ckan_instance, datapackage_id, resource, datastore):
  click.echo(f"Creating resource: {resource.name}")
  payload = {"package_id":datapackage_id,
               "name": resource.title,
               "description": resource.description,
               "url": resource.path}
  if(resource.path.startswith('http')):
    resource_ckan = ckan_instance.call_action('resource_create', payload)
  else:
    upload_files = {'upload': open(os.path.join(resource.basepath, resource.path), 'rb')}
    resource_ckan = ckan_instance.call_action('resource_create', payload, files=upload_files)
  if datastore == True:
    resource_update_datastore_metadata(ckan_instance,
                              resource_ckan['id'],
                              resource)
  return resource_ckan

def resource_update(ckan_instance, resource_id, resource, datastore):
  click.echo(f"Updating data and metadata of resource {resource.name}.")
  payload = {"id": resource_id,
             "name": resource.title,
             "description": resource.description,
             "url": resource.path}
  if(resource.path.startswith('http')):
    resource_ckan = ckan_instance.call_action('resource_update', payload)
  else:
    resource_ckan = ckan_instance.call_action('resource_update', payload,
                                       files={'upload': open(os.path.join(resource.basepath, resource.path), 'rb')})
  if datastore == True:
    resource_update_datastore_metadata(ckan_instance,
                                  resource_ckan['id'],
                                  resource)
  return resource_ckan

def resource_update_datastore_metadata(ckan_instance, resource_id, resource):
  click.echo(f"Updating resource {resource.name} datastore.")
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

def is_dataset_published(ckan_instance, dataset_id):
  try:
    result = ckan_instance.action.package_show(id = dataset_id)
  except Exception:
    return False

  if(result['state'] == 'deleted'):
    return False

  return True

def create_datapackage_json_resource(ckan_instance, datapackage):
  click.echo("Criando recurso: datapackage.json")
  basepath = find_dataset_basepath(datapackage)
  expand_datapackage(datapackage, basepath)
  resource_ckan = ckan_instance.action.resource_create(package_id = datapackage.name,
                                       name = 'datapackage.json',
                                       upload = open(f"{basepath}/temp/datapackage.json", 'rb'))
  os.system(f'rm -rf {basepath}/temp')
  return resource_ckan['id']

def update_datapackage_json_resource(ckan_instance, datapackage, resource_id):
  click.echo(f"Updating resource datapackage.json.")
  datapackage.pop('resources_ids', None)
  basepath = find_dataset_basepath(datapackage)
  expand_datapackage(datapackage, basepath)
  ckan_instance.action.resource_update(id = resource_id,
                                       upload = open(f"{basepath}/temp/datapackage.json", 'rb'))
  os.system(f'rm -rf {basepath}/temp')

def find_dataset_basepath(datapackage):
  if datapackage.basepath == '':
    return '.'
  else:
    return datapackage.basepath

def expand_datapackage(datapackage, basepath):
  datapackage.to_json(f'{basepath}/temp/datapackage.json')

def dataset_update(ckan_instance, datapackage, datastore, exit_code):
  different_resources = dataset_diff(ckan_instance, datapackage)
  if len(different_resources) > 0:
    click.echo(f'Updating dataset {ckan_instance.address}/dataset/{datapackage.name}.')
    ckan_datapackage_resource_id = get_ckan_datapackage_resource_id(ckan_instance, datapackage.name)
    for resource in different_resources:
      if resource['name'] != 'datapackage.json':
        if resource['data_diff'] or resource['metadada_diff']:
          resource_update(ckan_instance, resource['id'], datapackage.get_resource(resource['name']), datastore)
          if datastore == True:
            resource_update_datastore_metadata(ckan_instance, resource['id'], datapackage.get_resource(resource['name']))
    update_datapackage_json_resource(ckan_instance, datapackage, ckan_datapackage_resource_id)
    dataset_patch(ckan_instance, datapackage)
    click.echo(f'Dataset {datapackage.name} updated.')
  else:
    click.echo(f'Nothing to be updated in dataset {ckan_instance.address}/dataset/{datapackage.name}.')
    if exit_code == True:
      sys.exit(1)

def dataset_patch(ckan_instance, datapackage):
  datapackage['resources_ids'] = get_ckan_dataset_resources_ids(ckan_instance, datapackage)
  ckan_datapackage = frictionless_to_ckan(datapackage)
  ckan_datapackage['id'] = datapackage.name
  ckan_instance.call_action('package_patch', ckan_datapackage)

def dataset_diff(ckan_instance, datapackage):
  different_resources = list()
  ckan_dataset_resources_ids = get_ckan_dataset_resources_ids(ckan_instance, datapackage)
  ckan_dataset_resources_names = get_ckan_dataset_resources_names(ckan_dataset_resources_ids)
  for resource_name in ckan_dataset_resources_names:
    if resource_name in datapackage.resource_names or resource_name == 'datapackage.json':
      resource_id = ckan_dataset_resources_ids[resource_name]
      resource_diff = get_resource_diff(ckan_instance, datapackage, resource_name, resource_id)
      if resource_diff['data_diff'] or resource_diff['metadada_diff']:
        different_resources.append(resource_diff)
  return different_resources

def get_ckan_dataset_resources_ids(ckan_instance, datapackage):
  ckan_dataset = ckan_instance.action.package_show(id = datapackage.name)
  ckan_dataset_extras_property = ckan_dataset.get('extras')
  ckan_dataset_resources_ids = [i.get('value') for i in ckan_dataset_extras_property if i.get('key') == 'resources_ids']
  if len(ckan_dataset_resources_ids) == 0:
    click.echo(f"'resources_ids' property not found in 'extras' field of dataset {ckan_instance.address}/dataset/{datapackage.name}.")
    sys.exit(1)
  elif len(ckan_dataset_resources_ids) > 0:
    ckan_dataset_resources_ids = json.loads(ckan_dataset_resources_ids[0])
  return ckan_dataset_resources_ids

def get_ckan_dataset_resources_names(ckan_dataset_resources_ids):
  return [*ckan_dataset_resources_ids.keys()]

def get_resource_diff(ckan_instance, datapackage, resource_name, resource_id):
  resource_diff = dict()
  resource_diff['id'] = resource_id
  resource_diff['name'] = resource_name
  resource_diff['data_diff'] = is_resource_data_diff(ckan_instance,
                                                     datapackage,
                                                     resource_name,
                                                     resource_id)
  if resource_name != 'datapackage.json':
    resource_diff['metadada_diff'] = is_resource_metadata_diff(ckan_instance,
                                                       datapackage,
                                                       resource_name,
                                                       resource_id)
  else:
    resource_diff['metadada_diff'] = False
  return resource_diff

def is_resource_data_diff(ckan_instance, datapackage, resource_name, resource_id):
  local_data_hash = resource_hash(datapackage, resource_name)
  ckan_data_hash = resource_url_hash(ckan_instance, resource_id)
  if local_data_hash != ckan_data_hash:
    return True
  else:
    return False

def is_resource_metadata_diff(ckan_instance, datapackage, resource_name, resource_id):
  local_resource_metadata = datapackage.get_resource(resource_name)
  remote_dataset_metadata = get_remote_dataset_metadata(ckan_instance, datapackage.name)
  remote_resource_metadata = remote_dataset_metadata.get_resource(resource_name)
  if local_resource_metadata != remote_resource_metadata:
    return True
  else:
    return False

def get_remote_dataset_metadata(ckan_instance, dataset_name):
  ckan_datapackage_resource_id = get_ckan_datapackage_resource_id(ckan_instance, dataset_name)
  ckan_datapackage_resource = ckan_instance.action.resource_show(id=ckan_datapackage_resource_id)
  remote_dataset_metadata = Package(ckan_datapackage_resource['url'])
  return remote_dataset_metadata

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

def dataset_patch_resources_ids(ckan_instance, datapackage):
  ckan_datapackage = dict()
  ckan_datapackage['extras'] = frictionless_to_ckan(datapackage)['extras']
  ckan_datapackage['id'] = datapackage.name
  ckan_instance.call_action('package_patch', ckan_datapackage)

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

def get_ckan_datapackage_resource_id(ckan_instance, dataset_id):
  # Use show_package endpoint in ckan api to retrieve all dataset's resources
  ckan_datapackage_resources = ckan_instance.action.package_show(id=dataset_id)["resources"]
  # Filtering datackage_id - https://stackoverflow.com/a/48192370/11755155
  try:
    ckan_datapackage_resource_id = [i["id"] for i in ckan_datapackage_resources if i["url"].split('/')[-1] == "datapackage.json"][0]
    return ckan_datapackage_resource_id
  except IndexError:
    click.echo("Aborted: CKAN Dataset doesn't have required datapackage.json resource to complete the job.")
    sys.exit(1)

def get_dataset(ckan_host, link_id, path):
  if validate_url(link_id) and valid_dataset_url(link_id):
    ckan_host = split_dataset_url(link_id)[0]
    dataset_id = split_dataset_url(link_id)[1]
    download_dataset_resources(ckan_host, dataset_id, path)
  elif is_uuid(link_id):
    download_dataset_resources(ckan_host, link_id, path)
  elif not is_uuid(link_id) and valid_dataset_url(f"{ckan_host}/dataset/{link_id}"):
    download_dataset_resources(ckan_host, link_id, path)
  else:
    click.echo('Wrong arguments to get dataset. Chek dataset link or CKAN_HOST with dataset id or name informed.')
    sys.exit(1)

def download_dataset_resources(ckan_host, dataset_id, path):
  ckan_instance = RemoteCKAN(ckan_host)
  dataset_information = ckan_instance.action.package_show(id = dataset_id)
  dataset_name = dataset_information["name"]
  remote_dataset_metadata = get_remote_dataset_metadata(ckan_instance, dataset_name)
  path = path.split("/")
  path = list(filter(None, path))
  path = "/".join(path)
  if not os.path.exists(f'{path}/{dataset_name}'):
    click.echo(f'Creating {path}/{dataset_name} folder.')
    os.makedirs(f'{path}/{dataset_name}')
  else:
    if click.confirm(f'Folder {path}/{dataset_name} already exist. Do you want to delete it and continue?'):
      click.echo(f"Cleaning {path}/{dataset_name}'s folder contents.")
      shutil.rmtree(f'{path}/{dataset_name}')
      os.makedirs(f'{path}/{dataset_name}')
      for resource in dataset_information["resources"]:
        resource_url = resource["url"]
        if resource_url.split('/')[-1] == 'datapackage.json':
          click.echo('Downloading datapackage.json.')
          request.urlretrieve(resource_url, f'{path}/{dataset_name}/datapackage.json')
        else:
          file_name = resource_url.split('/')[-1].split('.')[0]
          file_path = remote_dataset_metadata.get_resource(file_name).path
          file_path = "/".join(file_path.split("/")[0:-1])
          os.makedirs(f'{path}/{dataset_name}/{file_path}', exist_ok=True)
          click.echo(f'Downloading {file_name} resource to {path}/{dataset_name}/{file_path}.')
          request.urlretrieve(resource_url, f'{path}/{dataset_name}/{file_path}/{file_name}.csv')
    else:
      click.echo('Process aborted.')

def split_dataset_url(dataset_url):
  dataset_url_list = list()
  dataset_url_splited = dataset_url.split('//')
  url_first_part = dataset_url_splited[0]
  url_second_part = dataset_url_splited[1].split('/')[0]
  host = f'{url_first_part}//{url_second_part}'
  dataset_id = dataset_url_splited[1].split('/')[2]
  dataset_url_list.append(host)
  dataset_url_list.append(dataset_id)
  return dataset_url_list

def valid_dataset_url(dataset_url):
  dataset_len = len(dataset_url.split('/'))
  if dataset_len >= 5:
    ckan_host = split_dataset_url(dataset_url)[0]
    dataset_id = split_dataset_url(dataset_url)[1]
    ckan_instance = RemoteCKAN(ckan_host)
    if is_dataset_published(ckan_instance, dataset_id):
      return True
    else:
      return False

def validate_url(url):
  response = validators.url(url)
  if response:
    return True
  else:
    return False

def is_uuid(uuid):
  matched = re.match('[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}', uuid)
  if bool(matched) == True:
    return True
  else:
    return False
