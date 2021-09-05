from pathlib import Path
from dotenv import load_dotenv
from dpckan import create_dataset
from dpckan import update_dataset
from dpckan import create_resource
from dpckan import update_resource

load_dotenv(dotenv_path=Path('.', '.env'))
