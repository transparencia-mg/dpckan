import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_resource_validations
from dpckan.functions import (load_complete_datapackage, 
                              update_datapackage_json_resource, 
                              resource_create,
                              resource_update_datastore_metadata,
                              get_ckan_dataset_resources_ids,
                              get_ckan_datapackage_resource_id,
                              dataset_patch_resources_ids,)

def create_resource(ckan_host, ckan_key, datapackage, resource_name):
  package = load_complete_datapackage(datapackage)
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  run_resource_validations(ckan_instance, package)
  # Create new resource
  resource_ckan = resource_create(ckan_instance,
                                  package.name,
                                  package.get_resource(resource_name))
  resource_update_datastore_metadata(ckan_instance,
                            resource_ckan['id'],
                            package.get_resource(resource_name))
  # Update dataset with new resource id
  package['resources_ids'] = get_ckan_dataset_resources_ids(ckan_instance, package)
  package['resources_ids'][resource_name] = resource_ckan['id']
  ckan_datapackage_resource_id = get_ckan_datapackage_resource_id(ckan_instance, package.name)
  update_datapackage_json_resource(ckan_instance, package, ckan_datapackage_resource_id)
  dataset_patch_resources_ids(ckan_instance, package)

@click.command(name='create')
@click.pass_context
def create_resource_cli(ctx):
  """
  Create dataset resource in a CKAN instance.
  """
  create_resource(ctx.obj['CKAN_HOST'], ctx.obj['CKAN_KEY'], ctx.obj['DATAPACKAGE'], ctx.obj['RESOURCE_NAME'])
