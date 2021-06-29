import click
import os
from dpckan.functions import is_datapackage_present
from dpckan.functions import get_ckan_key

@click.command(name='publish')
@click.option('--env',
              '-e',
              required=True,
              help='Ambiente aonde datasete será publicado (homologacao ou producao',
              prompt='Qual ambiente deseja publicar/atualizar seu dataset? homologacao ou producao?')
def publish(env):
  """
    Função responsável pela publicação/atualização de um Dataset(conjunto de dados) nos ambientes de produção e homologação.
    A função deverá ser executada no diretório raiz do Dataset, local aonde o arquivo datapackage.json se encontra.
    Chave Ckan do ambiente desejado deverá ser fornecida durante processo de publicação/atualização

    Documentar melhor a função

  """
  datapackage_id = is_datapackage_present(env)
  click.echo()
  ckan_key = get_ckan_key(env)
  print(f'O ambiente desejado é: {env}')
  print(f'Sua Chave é: {ckan_key}')
  print(f'datapackage_id presente: {datapackage_id}')
  print("Fim da Função Publish")
