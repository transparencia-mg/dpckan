import sys
import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_dataset_validations
from dpckan.functions import (
                              delete_dataset,
                              dataset_create,
                              load_complete_datapackage,
                              )

def create(ckan_host, ckan_key, datapackage, datastore, exit_code):
  local_datapackage = load_complete_datapackage(datapackage)
  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key)
  run_dataset_validations(ckan_instance, local_datapackage)
  try:
    dataset_create(ckan_instance, local_datapackage, datastore)
    print(f"Conjunto de dados {local_datapackage.name} criado.")
  except Exception:
    delete_dataset(ckan_instance, local_datapackage.name)
    print(f"Erro durante criação do conjunto de dados {local_datapackage.name}")
    if exit_code == True:
      sys.exit(1)

@click.command(name='create')
@click.pass_context
def create_cli(ctx):
  """
  Create dataset in a CKAN instance.
  """
  create(
         ctx.obj['CKAN_HOST'],
         ctx.obj['CKAN_KEY'],
         ctx.obj['DATAPACKAGE'],
         ctx.obj['DATASTORE'],
         ctx.obj['EXIT_CODE'],
         )
