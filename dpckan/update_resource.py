import sys
import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_resource_validations
from dpckan.functions import (
                              load_complete_datapackage,
                              update_datapackage_json_resource, 
                              resource_update,
                              get_ckan_datapackage_resource_id,
                              )

def update_resource(ckan_host, ckan_key, datapackage, datastore, exit_code, resource_name, resource_id):
  local_package = load_complete_datapackage(datapackage)
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  run_resource_validations(ckan_instance, local_package)
  try:
    resource_update(ckan_instance,
                    resource_id,
                    local_package.get_resource(resource_name),
                    datastore,
                    )
    # Find ckan datapackage resource id
    ckan_datapackage_resource_id = get_ckan_datapackage_resource_id(ckan_instance, local_package.name)
    # Update ckan datapackage resource
    update_datapackage_json_resource(ckan_instance, local_package, ckan_datapackage_resource_id)
  except Exception:
    print(f"Something went wrong during resource {resource_name} updating")    
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
  
