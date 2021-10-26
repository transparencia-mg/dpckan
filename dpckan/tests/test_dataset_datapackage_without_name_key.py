import os
import json
from click.testing import CliRunner
import unittest
from dpckan.tests import clone_online_repo
from dpckan.tests import get_file_path
from dpckan.create_dataset import create_cli
from dpckan.functions import (delete_dataset, datapackage_path)

class TestDatasetDatapackageWithoutNameKey(unittest.TestCase):
  """
    Testing dataset publication sucessfully
  """
  def test(self):
    """
      Testing dataset publication sucessfully homologacao environment
    """
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=get_file_path()):
      clone_online_repo(__file__)
      result = runner.invoke(create_cli)
      self.assertNotEqual(result.exit_code, 0)

if __name__ == '__main__':
  unittest.main()

