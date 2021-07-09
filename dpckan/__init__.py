from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path('.', '.env'))
from dpckan.create_resource import create_resource
from dpckan.create_dataset import create
from dpckan.updateDataSet import dataSet
from dpckan.update_resource import update_resource

