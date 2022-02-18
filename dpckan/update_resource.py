import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_resource_validations
from dpckan.functions import (load_complete_datapackage, 
                              update_datapackage_json_resource, 
                              resource_update,
                              resource_update_datastore_metadata,
                              dataset_update,
                              get_ckan_datapackage_resource_id,)

def update_resource(ckan_host, ckan_key, datapackage, resource_name, resource_id):
  package = load_complete_datapackage(datapackage)
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  run_resource_validations(ckan_instance, package)
  resource_update(ckan_instance,
                  resource_id,
                  package.get_resource(resource_name))
  resource_update_datastore_metadata(ckan_instance,
                            resource_id,
                            package.get_resource(resource_name))
  # Find ckan datapackage resource id
  ckan_datapackage_resource_id = get_ckan_datapackage_resource_id(ckan_instance, package.name)
  # Update ckan datapackage resource
  update_datapackage_json_resource(ckan_instance, package, ckan_datapackage_resource_id)

@click.command(name='update')
@click.argument('resource_id', required=True)
@click.pass_context
def update_resource_cli(ctx, resource_id):
  """
  Update dataset resource in a CKAN instance.
  """
  update_resource(ctx.obj['CKAN_HOST'], ctx.obj['CKAN_KEY'], ctx.obj['DATAPACKAGE'], ctx.obj['RESOURCE_NAME'], resource_id)
  