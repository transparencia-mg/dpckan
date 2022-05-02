import click
from dpckan.create_dataset import create_cli as dc
from dpckan.update_dataset import update_cli as du
from dpckan.create_resource import create_cli as rc
from dpckan.update_resource import update_resource_cli as ru
from dpckan.diff_dataset import diff_dataset_cli
from dpckan.diff_resource import diff_resource_cli
from dpckan.get_dataset import get_dataset_cli

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help='''
                   Host or link to CKAN's instance wanted.
                   Example: https://dados.mg.gov.br.
                   Not required if CKAN_HOST environment variable is defined.
                   ''')
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help='''
                   CKAN key of the user for the CKAN's environment wanted.
                   Not required if CKAN_KEY environment variable is defined.
                   ''')
@click.option('--datapackage', '-dp', required=True, default='datapackage.json',
              help='''
                   Local path to datapackage.json file.
                   Not required if the command run in the same directory as the datapackage.json file.
                   ''')
@click.option('--datastore/--no-datastore', default=False,
             help='''
             Load resource table schema to Data Store Data Dictionary.
             -no--datastore = False set as default.
             If you want load Data Store Data Dictionary --datastore flag must be informed.
             ''')
@click.option('--exit-code/--no-exit-code', default=False,
             help='''
             Set exit code to 1.
             --no-exit-code = False set as default.
             If you want exit code set to 1 exit-code flag must be informed.
             ''')
@click.pass_context
def cli(ctx, ckan_host, ckan_key, datapackage, datastore, exit_code):
  """
    Conjunto de comandos criados para publicações/atualizações de datasets em instâncias CKAN
  """
  ctx.ensure_object(dict)
  ctx.obj['CKAN_HOST'] = ckan_host
  ctx.obj['CKAN_KEY'] = ckan_key
  ctx.obj['DATAPACKAGE'] = datapackage
  ctx.obj['DATASTORE'] = datastore
  ctx.obj['EXIT_CODE'] = exit_code

@cli.group()
def dataset():
  """
    Funções responsáveis pela criação e atualização de conjuntos de dados em uma instância CKAN.
  """
  pass

dataset.add_command(dc)
dataset.add_command(du)
dataset.add_command(diff_dataset_cli)
dataset.add_command(get_dataset_cli)

@cli.group()
@click.argument('resource_name', required=True)
@click.pass_context
def resource(ctx, resource_name):
  """
    Funções responsáveis pela criação e atualização de recursos em conjuntos de dados publicados em uma instância CKAN.
  """
  ctx.ensure_object(dict)
  ctx.obj['RESOURCE_NAME'] = resource_name

resource.add_command(rc)
resource.add_command(ru)
resource.add_command(diff_resource_cli)
