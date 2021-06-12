from click.testing import CliRunner
import unittest
from dpckan.publish import publish

class TestDatasetWithDatapackageError(unittest.TestCase):
  """
    Testing syntax datapackage error
  """
  def test_homologa_env(self):
    runner = CliRunner()
    result = runner.invoke(publish, ['--env', 'homologacao'])
    self.assertNotEqual(result.exit_code, 0)
    self.assertEqual(result.output,
                      "----Arquivo datapackage.json com algum problema de sintaxe ou em branco----\n")
  def test_producao_env(self):
    runner = CliRunner()
    result = runner.invoke(publish, ['--env', 'producao'])
    self.assertNotEqual(result.exit_code, 0)
    self.assertEqual(result.output,
                      "----Arquivo datapackage.json com algum problema de sintaxe ou em branco----\n")

if __name__ == '__main__':
  unittest.main()
