import click
from dpckan.create_dataset import create_cli
from dpckan.update_dataset import update_cli
from dpckan.create_resource import create_resource
from dpckan.update_resource import update_resource

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
  """
    Conjunto de comandos criados para publicações/atualizações de datasets em instâncias CKAN
  """
  pass

@cli.group()
def dataset():
  pass

dataset.add_command(create_cli)
dataset.add_command(update_cli)

@cli.group()
def resource():
  pass

resource.add_command(create_resource, 'create')
resource.add_command(update_resource, 'update')
