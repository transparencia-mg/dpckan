import os
from click.testing import CliRunner
import unittest
import dpckan_test
from dpckan.publish import publish


class TestDatasetWithoutDatapackageFile(unittest.TestCase):
  """
    Testing error for lack of datapackage file inside dataset home directory
  """
  def test_homologa_env(self):
    """
      Testing error for lack of datapackage file inside dataset home directory (--env homologacao)
    """
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=dpckan_test.get_file_path()):
      dpckan_test.clone_online_repo(__file__)
      result = runner.invoke(publish)
      dpckan_test.clean_temp_folders()
      self.assertNotEqual(result.exit_code, 0)

  def test_production_env(self):
    """
      Testing error for lack of datapackage file inside dataset home directory (--env homologacao)
    """
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=dpckan_test.get_file_path()):
      dpckan_test.clone_online_repo(__file__)
      result = runner.invoke(publish)
      dpckan_test.clean_temp_folders()
      self.assertNotEqual(result.exit_code, 0)

if __name__ == '__main__':
  unittest.main()
