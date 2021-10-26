import os
from click.testing import CliRunner
import unittest
from dpckan.tests import clone_online_repo
from dpckan.tests import get_file_path
from dpckan.create_dataset import create_cli

class TestDatasetWithDatapackageError(unittest.TestCase):
  """
    Testing error for lack of datapackage file inside dataset home directory
  """
  def test(self):
    """
      Testing error for lack of datapackage file inside dataset home directory (--env homologacao)
    """
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=get_file_path()):
      clone_online_repo(__file__)
      result = runner.invoke(create_cli)
      self.assertNotEqual(result.exit_code, 0)

if __name__ == '__main__':
  unittest.main()

