import os
import json
from click.testing import CliRunner
import unittest
from dpckan.tests import clone_online_repo
from dpckan.tests import get_file_path
from dpckan.create_dataset import create
from dpckan.functions import (delete_dataset, datapackage_path,
                              load_complete_datapackage)

class TestDatasetPublishDatasetSuccessfully(unittest.TestCase):
  """
    Testing dataset publication sucessfully
  """
  def test_homologa_env(self):
    """
      Testing dataset publication sucessfully homologacao environment
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
      clone_online_repo(__file__)
      result = runner.invoke(create)
      # Deleting dataset after test
      path_datapackage = datapackage_path()
      dataset_dict = json.loads(load_complete_datapackage(path_datapackage))
      delete_dataset(os.environ.get('CKAN_HOST'), os.environ.get('CKAN_KEY'), dataset_dict['name'])
      self.assertEqual(result.exit_code, 0)

  def test_prod_env(self):
    """
      Testing dataset publication sucessfully producao environment
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
      clone_online_repo(__file__)
      result = runner.invoke(create, ['--host', f"{os.environ.get('CKAN_HOST_PRODUCAO')}",
                             '--key', f"{os.environ.get('CKAN_KEY_PRODUCAO')}"])
      # Deleting dataset after test
      path_datapackage = datapackage_path()
      dataset_dict = json.loads(load_complete_datapackage(path_datapackage))
      delete_dataset(os.environ.get('CKAN_HOST_PRODUCAO'), os.environ.get('CKAN_KEY_PRODUCAO'), dataset_dict['name'])
      self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
  unittest.main()

