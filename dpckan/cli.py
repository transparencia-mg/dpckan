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

@cli.group()
def dataset():
  pass

dataset.add_command(create)
dataset.add_command(update)

@cli.group()
def resource():
  pass

resource.add_command(create_resource, 'create')
resource.add_command(update_resource, 'update')
