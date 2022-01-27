import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_resource_validations
from dpckan.docstrings_common_definitions import (host_flag_,
                                                 key_flag_,
                                                 datapackage_flag_,
                                                 resource_id_flag_,
                                                 resource_name_flag_,
                                                 stop_flag_,)
from dpckan.functions import (load_complete_datapackage, 
                              update_datapackage_json_resource, 
                              resource_update,
                              resource_update_datastore_metadata,
                              dataset_update,
                              get_ckan_datapackage_resource_id,)

def update_resource(ckan_host, ckan_key, datapackage, resource_id, resource_name, stop):
  package = load_complete_datapackage(datapackage)
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  run_resource_validations(ckan_instance, package, stop)
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

@click.command()
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help=host_flag_) # -H to respect convention of -h in help option
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help=key_flag_)
@click.option('--datapackage', '-dp', required=True, default='datapackage.json',
              help=datapackage_flag_)
@click.option('--resource-id', '-id', required=True,
              help=resource_id_flag_)
@click.option('--resource-name', '-rn', required=True,
              help=resource_name_flag_)
@click.option('--stop', '-s', is_flag=True, help=stop_flag_)
def update_resource_cli(ckan_host, ckan_key, datapackage, resource_id, resource_name, stop):
  """
  Update resource in a dataset published in ckan.
  """
  update_resource(ckan_host, ckan_key, datapackage, resource_id, resource_name, stop)
