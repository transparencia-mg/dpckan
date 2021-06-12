from click.testing import CliRunner
import unittest
from dpckan.publish import publish

class TestDatasetWithDatapackageError(unittest.TestCase):
  """
    Conjunto de testes em datasets que não apresentam arquivo datapackage.json na raiz do conjunto
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
