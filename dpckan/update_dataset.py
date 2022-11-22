import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_dataset_validations
from dpckan.functions import (load_complete_datapackage, 
                              dataset_update, 
                              update_datapackage_json_resource,
                              dataset_path,
                              )
                              
def update(ckan_host, ckan_key, datapackage, datastore, exit_code):
  local_datapackage = load_complete_datapackage(datapackage)
  dataset = dataset_path(ckan_host, local_datapackage)
  click.echo(f"Updating dataset {dataset}")
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  try:
    # run_resource_validations(ckan_instance, local_package)
    dataset_update(ckan_instance, local_datapackage, datastore, exit_code)
    click.echo(f"Dataset {dataset} updated")
  except Exception:
    click.echo(f"Error during {dataset} updating")
    if exit_code == True:
      sys.exit(1)

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
