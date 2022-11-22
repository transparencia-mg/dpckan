import sys
import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_resource_validations
from dpckan.functions import (
                              load_complete_datapackage,
                              update_datapackage_json_resource, 
                              resource_create,
                              get_ckan_dataset_resources_ids,
                              get_ckan_datapackage_resource_id,
                              dataset_patch_resources_ids,
                              dataset_path,
                              )

def create(ckan_host, ckan_key, datapackage, datastore, exit_code, resource_name):
  local_datapackage = load_complete_datapackage(datapackage)
  dataset = dataset_path(ckan_host, local_datapackage)
  click.echo(f"Creating resource on {dataset}")
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  try:
    run_resource_validations(ckan_instance, local_datapackage)
    resource_ckan = resource_create(
                                    ckan_instance,
                                    local_datapackage.name,
                                    local_datapackage.get_resource(resource_name),
                                    datastore,
                                    )
    # Update dataset with new resource id
    local_datapackage['resources_ids'] = get_ckan_dataset_resources_ids(ckan_instance, local_datapackage)
    local_datapackage['resources_ids'][resource_name] = resource_ckan['id']
    ckan_datapackage_resource_id = get_ckan_datapackage_resource_id(ckan_instance, local_datapackage.name)
    dataset_patch_resources_ids(ckan_instance, local_datapackage)
    update_datapackage_json_resource(ckan_instance, local_datapackage, ckan_datapackage_resource_id)
    click.echo(f"Resource {resource_name} created on {dataset}")
  except Exception:
    print(f"Error creating {resource_name} resource on {dataset}")
    if exit_code == True:
      sys.exit(1)

@click.command(name='create')
@click.pass_context
def create_cli(ctx):
  """
  Create dataset resource in a CKAN instance.
  """
  create(
         ctx.obj['CKAN_HOST'],
         ctx.obj['CKAN_KEY'],
         ctx.obj['DATAPACKAGE'],
         ctx.obj['DATASTORE'],
         ctx.obj['EXIT_CODE'],
         ctx.obj['RESOURCE_NAME'],
        )
