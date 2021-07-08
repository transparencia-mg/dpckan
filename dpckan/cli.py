import click
from dpckan.publish import publish
from dpckan.resource_create import resource_upload
from dpckan.updateResource import resource_update_cli

@click.group()
def cli():
  """
    Conjunto de comandos criados para publicações/atualizações de datasets em instâncias CKAN
  """
  pass

cli.add_command(publish)
cli.add_command(resource_upload)
cli.add_command(resource_update_cli)
