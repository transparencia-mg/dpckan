import pytest
from frictionless import Package
from dpckan.functions import (load_complete_datapackage,)

source = './dpckan/tests/dataset_test_1/datapackage.json'

def test_load_complete_datapackage_dict():
    package = load_complete_datapackage(source)
    assert isinstance(package, dict) == True

def test_load_complete_datapackage_package():
    package = load_complete_datapackage(source)
    assert isinstance(package, Package) == True

