from frictionless import Package
from dpckan.functions import (
                              load_complete_datapackage,
                              get_ckan_dataset_resources_names,
                              is_uuid,
                              )
import pytest

source = './dpckan/tests/dataset_test_1/datapackage.json'

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