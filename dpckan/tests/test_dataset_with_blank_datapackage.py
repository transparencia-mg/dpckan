import os
from click.testing import CliRunner
import unittest
from dpckan.tests import clone_online_repo
from dpckan.tests import get_file_path
from dpckan.create_dataset import create_cli

class TestDatasetWithBlankDatapackage(unittest.TestCase):
  """
    Testing error for lack of datapackage file inside dataset home directory
  """
  def test_homologa_env(self):
    """
      Testing error for lack of datapackage file inside dataset home directory (--env homologacao)
    """
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=get_file_path()):
      clone_online_repo(__file__)
      result = runner.invoke(create_cli)
      self.assertNotEqual(result.exit_code, 0)

  def test_production_env(self):
    """
      Testing error for lack of datapackage file inside dataset home directory (--env homologacao)
    """
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=get_file_path()):
      clone_online_repo(__file__)
      result = runner.invoke(create_cli, ['--ckan-host', f"{os.environ.get('CKAN_HOST_PRODUCAO')}",
                             '--ckan-key', f"{os.environ.get('CKAN_KEY_PRODUCAO')}"])
      self.assertNotEqual(result.exit_code, 0)

if __name__ == '__main__':
  unittest.main()

