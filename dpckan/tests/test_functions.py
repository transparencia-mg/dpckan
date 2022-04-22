from frictionless import Package
from dpckan.functions import (
                              load_complete_datapackage,
                              get_ckan_dataset_resources_names,
                              find_dataset_basepath,
                              resource_hash,
                              is_uuid,
                              )
import pytest

source = './dpckan/tests/dataset_test_1/datapackage.json'
package = Package(source)

def test_load_complete_datapackage_dict():
    package = load_complete_datapackage(source)
    assert isinstance(package, dict) == True

def test_load_complete_datapackage_package():
    package = load_complete_datapackage(source)
    assert isinstance(package, Package) == True

def test_get_ckan_dataset_resources_names_list():
  ckan_dataset_resources_ids = {'letters-consonants': '780e2e9a-51f1-4571-95af-bedf05da0dc2',
                                'letters-vowels': '9e4f0dfe-5ecb-482d-a30d-8a9f49f7ac01',
                                'datapackage.json': 'd19de465-16d1-445a-934f-d11f29cadbee',}
  ckan_dataset_resources_names = get_ckan_dataset_resources_names(ckan_dataset_resources_ids)
  assert isinstance(ckan_dataset_resources_names, list) == True

@pytest.mark.parametrize("expect",[('./dpckan/tests/dataset_test_1'),('.')])
def test_find_dataset_basepath(expect):
  if expect == './dpckan/tests/dataset_test_1':
    assert find_dataset_basepath(package) == './dpckan/tests/dataset_test_1'
  else:
    package.basepath = ''
    assert find_dataset_basepath(package) == '.'

@pytest.mark.parametrize(
                          "name,expect",
                          [
                           ('letters-consonants', 'a4a881d0d7070e3357a2ded041c51010'),
                           ('letters', 'b8f894cd1bbbaac091920d7d5bf681ea'),
                           # ('datapackage.json', 'bf39f25e44d331fb44e67fb32b6e795b'),                           
                          ])
def test_resource_hash(name,expect):
  assert resource_hash(package, name) == expect

@pytest.mark.parametrize(
                          "_input,expect",
                          [
                           ('078c9abe-d53d-4e3c-8165-fabbe2d20e0c', True),
                           ('078c9abe-d53d-4e3c-8165-fabbe2d20e0', False),
                           ('078c9abe-d53d-4e3c-8165-fabbe2d20e0d', True),
                           ('ç78c9abe-d53d-4e3c-8165-fabbe2d20e0d', False),
                          ])
def test_is_uuid(_input,expect):
  assert is_uuid(_input) == expect