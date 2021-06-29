import click
from dpckan.publish import publish

@click.group()
def cli():
  """
    Conjunto de comandos criados para publicações/atualizações de datasets em instâncias CKAN
  """
  pass

cli.add_command(publish)
