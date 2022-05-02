import click
from ckanapi import RemoteCKAN
from dpckan.functions import (load_complete_datapackage, 
                              dataset_update, 
                              update_datapackage_json_resource,)
                              
def update(ckan_host, ckan_key, datapackage, datastore, exit_code):
  package = load_complete_datapackage(datapackage)

  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)

  # update_datapackage_json_resource(ckan_instance, package)
  dataset_update(ckan_instance, package, datastore, exit_code)

@click.command(name='update')
@click.pass_context
def update_cli(ctx):
  """
  Update dataset in a CKAN instance
  """
  update(
         ctx.obj['CKAN_HOST'], 
         ctx.obj['CKAN_KEY'], 
         ctx.obj['DATAPACKAGE'], 
         ctx.obj['DATASTORE'],
         ctx.obj['EXIT_CODE'],
         )
