from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path('.', '.env'))
from dpckan.createResource import criarArquivo2
from dpckan.publish import publish
from dpckan.updateDataSet import dataSet
from dpckan.updateResource import resource

