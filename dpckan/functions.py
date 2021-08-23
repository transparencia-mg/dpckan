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

def dataset_create(ckan_instance, datapackage):
    
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
    
    ckan_instance.call_action('package_create', dataset)
    
    create_datapackage_json_resource(ckan_instance, datapackage)
    
    for resource_name in datapackage.resource_names:
      resource_ckan = resource_create(ckan_instance,
                                      datapackage.name,
                                      datapackage.get_resource(resource_name))
      resource_update_datastore_metadata(ckan_instance,
                                resource_ckan['id'],
                                datapackage.get_resource(resource_name)
                                )
    

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

  dataset.update({ "id" : datapackage.name})

  ckan_instance.call_action('package_patch', dataset)