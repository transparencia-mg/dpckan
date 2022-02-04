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
                              resource_create,
                              resource_update_datastore_metadata,
                              get_ckan_dataset_resources_ids,
                              get_ckan_datapackage_resource_id,
                              dataset_patch,)

def create_resource(ckan_host, ckan_key, datapackage, resource_name, stop):
  package = load_complete_datapackage(datapackage)
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  run_resource_validations(ckan_instance, package, stop)
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
  dataset_patch(ckan_instance, package)

@click.command()
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help=host_flag_) # -H to respect convention of -h in help option
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help=key_flag_)
@click.option('--datapackage', '-dp', required=True, default='datapackage.json',
              help=datapackage_flag_)
@click.option('--resource-name', '-rn', required=True,
              help=resource_name_flag_)
@click.option('--stop', '-s', is_flag=True, help=stop_flag_)
def create_resource_cli(ckan_host, ckan_key, datapackage, resource_name, stop):
  """
  Create a resource in a dataset published in ckan.
  """
  create_resource(ckan_host, ckan_key, datapackage, resource_name, stop)

