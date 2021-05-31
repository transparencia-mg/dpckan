# DPKG CKAN MG

## Utilização

- Terminal

```
$ pip install dpkgckanmg
```

- Arquivo Python
```
# Publicar
from dpkgckanmg.publish import publish
publish(path/dir/datapackage, ckan_key)

# Criar Recurso
from dpkgckanmg.createResource import criarArquivo2
criarArquivo2(1, 2, 3)

# Atualizar Data Set
from dpkgckanmg.updateDataSet import dataSet
dataSet(1, 2, 3)

# Atualizar Recurso
from dpkgckanmg.updateResource import resource
resource(1, 2, 3)


### 1,2 3 deveráo ser retirados do arquivo .doc (gabriel atualizará)
```
