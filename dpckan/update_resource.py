import sys
import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_resource_validations
from dpckan.functions import (
                              load_complete_datapackage,
                              update_datapackage_json_resource, 
                              resource_update,
                              get_ckan_datapackage_resource_id,
                              dataset_path,
                              )

def update_resource(ckan_host, ckan_key, datapackage, datastore, exit_code, resource_name, resource_id):
  local_package = load_complete_datapackage(datapackage)
  dataset = dataset_path(ckan_host, local_package)
  click.echo(f"Updating resource on {dataset}")
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  try:
    run_resource_validations(ckan_instance, local_package)
    resource_update(ckan_instance,
                    resource_id,
                    local_package.get_resource(resource_name),
                    datastore,
                    )
    # Find ckan datapackage resource id
    ckan_datapackage_resource_id = get_ckan_datapackage_resource_id(ckan_instance, local_package.name)
    # Update ckan datapackage resource
    update_datapackage_json_resource(ckan_instance, local_package, ckan_datapackage_resource_id)
    click.echo(f"Resource {resource_name} updated on {dataset}")
  except Exception:
    print(f"Error updating {resource_name} resource on {dataset}")    
    if exit_code == True:
      sys.exit(1)

@click.command(name='update')
@click.argument('resource_id', required=True)
@click.pass_context
def update_resource_cli(ctx, resource_id):
  """
  Update dataset resource in a CKAN instance.
  """
  update_resource(
                  ctx.obj['CKAN_HOST'],
                  ctx.obj['CKAN_KEY'],
                  ctx.obj['DATAPACKAGE'],
                  ctx.obj['DATASTORE'],
                  ctx.obj['EXIT_CODE'],
                  ctx.obj['RESOURCE_NAME'],
                  resource_id,
                  )
  
