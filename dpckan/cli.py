import click
from dpckan.create_dataset import create_cli
from dpckan.update_dataset import update_cli
from dpckan.create_resource import create_resource_cli
from dpckan.update_resource import update_resource_cli

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
  """
    Conjunto de comandos criados para publicações/atualizações de datasets em instâncias CKAN
  """
  pass

@cli.group()
def dataset():
  """
    Funções responsáveis pela criação e atualização de conjuntos de dados em uma instância CKAN.
  """
  pass

dataset.add_command(create_cli)
dataset.add_command(update_cli)

@cli.group()
def resource():
  """
    Funções responsáveis pela criação e atualização de recursos em conjuntos de dados publicados em uma instância CKAN.
  """
  pass

resource.add_command(create_resource_cli, 'create')
resource.add_command(update_resource_cli, 'update')
