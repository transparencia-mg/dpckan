import ipdb
import os
import json
from click.testing import CliRunner
import unittest
from dpckan.create_dataset import create_cli
from dpckan.tests import (clone_online_repo, get_file_path, get_ckan_instance)
from dpckan.functions import (delete_dataset, datapackage_path,
                              load_complete_datapackage, is_dataset_published)

class TestDatasetPublishDatasetSuccessfully(unittest.TestCase):
  """
    Testing dataset publication sucessfully
  """
  def test_homologa_env(self):
    """
      Testing dataset publication sucessfully homologacao environment
    """
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=get_file_path()):
      clone_online_repo(__file__)
      ckan_instance = get_ckan_instance('CKAN_HOST', 'CKAN_KEY')
      path_datapackage = datapackage_path()
      datapackage = load_complete_datapackage(path_datapackage)
      datapackage_dict = dict(datapackage)
      dataset_name = datapackage_dict['name']
      # Deleting dataset before test
      if is_dataset_published(ckan_instance, datapackage):
        delete_dataset(ckan_instance, dataset_name)
      # Publish dataset
      result = runner.invoke(create_cli)
    # Deleting dataset after test
    self.assertEqual(result.exit_code, 0)
    delete_dataset(ckan_instance, dataset_name)

  def test_production_env(self):
    """
      Testing dataset publication sucessfully production environment
    """
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=get_file_path()):
      clone_online_repo(__file__)
      ckan_instance = get_ckan_instance('CKAN_HOST_PRODUCAO', 'CKAN_KEY_PRODUCAO')
      path_datapackage = datapackage_path()
      datapackage = load_complete_datapackage(path_datapackage)
      datapackage_dict = dict(datapackage)
      dataset_name = datapackage_dict['name']
      # Deleting dataset before test
      if is_dataset_published(ckan_instance, datapackage):
        delete_dataset(ckan_instance, dataset_name)
      # Publish dataset
      result = runner.invoke(create_cli, ['--ckan-host', f"{os.environ.get('CKAN_HOST_PRODUCAO')}",
                             '--ckan-key', f"{os.environ.get('CKAN_KEY_PRODUCAO')}"])
    # Deleting dataset after test
    delete_dataset(ckan_instance, dataset_name)
    self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
  unittest.main()
