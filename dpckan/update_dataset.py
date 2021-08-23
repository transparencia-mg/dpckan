import click
from ckanapi import RemoteCKAN
from dpckan.validations import run_validations
from dpckan.functions import (load_complete_datapackage, dataset_update, update_datapackage_json_resource)
                              

@click.command()
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: http://dados.mg.gov.br ou https://dados.mg.gov.br")  # -H para respeitar convenção de -h ser help
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
@click.option('--datapackage', '-dp', required=True, default='datapackage.json')
def update(ckan_host, ckan_key, datapackage):
  
  package = load_complete_datapackage(datapackage)
  run_validations(ckan_host, ckan_key, package)

  ckan_instance = RemoteCKAN(ckan_host, apikey = ckan_key) 
  
  update_datapackage_json_resource(ckan_instance, package)
  dataset_update(ckan_instance, package)
