import os
import click
from ckanapi import RemoteCKAN
from urllib import request
from dpckan.functions import get_dataset

@click.command(name='get')
@click.argument('path', default='.')
@click.pass_context
@click.option(
              '--link-id', '-li',
              required=True,
              help="Link or name or id of the wanted dataset"
              )
def get_dataset_cli(ctx, link_id, path):
  """
  Get a dataset published in ckan.
  """
  get_dataset(ctx.obj['CKAN_HOST'], link_id, path)
