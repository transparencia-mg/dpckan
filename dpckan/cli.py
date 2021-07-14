import click
from dpckan.create_dataset import create
from dpckan.update_dataset import update
from dpckan.create_resource import create_resource
from dpckan.update_resource import update_resource

@click.group()
def cli():
  """
    Conjunto de comandos criados para publicações/atualizações de datasets em instâncias CKAN
  """
  pass

cli.add_command(create)
cli.add_command(update)
cli.add_command(create_resource)
cli.add_command(update_resource)
