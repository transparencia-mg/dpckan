import os
from click.testing import CliRunner
import unittest
from ckanapi import RemoteCKAN

def run_tests():
  try:
    os.system("python -m unittest discover -s dpckan/tests -p 'test_*.py'")
    os.system('rm -rf dpckan/tests/tmp*')
  except Exception:
    os.system('rm -rf dpckan/tests/tmp*')

def clone_online_repo(file):
  """
    Cloning branch's online repo to proceed the test
    This online repo was created to store datasets configurations for tests
    All tests configurations are stored inside Repo Branchs
    To work the test_dataset_* file name must be the same as the branch
  """
  branch = get_file_name(file)
  online_repo = "https://github.com/dados-mg/dpckan-tests.git"
  os.system(f'git clone -q -b {branch} --single-branch {online_repo} .')

def get_file_name(file):
  """
    As explained in clone_online_repo method test_dataset_* file name must be branch's name
  """
  return file.split("/")[-1].split(".")[0]

def get_ckan_instance(ckan_host, ckan_key):
  ckan_host = os.environ.get(ckan_host)
  ckan_key = os.environ.get(ckan_key)
  ckan_instance = RemoteCKAN(ckan_host, apikey=ckan_key)
  return ckan_instance

def get_file_path():
  """
    Find tests files current directory where it must be executed.
    This folder must reproduce a dataset error that must be prevented
  """
  return os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
  run_tests()
