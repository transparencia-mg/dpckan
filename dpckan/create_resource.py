import click
from ckanapi import RemoteCKAN
from dpckan.functions import (load_complete_datapackage, 
                              update_datapackage_json_resource, 
                              resource_create,
                              resource_update_datastore_metadata,
                              dataset_update)

@click.command()
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: http://dados.mg.gov.br ou https://dados.mg.gov.br")  # -H para respeitar convenção de -h ser help
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
@click.option('--datapackage', '-dp', required=True, default='datapackage.json')
@click.argument('resource_name', required=True)
def create_resource(ckan_host, ckan_key, datapackage, resource_name):
  # try:
  package = load_complete_datapackage(datapackage)
  # Show package to find datapackage.json resource id
  # Update datapakcage.json resource
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  
  update_datapackage_json_resource(ckan_instance, package)
  dataset_update(ckan_instance, package)
  # Create new resource
  resource_ckan = resource_create(ckan_instance,
                                  package.name,
                                  package.get_resource(resource_name))
  resource_update_datastore_metadata(ckan_instance,
                            resource_ckan['id'],
                            package.get_resource(resource_name))

