import os
import click
from ckanapi import RemoteCKAN
from urllib import request
from dpckan.functions import get_dataset

@click.command(name='get')
@click.argument('url', required=True)
@click.argument('path', default='.')
@click.pass_context
def get_dataset_cli(ctx, url, path):
  """
  Get a dataset published in ckan.

  URL required argument could be a Link or name or id of the wanted dataset
  """
  get_dataset(ctx.obj['CKAN_HOST'], url, path)
