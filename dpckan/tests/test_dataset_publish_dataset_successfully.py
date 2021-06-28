import os
import json
from click.testing import CliRunner
import unittest
from dpckan.tests import clone_online_repo
from dpckan.tests import get_file_path
from dpckan.publish import publish
from dpckan.functions import (delete_dataset, datapackage_path, lerDadosJsonMapeado)

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
      result = runner.invoke(publish)
      self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
  unittest.main()

