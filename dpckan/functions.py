import ipdb
import os
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

def dataset_create(ckan_instance, package, datapackage):
  dataset = frictionless_to_ckan(package)
  ckan_instance.call_action('package_create', dataset)
  for resource_name in package.resource_names:
    resource_ckan = resource_create(ckan_instance,
                                    package.name,
                                    package.get_resource(resource_name))
    resource_update_datastore_metadata(ckan_instance,
                              resource_ckan['id'],
                              package.get_resource(resource_name)
                              )
    update_datapackage_with_ckan_ids(ckan_instance, datapackage, resource_name, resource_ckan['id'])
  create_datapackage_json_resource(ckan_instance, package)

def update_datapackage_with_ckan_ids(ckan_instance, datapackage, resource_name, resource_id):
  dp = Package(datapackage)
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
  dp.to_json(datapackage)


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
  
  ckan_instance.action.resource_create(package_id = datapackage.name,
                                       name = "datapackage.json",
                                       upload = open(os.path.join(datapackage.basepath, 'datapackage.json'), 'rb'))
  

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
  dataset = frictionless_to_ckan(datapackage)
  dataset['id'] = datapackage.name
  ckan_instance.call_action('package_patch', dataset)

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


def dataset_diff(ckan_instance, datapackage):
  dp_dataset = frictionless_to_ckan(datapackage)
  ckan_dataset = ckan_instance.action.package_show(id = datapackage.name)

  diffs = []
  oks = []
  # TODO, add more
  fields = ["title", "version", "url", "license_id"]

  for field in fields:
    if dp_dataset.get(field) == ckan_dataset.get(field):
      oks.append(field)
    else:
      diffs.append(
        {
          'field_name': field,
          'ckan_value': ckan_dataset.get(field),
          'datapackage_value': dp_dataset.get(field)
        }
      )

  # check org (dataset use ID, datapackage uses name)
  if dp_dataset['owner_org'] == ckan_dataset['organization']['name']:
    oks.append('owner_org')
  else:
    diffs.append(
        {
          'field_name': 'owner_org',
          'ckan_value': ckan_dataset['organization']['name'],
          'datapackage_value': dp_dataset['owner_org']
        }
      )

  # Analyze tags
  dp_tags = sorted([t['name'] for t in dp_dataset['tags']])
  ckan_tags = sorted([t['name'] for t in ckan_dataset['tags']])
  if dp_tags == ckan_tags:
    oks.append('tags')
  else:
    diffs.append(
        {
          'field_name': 'tags',
          'ckan_value': ckan_tags,
          'datapackage_value': dp_tags
        }
      )

  # Analyze notes
  dp_notes = dp_dataset['notes'].replace('\n', '')
  ckan_notes = ckan_dataset['notes'].replace('\n', '')
  if dp_tags == ckan_tags:
    oks.append('notes')
  else:
    diffs.append(
        {
          'field_name': 'notes',
          'ckan_value': ckan_tags,
          'datapackage_value': dp_tags
        }
      )

  return diffs, oks
